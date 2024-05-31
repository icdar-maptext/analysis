# Raw predictions sample from MapText submissions

*Generated on May, 31st, 2024*

Files structure: `{TASK}/{SUBSET}/{SELECTION}/{IMAGEID}.pdf` where

- `{TASK}` is "task1", "task2", "task3" or "task4"
- `{SUBSET}` is "rumsey", or "ign"
- `{SELECTION}` is "random", "easy" or "hard"
- `{IMAGEID}` is the image id in the dataset

Example: `20-raw-predictions/task2/ign/hard/000016.pdf`

For each image, the PDF contains a comparison of the raw predictions of each submission, with the ground truth.

For each task, the random images are the same, but the easy and hard images are different: their selection is based on the mean performance of all submissions regarding the main evaluation metric of the task.

Sorting strategies for each task:

- Task 1: by detection quality (Panoptic Quality) for isolated words
- Task 2: by detection quality (Panoptic Quality) for word groups
- Task 3: by detection quality (Panoptic Quality) for isolated words while constraining matches between the ground truth and predictions to have exactly the same transcription
- Task 4: by character quality (Panoptic Character Quality) for word groups


Task details and legend for each task:

- `task1/`: detections for isolated words. Red means cropped or ignored regions, blue means prediction, green is ground truth.
- `task2/`: detections for word groups. Groups are colored with different colors, and a link is drawn between successive group members. Ground truth is displayed separately.
- `task3/`: detections and transcriptions of isolated words. Groups are colored with different colors, and the transcription for each isolated work is overlaid as black text. Ground truth is displayed separately.
- `task4/`: detection and transcription of word groups. Same visualization as task3, but different sorting for easy and hard images.

