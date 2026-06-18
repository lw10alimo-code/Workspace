# Execution Scripts

This folder contains **deterministic Python scripts** — the tools that do the actual work.

## Principles

- Each script should do **one thing well** and be independently testable
- Load secrets from `.env` (use `python-dotenv`)
- Write intermediate outputs to `.tmp/` — never to the project root
- Deliverables go to cloud services (Google Sheets, Slides, etc.)
- Log clearly: what went in, what came out, any errors

## Running Scripts

```bash
# Always run from the project root so relative paths work
python execution/script_name.py
```

## Adding a New Script

1. Check existing scripts first — don't duplicate
2. Add a docstring at the top: purpose, inputs, outputs
3. Load env vars via `python-dotenv`
4. Write a quick smoke-test (can be a `if __name__ == "__main__"` block)
5. Update the relevant directive in `directives/` to reference the new script
