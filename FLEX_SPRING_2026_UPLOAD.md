# Spring 2026 FLEX upload

The paste-ready content is in [`spring_2026_flex.html`](spring_2026_flex.html).

To add it to the official Drupal page:

1. Open the official ISG **Teaching Insights** page and click **Edit**.
2. Open the accordion item whose Summary is **Facilitating Learning Excellence Award**.
3. In the Details editor, click **Source**.
4. In **Source** view, use Find to locate the exact sequence `<p class="footer">`. Paste the entire contents of `spring_2026_flex.html` immediately before that tag. This is the one and only insertion point: it comes after the closing `</details>` for the existing Fall 2025 and Winter 2025 season and before the footer/contact paragraph.
5. Change the existing footer email from `ices@illinois.edu` to `flex@illinois.edu` if that has not already been changed.
6. Save, then open the Spring 2026 section and spot-check several departments and names.

The generated block uses the existing site pattern: one expandable Spring 2026 section with expandable departments and course-level entries. NetIDs and other spreadsheet-only fields are excluded.

Do not paste the block inside the existing `<p class="footer">`, inside a department `<details>`, or into the Summary field. Paste it into the Details field's Source view as one complete block.
