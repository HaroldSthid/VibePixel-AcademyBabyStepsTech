# Spreadsheet Learning Artifact

Use the grid template to draw in a true 16x16 spreadsheet layout. Then export or copy the normalized rows for Colab.

## Quick path

1. Open `templates/avatar-16x16-grid.csv` to edit each frame on a visible 16x16 grid.
2. Use frame labels such as `idle_01`, `wave_01`, `wave_02` to keep frame order clear.
3. Fill grid cells with numeric palette IDs, `#RRGGBB`, or quoted `R,G,B` values such as `"255,204,0"`.
4. Leave a cell blank to represent transparency unless you intentionally document a background color.
5. Use `templates/avatar-16x16.csv` as the normalized row sample that Colab consumes.

## Contract

| Topic | Rule |
|-------|------|
| Learner grid | Each frame MUST provide a 16x16 editable grid. |
| Grid boundaries | Row and column labels SHOULD make the 0–15 boundaries visible to learners. |
| Normalized export | Exported rows MUST preserve frame order before row and column order. |
| Empty cells | Blank cells MUST be treated as transparent or as a documented background value. |
| Color inputs | v1 MUST support numeric palette IDs, Hex values, and RGB values. |

> CSV note: any RGB value that contains commas must stay inside one quoted field, for example `"255,204,0"`.

## Files

| File | Purpose |
|------|---------|
| `templates/avatar-16x16-grid.csv` | Learner-facing editable grid template with two 16x16 frame blocks. |
| `templates/avatar-16x16.csv` | Sparse normalized export sample for Colab parsing. |

## Export handoff

The normalized spreadsheet export should produce rows in this canonical shape:

```csv
frame_id,row,col,value
idle_01,0,0,#FFCC00
idle_01,0,1,"255,204,0"
idle_01,0,2,1
```

Colab consumes the exported rows, validates the frame size, and turns the ordered cells into image frames.

## Checklist

- [x] Every frame has a 16x16 learner grid.
- [x] Frame order is explicit in the exported data.
- [x] Hex, RGB, and numeric palette inputs are documented.
- [x] Blank cells are documented as transparent or background.
