# Git vs Jujutsu (jj) Workflow Comparison

## Core Philosophy Differences

| Aspect                | Git                           | Jujutsu                              |
| --------------------- | ----------------------------- | ------------------------------------ |
| **Tracking**          | Manual staging with `git add` | Automatic tracking of all changes    |
| **Commits**           | Immutable once created        | Changes are mutable by default       |
| **Working Directory** | Special state, not versioned  | Just another change in the graph     |
| **Branches**          | Pointers to commits           | Every change can have multiple names |

## Common Workflows Side-by-Side

### 1. Interactive Patch Splitting (Your Main Use Case)

#### Git Approach
```bash
# After doing work across multiple logical changes
git add -p                    # Interactively stage portions
git commit -m "Fix validation logic"
git add -p                    # Stage more portions
git commit -m "Update tests"
git add -p                    # Stage remaining
git commit -m "Update documentation"
```

#### Jj Approach
```bash
# After doing work (automatically tracked)
jj split                      # Interactive split into multiple changes
# OR for more control:
jj split --interactive        # Choose exactly what goes where
jj describe @                 # Describe current change
jj describe @-                # Describe previous change  
jj describe @--               # Describe change before that
```

**Jj Advantages:**
- Can split/unsplit changes at any time
- Can move hunks between any changes in your stack
- No need to think about staging upfront

### 2. Feature Branch Development

#### Git Approach
```bash
git checkout -b feature-branch
# Make commits
git push -u origin feature-branch
# Create PR, iterate with more commits
git rebase -i main            # Clean up before merge
```

#### Jj Approach
```bash
jj new main -m "Start feature work"
# Make changes (auto-tracked)
jj describe                   # Add commit message
jj new                        # Start next change in stack
# More work...
jj git push                   # Push entire stack
# Clean up with split/fold/reorder anytime
```

### 3. Fixing Mistakes in History

#### Git Approach
```bash
# Oops, need to fix commit 3 commits back
git rebase -i HEAD~3
# Mark commit for edit
git add fixed-file.py
git commit --amend
git rebase --continue
```

#### Jj Approach
```bash
# Fix any change at any time
jj edit abc123                # Edit specific change
# Make fixes
jj edit @                     # Back to latest
# OR
jj squash -r abc123           # Squash fixes into specific change
```

### 4. Reviewing Changes Before Pushing

#### Git Approach
```bash
git log --oneline main..HEAD
git diff main..HEAD
git diff HEAD~1..HEAD        # Look at specific commit
```

#### Jj Approach
```bash
jj log                        # Visual graph of all changes
jj show                       # Show current change
jj show @-                    # Show previous change
jj diff -r @-                 # Diff specific change
jj diff -r main..@            # Diff range
```

## Key Jj Commands for Your Workflow

### Essential Commands
```bash
jj split                      # Your bread and butter - split changes
jj fold                       # Combine changes (opposite of split)
jj describe                   # Add/edit commit message
jj show                       # View change contents
jj edit <change>              # Switch to editing a specific change
jj new                        # Create new change
jj abandon                    # Abandon unwanted changes
```

### Advanced Manipulation
```bash
jj move --from X --to Y       # Move hunks between changes
jj squash                     # Squash current change into parent
jj unsquash                   # Move hunks from parent to current
jj rebase -d <dest>           # Rebase changes
jj duplicate                  # Copy a change
```

## Migration Strategy

### Week 1: Learn the Basics
- `jj git clone <repo>`
- Use `jj split` instead of `git add -p`
- Use `jj log` to see your change graph
- Use `jj git push` to push (still uses Git remotes)

### Week 2: Embrace the Workflow
- Start using `jj new` for logical separation
- Practice with `jj edit` to fix older changes
- Try `jj fold` to combine changes

### Week 3: Advanced Features  
- Use `jj move` to reorganize hunks
- Try the automatic rebase features
- Explore `jj op log` (operation log - like Git reflog but better)

## Advantages for Your Use Case

1. **No Staging Area Mental Model**: Everything is automatically tracked
2. **Split Anytime**: Don't need to plan commits upfront
3. **Easy Reorganization**: Move code between any commits in your stack
4. **Better Visualization**: `jj log` shows your entire change graph
5. **Safer History Editing**: Operations are recorded and reversible
6. **Automatic Rebasing**: When you edit old changes, descendants rebase automatically

## Potential Drawbacks

1. **Learning Curve**: Different mental model from Git
2. **Tooling**: Less IDE/editor integration (though improving)
3. **Team Adoption**: Still need Git repos for collaboration
4. **Muscle Memory**: Need to unlearn some Git habits

## Getting Started Command

```bash
# Install jj (cargo install jj-cli or package manager)
jj git clone <your-repo>
cd <repo>
# Start working - all changes auto-tracked!
jj split                      # When ready to organize commits
```

The key insight is that jj's approach of "edit first, organize later" aligns perfectly with your workflow of doing exploratory work and then organizing it into reviewable commits.