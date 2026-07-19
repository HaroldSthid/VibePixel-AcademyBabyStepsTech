# Avatar Export Handoff

Store exported GIF or still-image avatars here before copying or publishing them for classroom use.

## Preferred public URL pattern

Use the repository-hosted raw HTTPS URL as the default handoff:

`https://raw.githubusercontent.com/<owner>/<repo>/<branch>/artifacts/exports/avatars/<file>.gif`

If the classroom setup publishes the repository through GitHub Pages, the same asset may be referenced from the Pages HTTPS URL instead.

## Notes

- Keep the committed file in this folder as the source of truth.
- Reference the published HTTPS URL from Colab or CodePen, not a local file path.
