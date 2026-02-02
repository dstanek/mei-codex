#terraform

- `count` takes a number and gives you index-based instances: `resource.foo[0]`, `resource.foo[1]`, etc.
- `for_each` takes:
    - a **map** → keys are map keys
    - a **set(string)** → keys are the string values
- A list is **not allowed** for `for_each`, so you convert it with `toset(...)`.