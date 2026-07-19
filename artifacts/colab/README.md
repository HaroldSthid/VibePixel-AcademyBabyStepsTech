# Colab Learning Artifact

Use this folder to parse the spreadsheet export, preview the avatar, and export a GIF or still image for the next workshop step.

## Quick path

1. Copy the exported spreadsheet CSV into the Colab session or point the notebook at `artifacts/spreadsheet/templates/avatar-16x16.csv`.
2. Open `vibepixel_avatar_pipeline.ipynb` and run the import, preview, and export cells in order. The first import cell will fetch `avatar_pipeline.py` automatically if it is missing, so students do not need to copy files by hand.
3. If your export has one frame only, use the generated still preview image.
4. Copy the exported GIF or PNG into `artifacts/exports/avatars/` when you want the repo-hosted handoff.

## Validation

Run `python validate_avatar_pipeline.py` in the same folder to check valid imports, invalid-cell guidance, preview rendering, multi-frame GIF export, and the single-frame fallback. If Pillow is missing, install it first with `pip install pillow`.

## Files

| File | Purpose |
|------|---------|
| `avatar_pipeline.py` | Readable Python flow for parsing, previewing, and exporting frames. |
| `vibepixel_avatar_pipeline.ipynb` | Colab notebook that mirrors the pipeline for learners. |
| `validate_avatar_pipeline.py` | Deterministic contract checks for import, preview, and export behavior. |

## Contract

| Topic | Rule |
|-------|------|
| Import | Accept numeric palette IDs, Hex values, RGB values, and blank cells. |
| Validation | Reject unsupported cells with a message that names the frame and cell. |
| Preview | Show an upscaled avatar preview before export. |
| Export | Write an animated GIF when multiple frames exist; write a still preview when only one frame exists. |

## Hand-off

The export step should produce a repository-friendly asset that can be copied to `artifacts/exports/avatars/` and shared through a public HTTPS URL in the CodePen slice.
