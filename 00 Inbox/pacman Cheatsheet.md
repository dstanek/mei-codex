# Pacman Cheat Sheet (Arch Linux)

> `pacman` is Arch’s package manager.  
> Most operations that modify the system need `sudo`.

---

## Basics

```bash
# Pacman help
pacman -h

# Pacman version
pacman -V
```

---

## Query: Check / Inspect Installed Packages

```bash
# Check if a package is installed (single package)
pacman -Q PACKAGE

# Detailed info about an installed package
pacman -Qi PACKAGE

# List all installed packages
pacman -Q

# List explicitly installed packages (not pulled as deps)
pacman -Qe

# List explicitly installed packages, names only
pacman -Qqe

# List packages installed as dependencies
pacman -Qd

# List *orphaned* packages (deps no longer required)
pacman -Qdt

# List packages that are *not* from the official repos (AUR/local)
pacman -Qm

# List packages that *are* from the official repos
pacman -Qn
```

---

## Search

```bash
# Search installed packages (local DB)
pacman -Qs PATTERN

# Search in sync (remote) databases / repos
pacman -Ss PATTERN
```

Examples:

```bash
pacman -Qs neovim
pacman -Ss neovim
```

---

## Install / Remove / Upgrade

> Most of these require `sudo`.

```bash
# Install a package from repos
sudo pacman -S PACKAGE

# Install multiple packages
sudo pacman -S PACKAGE1 PACKAGE2 ...

# Remove a package *only*
sudo pacman -R PACKAGE

# Remove a package and its dependencies not required by others
sudo pacman -Rs PACKAGE

# Remove a package, its deps, and config files (careful)
sudo pacman -Rns PACKAGE

# Upgrade the whole system (recommended Arch way)
sudo pacman -Syu

# Force refresh of all package databases, then upgrade
sudo pacman -Syyu
```

---

## Sync DB & Mirrors

```bash
# Refresh package databases (no upgrade)
sudo pacman -Sy

# Just update the package databases twice (e.g., if signature issues)
sudo pacman -Syy
```

> Note: On Arch, avoid partial upgrades (i.e., `-Sy` without `-u` then installing packages later).  
> Typically use `sudo pacman -Syu` to upgrade and install in one go.

---

## Files, Ownership, and “What owns this file?”

```bash
# List all files installed by a package
pacman -Ql PACKAGE

# Show which package owns a given file (installed packages)
pacman -Qo /path/to/file

# Query the sync DB for a file (repos; not necessarily installed)
pacman -F /path/to/file            # first ensure the file DB is enabled/updated
pacman -F FILE_NAME

# Check installed files of a package for missing/altered files
pacman -Qk PACKAGE
```

---

## Cleaning the Package Cache

> Pacman stores package files under `/var/cache/pacman/pkg/`.

```bash
# Remove cached packages that are no longer installed
sudo pacman -Sc

# Clear the entire cache (all cached packages; be careful)
sudo pacman -Scc
```

---

## Dealing with Orphans

```bash
# List orphaned packages (deps no longer needed)
pacman -Qdt

# Remove orphaned packages (review the list before running!)
sudo pacman -Rns $(pacman -Qqdt)
```

---

## Local Package Files (.pkg.tar.zst)

```bash
# Install a local package file
sudo pacman -U /path/to/package.pkg.tar.zst

# Install from a URL
sudo pacman -U https://example.com/package.pkg.tar.zst
```

---

## Useful One-Liners

```bash
# Check if a package is installed (script-friendly)
if pacman -Q neovim &>/dev/null; then
  echo "neovim is installed"
else
  echo "neovim is NOT installed"
fi

# List all explicitly installed packages, sorted
pacman -Qqe | sort

# List top-level packages that depend on a given package
pactree -r PACKAGE
```

---

## AUR Helpers (Not pacman, but commonly used)

> AUR helpers wrap pacman + build steps. Examples: `yay`, `paru`.

```bash
# Installing from AUR using yay (example)
yay -S PACKAGE

# Upgrade all system + AUR packages
yay -Syu
```

---

## References

- Arch Wiki – Pacman  
  https://wiki.archlinux.org/title/Pacman

- Arch Wiki – Pacman Tips & Tricks  
  https://wiki.archlinux.org/title/Pacman/Tips_and_tricks

- Pacman Rosetta (cheatsheet vs other distros)  
  https://wiki.archlinux.org/title/Pacman/Rosetta
