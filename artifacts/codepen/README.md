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

## Common learner fix: image sizing and missing fallback

A real submission (LISBEL's avatar workshop entry) built a CodePen card from scratch instead of the starter above, and hit two issues worth watching for when reviewing other learners' pens:

1. **Non-divisor image sizing.** The Colab export defaults to `scale=16`, so a GIF made from the 16x16 avatar grid is `256x256px`. Displaying it at a size that does not evenly divide 256 (e.g. `160px`) makes `image-rendering: pixelated` render unevenly sized pixel blocks. Use a clean divisor instead, such as `128px` (256 / 2) or the native `256px`.
2. **No fallback for a broken asset URL.** The spec (`openspec/specs/codepen-learning-artifact/spec.md`, "Asset URL is missing or private") requires a clear fallback instruction when the avatar URL fails to load. A bare `<img>` with no `error` handler just shows the browser's broken-image icon with no guidance.

Fix pattern (safe to hand to a learner as-is):

```html
<img id="avatar-img" src="PASTE_YOUR_PUBLIC_HTTPS_GIF_URL" alt="Avatar preview">
<p id="avatar-status" class="status" hidden>No pudimos cargar el avatar. Revisá que la URL sea pública.</p>
```

```css
.avatar-container img {
  width: 128px;   /* match a clean divisor of the GIF's native size */
  height: 128px;
  image-rendering: pixelated;
  transition: transform 0.1s ease; /* keep transient styles in CSS, not re-set on every event */
}
```

```js
const avatarImg = document.getElementById('avatar-img');
const avatarStatus = document.getElementById('avatar-status');

avatarImg.addEventListener('error', () => {
  avatarImg.hidden = true;
  avatarStatus.hidden = false;
});
```

## Related docs

- `../../docs/learner-flow.md`
- `../../docs/teacher-flow.md`
- `../../docs/verification-checklist.md`
