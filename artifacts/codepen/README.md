# CodePen Learning Artifact

This folder contains the MVP CodePen workshop starter.

## CodePen handoff

When you move this starter into CodePen, copy the content into the matching panel:

- HTML panel: copy only the block between the `CodePen HTML panel copy block` comments in `index.html`.
- CSS panel: copy the contents of `styles.css`.
- JS panel: copy the contents of `script.js`.

Do not paste the local `<link>` tag from the `<head>` or the local `<script>` tag from `index.html` into CodePen. Use the public GIF URL handoff in `avatarConfig.avatarAssetUrl` instead.

## Deterministic validation

Run `node artifacts/codepen/validate_codepen_starter.js` to confirm the starter still treats the template placeholder as unconfigured, rejects non-HTTPS URLs, and accepts a real public HTTPS GIF URL.

## What lives here

- `index.html` — workshop markup and learner edit zones
- `styles.css` — safe layout, accessory, and visual customization hooks
- `script.js` — public avatar URL handoff and simple workshop behavior
- `validate_codepen_starter.js` — deterministic URL fallback validation for the starter contract

## Related docs

- `../../docs/learner-flow.md`
- `../../docs/teacher-flow.md`
- `../../docs/verification-checklist.md`
