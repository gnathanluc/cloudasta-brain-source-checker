# Cloudasta Brain — Source-of-Truth Checker

**Live demo:** https://cloudasta-brain-source-checker-9pqvkebuhid2d5zsceyjxs.streamlit.app/

## What it does
This small Python/Streamlit prototype searches a fictional sample knowledge library and helps a coworker spot approved sources, drafts, outdated documents, and possible conflicts. It prioritizes approval status over document recency and recommends confirming conflicts with the listed owner.

## How to use it
1. Open the live demo link above.
2. In **What information are you looking for?**, enter a topic such as `onboarding price` or `onboarding checklist`.
3. Review each result's title, status, owner, date, and content.
4. If a conflict or approval gap is flagged, use the approved source as a starting point and confirm the current decision with the owner before acting.
5. To browse the sample library, select **Show all sample sources**.

## Quick checks
- `onboarding price`: should show the approved $5,000 policy alongside a draft $4,500 proposal and meeting notes that record no final approval. Check for a conflict/approval-gap warning.
- `onboarding checklist`: should show the approved Employee Onboarding SOP and the older checklist with an unconfirmed owner.
- `quarterly marketing forecast`: should return a no-match message because the sample library does not contain that topic.

## If it breaks
- **The app will not load:** refresh the page and try again. If it remains unavailable, check the app's Streamlit deployment page for an error.
- **No results appear:** try a broader keyword or check spelling; this prototype searches sample records only.
- **A result looks wrong:** remember that matching is keyword-based and inspect the displayed source details. Do not treat the tool as final approval.
- **Sources conflict:** do not assume the newest item is correct. Confirm with the listed owner before quoting a price or taking action.

## Important limitations
This is a demonstration prototype with fictional sample data. It is **not** connected to Cloudasta's Google Drive, Gmail, Meet, or Gemini Enterprise, and it does not use an AI model. Search is keyword-based; source owners and approval statuses are manually entered. A production version would need approved integrations, permissions aligned with source access, validated metadata, audit logging, and human review for consequential decisions.

## Run locally (optional)
Requires Python 3.10 or later. In the project folder, run:

```bash
pip install -r requirements.txt
streamlit run app.py
```
