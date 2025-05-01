"""
Utility functions to load data from the dataset and the submissions
"""

# Default paths to inputs, relative to top-level repo dir
from pathlib import Path
from functools import lru_cache
import glob
from typing import Literal, Union
import json

import pandas as pd
from PIL import Image
import numpy as np

from .paths import RELPATH_DIR_IMAGES, RELPATH_DIR_EVALUATIONS, RELPATH_DIR_SUBMISSIONS, RELPATH_DIR_GT, RELPATH_FILE_VALID_SUBMISSIONS
import warnings

# Some utility fonctions to obtain file lists

VALID_TASKS = [1, 2, 3, 4]
TypeTaskId = Literal[1, 2, 3, 4]

VALID_SUBSETS = ["rumsey", "ign", "twh"]
TypeDatasetName = Literal["rumsey", "ign", "twh"]
DATASET_NAMETOID: dict[TypeDatasetName, int] = {
    "rumsey": 1,
    "ign": 2,
    "twh": 3
}
DATASET_IDTONAME: dict[int, TypeDatasetName] = {
    1: "rumsey",
    2: "ign",
    3: "twh",
}

DATASET_NAME_TO_SUBDIR_NAME: dict[TypeDatasetName, str] = {
    "rumsey": "rumsey",
    "ign": "ign25",
    "twh": "tw25"
}

@lru_cache
def list_available_images(subset: TypeDatasetName) -> list[Path]:
    """Returns the list of available images for a given subset"""
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    file_ext = "png" if subset == "rumsey" else "jpg"
    subdir = DATASET_NAME_TO_SUBDIR_NAME[subset]
    glob_expr = RELPATH_DIR_IMAGES / subdir / "test" / f"*.{file_ext}"
    all_files = glob.glob(glob_expr.as_posix())
    return [Path(p) for p in sorted(all_files)]

@lru_cache
def list_evaluations(task: TypeTaskId, subset: TypeDatasetName) -> list[str]:
    """Returns the ids of the submission evaluations available for the given task and dataset

    Args:
        task (either 1, 2, 3 or 4): Task id
        subset (either "rumsey", "ign" or "twh"): subset name

    Returns:
        list[str]: list of available submission ids, to be loaded with `load_result()`
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    glob_expr = RELPATH_DIR_EVALUATIONS / f"t{task}" / f"f{subset_id}" / "*.json"
    all_files = glob.glob(glob_expr.as_posix())
    all_files = [Path(p) for p in sorted(all_files)]
    return [p.stem for p in all_files]


def load_evaluation(task: TypeTaskId, subset: TypeDatasetName, submission_id: str) -> dict:
    """Reads the evaluation json file associated to a particular submission, for a given task and dataset.

    Args:
        task (either 1, 2, 3 or 4): task id
        subset (either "rumsey", "ign" or "twh"): dataset name
        submission_id (str): submission id, as returned by `list_results()`

    Returns:
        dict: Content loaded from the result file
    """
    if task not in VALID_TASKS:
        raise ValueError(f"Invalid task id: {task}")
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    subset_id = DATASET_NAMETOID[subset]
    file_path = RELPATH_DIR_EVALUATIONS / f"t{task}" / f"f{subset_id}" / f"{submission_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_evaluations(taskid: TypeTaskId, subset: TypeDatasetName, filter_fn=None):
    """
    Load all evaluations for a given task and subset as dataframes.
    :param taskid: The task ID.
    :param subset: The subset.
    :param filter: A function that filters the results by submission id.
    :return: A list of results.
    """
    submission_ids = list_evaluations(taskid, subset)
    if filter_fn:
        submission_ids = [s for s in submission_ids if filter_fn(s)]

    results_global = []
    results_images = []

    for submission_id in submission_ids:
        # Read the results
        result_raw = load_evaluation(taskid, subset, submission_id)
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
    indexes_global = ['task_id', 'subset', 'submission_id']
    columns_global = (
        indexes_global
        + (["char_quality", "char_accuracy"] if taskid in (4,) else [])  # Only for task 4 as task 3 optimizes detection conditionned on perfect text prediction
        + ["quality", "tightness", "fscore", "precision", "recall"]
        )
    results_global_df = pd.DataFrame.from_records(results_global, columns=columns_global, index=indexes_global)

    indexes_images = ['task_id', 'subset', 'submission_id', 'image_id']
    columns_images = (
        indexes_images
        + (["char_quality", "char_accuracy"] if taskid in (4,) else [])  # Only for task 4 as task 3 optimizes detection conditionned on perfect text prediction
        + ["quality", "tightness", "fscore", "precision", "recall"]
        )
    results_images_df = pd.DataFrame.from_records(results_images, columns=columns_images, index=indexes_images)

    return results_global_df, results_images_df

@lru_cache
def list_submissions(task: TypeTaskId, subset: TypeDatasetName) -> list[str]:
    """Returns the ids of the available submissions

    Args:
        task (either 1, 2, 3 or 4): Task id
        subset (either "rumsey", "ign" or "twh"): subset name

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

def load_submission(task: TypeTaskId, subset: TypeDatasetName, submission_id: str) -> dict:
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
def load_gt(subset: TypeDatasetName) -> dict:
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


def list_gt_images(subset: TypeDatasetName) -> list[str]:
    """Returns the list of image ids for the ground truth of a given dataset

    Args:
        subset (either "rumsey" or "ign"): dataset name

    Returns:
        list[str]: list of image ids
    """
    if subset not in VALID_SUBSETS:
        raise ValueError(f"Invalid subset name: {subset}")
    gt = load_gt(subset)
    return sorted([e["image"] for e in gt])


def check_for_missing_images(subset: TypeDatasetName) -> list[str]:
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


def open_image(image_id: str) -> Image:
    """Opens an image from the dataset

    Args:
        image_id (str): image id in the form `{subset}/{split}/{filename}.{ext}`

    Returns:
        image: the image as a Pillow object
    """
    image_path = RELPATH_DIR_IMAGES / image_id
    return Image.open(image_path)


@lru_cache
def load_valid_submissions_metadata() -> pd.DataFrame:
    """Load the list of valid submissions

    Returns:
        pd.DataFrame: The list of valid submissions
    """
    valid_submissions =  pd.read_csv(RELPATH_FILE_VALID_SUBMISSIONS)
    # assert len(valid_submissions) == 42  # FIXME 2025
    return valid_submissions


def list_valid_submission_ids(task_id: Union[TypeTaskId, None] = None, subset: Union[TypeDatasetName, None] = None) -> list[int]:
    """Returns the list of valid submission ids

    Returns:
        list[int]: list of valid submission ids
    """
    valid_submissions_metadata = load_valid_submissions_metadata()
    # generate a mask for task_id and subset
    mask = np.ones(len(valid_submissions_metadata), dtype=bool)
    if task_id is not None:
        mask &= valid_submissions_metadata["task"] == task_id
    if subset is not None:
        mask &= valid_submissions_metadata["subset"] == subset
    if not mask.any():
        warnings.warn("No valid submission found for the given task and subset", UserWarning)
        return []
    # gather the submission ids
    valid_submissions_ids = valid_submissions_metadata.loc[mask, "submission_id"].tolist()
    return valid_submissions_ids

def load_valid_evaluations(task_id: TypeTaskId, subset: TypeDatasetName) -> pd.DataFrame:
    """Load the valid evaluations for a given task and subset

    Args:
        task_id (TypeTaskId): The task ID.
        subset (TypeDatasetName): The subset.

    Returns:
        pd.DataFrame: The valid evaluations for the given task and subset
    """
    valid_submissions_ids = list_valid_submission_ids(task_id, subset)
    results_global, results_images = load_evaluations(task_id, subset, lambda s: int(s) in valid_submissions_ids)
    return results_global, results_images
