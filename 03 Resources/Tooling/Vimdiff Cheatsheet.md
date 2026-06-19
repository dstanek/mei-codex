# Vimdiff Cheatsheet

## Open
- `vimdiff file1 file2`
- `vimdiff -o file1 file2` for horizontal splits
- `vimdiff -O file1 file2` for vertical splits

## Navigate
- `]c` next change
- `[c` previous change
- `:cnext` / `:cprev` if you prefer commands

## Copy Changes
- `do` get from the other buffer
- `dp` put into the other buffer
- `:diffget` / `:diffput` for explicit control

## Useful Commands
- `:set noscrollbind`
- `:set diffopt=filler,internal,algorithm:histogram`
- `:wqa` save and quit all
- `:qa!` quit without saving

## Merge Flow
- `git mergetool` can open `vimdiff`
- Use the middle buffer as the common base in a 3-way merge