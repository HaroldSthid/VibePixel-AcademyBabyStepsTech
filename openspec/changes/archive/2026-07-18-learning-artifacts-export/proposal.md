# Proposal: Learning Artifacts Export

## Intent

Deliver a public, GitHub-versioned MVP learning kit that lets business learners create a 16x16 avatar in spreadsheets, turn it into a GIF in Google Colab, and use it inside a modular CodePen workshop. This closes the current gap between the PRD vision and a committable, reviewable artifact set.

## Scope

### In Scope
- Define the MVP as three separate learning artifacts: Spreadsheet/Excel, Colab/Python, and CodePen with HTML, CSS, and JS kept separate.
- Support spreadsheet inputs using numeric IDs and raw Hex/RGB color values in v1.
- Treat Colab as the draft/sketch workspace for generating the base avatar/GIF pipeline.
- Treat CodePen as the workshop layer for customization, accessories, experiments, and simple interactive business logic.

### Out of Scope
- Multi-avatar, shared-space, maze, path, question-gate, or teacher/community-editable platform features.
- Building a conventional videogame, auth flow, backend service, or generator app.

## Capabilities

### New Capabilities
- `spreadsheet-learning-artifact`: Defines the 16x16 spreadsheet contract, frame separation, and Hex/RGB-compatible color input rules.
- `colab-learning-artifact`: Defines the Colab notebook flow for parsing frames, mapping colors, upscaling, and exporting a GIF.
- `codepen-learning-artifact`: Defines the CodePen starter contract with separated HTML/CSS/JS, learner edit zones, and workshop-style customization hooks.

### Modified Capabilities
- None.

## Approach

Start with a template learning kit, not an application. Specify the repository-delivered artifact set, expected handoff between spreadsheet → Colab → CodePen, sample learner path, and minimum evidence of success.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/changes/learning-artifacts-export/proposal.md` | New | Proposal for MVP artifact boundaries and goals |
| `openspec/changes/learning-artifacts-export/` | Modified | Will hold downstream spec, design, and tasks artifacts |
| `PRD_VibePixel_Academy_BabyStepsTech.docx` | Referenced | Source product intent for the learning pipeline |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| GIF handoff into CodePen remains ambiguous | Med | Lock a single classroom-safe hosting/reference path in specs |
| Too much workshop freedom weakens MVP clarity | Med | Define one minimum successful learner flow first |
| Future platform ideas leak into MVP | High | Keep collective-space phases explicitly out of scope |

## Rollback Plan

Revert to the current planning-only state by removing this change artifact and any downstream MVP-only specs if the repository-learning-kit approach proves wrong.

## Dependencies

- PRD alignment on the public repository delivery model
- A documented classroom-safe way to reference generated GIF assets from CodePen

## Success Criteria

- [ ] The MVP is defined as a public repository with separate Spreadsheet, Colab, and CodePen learning artifacts.
- [ ] Spreadsheet v1 explicitly supports Hex/RGB inputs in addition to numeric color IDs.
- [ ] Future collective-space ideas are documented as later phases, not MVP requirements.
