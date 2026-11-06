"""Simple upload interface for the Hiring Stall Alerter."""
from datetime import date

import streamlit as st

from logic import ValidationError, detect_stalled, read_csv

st.set_page_config(page_title="Hiring Stall Alerter", layout="wide")
st.title("Hiring Stall Alerter")
st.write("Find candidates who need a follow-up, ordered by longest inactivity.")
st.caption("Required columns: candidate_name, role, stage, last_activity_date. Dates: YYYY-MM-DD.")
threshold = st.number_input("Inactivity threshold (calendar days)", min_value=1, value=7, step=1)
uploaded = st.file_uploader("Upload a hiring-board CSV", type=["csv"])
today = date.today()
st.caption(f"Reference date: {today.isoformat()}. Hired, Rejected, and Withdrawn candidates are excluded.")
if uploaded is not None:
    try:
        stalled = detect_stalled(read_csv(uploaded), threshold=int(threshold), today=today)
    except ValidationError as exc:
        st.error("Please correct the CSV before continuing.")
        for problem in str(exc).splitlines():
            st.error(problem)
    else:
        if stalled.empty:
            st.success("No stalled candidates found.")
        else:
            st.write(f"{len(stalled)} stalled candidate(s)")
            st.dataframe(
                stalled[["candidate_name", "role", "stage", "days_inactive", "explanation", "next_action"]].rename(columns={
                    "candidate_name": "Candidate name", "role": "Role", "stage": "Stage",
                    "days_inactive": "Days inactive", "explanation": "Explanation", "next_action": "Next action",
                }), hide_index=True, width="stretch",
            )
else:
    st.info("Upload a CSV to check for stalled candidates.")
