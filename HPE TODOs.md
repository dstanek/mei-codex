### 1) `BackOff restarting failed container` (CrashLoopBackOff)

The container in that pod is crashing repeatedly.

**Quick debug**

`# Most recent logs (and the previous crash) kubectl -n apogee-zinc-app logs pod/zinc-app-745747498c-b4wlk -c simple kubectl -n apogee-zinc-app logs pod/zinc-app-745747498c-b4wlk -c simple --previous  # Why the kubelet restarted it / probe failures / OOMKilled / image/arch issues kubectl -n apogee-zinc-app describe pod zinc-app-745747498c-b4wlk`

**What to look for**

- Exit code & stack trace from the app.
    
- `OOMKilled` → raise limits or reduce usage.
    
- `ImagePullBackOff`/`ErrImagePull`.
    
- **Arch mismatch** (you’re on arm64): look for “exec format error”. Use a multi-arch image or the right arch tag.
    
- Liveness/readiness probe flapping.
    

---

### 2) `UpdateFailed externalsecret/... AccessDeniedException: Access to KMS is not allowed`

External Secrets Operator couldn’t decrypt a Secret because the pod’s IAM identity lacks KMS permissions for the CMK that protects the secret.

**Quick debug**

`# Confirm which SecretStore/ClusterSecretStore and AWS role it uses kubectl -n monitoring get externalsecret lunar-grafana-admin-secret -o yaml | yq '.spec..secretStoreRef,.spec.data'  # Check the pod’s IAM role via IRSA kubectl -n monitoring get sa <eso-service-account> -o yaml | yq '.metadata.annotations'`

**Fix**

- Ensure the pod’s IAM role has:
    
    - If AWS Secrets Manager: `secretsmanager:GetSecretValue`
        
    - If SSM Parameter Store: `ssm:GetParameter` (and `...WithDecryption`)
        
    - **And** KMS: `kms:Decrypt` (often `kms:DescribeKey`, maybe `kms:GenerateDataKey*` depending on flow)
        
- Update the **KMS key policy** or grants to allow that IAM role.
    
- Redeploy External Secrets or requeue the resource:
    
    `kubectl -n monitoring annotate externalsecret lunar-grafana-admin-secret reconcile="$(date +%s)" --overwrite`
    

---

### 3) `FailedGetResourceMetric ... unable to fetch metrics from resource metrics API: (get pods.metrics.k8s.io)`

Your HPAs that use CPU/memory can’t talk to **metrics-server** (the `metrics.k8s.io` API isn’t registered/healthy).

**Quick debug**

`kubectl get apiservice v1beta1.metrics.k8s.io -o yaml | yq '.status' kubectl -n kube-system get deploy metrics-server kubectl -n kube-system logs deploy/metrics-server`

**Fix**

- (Re)install or upgrade **metrics-server** compatible with Kubernetes 1.33.
    
- Ensure aggregator is healthy and metrics-server has the right args (e.g., `--kubelet-insecure-tls` in strict TLS environments).
    
- As a stopgap, temporarily scale those Deployments manually while HPAs are blind.
    

---

### 4) `FailedGetPodsMetric ... no custom metrics API (custom.metrics.k8s.io) registered`

An HPA is querying a **custom metric** (e.g., from Prometheus) but the **Custom Metrics API** isn’t available.

**Quick debug**

`kubectl get apiservice | grep custom.metrics # Expect something like v1beta1.custom.metrics.k8s.io -> Available=True  # Check your adapter (e.g., prometheus-adapter) kubectl -n monitoring get deploy -l app.kubernetes.io/name=prometheus-adapter kubectl -n monitoring logs deploy/prometheus-adapter`

**Fix**

- (Re)deploy your **metrics adapter** (Prometheus Adapter or equivalent) with rules mapping that metric.
    
- Verify the metric actually exists in Prometheus and matches the adapter rules.
    
- Again, manually set replicas until this is healthy.
    

---

### Put it together (fast triage order)

1. **CrashLoop pods**: get logs → fix image/arch, env, or probes.
    
2. **External Secret**: fix IRSA/KMS permissions (that’s a hard blocker for app startup).
    
3. **metrics-server**: restore `metrics.k8s.io` so CPU/mem HPAs work.
    
4. **custom metrics adapter**: restore `custom.metrics.k8s.io` for custom-metric HPAs.
    

If you paste:

- the `describe pod` for one crashing zinc pod,
    
- the service account annotations for External Secrets (and the KMS key ARN),
    
- `kubectl get apiservice v1beta1.metrics.k8s.io -o yaml | yq '.status'`,
    

I’ll call out the exact line to change in IAM/KMS and the helm values flags to use for metrics-server/adapter on 1.33.


# Put these in the cheatsheet
Totally—let’s do a focused, zsh-safe playbook to (a) list the pods on a node, (b) see what’s blocking eviction, and (c) point to the exact fix.

> Set your node name once:

`NODE=ip-10-0-1-246.ec2.internal`

# 1) See what’s on the node (and exclude DaemonSets/static pods)

`kubectl get pods -A --field-selector spec.nodeName="$NODE" -o json \ | jq -r '   .items   # drop DaemonSets and mirror/static pods   | map(select(((.metadata.ownerReferences // []) | any(.kind=="DaemonSet")) | not)          | select((.metadata.annotations // {})["kubernetes.io/config.mirror"] | not))   | map({       ns: .metadata.namespace,       pod: .metadata.name,       ctrl_kind: ((.metadata.ownerReferences // [])[0].kind // ""),       ctrl_name: ((.metadata.ownerReferences // [])[0].name // ""),       phase: .status.phase     })   | .[] | "\(.ns)\t\(.pod)\t\(.ctrl_kind)/\(.ctrl_name)\t\(.phase)" '`

# 2) Dry-run a drain (shows the _exact_ eviction blocker text)

`kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data \   --timeout=20m --dry-run=server -A -v=6`

Scan the output for:

- “**would violate PodDisruptionBudget**”
    
- “**didn’t match Pod’s node affinity/selector**”
    
- “**pods with local storage**”
    
- “**cannot evict…** finalizers”
    

# 3) For each listed pod, pull the useful bits fast

### 3a) Events (scheduler/eviction reasons)

`NS=<ns>; POD=<pod> kubectl describe pod -n "$NS" "$POD" | sed -n '/Events:/,$p'`

### 3b) PDBs that select this pod (+ whether disruption is allowed)

_(matchLabels only—covers the majority of PDBs)_

`PODLABELS=$(kubectl -n "$NS" get pod "$POD" -o json | jq -c '.metadata.labels') kubectl -n "$NS" get pdb -o json \ | jq -r --argjson L "$PODLABELS" '   .items[]   | {name:.metadata.name,      allowed:(.status.disruptionsAllowed // 0),      sel:(.spec.selector // {})}   | select((.sel.matchLabels // {}) as $m            | ($m|keys) as $ks            | all($ks[]; $L[.] == $m[.]))   | "PDB=\(.name)  disruptionsAllowed=\(.allowed)" '`

If you see `disruptionsAllowed=0`, that PDB is blocking eviction. Options:

- temporarily raise `maxUnavailable` / lower `minAvailable`, or
    
- scale the workload up so `disruptionsAllowed > 0`.
    

### 3c) Hard scheduling requirements (that may prevent rescheduling)

`kubectl -n "$NS" get pod "$POD" -o json \ | jq '{nodeSelector:.spec.nodeSelector,       nodeAffinity:.spec.affinity.nodeAffinity,       tolerations:.spec.tolerations}'`

If rescheduling fails with “didn’t match…”, ensure **target nodes** have the labels required here.

### 3d) PVC / zone coupling (common silent blocker)

`# Show any RWO PVCs bound to the pod and their zone/nodeAffinity kubectl -n "$NS" get pod "$POD" -o json \ | jq -r '   .spec.volumes[]? | select(.persistentVolumeClaim!=null)   | .persistentVolumeClaim.claimName ' | while read -r pvc; do   echo "=== PVC $pvc ==="   kubectl -n "$NS" get pvc "$pvc" -o json \   | jq '{sc:.spec.storageClassName, volume:.spec.volumeName}'   PV=$(kubectl -n "$NS" get pvc "$pvc" -o jsonpath='{.spec.volumeName}')   kubectl get pv "$PV" -o json \   | jq '{nodeAffinity:.spec.nodeAffinity, claimRef:.spec.claimRef}' done`

Bound PVs (RWO/EBS) must land in the **same AZ**. Make sure your replacement node group includes that AZ.

### 3e) Finalizers that keep a pod from going away

`kubectl -n "$NS" get pod "$POD" -o json \ | jq '.metadata.finalizers'`

If a controller crashed and left a finalizer, delete/update that controller or (safely) remove the finalizer.

# 4) Quick “what to change” matrix

- **PDB blocks** → temporarily relax PDB or scale replicas up, retry.
    
- **Label/affinity mismatch** → add the required label(s) to _all_ nodes in the target pool (and define them in your node group/launch template so they persist).
    
- **AZ/PVC mismatch** → ensure the node group has nodes in the PVC’s AZ; otherwise migrate the volume/workload.
    
- **Catch-all tolerations** → remove tolerations that re-attract pods to draining nodes.
    
- **Standalone pods/finalizers** → put under a controller or clear the finalizer.
    

# 5) Re-check progress / errors from EKS’ perspective

`CL=<cluster>; NG=<nodegroup> aws eks list-updates --name "$CL" --nodegroup-name "$NG" aws eks describe-update --name "$CL" --nodegroup-name "$NG" --update-id <ID> \   --query 'update.{status:status,errors:errors}'`

---

If you paste:

- the **`kubectl drain --dry-run`** output for one problem node (the lines with “would violate…”), and
    
- the **PDB line(s)** from 3b for a pod that won’t move,
    

I’ll tell you the one minimal change that will unblock the rollout (specific PDB tweak vs. node label/zone fix).