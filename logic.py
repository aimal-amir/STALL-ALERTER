"""CSV validation and transparent hiring stall detection rules."""
from datetime import date, datetime
from numbers import Integral

import pandas as pd

REQUIRED_COLUMNS = ("candidate_name", "role", "stage", "last_activity_date")
CLOSED_STAGES = {"hired", "rejected", "withdrawn"}
# Stage only breaks ties in inactivity; unfamiliar stages keep their CSV order.
STAGE_ORDER = {"offer": 0, "interview": 1, "screening": 2, "applied": 3}
FOLLOW_UP_WITH = {
    "applied": "Recruiter / application reviewer",
    "screening": "Screening owner",
    "interview": "Interviewer / hiring manager",
    "offer": "Offer owner, then candidate",
}
ACTIONS = {
    "applied": "Review the application and decide the next step.",
    "screening": "Check screening progress and arrange the next step.",
    "interview": "Ask the interviewer for feedback.",
    "offer": "Check the offer status and follow up with the candidate.",
}


class ValidationError(ValueError):
    """Input problems that can be shown directly to the user."""


def read_csv(source):
    """Read a path or uploaded file, preserving text such as names equal to NA."""
    try:
        return pd.read_csv(source, dtype=str, keep_default_na=False)
    except (ValueError, OSError, UnicodeError, pd.errors.ParserError) as exc:
        raise ValidationError(
            "Could not read the CSV. Upload a UTF-8 CSV with a header row and consistent columns."
        ) from exc


def validate_data(data, today=None):
    """Return cleaned data or report all detected problems; row 1 is the header."""
    today = today or date.today()
    errors = []
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing) + ".")
    if data.empty:
        errors.append("The CSV contains no candidate rows.")
    cleaned = data.copy().reset_index(drop=True)
    for column in REQUIRED_COLUMNS:
        if column not in cleaned:
            continue
        cleaned[column] = cleaned[column].astype("string").str.strip()
        blank = cleaned[column].isna() | cleaned[column].eq("")
        if blank.any():
            rows = ", ".join(str(i + 2) for i in cleaned.index[blank])
            errors.append(f"Blank required value in '{column}' at CSV row(s): {rows}.")
    if "last_activity_date" in cleaned:
        parsed = []
        invalid, future = [], []
        for i, value in enumerate(cleaned["last_activity_date"]):
            if pd.isna(value) or value == "":
                parsed.append(None)
                continue
            try:
                if len(value) != 10 or value[4] != "-" or value[7] != "-":
                    raise ValueError
                activity = datetime.strptime(value, "%Y-%m-%d").date()
                if activity.isoformat() != value:
                    raise ValueError
                parsed.append(activity)
                if activity > today:
                    future.append(str(i + 2))
            except ValueError:
                parsed.append(None)
                invalid.append(str(i + 2))
        if invalid:
            errors.append("Invalid date at CSV row(s): " + ", ".join(invalid) + ". Use valid dates in YYYY-MM-DD format.")
        if future:
            errors.append("Future activity date at CSV row(s): " + ", ".join(future) + f". Dates must be on or before {today.isoformat()}.")
        cleaned["last_activity_date"] = parsed
    if errors:
        raise ValidationError("\n".join(errors))
    return cleaned


def detect_stalled(data, threshold=7, today=None):
    """Build a follow-up queue by inactivity, then stage, then original CSV order."""
    if isinstance(threshold, bool) or not isinstance(threshold, Integral) or threshold < 1:
        raise ValidationError("The inactivity threshold must be a positive whole number.")
    today = today or date.today()
    result = validate_data(data, today)
    result["days_inactive"] = result["last_activity_date"].map(lambda activity: (today - activity).days)
    stages = result["stage"].str.casefold()
    result = result.loc[~stages.isin(CLOSED_STAGES) & result["days_inactive"].ge(threshold)].copy()
    result["next_action"] = result["stage"].str.casefold().map(ACTIONS).fillna(
        "Review the latest activity and confirm the next step."
    )
    result["explanation"] = result.apply(
        lambda row: f"{row['candidate_name']} has been inactive for {row['days_inactive']} days, meeting the {threshold}-day follow-up threshold.", axis=1
    ) if not result.empty else pd.Series(dtype=str)
    result["follow_up_with"] = result["stage"].str.casefold().map(FOLLOW_UP_WITH).fillna(
        "Recruiter / current stage owner"
    )
    result["days_over_threshold"] = result["days_inactive"] - threshold
    result["_stage_order"] = result["stage"].str.casefold().map(STAGE_ORDER).fillna(4)
    result = result.sort_values(
        ["days_inactive", "_stage_order"], ascending=[False, True], kind="stable"
    ).drop(columns="_stage_order").reset_index(drop=True)
    result["follow_up_rank"] = range(1, len(result) + 1)
    result["priority_reason"] = result["days_over_threshold"].map(
        lambda days: f"{days} day(s) beyond the follow-up threshold. Longest inactivity first; ties use Offer, Interview, Screening, Applied, then other stages."
    )
    return result
