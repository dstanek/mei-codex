## Reorder Commits

```bash

# Move one commit "u" so it comes right after "s"
jj rebase -r u --after s

# Move a whole set (u and v) after s
jj rebase -r 'u|v' --after s

# Reparent a commit (make "t" a child of "base")
jj rebase -r t -d base
```

## Merge (squash) commits

```bash
# Squash the working change into its parent (like `git commit --amend`)
jj squash

# Squash a specific commit into its parent
jj squash -r <rev>

# Squash multiple commits (D..E) into C
jj squash --from 'D::E' --into C

# Interactive hunk-level squash (super handy for curating a single commit)
jj squash -i
```

## Reorder and Merge
```bash
# 1) Reorder: place the commits you want to combine next to the target
jj rebase -r X --after TARGET
jj rebase -r Y --after X

# 2) Squash them together into TARGET
jj squash --from 'X|Y' --into TARGET
```

## Power tools

- **`jj absorb`**: automatically moves stray edits from your working copy into the “right” earlier commits—often nicer than manual `squash -i`. [v5.chriskrycho.com](https://v5.chriskrycho.com/journal/jujutsu-megamerges-and-jj-absorb/?utm_source=chatgpt.com)
    
- **`jj abandon`**: delete a commit and rebase its descendants (useful after squashing). [jj-vcs.github.io](https://jj-vcs.github.io/jj/latest/cli-reference/?utm_source=chatgpt.com)