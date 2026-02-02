List the orphaned packages:
```bash
pacman -Qdtq
```

Remove the orphaned packages:
```bash
sudo pacman -Rns $(pacman -Qdtq)
```

Remove an AUR package along with its dependencies:
```bash
yay -Rns <package>
```

