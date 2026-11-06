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