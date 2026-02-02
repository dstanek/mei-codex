## Generate YAML without applying it

Use the `--dry-run=client -o yaml` flags with any `kubectl create` or `kubectl run` command:

bash

```bash
# Create a deployment YAML
kubectl create deployment my-app --image=nginx --dry-run=client -o yaml

# Create a service YAML
kubectl create service clusterip my-service --tcp=80:80 --dry-run=client -o yaml

# Create a pod YAML
kubectl run my-pod --image=nginx --dry-run=client -o yaml

# Create a configmap YAML
kubectl create configmap my-config --from-literal=key=value --dry-run=client -o yaml
```