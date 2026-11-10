# Development Log

## Day 1 — Scope and sample data

### Starting assumption
A simple inactivity threshold and stage-based follow-up suggestions should be enough for a useful first version.

### How I used AI
I used AI to help break down the assignment, define the first-version scope, and create fictional sample data.

### Decisions made
- Use Python, Streamlit, and pandas.
- Flag candidates inactive for at least 7 days by default.
- Exclude Hired, Rejected, and Withdrawn candidates.
- Prioritize candidates by longest inactivity.
- Use transparent rules without an AI API.

### Data improvements
Reviewing my initial CSV with AI identified a misspelled role column, a missing stage column, and ambiguous date formatting. The revised sample uses the required columns and YYYY-MM-DD dates.

### Verification prepared
The sample includes candidates above, below, and exactly at the threshold, plus closed candidates.

For a reference date of November 6, 2026 and a 7-day threshold, the expected order is:
1. Jamie Brooks — 15 days
2. Alex Morgan — 12 days
3. Drew Parker — 8 days
4. Casey Patel — 7 days

### Current status
The scope and sample data are ready. The application has not yet been verified.

### Next step
Build and run the first Streamlit version, then compare its results with the expected list.



## Day 2 — Scenario testing and behavior verification

### Goal
Verify that the app behaves correctly across normal inputs, edge cases, and invalid data.

### Scenarios tested
- Uploaded valid sample data and compared the results with manually calculated expectations.
- Changed the inactivity threshold and checked that the results updated correctly.
- Checked candidates exactly at the threshold and below it.
- Confirmed that Hired, Rejected, and Withdrawn candidates were excluded.
- Checked that closed stages were recognized despite capitalization and surrounding spaces.
- Uploaded data with missing columns, blank required values, invalid dates, and future dates.
- Checked the message displayed when no candidates met the threshold.
- Reviewed explanations and suggested actions for flagged candidates.

### How I verified behavior
I compared the displayed candidates, inactivity calculations, and ordering with the expected results for the reference date used during testing. I also checked whether invalid inputs produced understandable errors rather than misleading results.

### Results
The scenarios I tested behaved as expected. The app identified stalled candidates, excluded closed stages, prioritized longer inactivity, and provided clear validation messages.

### What I learned
A successful upload alone does not prove that the tool works correctly. Testing boundary conditions and invalid inputs gave me stronger evidence that its behavior matches the requirements. Date-based results also need a clear reference date because they change each day.

### Next step
Get feedback from another person on whether the results and suggested actions are easy to understand.