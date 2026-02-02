## Remove package

`sudo pacman -Rcns <package>`

If I see a potential problem with `-c` I can run:

`sudo pacman -Runs <package>`

|      | Description                                             |
| ---- | ------------------------------------------------------- |
| `-R` | remove                                                  |
| `-c` | cascade (I always check what will get removed)          |
| `-n` | no save (when I remove something I really want it gone) |
| `-s` | remove dependencies ( mostly for cleanup)               |
| `-u` | avoid removing packages if other packages depend on it  |
