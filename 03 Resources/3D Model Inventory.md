---
type: topic
created: 2026-08-17 20:45
tags: [3d-printing, inventory]
---
# 3D Model Inventory

Snapshot of every 3D model file in Google Drive as of **2026-08-17**, taken during the
Drive reorg ([[Drive Reorg 2026-08-17]]) so the model cleanup can be deferred without
losing track of what exists.

> **Nothing here has been moved or renamed.** The reorg stopped at the models on purpose —
> sorting authored-vs-downloaded, resolving duplicate names, and deciding what to keep
> needs someone who knows what the objects are.

**28 files across 4 locations.** Drive folder: [3D Modeling](https://drive.google.com/drive/folders/1tCFBbyXrnamMtROLiUbHegkvMaqnUM61)

## My Drive root — 9 loose files

Never filed. These are the reorg's leftovers.

| File | Size | Notes |
|---|---|---|
| `Hook.3mf` | 7 KB | Same object as the two below? |
| `hooks.step` | 4.8 MB | CAD source |
| `hooks.stl` | 116 KB | Mesh export |
| `cyl.3mf` | 6.7 KB | "cyl" = cylinder; a test print? |
| `dress_cookie_cutter.stp` | **182 MB** | Preheat to 350 work. Largest model file in Drive |
| `Paige Coin2.3mf` | 20 KB | Paige Stanek Creations |
| `Paige Coin3.3mf` | 351 KB | v3 — 17× larger than v2 |
| `shapr3d_export_2025-09-26_10h51m.3mf` | 5 KB | Tool default name; object unknown |
| `Outside Fridge Handle Cover2.stl` | 16,684 B | **See the fridge-handle problem below** |

## `3D Modeling/` top level — 5 loose files

| File | Size | Notes |
|---|---|---|
| `Outside Fridge Handle Cover.stl` | 16,684 B | |
| `Outside Fridge Handle Cover.stl` | 18,684 B | **Identical name, different file** |
| `Shoerackpeg.stl` | 2,284 B | Mesh |
| `Shoerackpeg.gcode.3mf` | 53,820 B | Sliced — printer-ready, not a model |
| `gridplates-400x322-Standard-4ba4d.stl` | 1.6 MB | Gridfinity baseplate; belongs in `GridFinity/` |

## `3D Modeling/My Models/` — 1 file

| File | Size | Notes |
|---|---|---|
| `martini.scad` | 4.6 KB | OpenSCAD source. **The only file in here** |

## `3D Modeling/Downloaded Models/` — 4 files

| File | Size | Notes |
|---|---|---|
| `README.md` | 26 B | |
| `MiniToolBox+Base+Files.3mf` | 2.1 MB | `+` separators from a download |
| `megaphone-cookie-cutter-multiple-sizes-available20250415-1-7y1r7z.zip` | 615 KB | **Never unpacked.** Cookie cutter → Preheat to 350 |
| `V2SPINNYRACK.rar` | 9.2 MB | **Never unpacked.** ALLCAPS, and `.rar` needs a tool most systems lack |

## `3D Modeling/GridFinity/` — 9 files

All Gridfinity bins from a parametric generator, all carrying a 5-character hash.

| File | Size |
|---|---|
| `gf-extended-bin-1x2x4-s1x1-ac8ce.stl` | 180 KB |
| `gf-extended-bin-1x3x4-s1x1-edb15.stl` | 216 KB |
| `gf-extended-bin-1x5x4-s1x1-79a31.stl` | 288 KB |
| `gf-extended-bin-1x5x6-s1x1-e20e6.stl` | 288 KB |
| `gf-extended-bin-3x2x4-s1x1-a88f8 (1).stl` | 283 KB |
| `gf-rebuilt-bin-2x2x4-s1x1-Standard-d0e6d.stl` | 584 KB |
| `gf-rebuilt-bin-3x4x4-s1x1-Standard-26369.stl` | 1.4 MB |
| `gf-rebuilt-bin-4x2x4-s1x1-Standard-bf0bc.stl` | 997 KB |
| `gf-relocated-bin-…` *(see Drive; naming follows the same pattern)* | |

The `WxDxH` dimensions in these names are genuinely useful — this is one case where a
generator's naming beats anything hand-written. Only the trailing hash and the ` (1)`
are noise.

---

## What makes this a real cleanup, not a filing job

**The fridge handle.** Three files, two names, no versioning that means anything:

- `3D Modeling/Outside Fridge Handle Cover.stl` — 16,684 B
- `3D Modeling/Outside Fridge Handle Cover.stl` — 18,684 B ← *same name*
- root `Outside Fridge Handle Cover2.stl` — 16,684 B ← *same size as the first*

So "Cover2" is probably a copy of the smaller one rather than a second version, and the
18,684-byte file is the actual revision. That can only be settled by opening them.

**`My Models/` vs `Downloaded Models/` is not being used.** One authored file sits in
`My Models/`, while 14 authored-or-downloaded files sit loose at root and in
`3D Modeling/` top level. The distinction is worth keeping — you can re-download a
Printables model, you cannot re-derive your own `.scad` — but it needs enforcing.

**Source vs export vs sliced are mixed together.** `hooks.step` (CAD source),
`hooks.stl` (mesh export) and `Shoerackpeg.gcode.3mf` (sliced, printer- and
filament-specific) are three different kinds of artefact with different lifespans. Sliced
files are disposable; `.scad` and `.step` sources are not.

**Two archives were never unpacked**, so their contents are invisible to search and to
this inventory.

**One file is 182 MB** — `dress_cookie_cutter.stp` is larger than everything else here
combined.

## Suggested approach when you tackle it

1. Open the three fridge-handle files, keep one, delete the rest.
2. Unpack the `.zip` and `.rar`, then delete the archives.
3. Split by provenance: `Sources/` (`.scad`, `.step`, `.stp`), `Prints/` (`.stl`, `.3mf`),
   `Downloaded/`. Drop sliced `.gcode.3mf` files entirely — they regenerate.
4. Move `gridplates-…stl` into `GridFinity/` where its siblings live.
5. Route business models to the folders that already exist for them:
   `3D Modeling/PreheatTo350/` (cookie cutters) and `3D Modeling/PaigeStanekCreations/` —
   both currently empty.
6. Name the one unknown: `shapr3d_export_2025-09-26_10h51m.3mf`.

Naming pattern to apply, per [[Conventions]]: `{Object} v{n}.{ext}` — so
`Fridge Handle Cover v2.stl`, not `Outside Fridge Handle Cover2.stl`.
