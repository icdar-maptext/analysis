"""
Defaut paths to resources.
"""

# Default paths to inputs, relative to top-level repo dir
from pathlib import Path

# IMAGES
RELPATH_DIR_IMAGES = Path("data/00-input/images")
# images for each dataset will then be
# - `{RELPATH_DIR_IMAGES}/rumsey/test/*.png` for "rumsey" dataset
# - `{RELPATH_DIR_IMAGES}/ign/test/*.jpg` for "ign" dataset

# RESULTS / EVALUATIONS
RELPATH_DIR_RESULTS = Path("data/00-input/ch28")
# results for each submission will then be
# `{RELPATH_DIR_RESULTS}/t{TASKID}/f{FILEID}/{SUBID}.json` where:
# - `TASKID` in (1, 2, 3, 4) is the task identifier
# - `FILEID` in (1, 2) is the dataset identifier: 1 for "rumsey", 2 for "ign"
# - `SUBID` is the unique submission id (see associated `submission.csv` file in submissions dir)


# PARTICIPANTS' SUBMISSIONS
RELPATH_DIR_SUBMISSIONS = Path("data/00-input/submissions_competition-20240507073418/data/ch28")
# each submission has the same naming structure as the evaluation files
# (but with different content of course)
# there is an extra `submission.csv` containing identifiers and other coarse information

# METADATA FOR SUBMISSIONS
RELPATH_FILE_SUBMISSIONS_META = Path("data/00-input/submissions_competition-20240507073418/data/submissions.csv")

# GT
RELPATH_DIR_GT = Path("data/00-input/gt")
# gt files for each dataset will then be
# - `{RELPATH_DIR_GT}/rumsey/test.json` for "rumsey" dataset
# - `{RELPATH_DIR_GT}/ign/test.json` for "ign" dataset

# VALID SUMISSIONS
RELPATH_FILE_VALID_SUBMISSIONS = Path("valid_submissions.csv")
# list of valid submissions (submission ids) to consider for the analysis
# format: task,subset,submission_id
