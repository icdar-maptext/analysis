"""
Utility functions to load data from the dataset and the submissions
"""

# Default paths to inputs, relative to top-level repo dir
from pathlib import Path
from functools import lru_cache
import glob
from typing import Literal
import json

from .paths import RELPATH_DIR_IMAGES, RELPATH_DIR_RESULTS, RELPATH_DIR_SUBMISSIONS, RELPATH_DIR_GT

# Some utility fonctions to obtain file lists

VALID_TASKS = [1, 2, 3, 4]
TYPE_TASK_ID = Literal[1, 2, 3, 4]

VALID_SUBSETS = ["rumsey", "ign"]
TYPE_DATASET_NAME = Literal["rumsey", "ign"]
DATASET_NAMETOID: dict[TYPE_DATASET_NAME, int] = {
    "rumsey": 1,
    "ign": 2
}
DATASET_IDTONAME: dict[int, TYPE_DATASET_NAME] = {
    1: "rumsey",
    2: "ign"
}

@lru_cache
def list_available_images(subset: TYPE_DATASET_NAME) -> list[Path]:
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    file_ext = "png" if subset == "rumsey" else "jpg"
    glob_expr = RELPATH_DIR_IMAGES / subset / "test" / f"*.{file_ext}"
    all_files = glob.glob(glob_expr.as_posix())
    return [Path(p) for p in sorted(all_files)]

@lru_cache
def list_results(task: TYPE_TASK_ID, subset: TYPE_DATASET_NAME) -> list[str]:
    """Returns the ids of the submissions available for the given task and dataset

    Args:
        task (__TYPE_TASK_ID): Task id
        subset (__TYPE_DATASET_NAME): subset name

    Returns:
        list[str]: list of available submission ids, to be loaded with `load_result()`
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    glob_expr = RELPATH_DIR_RESULTS / f"t{task}" / f"f{subset_id}" / "*.json"
    all_files = glob.glob(glob_expr.as_posix())
    all_files = [Path(p) for p in sorted(all_files)]
    return [p.stem for p in all_files]

def load_result(task: TYPE_TASK_ID, subset: TYPE_DATASET_NAME, submission_id: str) -> dict:
    """Reads the json file associated to a particular submission, for a given task and dataset.

    Args:
        task (__TYPE_TASK_ID): task id
        subset (__TYPE_DATASET_NAME): dataset name
        submission_id (str): submission id, as returned by `list_results()`

    Returns:
        dict: Content loaded from the result file
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    file_path = RELPATH_DIR_RESULTS / f"t{task}" / f"f{subset_id}" / f"{submission_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@lru_cache
def list_submissions(task: TYPE_TASK_ID, subset: TYPE_DATASET_NAME) -> list[str]:
    """Returns the ids of the available submissions

    Args:
        task (__TYPE_TASK_ID): Task id
        subset (__TYPE_DATASET_NAME): subset name

    Returns:
        list[str]: list of available submission ids, to be loaded with `load_submission()`
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    glob_expr = RELPATH_DIR_SUBMISSIONS / f"t{task}" / f"f{subset_id}" / "*.json"
    all_files = glob.glob(glob_expr.as_posix())
    all_files = [Path(p) for p in sorted(all_files)]
    return [p.stem for p in all_files]

def load_submission(task: TYPE_TASK_ID, subset: TYPE_DATASET_NAME, submission_id: str) -> dict:
    """Reads the json file associated to a particular submission, for a given task and dataset.

    Args:
        task (__TYPE_TASK_ID): task id
        subset (__TYPE_DATASET_NAME): dataset name
        submission_id (str): submission id, as returned by `list_submissions()`

    Returns:
        dict: Content loaded from the submission file
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    file_path = RELPATH_DIR_SUBMISSIONS / f"t{task}" / f"f{subset_id}" / f"{submission_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@lru_cache
def load_gt(subset: TYPE_DATASET_NAME) -> dict:
    """Reads the ground truth file for a given dataset

    Args:
        subset (__TYPE_DATASET_NAME): dataset name

    Returns:
        dict: Content loaded from the ground truth file
    """
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    file_path = RELPATH_DIR_GT / subset / "test.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_gt_images(subset: TYPE_DATASET_NAME) -> list[str]:
    """Returns the list of image ids for the ground truth of a given dataset

    Args:
        subset (__TYPE_DATASET_NAME): dataset name

    Returns:
        list[str]: list of image ids
    """
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    gt = load_gt(subset)
    return list(gt.keys())


def check_for_missing_images(subset: TYPE_DATASET_NAME) -> list[str]:
    """Checks if there are missing images in the ground truth

    Args:
        subset (__TYPE_DATASET_NAME): dataset name

    Returns:
        list[str]: list of image ids that are missing from the ground truth
    """
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    gt = [e["image"] for e in load_gt(subset)]
    images = list_available_images(subset)
    # remove prefix and suffix to get the image id
    image_ids = [p.relative_to(RELPATH_DIR_IMAGES).as_posix() for p in images]
    return [img_id for img_id in image_ids if img_id not in gt]
