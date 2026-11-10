# Hiring Stall Alerter

A small tool that helps recruiters identify candidates who have been inactive for too long and decide who to follow up with first.

Built for the **Unlearn, Use, Raise the Load** assignment.

## Project Status

The first working version is implemented in `app.py` and `logic.py`.

## Problem

Candidates can get stuck in a hiring pipeline when feedback or next steps are delayed. Manually checking every candidate makes it easy to miss someone who needs follow-up.

## Goal

Upload a hiring-board CSV and receive a prioritized list of stalled candidates, with an explanation and a suggested next action for each.

## First-Version Features

- Upload a CSV of candidates.
- Set an inactivity threshold, defaulting to 7 days.
- Identify candidates whose inactivity meets or exceeds the threshold.
- Exclude Hired, Rejected, and Withdrawn candidates.
- Sort results by longest inactivity first.
- Show a short explanation and stage-based next action.
- Display clear errors for invalid input.

The first version does not need login, a database, or automatic messaging.

## Tech Stack

- **Python:** application logic.
- **Streamlit:** web interface.
- **pandas:** CSV processing and date handling.
- **Git and GitHub:** version control.

AI will support development, debugging, and review. The app itself uses transparent rules and does not require an AI API.

## Input Data

The CSV must contain these columns:

| Column | Description |
| --- | --- |
| candidate_name | Candidate's name |
| role | Job the candidate applied for |
| stage | Current hiring stage |
| last_activity_date | Latest activity date in YYYY-MM-DD format |

An optional `id` column is also allowed.

Example:

```csv
id,candidate_name,role,stage,last_activity_date
1,Alex Morgan,QA Engineer,Interview,2026-10-25
2,Sam Taylor,Software Developer,Screening,2026-11-04
3,Jordan Lee,QA Engineer,Hired,2026-10-15
4,Casey Patel,Designer,Offer,2026-10-30
```

All sample candidates are fictional.

## Detection Rules

1. Calculate days inactive using today's date minus the last activity date.
2. Use calendar days, including weekends and holidays.
3. Flag candidates whose days inactive are greater than or equal to the threshold.
4. Exclude Hired, Rejected, and Withdrawn stages.
5. Ignore capitalization and surrounding spaces when checking stages.
6. Sort flagged candidates by days inactive, descending.
7. For equal inactivity, follow up in stage order: Offer, Interview, Screening, Applied, then other active stages. Candidates still tied keep their CSV order.
8. Assign a numbered follow-up order and show days beyond the threshold, the priority rule, the suggested contact, and next action. Highlight the first candidate above the table.

This queue prioritizes workflow follow-up, not candidate suitability. Stage is only a tie breaker: an older Applied candidate still comes before a newer Offer candidate. Contact labels describe suggested responsibilities; the CSV does not identify actual owners. Review the latest notes before acting.

The threshold must be a positive whole number and defaults to 7.

For example, on November 6, 2026, a candidate last active on October 30, 2026 is exactly 7 days inactive and should be flagged.

## Results

For each stalled candidate, display:

- Candidate name
- Role
- Stage
- Days inactive
- Explanation
- Suggested next action

Example explanation:

“Alex Morgan has been inactive for 12 days, meeting the 7-day follow-up threshold.”

Suggested actions:

| Stage | Action |
| --- | --- |
| Applied | Review the application and decide the next step. |
| Screening | Check screening progress and arrange the next step. |
| Interview | Ask the interviewer for feedback. |
| Offer | Check the offer status and follow up with the candidate. |
| Other active stage | Review the latest activity and confirm the next step. |

A human reviews the recommendations and performs any follow-up.

## Input Validation

Show a clear error when:

- The file cannot be read as a CSV.
- Required columns are missing.
- The file contains no candidate rows.
- Required values are blank.
- Dates are invalid or not in YYYY-MM-DD format.
- Activity dates are in the future.

Identify affected rows where possible. Ask the user to correct invalid data before showing results.

If the input is valid but no candidates are stalled, display:

“No stalled candidates found.”

## Project Structure

```text
stall-alerter/
├── app.py
├── logic.py
├── sample.csv
├── requirements.txt
└── README.md
```

- `app.py`: Streamlit interface.
- `logic.py`: Validation and stall detection.
- `sample.csv`: Fictional candidate data.
- `requirements.txt`: Python dependencies.

## Setup and Run

Run these commands from the project folder.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The initial requirements.txt should contain:

```text
streamlit
pandas
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal and upload `sample.csv`.

`MOCK_DATA.csv` contains a larger valid example with 12 fictional candidates. You can upload either example CSV.

For `sample.csv`, using November 6, 2026 and a seven-day threshold gives Alex Morgan (12 days) followed by Casey Patel (7 days). Sam Taylor is below the threshold and Jordan Lee is Hired. Results change with the machine’s current date.

Run the automated checks with:

```bash
python -m unittest -v
```

Validation checks every row, including closed candidates, before showing results. Error row numbers count the header as row 1. Unknown active stages receive a general next-action suggestion; extra columns are allowed.

## Definition of Working

The first version is working when:

- Uploading the sample CSV produces the manually expected results.
- A candidate exactly 7 days inactive is flagged at a threshold of 7.
- A candidate below the threshold is excluded.
- Closed candidates are excluded.
- Results appear in descending order of inactivity.
- Changing the threshold updates the results correctly.
- Every flagged candidate has an explanation and suggested action.
- Invalid data produces understandable errors.
- No matches produces a clear message.

Use a fixed reference date when testing the detection logic so expected results remain consistent.

## AI-First Development Log

Record brief notes each day:

- What did I assume?
- What did I ask AI to help with?
- What worked or failed?
- What did I change?
- How did I verify the result?

Record actual observations and completed checks.

## Limitations

- Calendar days do not account for weekends or holidays.
- Results depend on accurate activity dates.
- Some delays may be intentional and require human judgment.
- Follow-up priority uses inactivity, with hiring stage to break ties. No deadlines, role urgency, or actual owner information are available in the current CSV.
- Today's date comes from the machine running the app.
