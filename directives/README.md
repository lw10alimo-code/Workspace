# Directives

This folder contains **SOPs (Standard Operating Procedures)** written in Markdown.

Each directive defines:
- **Goal** – what the task is trying to accomplish
- **Inputs** – what data or parameters are required
- **Tools/Scripts** – which `execution/` scripts to run and in what order
- **Outputs** – what the deliverable looks like and where it lives
- **Edge Cases** – known failure modes, API limits, and how to handle them

## Conventions

- One directive per workflow/task type
- Keep directives stable — update them as you learn, but never overwrite without intent
- Treat these as living documents: improve them as edge cases are discovered
- Directives are the **instruction set**; `execution/` scripts are the **tools**

## Adding a New Directive

Create a new `.md` file named after the task, e.g. `scrape_website.md`, `send_report.md`.

Use this template:

```markdown
# [Task Name]

## Goal
Describe what this task does and why.

## Inputs
- `param1` – description
- `param2` – description

## Steps
1. Run `execution/script_name.py` with inputs X and Y
2. Check output at `.tmp/output.json`
3. Upload result to Google Sheets (see `execution/upload_to_sheets.py`)

## Outputs
- Google Sheet: [link or description]

## Edge Cases & Notes
- API rate limit: X requests/minute → use batch endpoint if >N items
- Token expiry: re-run `execution/auth.py` to refresh
```
