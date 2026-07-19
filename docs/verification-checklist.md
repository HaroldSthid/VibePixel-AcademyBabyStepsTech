# CodePen Verification Checklist

Use this manual checklist after the PR3 slice lands.

## File and structure checks

- [ ] `artifacts/codepen/index.html` exists and reads as workshop markup.
- [ ] `artifacts/codepen/styles.css` exists and contains labeled customization sections.
- [ ] `artifacts/codepen/script.js` exists and defines `avatarConfig.avatarAssetUrl`.
- [ ] `docs/learner-flow.md` and `docs/teacher-flow.md` exist.

## Upstream handoff checks

- [ ] The spreadsheet CSV contract still uses frame, row, column, and value fields.
- [ ] Invalid color guidance is documented for unsupported cell values.
- [ ] The Colab preview/export flow is still described clearly for learners.

## Behavior checks

- [ ] The preview panel and edit zones are visibly separated.
- [ ] A missing or private asset URL shows a clear fallback message.
- [ ] A public HTTPS URL updates the preview without extra tooling.
- [ ] `node artifacts/codepen/validate_codepen_starter.js` passes and confirms placeholder fallback, non-HTTPS rejection, and public HTTPS acceptance.
- [ ] The badge text and visibility controls behave predictably.
- [ ] The CodePen HTML panel uses body markup only, with CSS and JS pasted into their own panels instead of local file links.

## Classroom checks

- [ ] The learner flow still reads spreadsheet → Colab → exported asset → CodePen.
- [ ] The teacher flow still treats future collective-space ideas as non-goals.

## Manual sanity check

- [x] Replace the placeholder URL with a public raw GitHub or GitHub Pages GIF URL and confirm the workshop preview renders.
  - Verified with a public HTTPS GIF (`https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif`) in CodePen; preview rendered successfully.
