"""
Utility functions to load data from the dataset and the submissions
"""

# Default paths to inputs, relative to top-level repo dir
from pathlib import Path
from functools import lru_cache
import glob
from typing import Literal
import json

import pandas as pd

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
    """Returns the list of available images for a given subset"""
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
        task (either 1, 2, 3 or 4): Task id
        subset (either "rumsey" or "ign"): subset name

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
        task (either 1, 2, 3 or 4): task id
        subset (either "rumsey" or "ign"): dataset name
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


def load_results(taskid: TYPE_TASK_ID, subset: TYPE_DATASET_NAME, filter_fn=None):
    """
    Load all results for a given task and subset as dataframes.
    :param taskid: The task ID.
    :param subset: The subset.
    :param filter: A function that filters the results by submission id.
    :return: A list of results.
    """
    submission_ids = list_results(taskid, subset)
    if filter_fn:
        submission_ids = [s for s in submission_ids if filter_fn(s)]
 
    results_global = []
    results_images = []

    for submission_id in submission_ids:
        # Read the results
        result_raw = load_result(taskid, subset, submission_id)
        result_global = result_raw['results']
        result_images = result_raw['images']

        # Process global results first
        result_global['task_id'] = taskid
        result_global['subset'] = subset
        result_global['submission_id'] = submission_id
        results_global.append(result_global)

        # # Add the submission ID to the results
        for image_id, result_image in result_images.items():
            result_image['task_id'] = taskid
            result_image['subset'] = subset
            result_image['submission_id'] = submission_id
            result_image['image_id'] = image_id
            results_images.append(result_image)

   # Create two dataframes: one for the global results and one for the image results
    results_global_df = pd.DataFrame.from_records(
        results_global,
        columns=['task_id', 'subset', 'submission_id',
                 "quality", "fscore", "tightness", "precision", "recall"],
        index=['task_id', 'subset', 'submission_id'])

    results_images_df = pd.DataFrame.from_records(
        results_images,
        columns=['task_id', 'subset', 'submission_id', 'image_id',
                 "quality", "fscore", "tightness", "precision", "recall"],
        index=['task_id', 'subset', 'submission_id', 'image_id'])

    return results_global_df, results_images_df

@lru_cache
def list_submissions(task: TYPE_TASK_ID, subset: TYPE_DATASET_NAME) -> list[str]:
    """Returns the ids of the available submissions

    Args:
        task (either 1, 2, 3 or 4): Task id
        subset (either "rumsey" or "ign"): subset name

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
        task (either 1, 2, 3 or 4): task id
        subset (either "rumsey" or "ign"): dataset name
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
        subset (either "rumsey" or "ign"): dataset name

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
        subset (either "rumsey" or "ign"): dataset name

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
        subset (either "rumsey" or "ign"): dataset name

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
