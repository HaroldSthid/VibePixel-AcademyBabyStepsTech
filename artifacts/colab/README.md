# Colab Learning Artifact

Usá esta carpeta para importar la exportación de la planilla, previsualizar el avatar y exportar un GIF o una imagen fija para el siguiente paso del taller.

## Ruta rápida

1. Abrí `vibepixel_avatar_pipeline.ipynb` y ejecutá las celdas en orden. La notebook baja `avatar_pipeline.py` y un CSV de ejemplo automáticamente si faltan, así que podés ver el flujo completo sin subir archivos a mano.
2. Si ya tenés tu propia exportación, reemplazá `avatar-16x16.csv` por ese archivo y volvé a ejecutar la celda de carga.
3. Si tu exportación tiene un solo frame, usá la imagen fija generada como preview.
4. Copiá el GIF o PNG exportado en `artifacts/exports/avatars/` cuando quieras dejar listo el handoff dentro del repo.

## Validación

Ejecutá `python validate_avatar_pipeline.py` en la misma carpeta para chequear imports válidos, ayuda ante celdas inválidas, renderizado del preview, exportación GIF multi-frame, el fallback de primera corrida del CSV y el mensaje de recuperación del notebook. Si falta Pillow, instalalo con `pip install pillow` primero.

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
