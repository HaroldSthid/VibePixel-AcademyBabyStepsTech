"""Deterministic contract checks for the Colab avatar pipeline.

Run this file from the `artifacts/colab/` folder after installing Pillow.
It validates the learner-facing parser/export behavior without requiring
the full application stack.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from avatar_pipeline import AvatarPipelineError, Image, export_avatar, load_avatar_frames, preview_avatar


VALID_IMPORT_CSV = """frame_id,row,col,value
idle_01,0,0,1
idle_01,0,1,#FFCC00
idle_01,0,2,"255,204,0"
idle_01,1,0,
wave_01,0,0,2
wave_01,0,1,#00CCFF
wave_01,0,2,"0,153,255"
wave_01,1,0,3
"""

INVALID_CELL_CSV = """frame_id,row,col,value
bad_01,0,0,1
bad_01,0,1,not-a-color
"""

DUPLICATE_BLANK_CSV = """frame_id,row,col,value
blank_01,0,0,
blank_01,0,0,
"""


def _write_fixture(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.write_text(content, encoding="utf-8")
    return path


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_valid_imports() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = _write_fixture(Path(temp_dir), "valid.csv", VALID_IMPORT_CSV)
        frames = load_avatar_frames(csv_path)

    _check(len(frames) == 2, f"Expected 2 frames, got {len(frames)}.")
    _check([frame_id for frame_id, _ in frames] == ["idle_01", "wave_01"], "Frame order changed.")

    idle_frame = frames[0][1]
    wave_frame = frames[1][1]
    _check(idle_frame[0][0] == (255, 204, 0), "Numeric palette ID did not resolve to the expected color.")
    _check(idle_frame[0][1] == (255, 204, 0), "Hex color did not parse correctly.")
    _check(idle_frame[0][2] == (255, 204, 0), "Quoted RGB value did not parse correctly.")
    _check(idle_frame[1][0] is None, "Blank cells should remain transparent.")
    _check(wave_frame[0][0] == (0, 204, 255), "Second frame palette ID did not resolve correctly.")


def check_invalid_cell_guidance() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = _write_fixture(Path(temp_dir), "invalid.csv", INVALID_CELL_CSV)
        try:
            load_avatar_frames(csv_path)
        except AvatarPipelineError as exc:
            message = str(exc)
            _check("Unsupported color value 'not-a-color' at bad_01[0,1]." in message, "Invalid-cell guidance omitted the cell label.")
            _check("Use a numeric palette ID, #RRGGBB, R,G,B, or blank." in message, "Invalid-cell guidance omitted the learner fix hint.")
        else:
            raise AssertionError("Expected AvatarPipelineError for an unsupported color value.")


def check_duplicate_blank_detection() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = _write_fixture(Path(temp_dir), "duplicate_blank.csv", DUPLICATE_BLANK_CSV)
        try:
            load_avatar_frames(csv_path)
        except AvatarPipelineError as exc:
            message = str(exc)
            _check("Duplicate cell entry at blank_01[0,0]." in message, "Duplicate blank cells should point to the repeated coordinate.")
            _check("blank/transparent values" in message, "Duplicate blank cells should be rejected explicitly.")
        else:
            raise AssertionError("Expected duplicate blank cells to fail.")


def check_preview_and_exports() -> dict[str, str]:
    if Image is None:
        return {"status": "skipped", "reason": "Pillow is not installed; preview/export checks require it."}

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        csv_path = _write_fixture(temp_path, "valid.csv", VALID_IMPORT_CSV)
        frames = load_avatar_frames(csv_path)

        preview = preview_avatar(frames, scale=2)
        _check(preview.size == (32, 32), f"Preview size changed: {preview.size}.")
        _check(preview.mode == "RGBA", f"Preview mode changed: {preview.mode}.")
        _check(preview.getpixel((0, 0)) == (255, 204, 0, 255), "Preview did not render the expected pixel color.")
        _check(preview.getpixel((3, 3))[3] == 0, "Transparent preview pixels should stay transparent.")

        gif_result = export_avatar(frames, temp_path, stem="avatar", scale=2, duration_ms=90)
        _check(gif_result["kind"] == "gif", f"Expected GIF export, got {gif_result['kind']}.")
        gif_path = Path(str(gif_result["path"]))
        preview_path = Path(str(gif_result["preview_path"]))
        _check(gif_path.exists(), "GIF export file was not created.")
        _check(preview_path.exists(), "Preview PNG for the GIF export was not created.")

        with Image.open(gif_path) as gif_image:
            _check(getattr(gif_image, "is_animated", False), "Multi-frame export should be animated.")
            _check(gif_image.n_frames == 2, f"Expected 2 exported GIF frames, got {gif_image.n_frames}.")

        still_result = export_avatar(frames[:1], temp_path, stem="avatar_single", scale=2)
        _check(still_result["kind"] == "still", f"Expected still export, got {still_result['kind']}.")
        still_path = Path(str(still_result["path"]))
        _check(still_path.name == "avatar_single_preview.png", "Single-frame fallback should write a preview PNG.")
        _check(still_path.exists(), "Single-frame preview PNG was not created.")

    return {"status": "passed", "reason": "Pillow available and export checks passed."}


def run_contract_checks() -> list[dict[str, str]]:
    checks = []

    check_valid_imports()
    checks.append({"check": "valid_imports", "status": "passed"})

    check_invalid_cell_guidance()
    checks.append({"check": "invalid_cell_guidance", "status": "passed"})

    check_duplicate_blank_detection()
    checks.append({"check": "duplicate_blank_detection", "status": "passed"})

    checks.append({"check": "preview_and_exports", **check_preview_and_exports()})

    return checks


def main() -> int:
    results = run_contract_checks()
    print(json.dumps({"checks": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
