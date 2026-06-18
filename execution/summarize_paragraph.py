# -*- coding: utf-8 -*-
"""
summarize_paragraph.py
----------------------
Purpose : Accept a paragraph from the user interactively and return
          a bullet-point summary using Google Gemini.
Inputs  : Paragraph typed/pasted at the CLI prompt.
Outputs : Bullet-point summary printed to stdout.
          Last summary also saved to .tmp/last_summary.txt
Requires: GOOGLE_API_KEY in .env  |  pip install google-genai python-dotenv
"""

import os
import sys
import textwrap

try:
    from google import genai
    from dotenv import load_dotenv
except ImportError:
    print("\n[ERROR] Missing dependencies. Run:\n")
    print("  pip install google-genai python-dotenv\n")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
MODEL = "gemini-2.5-flash"  # only model with quota on this project

SYSTEM_PROMPT = textwrap.dedent("""
    You are a concise summarizer. Given a paragraph, produce a clear
    bullet-point summary. Rules:
    - Use '-' as the bullet character
    - Each bullet must be one sentence, 20 words or fewer
    - Capture every key idea; omit filler and repetition
    - Return ONLY the bullets, no intro or outro text
""").strip()

# ── Setup ─────────────────────────────────────────────────────────────────────
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("\n[ERROR] GOOGLE_API_KEY not found.")
    print("  -> Add it to your .env file:  GOOGLE_API_KEY=your_key_here\n")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# ── Input ─────────────────────────────────────────────────────────────────────
def get_paragraph() -> str:
    """Prompt the user to paste a paragraph; blank line signals end of input."""
    print("\n" + "-" * 60)
    print("  Paragraph Summarizer  (powered by Google Gemini)")
    print("-" * 60)
    print("Paste or type your paragraph below.")
    print("Press ENTER on a blank line when done.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "" and lines:      # blank line = end of input
            break
        lines.append(line)

    text = " ".join(lines).strip()

    if not text:
        print("\n[ERROR] No text entered. Please try again.\n")
        return get_paragraph()        # re-prompt

    return text

# ── Summarize ─────────────────────────────────────────────────────────────────
def summarize(paragraph: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=paragraph,
        config={"system_instruction": SYSTEM_PROMPT},
    )
    return response.text.strip()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    paragraph = get_paragraph()

    print("\nSummarizing...\n")
    try:
        summary = summarize(paragraph)
    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        sys.exit(1)

    print("-" * 60)
    print("  Summary")
    print("-" * 60)
    print(summary)
    print("-" * 60 + "\n")

    # Persist last summary for chaining into other workflows
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/last_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("(Saved to .tmp/last_summary.txt)\n")


if __name__ == "__main__":
    main()
