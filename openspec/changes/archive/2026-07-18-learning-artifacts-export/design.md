# Design: Learning Artifacts Export

## Technical Approach

Build a GitHub-versioned learning kit, not a deployed app. The repository will contain separate artifact families for Spreadsheet/Excel, Colab/Python, CodePen, exported assets, and learner/teacher documentation. The core contract is a small, reviewable data path: 16x16 spreadsheet rows become ordered Colab frame arrays, Colab exports a repository-hosted GIF/still asset, and CodePen consumes that public HTTPS URL through a learner-editable config.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Delivery model | Static repository learning kit | Generator app, deployed platform | Current repo has no app stack or test runner; static artifacts match the MVP and keep review scope small. |
| Artifact boundaries | Separate `artifacts/spreadsheet/`, `artifacts/colab/`, `artifacts/codepen/`, `artifacts/exports/`, `docs/` | One mixed workshop folder | Separate families mirror learner tools and make teacher review/updates easier. |
| Asset handoff | Colab output is committed or copied under `artifacts/exports/avatars/` and referenced via a public raw/GitHub Pages HTTPS URL | CodePen asset hosting, base64 | Repository-hosted URL is MVP-safe, inspectable, and avoids requiring extra CodePen account features. |
| Future spaces | Document extension points only | Build shared-space mechanics now | Proposal and specs explicitly exclude collective spaces, routes, gates, mazes, and teacher/community platform editing from MVP. |

## Data Flow

```text
Spreadsheet frame sheets/CSV
  └─ rows: frame_id,row,col,value
      value: numeric color ID | #RRGGBB | R,G,B | blank
          ↓
Colab parser validates 16x16 frames and color values
          ↓
Colab preview/upscale/export creates GIF or still image
          ↓
artifacts/exports/avatars/<sample-or-learner>.gif
          ↓
CodePen JS config: avatarAssetUrl = "https://.../avatar.gif"
          ↓
CodePen HTML/CSS/JS workshop renders and customizes avatar
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `artifacts/spreadsheet/README.md` | Create | Spreadsheet learner contract, export instructions, blank-cell behavior. |
| `artifacts/spreadsheet/templates/avatar-16x16.csv` | Create | Committable sample/template using frame, row, column, and color value columns. |
| `artifacts/colab/README.md` | Create | Colab flow and learner steps. |
| `artifacts/colab/vibepixel_avatar_pipeline.ipynb` | Create | Notebook for parse, validate, preview, upscale, and export. |
| `artifacts/colab/avatar_pipeline.py` | Create | Plain Python companion for review/readability. |
| `artifacts/codepen/index.html` | Create | HTML panel content with safe learner zones. |
| `artifacts/codepen/styles.css` | Create | CSS panel content with safe style/accessory zones. |
| `artifacts/codepen/script.js` | Create | JS panel content and `avatarAssetUrl` config. |
| `artifacts/exports/avatars/README.md` | Create | Explains generated asset storage and public URL copying. |
| `docs/learner-flow.md` | Create | Happy-path spreadsheet → Colab → CodePen guide. |
| `docs/teacher-flow.md` | Create | Facilitation, review checklist, and future extension notes. |

## Interfaces / Contracts

Spreadsheet rows use this canonical schema:

```csv
frame_id,row,col,value
idle_01,0,0,#FFCC00
idle_01,0,1,255,204,0
idle_01,0,2,1
```

Rules: each frame MUST resolve to a 16x16 grid; `row` and `col` are zero-based integers 0–15; `value` accepts numeric palette IDs, `#RRGGBB`, `R,G,B`, or blank. Blank cells are transparent unless docs choose a named background.

CodePen consumes only:

```js
const avatarConfig = { avatarAssetUrl: "https://.../avatar.gif" };
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Static | Required folders/files exist | Manual file checklist; no test runner exists. |
| Schema | CSV examples match row contract and 16x16 frame rules | Review sample rows and documented validation errors. |
| Colab/Python | Notebook/script readability and expected parse/export steps | Manual read-through plus optional Colab run by implementer. |
| CodePen | HTML/CSS/JS are separated and import-ready | Paste panels into CodePen and verify asset URL config/fallback guidance. |
| Docs | Learner and teacher flows cover happy path and non-goals | Acceptance checklist against specs. |

## Migration / Rollout

No migration required. Roll out as one repository learning-kit slice; if review exceeds 400 changed lines, split by work unit: spreadsheet contract, Colab pipeline, CodePen starter, then docs/assets.

## Open Questions

- [ ] Should public asset URLs use raw GitHub URLs or GitHub Pages as the preferred classroom path?
