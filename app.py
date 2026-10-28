import streamlit as st
from datetime import date
import re

st.set_page_config(page_title="Cloudasta Brain | Source-of-Truth Checker", page_icon="🧠", layout="wide")

SOURCES = [
    {
        "id": "SRC-001",
        "title": "Approved Pricing Policy",
        "type": "Policy",
        "owner": "Finance",
        "status": "Approved",
        "effective_date": "2026-10-01",
        "topic": "Pricing",
        "content": "Standard onboarding package price is $5,000. This policy is approved by Finance and effective October 1, 2026.",
        "notes": "Official policy; use unless Finance confirms a newer approved version."
    },
    {
        "id": "SRC-002",
        "title": "Draft Pricing Proposal",
        "type": "Proposal",
        "owner": "Sales",
        "status": "Draft — not approved",
        "effective_date": "2026-10-20",
        "topic": "Pricing",
        "content": "Proposed onboarding package price is $4,500. This draft has not been approved by Finance.",
        "notes": "A newer date does not make a draft authoritative."
    },
    {
        "id": "SRC-003",
        "title": "Pricing Discussion — Meeting Notes",
        "type": "Meeting notes",
        "owner": "Sales / Finance",
        "status": "Discussion — no final decision",
        "effective_date": "2026-10-23",
        "topic": "Pricing",
        "content": "Meeting participants discussed possibly changing the onboarding package price to $4,500. No final approval or decision was recorded.",
        "notes": "Meeting notes document discussion, not necessarily an approved decision."
    },
    {
        "id": "SRC-004",
        "title": "Employee Onboarding SOP",
        "type": "SOP",
        "owner": "People Operations",
        "status": "Approved",
        "effective_date": "2026-09-15",
        "topic": "Onboarding",
        "content": "New employees should complete account setup, security training, and role-specific onboarding during their first week.",
        "notes": "Approved procedure; check with People Operations if the process has changed."
    },
    {
        "id": "SRC-005",
        "title": "Old Onboarding Checklist",
        "type": "Checklist",
        "owner": "Unknown",
        "status": "Outdated — owner unconfirmed",
        "effective_date": "2025-02-01",
        "topic": "Onboarding",
        "content": "Older checklist includes account setup and training tasks. It has no confirmed current owner.",
        "notes": "Treat as historical reference only until reviewed."
    },
]

def normalize(text):
    return re.findall(r"[a-z0-9$]+", text.lower())

def score_source(source, terms):
    searchable = " ".join([
        source["title"], source["type"], source["owner"], source["status"],
        source["topic"], source["content"], source["notes"], source["effective_date"]
    ]).lower()
    return sum(1 for term in terms if term in searchable)

def is_approved(source):
    return source["status"] == "Approved"

def source_rank(source):
    # Approval status takes priority over recency.
    if source["status"] == "Approved":
        return 0
    if source["status"].startswith("Discussion"):
        return 1
    if source["status"].startswith("Draft"):
        return 2
    return 3

st.title("🧠 Cloudasta Brain")
st.caption("Source-of-Truth Checker · Python prototype using fictional sample documents")

with st.sidebar:
    st.header("About this prototype")
    st.write("Search a small sample knowledge library and identify approved sources, outdated material, and conflicts.")
    st.info("Demo only: this tool is not connected to Cloudasta's Google Workspace and does not provide legal, pricing, or security approval.")
    st.markdown("**Source priority**")
    st.markdown("1. Approved current source\n2. Recorded decision/approval\n3. Meeting notes or drafts\n4. Outdated or unverified material")

st.subheader("Search the knowledge library")
query = st.text_input("What information are you looking for?", placeholder="Try: onboarding price or onboarding checklist")
show_all = st.checkbox("Show all sample sources", value=False)

if query.strip() or show_all:
    terms = [t for t in normalize(query) if len(t) > 1]
    if show_all and not terms:
        results = SOURCES[:]
    else:
        scored = [(score_source(s, terms), s) for s in SOURCES]
        results = [s for score, s in scored if score > 0]
        results.sort(key=lambda s: (source_rank(s), -score_source(s, terms), s["title"].lower()))

    if not results:
        st.warning("No matching source was found in this sample library. Try a broader keyword or ask the document owner.")
    else:
        st.write(f"**{len(results)} matching source(s)**")
        approved = [s for s in results if is_approved(s)]
        topics = {s["topic"] for s in results}
        if len(topics) == 1 and len(results) > 1:
            contents = " ".join(s["content"] for s in results).lower()
            prices = sorted(set(re.findall(r"\$[\d,]+", contents)))
            statuses = [s["status"] for s in results]
            if len(prices) > 1 or any(not is_approved(s) for s in results):
                st.warning("Potential conflict or approval gap detected. Do not treat the newest document as authoritative automatically.")
                if approved:
                    st.success(f"Best starting point: **{approved[0]['title']}** — marked Approved.")
                st.write("**Recommended next step:** confirm the current decision with the listed owner before quoting or acting.")
        for s in results:
            status = s["status"]
            with st.expander(f"{s['title']}  ·  {status}", expanded=True):
                c1, c2, c3 = st.columns(3)
                c1.metric("Source ID", s["id"])
                c2.metric("Owner", s["owner"])
                c3.metric("Effective / document date", s["effective_date"])
                st.write(f"**Type:** {s['type']}  |  **Topic:** {s['topic']}")
                st.write(s["content"])
                st.caption(s["notes"])
                if is_approved(s):
                    st.success("Approved source")
                elif status.startswith("Outdated"):
                    st.error("Do not rely on this as the current source without owner verification.")
                else:
                    st.warning("Not an approved source of truth.")

st.divider()
st.subheader("Try these test queries")
st.markdown("- `onboarding price` — checks whether different prices and unapproved sources are flagged.")
st.markdown("- `onboarding checklist` — compares current onboarding guidance with an older checklist.")

st.caption("Prototype limitations: keyword search only; sample data only; approval labels are manually entered; no live Google Workspace connection.")
