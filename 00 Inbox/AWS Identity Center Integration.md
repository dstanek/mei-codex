# AWS Identity Center Integration

## Overview

AWS Identity Center serves as the central identity provider for our multi-account AWS environment. It provides a single sign-on capability and centralized permission management across all AWS accounts in our organization. Unfortunately we don't own Identity Center and rely on CDRM to make configuration changes when we create [tickets].

## Key Concepts

**Identity Store**

- Central repository for users and groups
- Integrates with our HPE SSO provider
- Manages user attributes and group memberships

**Permission Sets**

- Templates that define what users can do in AWS accounts
- Map to IAM roles in target accounts
- Contain AWS managed policies, customer managed policies, and inline policies
- Enable consistent permissions across multiple accounts

**Account Assignments**

- Link users/groups to permission sets in specific AWS accounts
- Create the actual access relationships
- Generate corresponding IAM roles automatically

**Multi-Account Structure**

- Centrally managed by the CDRM team
- Permissions propagated to member accounts
- Single sign-on portal for users to access all accounts

## How It Works

1. **User Authentication**: Users sign in through the AWS access portal using HPE SSO
2. **Role Selection**: Users see available accounts and roles based on their assignments
3. **Role Assumption**: When accessing an account, Identity Center generates temporary credentials for the corresponding IAM role
4. **Permission Enforcement**: The IAM role's policies determine what actions the user can perform

## Identity Center to IAM Mapping

In our Zephyr environment, each role defined in this document corresponds to:

**Identity Center Side:**

- **Permission Set**: Named to match our role (e.g., "Engineer-Dev", "Observer")
- **Account Assignment**: Links users/groups to permission sets in specific accounts

**IAM Side (automatically created):**

- **IAM Role**: Named like `AWSReservedSSO_Engineer-Dev_abc123def456`
- **Trust Policy**: Allows Identity Center to assume the role
- **Permission Policies**: Attached based on the permission set definition

## Benefits for Zephyr

- **Centralized Management**: Define roles once, deploy across all accounts
- **Consistent Security**: Same role has same permissions in dev/qa/prod
- **Audit Trail**: CloudTrail logs show both Identity Center and IAM activities
- **Temporary Credentials**: No long-lived access keys to manage
- **Easy Onboarding**: Add users to groups, automatically get appropriate access; assuming CDRM is responsive.

## Implementation Notes

- Permission sets should mirror the roles defined in this document
- Use AWS managed policies where possible (ReadOnlyAccess, etc.)
- Custom policies for specific needs (e.g., ManagedBy tag enforcement)
- Group-based assignments preferred over individual user assignments
- Regular access reviews through Identity Center console

## Example Permission Set Structure

```yaml
# Example: Engineer-Dev permission set
permission_set:
  name: "Engineer-Dev"
  description: "Development environment engineering access"
  session_duration: "PT8H"  # 8 hours
  policies:
    aws_managed:
      - "ReadOnlyAccess"
    customer_managed:
      - "engineer-dev-mutate-owned"
    inline_policy: |
      {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Deny",
            "Action": "secretsmanager:*",
            "Resource": "*"
          }
        ]
      }
```