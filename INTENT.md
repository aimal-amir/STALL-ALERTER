# Project Intent

## What I am building

A hiring stall alerter that reads a hiring-board CSV, identifies candidates who have been inactive for a chosen number of days, and recommends who to follow up with first.

## Who it is for

Recruiters and hiring coordinators who need a quick way to spot delayed candidates without manually reviewing every row of a hiring board.

## Problem I want to solve

Candidates can remain in a hiring stage without timely feedback or a clear next step. I want to make these delays visible and give the recruiter a practical follow-up list.

## Intended outcome

A user can upload a CSV, choose an inactivity threshold, and see:
- Which active candidates meet or exceed the threshold.
- How long each candidate has been inactive.
- Why each candidate was flagged.
- A suggested next action based on their hiring stage.

Candidates are ordered by longest inactivity first. Equal inactivity is ordered by Offer, Interview, Screening, Applied, then other stages; remaining ties preserve CSV order. The queue shows a numbered rank, suggested contact, and next action. A human reviews the recommendations and handles follow-up.

## Why I chose this scope

The workflow is small enough to build and evaluate within five days. Its rules are easy to explain, and I can compare the output with manually calculated expectations.

## Technical approach

Use Python, Streamlit, and pandas. Start with transparent rules:
- Default to a 7-day inactivity threshold.
- Exclude Hired, Rejected, and Withdrawn candidates.
- Use calendar days.
- Validate the input before displaying results.

The first version does not need accounts, a database, or automatic messaging.

## How I intend to work with AI

Use AI to help plan, implement, debug, and review the tool. Check its suggestions against the requirements and verify results independently.

Document assumptions, errors, changes, and evidence in DEVELOPMENT_LOG.md.

## Assumptions to test

- Days since last activity is a useful signal for follow-up.
- Longest inactivity is a useful initial priority rule.
- Stage-based suggestions help users decide what to do next.

These assumptions may change after testing and feedback.

## Success criteria

The tool produces the expected follow-up list from the sample CSV, handles threshold boundaries and closed stages correctly, and gives understandable feedback for invalid data.

## Limitations

A flag indicates that a candidate needs review; it does not prove that something is wrong. Intentional delays, weekends, holidays, and role urgency are not accounted for in the first version.