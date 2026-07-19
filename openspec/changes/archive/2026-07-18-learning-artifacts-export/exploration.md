## Exploration: learning-artifacts-export

### Current State
The workspace currently contains a PRD document and SDD/OpenSpec metadata only; no application stack, source code, or test runner is present. The PRD defines a low-friction educational pipeline for business students: create 16x16 avatar frames in Excel/spreadsheets, process them in Google Colab/Python into downloadable animated GIFs, then deploy them in CodePen using separated HTML, CSS, and JS boxes for a trivia/simulator activity.

The product intent is directionally clear enough to plan an SDD change, but the formal proposal should first resolve artifact ownership and educational scope: whether the deliverable is a static learning kit, a generated export package, or a future application that produces those assets.

### Affected Areas
- `PRD_VibePixel_Academy_BabyStepsTech.docx` — Primary source of product intent, data pipeline, learner audience, and acceptance criteria.
- `openspec/config.yaml` — Confirms no executable stack or test runner exists yet; planning must treat this as artifact/content delivery unless a codebase is introduced.
- `openspec/changes/learning-artifacts-export/` — Change folder for SDD artifacts related to this exploration.
- Future Excel/Spreadsheet artifact — Must define the 16x16 matrix format, color ID palette, and rest/action frame separation.
- Future Google Colab/Python artifact — Must define the notebook flow for loading spreadsheet data, mapping colors, upscaling pixel art, and exporting GIFs.
- Future CodePen artifact — Must provide separated HTML, CSS, and JS snippets with clear student-safe modification zones.

### Approaches
1. **Template Learning Kit** — Produce separate, human-readable teaching artifacts: spreadsheet template, Colab notebook, and CodePen snippets.
   - Pros: Lowest friction for students; aligns directly with the PRD; easy to review under a 400-line budget; does not require inventing an app stack.
   - Cons: Manual versioning unless a repository structure is later added; acceptance depends on educational clarity, not automated tests.
   - Effort: Medium

2. **Export Package Specification** — Define a formal folder/package contract that includes the spreadsheet schema, notebook, CodePen HTML/CSS/JS files, fixtures, and expected outputs.
   - Pros: Better long-term maintainability; easier to validate deliverable completeness; supports future automation.
   - Cons: Requires more decisions about file formats, naming, and packaging before implementation.
   - Effort: Medium

3. **Generator Application** — Build tooling that generates the spreadsheet, notebook, CodePen snippets, and sample assets automatically.
   - Pros: Scales if many cohorts or variants are needed; can enforce schema and reduce manual mistakes.
   - Cons: Over-engineered for the current workspace; introduces stack, tests, and UX decisions not present in the PRD.
   - Effort: High

### Recommendation
Start with the **Template Learning Kit** and specify it as three separate learning artifacts: Excel/Spreadsheet, Google Colab/Python, and CodePen with CSS, HTML, and JS separated. Treat the first SDD proposal as an educational content/package change, not an application build. Add a lightweight package contract only where it improves reviewability: expected filenames, learner edit zones, sample input, and expected generated GIF behavior.

### Risks
- The PRD describes the learning flow but does not yet define exact deliverable filenames, repository layout, or whether artifacts should be committed as source files, downloadable assets, or external links.
- CodePen cannot natively host generated GIF files unless students upload or reference an accessible asset URL; this needs an explicit student-safe path.
- Supporting both numeric color IDs and raw Hex/RGB values may complicate the first lesson; the MVP should likely choose one canonical input mode.
- “Exhaustively commented” code can reduce cognitive load if structured well, but too many comments can overwhelm students; comments should mark safe edit zones and critical concepts.
- No test runner exists, so verification will need content review, sample-run evidence, and possibly manual acceptance checklists until an executable stack is added.

### Ready for Proposal
Yes, with a short product question round first. The orchestrator should ask the highest-value product questions below before creating the formal proposal so the proposal can lock MVP scope, artifact boundaries, and learner success criteria.

### Questions for User
1. Should the MVP deliverable be a downloadable/committable learning kit in the repo, or a set of external share links/templates for Excel, Colab, and CodePen?
2. For the spreadsheet MVP, should students use numeric color IDs only, or must the first version also support raw Hex/RGB values?
3. How should students make the generated GIF available to CodePen: manual upload, base64/data URL, GitHub-hosted asset, or another classroom-approved method?
4. What is the minimum successful learning outcome: generating the GIF, wiring it into CodePen, or completing a working trivia/simulator interaction?
5. Should the CodePen starter prioritize a business trivia quiz, a decision-tree simulator, or a generic template that teachers customize per lesson?
