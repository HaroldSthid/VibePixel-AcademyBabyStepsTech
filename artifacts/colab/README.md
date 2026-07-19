# Colab Learning Artifact

Usá esta carpeta para el flujo de Colab del avatar y para el nuevo Colab paso a paso del desafío RGB.

## Ruta rápida

1. Abrí `vibepixel_avatar_pipeline.ipynb` para el flujo del avatar o `rgb_discovery_challenge.ipynb` para el desafío RGB paso a paso.
2. En la notebook RGB, dejá la imagen de ejemplo si querés una primera corrida automática; después podés cambiar la variable por tu JPG/PNG.
3. Usá los nombres de salida claros (`rgb-discovery-output.csv` y `rgb-discovery-revealed.png`) para compartir la evidencia sin confundir archivos.
4. Copiá los resultados a la carpeta de entrega que uses en tu clase o propuesta.

## Si algo falla

- Si aparece un error que nombra `avatar_pipeline`, en Colab abrí **Runtime** en el menú superior, elegí **Restart runtime** y corré desde la primera celda. El notebook debería descargar el archivo solo.
- Si aparece `rgb_discovery_tools.py` o la imagen de ejemplo faltante, hacé lo mismo: **Runtime → Restart runtime** y empezá desde la primera celda para que baje los archivos automáticamente.
- Si la red o GitHub están bloqueados, probá más tarde o pedile ayuda a quien esté facilitando la clase.
- Cuando todo vuelve a andar, deberías ver la importación completa, la vista previa y la exportación final sin tocar archivos a mano.

## Validación para facilitadores / mantenimiento

Ejecutá `python validate_avatar_pipeline.py` para el flujo del avatar o `python validate_rgb_discovery_challenge.py` para el flujo RGB. Ambos chequearán imports válidos, fallback de primera corrida y exportación correcta. Si falta Pillow, instalalo con `pip install pillow` primero.

## Files

| File | Purpose |
|------|---------|
| `avatar_pipeline.py` | Readable Python flow for parsing, previewing, and exporting frames. |
| `vibepixel_avatar_pipeline.ipynb` | Colab notebook that mirrors the avatar pipeline for learners. |
| `rgb_discovery_tools.py` | RGB image-to-CSV and CSV-to-image helpers for the step-by-step challenge. |
| `rgb_discovery_challenge.ipynb` | Colab notebook that guides learners through upload, export, rebuild, and submission prep. |
| `validate_avatar_pipeline.py` | Deterministic contract checks for import, preview, and export behavior. |
| `validate_rgb_discovery_challenge.py` | Deterministic checks for the RGB challenge notebook and helper. |

## Contract

| Topic | Rule |
|-------|------|
| Import | Accept numeric palette IDs, Hex values, RGB values, and blank cells. |
| Validation | Reject unsupported cells with a message that names the frame and cell. |
| Preview | Show an upscaled avatar preview before export. |
| Export | Write an animated GIF when multiple frames exist; write a still preview when only one frame exists. |

## Hand-off

The export step should produce a repository-friendly asset that can be copied to `artifacts/exports/avatars/` and shared through a public HTTPS URL in the CodePen slice.
