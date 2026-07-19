"""Utilities for the RGB discovery challenge Colab notebook.

The helpers keep the notebook small while still letting learners:
- open an uploaded JPG/PNG or a bundled sample image,
- convert pixels into RGB/hex rows,
- export a CSV,
- rebuild a PNG from the CSV,
- and prepare the final submission files.
"""

from __future__ import annotations

import csv
import re
import shutil
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - Colab installs Pillow separately.
    Image = None
    ImageDraw = None
    ImageFont = None

if Image is not None:
    _RESAMPLING = getattr(Image, "Resampling", Image)
    LANCZOS = getattr(_RESAMPLING, "LANCZOS", getattr(Image, "LANCZOS", 1))
    NEAREST = getattr(_RESAMPLING, "NEAREST", getattr(Image, "NEAREST", 0))
else:  # pragma: no cover - import failure path.
    LANCZOS = 1
    NEAREST = 0


RAW_SAMPLE_IMAGE_URL = (
    "https://raw.githubusercontent.com/HaroldSthid/"
    "VibePixel-AcademyBabyStepsTech/main/artifacts/rgb-discovery/rgb-discovery-preview.png"
)
DEFAULT_SAMPLE_IMAGE_NAME = "rgb-discovery-preview.png"
DEFAULT_OUTPUT_CSV = "rgb-discovery-output.csv"
DEFAULT_OUTPUT_PNG = "rgb-discovery-revealed.png"
DEFAULT_MAX_SIDE = 48
DEFAULT_DOWNLOAD_TIMEOUT = 10


class RGBDiscoveryError(ValueError):
    """Raised when the RGB discovery challenge cannot be completed."""


def _require_pillow() -> None:
    if Image is None or ImageDraw is None or ImageFont is None:
        raise RGBDiscoveryError(
            "Pillow is required. Install it in Colab with `pip install pillow`."
        )


def normalize_student_alias(student_alias: str | Path) -> str:
    """Normalize and validate the student alias used for delivery files."""

    alias = "".join(str(student_alias).split()).upper()
    if not alias:
        raise RGBDiscoveryError(
            "Necesitamos tu alias de entrega. Usá 6 letras en mayúsculas, por ejemplo HARPIR."
        )

    if not re.fullmatch(r"[A-Z]{6}", alias):
        raise RGBDiscoveryError(
            "Tu alias debe tener exactamente 6 letras A-Z, sin espacios ni símbolos. "
            "Ejemplo: HARPIR."
        )

    return alias


def student_output_filename(student_alias: str | Path, base_filename: str) -> str:
    """Build an alias-prefixed filename for the submission assets."""

    alias = normalize_student_alias(student_alias)
    return f"{alias}-{base_filename}"


def download_sample_image(destination: str | Path, *, timeout: int = DEFAULT_DOWNLOAD_TIMEOUT) -> Path:
    """Download the bundled sample image when it is missing locally."""

    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(RAW_SAMPLE_IMAGE_URL, timeout=timeout) as response:
            target.write_bytes(response.read())
    except Exception as exc:  # pragma: no cover - network dependent.
        raise FileNotFoundError(
            "No pudimos descargar la imagen de ejemplo automáticamente. Revisá tu conexión, "
            "subí tu propio JPG/PNG y volvé a ejecutar esta celda."
        ) from exc

    return target


def resolve_source_image(
    uploaded_image_path: str | Path | None = None,
    *,
    sample_image_path: str | Path = DEFAULT_SAMPLE_IMAGE_NAME,
    timeout: int = DEFAULT_DOWNLOAD_TIMEOUT,
) -> Path:
    """Return the image learners should use for the challenge."""

    uploaded = Path(uploaded_image_path) if uploaded_image_path else None
    if uploaded and uploaded.exists():
        return uploaded

    sample = Path(sample_image_path)
    if sample.exists():
        return sample

    return download_sample_image(sample, timeout=timeout)


def open_rgb_image(image_path: str | Path) -> Image.Image:
    """Open an image and normalize it to RGB."""

    _require_pillow()
    path = Path(image_path)
    if not path.exists():
        raise RGBDiscoveryError(f"No encontramos la imagen de entrada: {path}")

    return Image.open(path).convert("RGB")


def fit_study_image(image: Image.Image, *, max_side: int = DEFAULT_MAX_SIDE) -> Image.Image:
    """Shrink large inputs so the resulting CSV stays lightweight."""

    _require_pillow()
    study = image.copy()
    study.thumbnail((max_side, max_side), LANCZOS)
    return study


def image_to_rgb_rows(image: Image.Image) -> list[dict[str, str]]:
    """Convert an image into CSV-ready pixel rows."""

    _require_pillow()
    rgb = image.convert("RGB")
    rows: list[dict[str, str]] = []
    for y in range(rgb.height):
        for x in range(rgb.width):
            red, green, blue = rgb.getpixel((x, y))
            rows.append(
                {
                    "row": str(y),
                    "col": str(x),
                    "r": str(red),
                    "g": str(green),
                    "b": str(blue),
                    "hex": f"#{red:02X}{green:02X}{blue:02X}",
                }
            )
    return rows


def write_rgb_csv(image: Image.Image, output_path: str | Path) -> Path:
    """Write the pixel matrix to a CSV file and return its path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = image_to_rgb_rows(image)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["row", "col", "r", "g", "b", "hex"])
        writer.writeheader()
        writer.writerows(rows)
    return path


def read_rgb_csv(csv_path: str | Path) -> tuple[Image.Image, list[dict[str, str]]]:
    """Read the exported CSV back into pixels and the original rows."""

    path = Path(csv_path)
    if not path.exists():
        raise RGBDiscoveryError(f"No encontramos el CSV exportado: {path}")

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"row", "col", "r", "g", "b"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise RGBDiscoveryError(
                f"El CSV necesita estas columnas: {', '.join(sorted(missing))}."
            )

        rows: list[dict[str, str]] = []
        pixels: list[tuple[int, int, int, int]] = []
        max_row = -1
        max_col = -1
        for line_number, row in enumerate(reader, start=2):
            try:
                y = int((row.get("row") or "").strip())
                x = int((row.get("col") or "").strip())
                red = int((row.get("r") or "").strip())
                green = int((row.get("g") or "").strip())
                blue = int((row.get("b") or "").strip())
            except ValueError as exc:
                raise RGBDiscoveryError(
                    f"Hay una fila inválida en la línea {line_number}. Revisá row, col, r, g y b."
                ) from exc

            problems: list[str] = []
            if x < 0 or y < 0:
                problems.append(f"coordenadas negativas (row={y}, col={x})")

            out_of_range_channels = [
                f"{name}={value}"
                for name, value in (("r", red), ("g", green), ("b", blue))
                if value < 0 or value > 255
            ]
            if out_of_range_channels:
                problems.append(f"valores RGB fuera de rango ({', '.join(out_of_range_channels)})")

            if problems:
                raise RGBDiscoveryError(
                    f"Hay un dato inválido en la línea {line_number}: {'; '.join(problems)}. "
                    "Las coordenadas deben ser 0 o mayores y los valores RGB deben estar entre 0 y 255."
                )

            rows.append(row)
            pixels.append((x, y, red, green, blue))
            max_row = max(max_row, y)
            max_col = max(max_col, x)

    if max_row < 0 or max_col < 0:
        raise RGBDiscoveryError("El CSV no tiene filas de píxeles para reconstruir.")

    canvas = Image.new("RGB", (max_col + 1, max_row + 1), (255, 255, 255))
    for x, y, red, green, blue in pixels:
        canvas.putpixel((x, y), (red, green, blue))

    return canvas, rows


def rebuild_png_from_csv(csv_path: str | Path, output_path: str | Path) -> Path:
    """Rebuild the image from CSV rows and save it as PNG."""

    image, _ = read_rgb_csv(csv_path)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return path


def make_comparison_panel(
    original: Image.Image,
    revealed: Image.Image,
    *,
    scale: int = 6,
    padding: int = 16,
) -> Image.Image:
    """Create a simple side-by-side comparison image."""

    _require_pillow()
    left = original.resize((original.width * scale, original.height * scale), NEAREST)
    right = revealed.resize((revealed.width * scale, revealed.height * scale), NEAREST)
    label_height = 28
    width = left.width + right.width + padding * 3
    height = max(left.height, right.height) + padding * 2 + label_height
    panel = Image.new("RGB", (width, height), (248, 246, 240))
    draw = ImageDraw.Draw(panel)
    font = ImageFont.load_default()

    draw.text((padding, padding), "Original", fill=(23, 23, 23), font=font)
    draw.text((left.width + padding * 2, padding), "Revealed", fill=(23, 23, 23), font=font)
    panel.paste(left, (padding, padding + label_height))
    panel.paste(right, (left.width + padding * 2, padding + label_height))
    return panel


def prepare_submission_assets(
    csv_path: str | Path,
    png_path: str | Path,
    output_dir: str | Path,
    student_alias: str | Path,
) -> dict[str, str]:
    """Copy the final files into a shareable Top 10 submission folder."""

    alias = normalize_student_alias(student_alias)
    destination = Path(output_dir) / alias
    destination.mkdir(parents=True, exist_ok=True)

    csv_target = destination / student_output_filename(alias, DEFAULT_OUTPUT_CSV)
    png_target = destination / student_output_filename(alias, DEFAULT_OUTPUT_PNG)
    shutil.copy2(csv_path, csv_target)
    shutil.copy2(png_path, png_target)

    return {
        "csv": str(csv_target),
        "png": str(png_target),
        "folder": str(destination),
    }
