# Tasks: Learning Artifacts Export

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 650-900 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 -> PR 2 -> PR 3 |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Spreadsheet contract + sample export | PR 1 | `artifacts/spreadsheet/`; manual schema review included |
| 2 | Colab parser + export pipeline | PR 2 | `artifacts/colab/`; depends on PR 1 sample CSV |
| 3 | CodePen starter + docs + verification | PR 3 | `artifacts/codepen/`, `artifacts/exports/`, `docs/`; depends on PR 2 asset path |

## Phase 1: Foundation

- [x] 1.1 Create `artifacts/spreadsheet/`, `artifacts/colab/`, `artifacts/codepen/`, and `artifacts/exports/avatars/` with placeholder structure aligned to the design.
- [x] 1.2 Create `artifacts/exports/avatars/README.md` defining the repository-hosted GIF/still handoff and the preferred public HTTPS URL pattern.

## Phase 2: Spreadsheet + Colab Core

- [x] 2.1 Create `artifacts/spreadsheet/README.md` documenting the 16x16 grid, frame ordering, blank-cell transparency rule, and supported numeric/Hex/RGB inputs.
- [x] 2.2 Split the spreadsheet artifact into a learner-facing 16x16 grid template and a sparse normalized export sample, and document the distinction in `artifacts/spreadsheet/README.md`.
- [x] 2.3 Create `artifacts/colab/avatar_pipeline.py` with readable parse/validate/preview/export steps and explicit invalid-cell guidance.
- [x] 2.4 Create `artifacts/colab/vibepixel_avatar_pipeline.ipynb` mirroring the Python flow for import, preview, GIF export, and single-frame fallback guidance.
- [x] 2.5 Create `artifacts/colab/README.md` explaining how learners load exported spreadsheet data, run preview/export, and copy the resulting asset into the repo workflow.

### PR2 Validation Evidence

- Deterministic contract checks live in `artifacts/colab/validate_avatar_pipeline.py` and cover valid imports, invalid-cell guidance, preview rendering, multi-frame GIF export, single-frame fallback, and explicit duplicate blank-cell rejection.

## Phase 3: CodePen + Learning Flow

- [x] 3.1 Create `artifacts/codepen/index.html` with separated workshop markup and clearly labeled learner edit zones.
- [x] 3.2 Create `artifacts/codepen/styles.css` with safe customization sections for layout, accessories, and simple visual experiments.
- [x] 3.3 Create `artifacts/codepen/script.js` with `avatarConfig.avatarAssetUrl`, public-URL fallback messaging, and simple workshop behavior hooks.
- [x] 3.4 Create `docs/learner-flow.md` covering the happy path: spreadsheet -> Colab -> exported asset -> CodePen.
- [x] 3.5 Create `docs/teacher-flow.md` with facilitation notes, review checkpoints, and MVP non-goals for future platform ideas.

## Phase 4: Verification + Cleanup

- [x] 4.1 Add `docs/verification-checklist.md` with manual checks for file presence, CSV contract, invalid-color guidance, preview/export flow, public URL handoff, and CodePen panel separation.
- [x] 4.2 Manually verify the sample CSV against specs, optional Colab run steps in the notebook/script, and CodePen import readiness; record any follow-up fixes in the touched artifact docs.
  - Evidence: verified in a live CodePen session that the HTML panel uses body-only markup, CSS/JS are pasted into separate panels, and a public HTTPS GIF URL (`https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif`) renders with the status message `Connected to a public avatar URL.`
  - Note: deterministic validation still lives in `artifacts/codepen/validate_codepen_starter.js` and the handoff docs keep the explicit panel-copy guidance.
