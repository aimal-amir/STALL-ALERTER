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

## November 10, 2026 — Final follow-up mechanism and delivery

### Goal
Finish the mechanism for deciding which stalled candidate to follow up with first and what action to take.

### How I used AI
I used AI to review the existing implementation, make the priority rules explicit, implement the follow-up queue, investigate a runtime error, and document the final project behavior.

### Changes completed
- Kept longest inactivity as the primary priority rule.
- Added a stage tie breaker: Offer, Interview, Screening, Applied, then other active stages. Remaining ties preserve CSV order.
- Added numbered follow-up ranks, days beyond the threshold, priority explanations, and suggested contact roles.
- Highlighted the first candidate above the results table with their suggested contact and next action.
- Kept closed-stage exclusions, input validation, and the adjustable inactivity threshold.
- Updated `INTENT.md` and `README.md` to explain the final mechanism.
- Created `DIRECTIVE.md` with the final workflow, input requirements, ranking rules, actions, scope, and acceptance criteria.

### Error found and correction
The running app raised `KeyError: 'follow_up_with'` when displaying the first candidate. The code on disk already produced that column, suggesting that Streamlit had retained the older imported logic while rerunning the updated interface. The app now reloads the logic module on reruns so the interface and result columns stay synchronized.

The original UI test only checked the screen before an upload. I added a regression test that simulates stale imported logic, uploads CSV content, and checks that the first-candidate message and follow-up table render successfully.

### Verification
Ran `.venv/bin/python -m unittest -v`: all 6 tests passed after the fix. The checks cover threshold boundaries, closed stages, unknown stages, ordering and ties, contact and action output, invalid data, the initial screen, and the uploaded-CSV path with stale logic. `git diff --check` also passed for the follow-up implementation.

### Delivery
Created the `final` branch and pushed it to `origin/final` on GitHub. The implementation and `DIRECTIVE.md` were already committed when the branch was created. This log entry was added after that push.

### What I learned
Passing logic tests and an empty-screen UI test did not verify the complete upload workflow. Testing the path that actually displays results helped catch the integration gap. Explicit ranks and contact suggestions also make the existing inactivity rule easier to act on.

### Final scope and limitations
The tool recommends workflow follow-up; a human reviews the latest notes and performs the action. Contacts are responsibility labels rather than named owners. It reads CSV exports and does not update a live sheet or send messages. Ranking does not account for deadlines, role urgency, intentional holds, weekends, or holidays.
