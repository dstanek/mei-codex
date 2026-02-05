---
type: topic
aliases: [Type Systems, Type Theory]
---

# Typing

Type systems in programming languages — how types are checked and enforced.

## Key Concepts

### Nominal Subtyping
- Types are compatible based on explicit declarations
- Example: Java, C# — a class must explicitly `extend` or `implement`

### Structural Subtyping
- Types are compatible based on structure (shape)
- Example: TypeScript, Go interfaces — if it has the right methods, it matches

## Related Notes

```dataview
LIST
FROM ""
WHERE contains(lower(file.name), "typing") OR contains(lower(file.name), "python")
LIMIT 10
```

## Resources

- [Python typing module](https://docs.python.org/3/library/typing.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)

## Open Questions

- When to use strict typing vs. duck typing in Python?
