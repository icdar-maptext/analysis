"""
Defaut paths to resources.
"""

# Default paths to inputs, relative to top-level repo dir
from pathlib import Path
from functools import lru_cache
import glob
from typing import Literal
import json

# IMAGES
RELPATH_DIR_IMAGES = Path("data/00-input/images")
# images for each dataset will then be
# - `{RELPATH_DIR_IMAGES}/rumsey/test/*.png` for "rumsey" dataset
# - `{RELPATH_DIR_IMAGES}/ign/test/*.jpg` for "ign" dataset

# RESULTS / EVALUATIONS
RELPATH_DIR_RESULTS = Path("data/00-input/defaults-20240507074007/data/ch28")
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

# GT
RELPATH_DIR_GT = Path("data/00-input/gt")
# gt files for each dataset will then be
# - `{RELPATH_DIR_GT}/rumsey/test.json` for "rumsey" dataset
# - `{RELPATH_DIR_GT}/ign/test.json` for "ign" dataset


# Some utility fonctions to obtain file lists

__TYPE_TASK_ID = Literal[1, 2, 3, 4]

__TYPE_DATASET_NAME = Literal["rumsey", "ign"]
__DATASET_NAMETOID: dict[__TYPE_DATASET_NAME, int] = {
    "rumsey": 1,
    "ign": 2
}
__DATASET_IDTONAME: dict[int, __TYPE_DATASET_NAME] = {
    1: "rumsey",
    2: "ign"
}

@lru_cache
def __image_list(subset: __TYPE_DATASET_NAME) -> list[Path]:
    file_ext = "png" if subset == "rumsey" else "jpg"
    all_files = glob.glob(RELPATH_DIR_IMAGES / subset / "test" / f"*.{file_ext}")
    return [Path(p) for p in sorted(all_files)]

def image_list_rumsey() -> list[Path]:
    """
    Returns the list of images for the "rumsey" dataset
    """
    return __image_list("rumsey")

def image_list_ign() -> list[Path]:
    """
    Returns the list of images for the "ign" dataset
    """
    return __image_list("ign")

@lru_cache
def results_list(task: __TYPE_TASK_ID, subset: __TYPE_DATASET_NAME) -> list[str]:
    """Returns the ids of the submissions available for the given task and dataset

    Args:
        task (__TYPE_TASK_ID): Task id
        subset (__TYPE_DATASET_NAME): subset name

    Returns:
        list[str]: list of available submission ids, to be loaded with `results_read()`
    """
    subset_id = __DATASET_NAMETOID[subset]
    all_files = glob.glob(RELPATH_DIR_RESULTS / f"t{task}" / f"f{subset_id}" / "*.json")
    all_files = [Path(p) for p in sorted(all_files)]
    return [p.stem for p in all_files]

def results_read(task: __TYPE_TASK_ID, subset: __TYPE_DATASET_NAME, submission_id: str) -> dict:
    """Reads the json file associated to a particular submission, for a given task and dataset.

    Args:
        task (__TYPE_TASK_ID): task id
        subset (__TYPE_DATASET_NAME): dataset name
        submission_id (str): submission id, as returned by `results_list()`

    Returns:
        dict: Content loaded from the result file
    """
    subset_id = __DATASET_NAMETOID[subset]
    file_path = RELPATH_DIR_RESULTS / f"t{task}" / f"f{subset_id}" / f"{submission_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@lru_cache
def submissions_list(task: __TYPE_TASK_ID, subset: __TYPE_DATASET_NAME) -> list[str]:
    """Returns the ids of the available submissions

    Args:
        task (__TYPE_TASK_ID): Task id
        subset (__TYPE_DATASET_NAME): subset name

    Returns:
        list[str]: list of available submission ids, to be loaded with `submissions_read()`
    """
    subset_id = __DATASET_NAMETOID[subset]
    all_files = glob.glob(RELPATH_DIR_SUBMISSIONS / f"t{task}" / f"f{subset_id}" / "*.json")
    all_files = [Path(p) for p in sorted(all_files)]
    return [p.stem for p in all_files]

def submissions_read(task: __TYPE_TASK_ID, subset: __TYPE_DATASET_NAME, submission_id: str) -> dict:
    """Reads the json file associated to a particular submission, for a given task and dataset.

    Args:
        task (__TYPE_TASK_ID): task id
        subset (__TYPE_DATASET_NAME): dataset name
        submission_id (str): submission id, as returned by `submissions_list()`

    Returns:
        dict: Content loaded from the submission file
    """
    subset_id = __DATASET_NAMETOID[subset]
    file_path = RELPATH_DIR_SUBMISSIONS / f"t{task}" / f"f{subset_id}" / f"{submission_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def gt_read(subset: __TYPE_DATASET_NAME) -> dict:
    """Reads the ground truth file for a given dataset

    Args:
        subset (__TYPE_DATASET_NAME): dataset name

    Returns:
        dict: Content loaded from the ground truth file
    """
    file_path = RELPATH_DIR_GT / subset / "test.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
