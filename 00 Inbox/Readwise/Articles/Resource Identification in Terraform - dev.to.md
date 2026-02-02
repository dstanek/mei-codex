---
Author: dev.to
Tags: readwise_inbox, readwise
Note Created: Thursday 23rd October 2025 23:57
Last modified: Thursday 23rd October 2025 23:57
---
# Resource Identification in Terraform

![rw-book-cover](https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fraw.githubusercontent.com%2Fmusukvl%2Farticle-terraform-resource-identification%2Fmaster%2Flogo.jpg)

## Metadata
- Author: [[dev.to]]
- Full Title: Resource Identification in Terraform
- Category: #articles
- Document Tags: [[asap]] 
- Summary: Terraform resources are identified at three levels: in the code (.tf-file), in the Terraform state file, and as actual resources in the cloud. Proper understanding of these identifiers is crucial to prevent unintended resource recreation and data loss. Using constructs like `for_each` or `count` allows for creating multiple resource instances, but understanding how they are referenced is key for maintainable code.
- URL: https://dev.to/musukvl/terraform-resources-identification-5bgg

## Highlights
### id865961189

> .tf-file code as `resource` block.

 * [View Highlight](https://read.readwise.io/read/01jpt6at2bsdz8mqkmny9g09ay)
### id865961259

> has record in Terraform state file.

 * [View Highlight](https://read.readwise.io/read/01jpt6bcab4bx0kjm033qxafh1)
### id865961287

> resource created in a cloud.

 * [View Highlight](https://read.readwise.io/read/01jpt6bwmk16gcgmv16pp2nff8)
### id865961309

> level resource has its own identification.

 * [View Highlight](https://read.readwise.io/read/01jpt6cg9q2vz7xsbhdtaw29tn)
### id865961699

> resource type

 * [View Highlight](https://read.readwise.io/read/01jpt6erpv9j3f1dqh5cbpyrsf)
### id865961700

> resource name

 * [View Highlight](https://read.readwise.io/read/01jpt6ewv5rrhzjfyrak5mhzme)
### id865961758

> In the terraform state the storage account is identified with `type` and `name` fields:

 * [View Highlight](https://read.readwise.io/read/01jpt6fg83c2qw1vwy4stshn1m)
### id865962031

> Terraform realizes that it has no matching code definition

 * [View Highlight](https://read.readwise.io/read/01jpt6hef5y3qz696q9ywme2mw)
### id865962048

> Terraform realizes that it has no matching record in the state for resource

 * [View Highlight](https://read.readwise.io/read/01jpt6hjbrfmcjwpphvn5wzh94)
### id865962097

> Changing attributes could cause resource recreation in some cases and depends on resource provider, but changing identifier *always* cause resource recreation.

 * [View Highlight](https://read.readwise.io/read/01jpt6jy2t3nd6vr6c9s33es2e)
### id865962124

> for_each

 * [View Highlight](https://read.readwise.io/read/01jpt6kg7ty5bsjss3ry5fgg3y)
### id865962156

> count

 * [View Highlight](https://read.readwise.io/read/01jpt6m18jj3wdscccjggw2jkx)
