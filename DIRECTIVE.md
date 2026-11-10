# Final Project Directive — Hiring Stall Alerter

Date: November 10, 2026

## Purpose

Deliver a working tool that turns a hiring-board CSV into an ordered follow-up queue for recruiters and hiring coordinators. The user must be able to answer: **Who should I follow up with first, why, and what should I do next?**

This directive defines the final first-version behavior. `INTENT.md` records the project purpose and assumptions; this document specifies the rules, outputs, boundaries, and completion criteria.

## User workflow

1. Export the hiring sheet as a CSV and upload it to the Streamlit app.
2. Choose an inactivity threshold, defaulting to 7 calendar days.
3. Correct any reported input errors before viewing results.
4. Review the highlighted first candidate and the numbered follow-up queue.
5. Check the latest hiring notes, contact the appropriate person, and perform the suggested action.
6. Update the source hiring sheet after meaningful activity and upload a fresh export when needed.

## Input requirements

The CSV must contain these exact column names:

| Column | Required value |
| --- | --- |
| `candidate_name` | Candidate name |
| `role` | Position applied for |
| `stage` | Current hiring stage |
| `last_activity_date` | Valid date in `YYYY-MM-DD` format |

An optional `id` and other extra columns are allowed. Trim surrounding spaces from required values. Match stages without regard to capitalization. Use the date of the latest meaningful hiring activity for `last_activity_date`.

Reject unreadable CSVs, missing required columns, files without candidate rows, blank required values, invalid dates, and future activity dates. Validate every row, including candidates in closed stages. Identify affected CSV rows where possible, counting the header as row 1. Do not display a partial queue when validation fails.

## Selection and priority mechanism

Use transparent rules that produce the same order for the same data, threshold, and reference date:

1. Calculate `days_inactive = reference_date - last_activity_date` in calendar days.
2. Exclude Hired, Rejected, and Withdrawn candidates.
3. Include active candidates whose inactivity is greater than or equal to the selected threshold. The threshold must be a positive whole number.
4. Order candidates by days inactive, highest first.
5. Break equal-inactivity ties by stage: Offer → Interview → Screening → Applied → other active stages.
6. Preserve the original CSV order when candidates remain tied.
7. Assign consecutive follow-up ranks starting at 1.

Stage only breaks ties. A candidate in Applied with 12 days of inactivity comes before a candidate in Offer with 8 days of inactivity. Unknown active stages remain eligible and receive a general action.

Calculate days beyond the threshold as `days_inactive - threshold`. A candidate exactly at the threshold has zero days beyond it and is still included.

## Follow-up actions

| Stage | Suggested contact | Next action |
| --- | --- | --- |
| Applied | Recruiter / application reviewer | Review the application and decide the next step. |
| Screening | Screening owner | Check screening progress and arrange the next step. |
| Interview | Interviewer / hiring manager | Ask the interviewer for feedback. |
| Offer | Offer owner, then candidate | Check the offer status and follow up with the candidate. |
| Other active stage | Recruiter / current stage owner | Review the latest activity and confirm the next step. |

Contact labels describe responsibilities. Actual owner names and contact details are not available in the current input.

## Required interface output

Display the reference date, selected threshold, exclusion rule, and ordering rule. For a valid upload with matches, highlight the first candidate with their role, days inactive, suggested contact, and action.

The table must show:

- Follow-up order.
- Candidate name, role, and stage.
- Days inactive and days beyond the threshold.
- A readable explanation of the priority rule.
- Suggested contact and next action.

If a valid upload has no matches, display **“No stalled candidates found.”** Before an upload, prompt the user to upload a CSV.

## Implementation and operating boundaries

Use Python, pandas, and Streamlit. Keep validation and queue rules in `logic.py`, the interface in `app.py`, and automated checks in `test_logic.py`. Keep the interface and imported rules synchronized during Streamlit reruns.

This version reads uploaded CSV exports. It does not connect directly to a live sheet, update the source sheet, send messages, maintain follow-up history, or require accounts, a database, or an AI API. A human reviews recommendations and performs follow-up.

The queue prioritizes hiring workflow follow-up; it does not assess candidate suitability or make hiring decisions. Inactivity and stage are the only priority signals. Deadlines, role urgency, intentional holds, weekends, and holidays do not change the ranking. The reference date comes from the machine running the app and must be visible to the user.

## Acceptance criteria and verification

The first version is complete when:

- Sample uploads produce the expected candidates, inactivity values, and order for a fixed reference date.
- Candidates exactly at the threshold are included; those below it are excluded.
- Closed stages are excluded despite capitalization or surrounding spaces.
- Inactivity takes precedence over stage, stage ties follow the defined order, and remaining ties retain CSV order.
- Every result has a rank, priority reason, contact label, and next action.
- Unknown active stages receive the general recommendation.
- Invalid input produces clear errors and no partial results.
- Empty results display the specified message.
- Both the initial screen and an uploaded CSV render without exceptions, including after the logic module is reloaded.

Run the automated checks from the project directory:

```bash
.venv/bin/python -m unittest -v
```

For a manual check, use `MOCK_DATA.csv` with a reference date of November 10, 2026 and a 7-day threshold. The expected queue is Jamie Brooks (19 days), Alex Morgan (16), Drew Parker (12), Casey Patel (11), Quinn Adams (10), and Riley Chen (9). Results change with the reference date.

Start the app with:

```bash
.venv/bin/streamlit run app.py
```

Record completed verification and observed limitations in `DEVELOPMENT_LOG.md`. Treat changes to ranking signals, data requirements, or automatic actions as scope changes and update this directive alongside the implementation.
