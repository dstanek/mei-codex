---
tags:
  - rust
---

# Rust Boxing Explained

In Rust, **boxing** means putting a value on the **heap** by wrapping it in `Box<T>`.

```rust
let x = Box::new(42);
```

`x` is a pointer on the stack; `42` lives on the heap.

## Why boxing exists

Rust requires every value's size to be known at compile time. Recursive types break this:

```rust
enum List {
    Cons(i32, List), // infinite size — rejected
    Nil,
}
```

`Box` breaks the cycle by storing a fixed-size pointer instead of the value inline:

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

## When you need `Box<T>`

### Recursive types

```rust
enum Expr {
    Number(i64),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}
```

### Trait objects (dynamic dispatch)

When you need a heterogeneous collection behind a common trait:

```rust
let animals: Vec<Box<dyn Animal>> = vec![Box::new(Dog), Box::new(Cat)];
```

`dyn Animal` has no known size; `Box<dyn Animal>` does.

### Large values you don't want to move

```rust
let b = Box::new(BigThing { data: [0u8; 1_000_000] });
```

Moving `Box<BigThing>` moves only the pointer, not the array.

## Alternatives to boxing

### Generics instead of `Box<dyn Trait>`

```rust
// instead of
fn run(storage: Box<dyn Storage>) { ... }

// use
fn run<S: Storage>(storage: S) { ... }
// or, if you only need a borrow
fn run(storage: &impl Storage) { ... }
```

Static dispatch, no heap allocation.

### `impl Trait` for return types

```rust
// instead of
fn make_iterator() -> Box<dyn Iterator<Item = i32>> {
    Box::new(vec![1, 2, 3].into_iter())
}

// use
fn make_iterator() -> impl Iterator<Item = i32> {
    vec![1, 2, 3].into_iter()
}
```

This only works when all return paths produce the **same concrete type**. If branches diverge, use `Box<dyn ...>` or an enum.

### Enum for a closed set of types

Instead of `Vec<Box<dyn Shape>>`:

```rust
enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle { radius } => std::f64::consts::PI * radius * radius,
            Shape::Rectangle { width, height } => width * height,
        }
    }
}
```

Statically sized, no dynamic dispatch.

### Recursive structures: indirection is unavoidable

You must use *some* pointer. Options:

- `Box<T>` — unique ownership
- `Rc<T>` — shared ownership (single-threaded)
- `Arc<T>` — shared ownership (multi-threaded)
- Index into a `Vec` (arena style) — avoids per-node heap allocation

## Summary

| Situation | Instead of | Use |
|---|---|---|
| Accept a trait | `Box<dyn Trait>` | generics / `impl Trait` |
| Return one concrete type | `Box<dyn Trait>` | `impl Trait` |
| Return multiple concrete types | `Box<dyn Trait>` | enum |
| Recursive data | `Box<T>` | keep `Box`, or `Rc`/`Arc`, or arena |
| Shared ownership | `Box<T>` | `Rc<T>` or `Arc<T>` |
