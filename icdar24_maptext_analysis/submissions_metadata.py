
import pandas as pd


from .paths import RELPATH_FILE_SUBMISSIONS_META

SUBMISSION_METADATA = pd.read_csv(RELPATH_FILE_SUBMISSIONS_META, index_col="ID")

USER_TO_TEAM_NAME: dict[str, str] = {
    'user_9': "",  # "Org.",  # MapText Organizers
    'user_36250': "",
    'user_51436': "",
    'user_43613': "",
    'user_50898': "",
    'user_53700': "",
    'user_53137': "",
    'user_51343': "",
}

def lookup_generate_title(submission_id: int) -> str:
    """
    Generate a title for a submission based on the submission ID.

    Args:
        submission_id (int): The ID of the submission.

    Returns:
        str: The generated title for the submission.
    """
    sub_name = SUBMISSION_METADATA.loc[submission_id, "Title"]
    user_id = SUBMISSION_METADATA.loc[submission_id, "User"]
    team_name = USER_TO_TEAM_NAME[user_id]
    return f"{team_name} {sub_name}" if len(team_name) > 0 else sub_name  # ← change the format for titles here (abreviation is handled in `shorten_title()`)

def shorten_title(title: str, max_length: int = 30) -> str:
    if max_length < 20:
        raise ValueError("max_length must be at least 20")
    new_title = title.strip()
    if len(new_title) > max_length:
        suffix_length = 15
        prefix_length = max_length - suffix_length - 3
        new_title = new_title[:prefix_length] + "..." + new_title[-suffix_length:]
    # print(f"{title} -> {new_title}")
    return new_title

