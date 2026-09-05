# Spring 2026 FLEX upload

The paste-ready content is in [`spring_2026_flex.html`](spring_2026_flex.html).

To add it to the official Drupal page:

1. Open the official ISG **Teaching Insights** page and click **Edit**.
2. Open the accordion item whose Summary is **Facilitating Learning Excellence Award**.
3. In the Details editor, click **Source**.
4. In **Source** view, use Find to locate `<summary>Fall 2025 and Winter 2025</summary>`. Move to the `<details class="season-block" open="">` immediately before that summary, then paste the entire contents of `spring_2026_flex.html` immediately before that opening `<details>` tag. This puts the newest Spring 2026 section first.
5. Change the existing footer email from `ices@illinois.edu` to `flex@illinois.edu` if that has not already been changed.
6. Save, then open the Spring 2026 section and spot-check several departments and names.

The generated block uses the existing site pattern: one expandable Spring 2026 section with expandable departments and course-level entries. NetIDs and other spreadsheet-only fields are excluded.

Do not paste the block inside the existing semester or department `<details>`, into the footer, or into the Summary field. Paste it into the Details field's Source view as one complete block.
