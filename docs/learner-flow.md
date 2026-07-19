# Learner Flow: Spreadsheet to CodePen

Use this path when you want the fastest classroom-safe MVP journey.

## Quick path

1. Build the avatar in the spreadsheet template.
2. Export or copy the frame data into the Colab notebook.
3. Run the Colab import, preview, and GIF export steps.
4. Copy the exported GIF to the repository-hosted avatar folder or its public HTTPS URL.
5. Paste that URL into `artifacts/codepen/script.js`.
6. Open the CodePen starter, then copy only the block between the `CodePen HTML panel copy block` comments in `artifacts/codepen/index.html` into the CodePen HTML panel, the full contents of `artifacts/codepen/styles.css` into the CSS panel, and the full contents of `artifacts/codepen/script.js` into the JS panel.
7. Do not paste the local `<link>` tag from the `<head>` or the local `<script>` tag into CodePen, and do not rely on repo-relative file paths there.

## What to edit

| Area | Learner action |
|---|---|
| Spreadsheet | Draw the avatar frames |
| Colab | Validate, preview, and export the GIF |
| CodePen HTML | Change copy, labels, and small content blocks after copying the body markup only |
| CodePen CSS | Tweak layout, colors, accessories, and simple visuals after pasting `styles.css` |
| CodePen JS | Update the asset URL and tiny interactions after pasting `script.js` |

## Success check

- The CodePen preview shows the exported avatar.
- The status message is clear if the URL is missing or private.
- The learner can customize the workshop without build tooling.
- The CodePen panels are independent; there are no local file references to chase.

## Next step

If the avatar URL changes, update `avatarConfig.avatarAssetUrl` and re-open the starter.
