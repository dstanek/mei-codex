---

config:

look: handDrawn

---

flowchart LR

subgraph LOAD_STATE

S1["Read Statefile<br/>(IDs & Cached Attributes)"]

end

subgraph REFRESH

S1 --> P1["Provider Read Calls<br/>(Only resources in state)"]

P1 --> S2["Filter to Schema Fields<br/>(Keep Required/Optional/Computed)"]

S2 --> R1[Refreshed State]

end

subgraph DIFF

C1["HCL Config<br/>(Desired State)"]

R1[Refreshed State]

C1 --> T1[Terraform Core]

R1 --> T1

T1 --> Plan[Execution Plan]

end

subgraph PLAN_ARTIFACT

Plan --> |"`terraform plan -out=plan.tfplan`"| PF[Saved Plan File]

end

subgraph APPLY

PF --> Apply[terraform apply plan.tfplan]

Apply --> |Execute Actions| Cloud[Cloud APIs]

Cloud --> NewState[New State Snapshot]

NewState --> |Write| S1

end