---
type: topic
aliases: [Terraform for_each, Terraform count]
---

# Terraform Collection Expansion

Rules for expanding collections in Terraform using `count` and `for_each`.

## Key Concepts

### count
- Takes a number and gives you index-based instances
- Example: `resource.foo[0]`, `resource.foo[1]`
- Use when instances are interchangeable

### for_each
- Takes a map or set and gives you key-based instances
- Example: `resource.foo["us-east-1"]`, `resource.foo["us-west-2"]`
- Use when instances have meaningful identifiers

## Rules

1. **count** — use for identical resources where order doesn't matter
2. **for_each with map** — use when you need to reference by key
3. **for_each with set** — use when you have a list of unique values

## Related Notes

```dataview
LIST
FROM ""
WHERE contains(lower(file.name), "terraform")
LIMIT 10
```

## Resources

- [Terraform count docs](https://developer.hashicorp.com/terraform/language/meta-arguments/count)
- [Terraform for_each docs](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
