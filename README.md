# VibePixel Academy BabyStepsTech

VibePixel Academy BabyStepsTech is a learning kit for building a small avatar workflow across three tools learners already recognize: spreadsheets, Google Colab, and CodePen. The goal is not to hide the process behind one app. The goal is to make each step visible, editable, and teachable.

## Quick path

1. Draw avatar frames in the spreadsheet template.
2. Use the Colab/Python pipeline to validate, preview, and export the avatar.
3. Copy the exported public HTTPS GIF URL into the CodePen starter.
4. Paste the starter HTML, CSS, and JS into separate CodePen panels.
5. Customize the workshop and verify the preview works.

## Learning artifacts

| Artifact | Path | Purpose |
|---|---|---|
| Spreadsheet / Excel | `artifacts/spreadsheet/` | Learners draw 16x16 avatar frames and learn the data contract. |
| Colab / Python | `artifacts/colab/` | Learners validate color data, preview frames, and export avatar assets. |
| CodePen / HTML-CSS-JS | `artifacts/codepen/` | Learners customize a browser workshop using separated panels. |
| Exported assets | `artifacts/exports/avatars/` | Public avatar/GIF handoff location for CodePen URLs. |
| Classroom docs | `docs/` | Learner flow, teacher flow, and verification checklist. |

## Learner flow

Start here:

- `docs/learner-flow.md`
- `artifacts/spreadsheet/README.md`
- `artifacts/colab/README.md`
- `artifacts/codepen/README.md`

The intended path is:

```text
Spreadsheet -> Colab/Python -> exported GIF URL -> CodePen workshop
```

## Teacher flow

Start with `docs/teacher-flow.md`.

For the MVP, keep the classroom focus tight:

- visible data flow
- Hex/RGB color practice
- small Python transformations
- separated HTML, CSS, and JS editing
- public asset handoff with clear fallback behavior

Future collective spaces, avatar invitations, mazes, route challenges, and community editing are intentionally out of scope for this first kit.

## Verify the kit

Run the deterministic checks from the repository root:

```bash
python "artifacts/colab/validate_avatar_pipeline.py"
node --check "artifacts/codepen/script.js"
node "artifacts/codepen/validate_codepen_starter.js"
```

Then follow the manual checklist:

- `docs/verification-checklist.md`

## Good habits modeled here

- Keep learner artifacts separated by tool and responsibility.
- Prefer explicit contracts over hidden magic.
- Validate executable examples before teaching them.
- Do not publish local metadata, caches, or private PRD files.
- Keep future vision documented, but outside the MVP implementation.

## SDD traceability

This repository was built with a formal SDD flow. Specs are available in:

- `openspec/specs/`

The archived completed change is available in:

- `openspec/changes/archive/2026-07-18-learning-artifacts-export/`
