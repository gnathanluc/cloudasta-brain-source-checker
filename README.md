# Cloudasta Brain — Source-of-Truth Checker

## What it does
This Python prototype searches a small fictional knowledge library and helps a coworker identify which source is approved, which items are drafts or meeting notes, and where information may conflict.

## How to use it
1. Open the app.
2. Search for a topic such as `onboarding price` or `onboarding checklist`.
3. Review the source title, owner, status, date, and content.
4. If the app flags a conflict, use the approved source as the starting point and verify with the named owner before making a commitment.
5. Try **Show all sample sources** to inspect the sample library.

## How to run it
Install Python 3.10+ and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will open the app in a browser. If it does not open automatically, use the local URL printed in the terminal.

## What to do when it breaks
- If the app will not start, confirm Python is installed and run `pip install -r requirements.txt` again.
- If a search returns no results, try a broader keyword or check the spelling.
- If the result looks wrong, inspect the sample source records and the keyword-matching logic in `app.py`.
- If documents conflict, do not assume the newest file is correct. Confirm approval and ask the listed owner.

## Limitations and safety
This is a demo prototype using fictional data. It is not connected to Cloudasta's Drive, Gmail, Meet, or Gemini Enterprise. It uses keyword matching, not an AI model. Source status and ownership are manually supplied, so a real deployment would need validated metadata, access controls, audit logging, and human review for high-impact decisions.

## Test scenario
Search `onboarding price`. The sample library contains an approved $5,000 pricing policy, a draft $4,500 proposal, and meeting notes discussing a possible $4,500 change without final approval. The expected behavior is to flag an approval gap and direct the user to verify with Finance rather than silently treating the newest item as correct.
