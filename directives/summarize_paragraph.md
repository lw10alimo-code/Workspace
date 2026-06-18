# Summarize Paragraph

## Goal
Accept a free-form paragraph from the user via an interactive CLI prompt,
send it to Google Gemini, and return a clean bullet-point summary to stdout.

## Inputs
- Paragraph text — typed or pasted by the user at the CLI prompt
- `GOOGLE_API_KEY` — must be set in `.env`

## Tools / Scripts
| Step | Script | Purpose |
|------|--------|---------|
| 1 | `execution/summarize_paragraph.py` | Takes the paragraph, calls Gemini, prints bullet points |

## Steps
1. Run `python execution/summarize_paragraph.py` from the project root.
2. When prompted, paste or type the paragraph and press Enter twice (blank line = done).
3. The script calls `gemini-1.5-flash` with a summarization prompt.
4. Bullet points are printed to stdout.

## Outputs
- Bullet-point summary printed to terminal.
- (Optional future): save to `.tmp/last_summary.txt` for chaining into other workflows.

## Edge Cases & Notes
- **Missing API key**: script exits with a clear error message — add `GOOGLE_API_KEY` to `.env`.
- **Empty input**: script re-prompts rather than sending a blank request.
- **SDK**: uses `google-genai` (NOT the deprecated `google-generativeai`). Install: `pip install google-genai python-dotenv`.
- **Do NOT import `google.genai.types`**: it is unnecessary and causes recurring linter errors (especially when the IDE uses a different Python than the one with the package installed). Pass config as a plain dict instead: `config={"system_instruction": ...}`.
- **Model availability**: `gemini-1.5-flash` is NOT available on all API keys. Confirmed working models for this project (tried in order):
  1. `gemini-2.0-flash-lite` (fastest, lowest quota cost)
  2. `gemini-2.0-flash`
  3. `gemini-2.5-flash` (current active fallback)
- **Rate limits / 429**: script automatically falls back through `MODELS` list on `RESOURCE_EXHAUSTED`. If all models fail, add billing to the Google Cloud project or wait for quota reset.
- **Windows encoding**: do NOT use Unicode box-drawing characters (e.g. `─`) in print statements — use plain ASCII `-` instead to avoid `cp1252` encode errors.
- **Model list**: to check which models are available on a given API key, run:
  ```python
  from google import genai; from dotenv import load_dotenv; load_dotenv(); import os
  client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
  [print(m.name) for m in client.models.list() if 'generateContent' in (m.supported_actions or [])]
  ```
