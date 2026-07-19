"""Colab avatar pipeline for the learning-artifacts-export slice.

Parse exported spreadsheet rows, validate frame data, render a preview,
and export either an animated GIF or a still preview image.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, Mapping

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover - Colab installs Pillow separately.
    Image = None
    ImageDraw = None


FRAME_SIZE = 16
DEFAULT_SCALE = 16
DEFAULT_DURATION_MS = 180
DEFAULT_PALETTE = {
    1: (255, 204, 0),
    2: (0, 204, 255),
    3: (255, 102, 153),
    4: (102, 255, 153),
}

HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
INT_RE = re.compile(r"^\d+$")
RGB_RE = re.compile(r"^\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*$")


class AvatarPipelineError(ValueError):
    """Raised when the spreadsheet export cannot be parsed or rendered."""


def _cell_label(frame_id: str, row: int, col: int) -> str:
    return f"{frame_id}[{row},{col}]"


def _empty_frame(size: int = FRAME_SIZE) -> list[list[tuple[int, int, int] | None]]:
    return [[None for _ in range(size)] for _ in range(size)]


def _parse_rgb(raw: str) -> tuple[int, int, int]:
    parts = [part.strip() for part in raw.split(",")]
    if len(parts) != 3:
        raise AvatarPipelineError("RGB values must contain exactly three comma-separated channels.")

    channels: list[int] = []
    for part in parts:
        if not part.isdigit():
            raise AvatarPipelineError(f"RGB channel '{part}' is not a whole number.")
        value = int(part)
        if value < 0 or value > 255:
            raise AvatarPipelineError(f"RGB channel '{part}' is outside the 0-255 range.")
        channels.append(value)

    return tuple(channels)  # type: ignore[return-value]


def parse_color_value(
    raw: str | None,
    *,
    palette: Mapping[int, tuple[int, int, int]] | None = None,
    cell_label: str,
) -> tuple[int, int, int] | None:
    """Normalize a spreadsheet cell to RGB or transparency."""

    value = "" if raw is None else raw.strip()
    if value == "":
        return None

    if HEX_COLOR_RE.match(value):
        return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))

    if RGB_RE.match(value):
        return _parse_rgb(value)

    if INT_RE.match(value):
        palette_map = dict(DEFAULT_PALETTE)
        if palette:
            palette_map.update({int(key): tuple(color) for key, color in palette.items()})

        numeric_id = int(value)
        if numeric_id not in palette_map:
            raise AvatarPipelineError(
                f"Unknown palette ID '{numeric_id}' at {cell_label}. Use a defined palette ID, #RRGGBB, R,G,B, or blank."
            )
        return palette_map[numeric_id]

    raise AvatarPipelineError(
        f"Unsupported color value '{value}' at {cell_label}. Use a numeric palette ID, #RRGGBB, R,G,B, or blank."
    )


def load_avatar_frames(
    csv_path: str | Path,
    *,
    palette: Mapping[int, tuple[int, int, int]] | None = None,
    frame_size: int = FRAME_SIZE,
) -> list[tuple[str, list[list[tuple[int, int, int] | None]]]]:
    """Read ordered frame rows from the spreadsheet export."""

    path = Path(csv_path)
    if not path.exists():
        raise AvatarPipelineError(f"Missing spreadsheet export: {path}")

    frames: OrderedDict[str, list[list[tuple[int, int, int] | None]]] = OrderedDict()
    seen_cells: dict[str, set[tuple[int, int]]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"frame_id", "row", "col", "value"}
        missing = expected - set(reader.fieldnames or [])
        if missing:
            raise AvatarPipelineError(
                f"CSV header is missing required columns: {', '.join(sorted(missing))}."
            )

        for line_number, row in enumerate(reader, start=2):
            frame_id = (row.get("frame_id") or "").strip()
            if not frame_id:
                raise AvatarPipelineError(f"Missing frame_id on CSV row {line_number}.")

            try:
                row_index = int((row.get("row") or "").strip())
                col_index = int((row.get("col") or "").strip())
            except ValueError as exc:
                raise AvatarPipelineError(
                    f"Row and col must be whole numbers at line {line_number}."
                ) from exc

            if row_index < 0 or row_index >= frame_size or col_index < 0 or col_index >= frame_size:
                raise AvatarPipelineError(
                    f"Cell index out of range at {_cell_label(frame_id, row_index, col_index)}."
                    f" Expected 0-{frame_size - 1}."
                )

            cell_label = _cell_label(frame_id, row_index, col_index)
            color = parse_color_value(row.get("value"), palette=palette, cell_label=cell_label)
            frame_seen = seen_cells.setdefault(frame_id, set())
            coordinate = (row_index, col_index)
            if coordinate in frame_seen:
                raise AvatarPipelineError(
                    f"Duplicate cell entry at {cell_label}. Each frame coordinate may appear only once, "
                    f"including blank/transparent values."
                )
            frame_seen.add(coordinate)

            frame = frames.setdefault(frame_id, _empty_frame(frame_size))
            frame[row_index][col_index] = color

    if not frames:
        raise AvatarPipelineError(f"No frame rows were found in {path}.")

    return list(frames.items())


def render_frame(
    frame: list[list[tuple[int, int, int] | None]],
    *,
    scale: int = DEFAULT_SCALE,
) -> Image.Image:
    """Render a single frame to an RGBA image."""

    _require_pillow()
    image = Image.new("RGBA", (FRAME_SIZE * scale, FRAME_SIZE * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for row_index, row in enumerate(frame):
        for col_index, color in enumerate(row):
            if color is None:
                continue
            left = col_index * scale
            top = row_index * scale
            draw.rectangle([left, top, left + scale - 1, top + scale - 1], fill=(*color, 255))

    return image


def preview_avatar(
    frames: list[tuple[str, list[list[tuple[int, int, int] | None]]]],
    *,
    scale: int = DEFAULT_SCALE,
) -> Image.Image:
    """Render the first frame as a learner preview."""

    return render_frame(frames[0][1], scale=scale)


def export_avatar(
    frames: list[tuple[str, list[list[tuple[int, int, int] | None]]]],
    output_dir: str | Path,
    *,
    stem: str = "avatar",
    scale: int = DEFAULT_SCALE,
    duration_ms: int = DEFAULT_DURATION_MS,
) -> dict[str, str | int]:
    """Export a GIF for multi-frame avatars or a still preview for single-frame avatars."""

    _require_pillow()
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rendered_frames = [(frame_id, render_frame(frame, scale=scale)) for frame_id, frame in frames]
    preview_path = out_dir / f"{stem}_preview.png"
    rendered_frames[0][1].save(preview_path)

    if len(rendered_frames) == 1:
        return {
            "kind": "still",
            "frame_count": 1,
            "frame_id": rendered_frames[0][0],
            "path": str(preview_path),
            "message": "Only one frame was found, so the export is a still preview image.",
        }

    gif_path = out_dir / f"{stem}.gif"
    rendered_frames[0][1].save(
        gif_path,
        save_all=True,
        append_images=[image for _, image in rendered_frames[1:]],
        duration=duration_ms,
        loop=0,
    )
    return {
        "kind": "gif",
        "frame_count": len(rendered_frames),
        "frame_id": rendered_frames[0][0],
        "path": str(gif_path),
        "preview_path": str(preview_path),
        "message": "Animated GIF exported successfully.",
    }


def _require_pillow() -> None:
    if Image is None or ImageDraw is None:
        raise AvatarPipelineError(
            "Pillow is required for preview/export. Install it in Colab with `pip install pillow`."
        )


def _load_palette(path: str | Path | None) -> Mapping[int, tuple[int, int, int]] | None:
    if not path:
        return None

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    palette: dict[int, tuple[int, int, int]] = {}
    for raw_key, raw_color in payload.items():
        key = int(raw_key)
        if not isinstance(raw_color, list) or len(raw_color) != 3:
            raise AvatarPipelineError("Palette JSON values must be [r, g, b] arrays.")
        palette[key] = tuple(int(channel) for channel in raw_color)
    return palette


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse, preview, and export avatar frames from spreadsheet CSV data.")
    parser.add_argument("csv_path", help="Path to the exported spreadsheet CSV.")
    parser.add_argument("--output-dir", default="exports", help="Directory for the preview/GIF output.")
    parser.add_argument("--stem", default="avatar", help="Output filename stem.")
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE, help="Pixel scale for preview/export images.")
    parser.add_argument(
        "--duration-ms",
        type=int,
        default=DEFAULT_DURATION_MS,
        help="Frame duration in milliseconds for the GIF export.",
    )
    parser.add_argument(
        "--palette-json",
        default=None,
        help="Optional JSON file mapping numeric palette IDs to [r, g, b] arrays.",
    )

    args = parser.parse_args(list(argv) if argv is not None else None)
    frames = load_avatar_frames(args.csv_path, palette=_load_palette(args.palette_json))
    preview_avatar(frames, scale=args.scale)
    result = export_avatar(frames, args.output_dir, stem=args.stem, scale=args.scale, duration_ms=args.duration_ms)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
