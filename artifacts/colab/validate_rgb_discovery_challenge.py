"""Deterministic checks for the RGB discovery Colab notebook.

Run this file from `artifacts/colab/` after installing Pillow.
It validates the notebook structure and the helper pipeline without
requiring the full application stack.
"""

from __future__ import annotations

import json
import re
import os
import tempfile
from pathlib import Path

from rgb_discovery_tools import (
    HELPER_VERSION,
    DEFAULT_OUTPUT_CSV,
    DEFAULT_OUTPUT_PNG,
    fit_study_image,
    image_to_rgb_rows,
    make_comparison_panel,
    open_rgb_image,
    prepare_submission_assets,
    normalize_student_alias,
    student_output_filename,
    rebuild_png_from_csv,
    resolve_source_image,
    write_rgb_csv,
)


NOTEBOOK_PATH = Path(__file__).with_name("rgb_discovery_challenge.ipynb")
HELPER_PATH = Path(__file__).with_name("rgb_discovery_tools.py")
SAMPLE_IMAGE_PATH = Path(__file__).resolve().parents[1] / "rgb-discovery" / "rgb-discovery-preview.png"


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_notebook() -> dict:
    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def _code_cells(notebook: dict) -> list[dict]:
    return [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]


def _compile_notebook_code_cells(notebook: dict) -> None:
    for index, cell in enumerate(_code_cells(notebook), start=1):
        compile("".join(cell.get("source", [])), f"{NOTEBOOK_PATH.name}#cell{index}", "exec")


def _cell_source_by_id(notebook: dict, cell_id: str) -> str:
    for cell in _code_cells(notebook):
        if cell.get("metadata", {}).get("id") == cell_id:
            return "".join(cell.get("source", []))
    raise AssertionError(f"Could not find notebook code cell with id '{cell_id}'.")


def _bootstrap_source_with_helper_url(notebook: dict, helper_url: str) -> str:
    source = _cell_source_by_id(notebook, "bootstrap")
    return re.sub(r'HELPER_URL = ".*?"', f'HELPER_URL = "{helper_url}"', source, count=1)


def check_notebook_contract() -> None:
    notebook = _load_notebook()
    notebook_text = json.dumps(notebook, ensure_ascii=False)

    _check("rgb_discovery_tools.py" in notebook_text, "Notebook should bootstrap the helper module.")
    _check("EXPECTED_HELPER_VERSION" in notebook_text, "Notebook should pin the helper version.")
    _check("REQUIRED_HELPER_ATTRIBUTES" in notebook_text, "Notebook should validate the helper API.")
    _check("student_alias" in notebook_text, "Notebook should ask for the student alias.")
    _check("normalize_student_alias" in notebook_text, "Notebook should validate the alias format.")
    _check("submissions" in notebook_text, "Notebook should prepare a submissions folder.")
    _check("Privacidad" in notebook_text, "Notebook should include a privacy note.")
    _check("Evidencia de logro" in notebook_text, "Notebook should explain the evidence of success.")

    _compile_notebook_code_cells(notebook)

    for cell_id in ["bootstrap", "choose-image", "student-alias", "export-csv", "rebuild-png", "submission"]:
        _check(cell_id in notebook_text, f"Notebook should include a '{cell_id}' code cell.")


def check_bootstrap_refreshes_stale_helper() -> None:
    notebook = _load_notebook()
    bootstrap_source = _bootstrap_source_with_helper_url(notebook, HELPER_PATH.resolve().as_uri())

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        stale_helper = temp_path / "rgb_discovery_tools.py"
        stale_helper.write_text(
            'HELPER_VERSION = "0.0.1"\n\n'
            'def download_sample_image(*args, **kwargs):\n'
            '    raise RuntimeError("stale helper should be replaced")\n',
            encoding="utf-8",
        )

        namespace = {"__name__": "__main__"}
        previous_cwd = Path.cwd()
        try:
            os.chdir(temp_path)
            exec(compile(bootstrap_source, f"{NOTEBOOK_PATH.name}#bootstrap", "exec"), namespace)
        finally:
            os.chdir(previous_cwd)

        rgb = namespace["rgb"]
        _check(hasattr(rgb, "normalize_student_alias"), "Bootstrap should refresh stale helpers until normalize_student_alias exists.")
        _check(getattr(rgb, "HELPER_VERSION", None) == HELPER_VERSION, "Bootstrap should load the expected helper version.")


def check_helper_round_trip() -> None:
    _check(HELPER_PATH.exists(), "Helper file is missing.")
    _check(SAMPLE_IMAGE_PATH.exists(), "Sample preview image is missing.")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        student_alias = normalize_student_alias("har pir")
        sample = resolve_source_image(sample_image_path=SAMPLE_IMAGE_PATH)
        source_image = open_rgb_image(sample)
        study_image = fit_study_image(source_image, max_side=32)

        csv_path = write_rgb_csv(study_image, temp_path / student_output_filename(student_alias, DEFAULT_OUTPUT_CSV))
        _check(csv_path.exists(), "CSV export was not created.")
        _check(csv_path.name == f"{student_alias}-{DEFAULT_OUTPUT_CSV}", "CSV export should use the student alias convention.")

        rows = image_to_rgb_rows(study_image)
        _check(len(rows) == study_image.width * study_image.height, "Pixel rows count does not match the image size.")
        _check({"row", "col", "r", "g", "b", "hex"}.issubset(rows[0].keys()), "CSV rows should include RGB and hex values.")

        png_path = rebuild_png_from_csv(csv_path, temp_path / student_output_filename(student_alias, DEFAULT_OUTPUT_PNG))
        _check(png_path.exists(), "Reconstructed PNG was not created.")
        _check(png_path.name == f"{student_alias}-{DEFAULT_OUTPUT_PNG}", "PNG export should use the student alias convention.")

        revealed = open_rgb_image(png_path)
        _check(revealed.size == study_image.size, "Reconstructed PNG size changed.")

        panel = make_comparison_panel(study_image, revealed)
        _check(panel.width > study_image.width, "Comparison panel should be wider than the source image.")

        bundle = prepare_submission_assets(csv_path, png_path, temp_path / "submissions", student_alias)
        _check(Path(bundle["csv"]).exists(), "Submission CSV copy is missing.")
        _check(Path(bundle["png"]).exists(), "Submission PNG copy is missing.")
        _check(Path(bundle["folder"]) == temp_path / "submissions" / student_alias, "Submission folder should use the student alias.")
        _check(Path(bundle["csv"]).name == f"{student_alias}-{DEFAULT_OUTPUT_CSV}", "Submission CSV should keep the alias prefix.")
        _check(Path(bundle["png"]).name == f"{student_alias}-{DEFAULT_OUTPUT_PNG}", "Submission PNG should keep the alias prefix.")


def check_helper_validation_errors() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        invalid_aliases = [
            "",
            "ABC",
            "ABCDEFG",
            "ABC!DE",
            "ABC123",
        ]
        for invalid_alias in invalid_aliases:
            try:
                normalize_student_alias(invalid_alias)
            except ValueError as exc:
                _check(
                    "6 letras" in str(exc) or "6 letters" in str(exc),
                    f"Invalid alias '{invalid_alias}' should explain the 6-letter format.",
                )
            else:
                raise AssertionError(f"Invalid alias '{invalid_alias}' should not validate successfully.")

        negative_coords_csv = temp_path / "negative-coords.csv"
        negative_coords_csv.write_text(
            "row,col,r,g,b\n-1,0,0,0,0\n",
            encoding="utf-8",
        )
        try:
            rebuild_png_from_csv(negative_coords_csv, temp_path / DEFAULT_OUTPUT_PNG)
        except ValueError as exc:
            _check("coordenadas negativas" in str(exc), "Negative coordinate errors should be learner-friendly.")
        else:
            raise AssertionError("Negative coordinate CSV should not rebuild successfully.")

        out_of_range_rgb_csv = temp_path / "out-of-range-rgb.csv"
        out_of_range_rgb_csv.write_text(
            "row,col,r,g,b\n0,0,256,-1,300\n",
            encoding="utf-8",
        )
        try:
            rebuild_png_from_csv(out_of_range_rgb_csv, temp_path / DEFAULT_OUTPUT_PNG)
        except ValueError as exc:
            _check("valores RGB fuera de rango" in str(exc), "RGB range errors should be learner-friendly.")
        else:
            raise AssertionError("Out-of-range RGB CSV should not rebuild successfully.")


def main() -> int:
    check_notebook_contract()
    check_bootstrap_refreshes_stale_helper()
    check_helper_round_trip()
    check_helper_validation_errors()
    print(json.dumps({"status": "passed", "notebook": str(NOTEBOOK_PATH)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
