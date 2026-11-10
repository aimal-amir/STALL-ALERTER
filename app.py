"""Simple upload interface for the Hiring Stall Alerter."""
from datetime import date
import importlib

import streamlit as st

import logic

# Streamlit reruns this script while imported modules may remain in memory.
# Reload the rules so the interface and result columns stay in sync after edits.
logic = importlib.reload(logic)

st.set_page_config(page_title="Hiring Stall Alerter", layout="wide")
st.title("Hiring Stall Alerter")
st.write("Find candidates who need a follow-up, ordered by longest inactivity.")
st.caption("Priority: longest inactivity first. Ties: Offer → Interview → Screening → Applied → other stages; remaining ties keep CSV order.")
st.caption("Required columns: candidate_name, role, stage, last_activity_date. Dates: YYYY-MM-DD.")
threshold = st.number_input("Inactivity threshold (calendar days)", min_value=1, value=7, step=1)
uploaded = st.file_uploader("Upload a hiring-board CSV", type=["csv"])
today = date.today()
st.caption(f"Reference date: {today.isoformat()}. Hired, Rejected, and Withdrawn candidates are excluded.")
if uploaded is not None:
    try:
        stalled = logic.detect_stalled(logic.read_csv(uploaded), threshold=int(threshold), today=today)
    except logic.ValidationError as exc:
        st.error("Please correct the CSV before continuing.")
        for problem in str(exc).splitlines():
            st.error(problem)
    else:
        if stalled.empty:
            st.success("No stalled candidates found.")
        else:
            st.write(f"{len(stalled)} stalled candidate(s)")
            first = stalled.iloc[0]
            st.info(
                f"Follow up first: {first['candidate_name']} ({first['role']}) — "
                f"{first['days_inactive']} days inactive. Contact: {first['follow_up_with']}. "
                f"{first['next_action']}"
            )
            st.dataframe(
                stalled[["follow_up_rank", "candidate_name", "role", "stage", "days_inactive", "days_over_threshold", "priority_reason", "follow_up_with", "next_action"]].rename(columns={
                    "follow_up_rank": "Follow-up order", "days_over_threshold": "Days beyond threshold",
                    "priority_reason": "Why this priority", "follow_up_with": "Follow up with",
                    "candidate_name": "Candidate name", "role": "Role", "stage": "Stage",
                    "days_inactive": "Days inactive", "explanation": "Explanation", "next_action": "Next action",
                }), hide_index=True, width="stretch",
            )
else:
    st.info("Upload a CSV to check for stalled candidates.")
