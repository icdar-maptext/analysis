# Results Analysis for the *ICDAR 2025 Competition on Historical Map Text Detection, Recognition, and Linking*

This repository contains the official results analysis implementation for the ICDAR'25 MapText competition.
(Analysis code for the ICDAR'24 MapText competition is available through repository tag `icdar-2024`.)

It features a collection of tools to produce tables, graphs and figures for the report, from submissions, evaluations and dataset.


## Prepare local data
You need to gather:
- images for the test sets ("rumsey", "ign" and "twh" datasets)
- submissions from participants
- evaluation results
- ground truth for test sets ("rumsey", "ign" and "twh" datasets) ← optional, for organizers only until ground truth for test set is publicly released.

These files will be stored under `data/00-inputs/` and left unchanged during further work.

Here are the (Linux) commands to download and prepare these files.
```sh
# Download and prepare images
mkdir -p data/00-input/images/
## rumsey dataset
wget -O data/00-input/images/test-rumsey.zip https://zenodo.org/records/10776183/files/test.zip?download=1
unzip data/00-input/images/test-rumsey.zip -d data/00-input/images/
rm data/00-input/images/test-rumsey.zip
## ign dataset
wget -O data/00-input/images/test-ign.zip https://zenodo.org/records/14620633/files/ign25_test.zip?download=1
unzip data/00-input/images/test-ign.zip -d data/00-input/images/
rm data/00-input/images/test-ign.zip
## twh dataset
wget -O data/00-input/images/test-twh.zip https://zenodo.org/records/14958343/files/tw25.zip?download=1
unzip data/00-input/images/test-twh.zip -d data/00-input/images/
rm data/00-input/images/test-twh.zip

# Download and prepare participants' submissions (all datasets)
mkdir -p data/00-input/submissions/
wget -O data/00-input/maptext25-submissions.tar.bz2 https://zenodo.org/records/15297995/files/submissions.tar.bz2?download=1
tar -C data/00-input/submissions -xaf data/00-input/maptext25-submissions.tar.bz2
rm data/00-input/maptext25-submissions.tar.bz2
wget -O data/00-input/submissions.csv https://zenodo.org/records/15297995/files/submissions.csv?download=1


# Download and prepare evaluation results (all datasets)
mkdir -p data/00-input/evaluations/
wget -O data/00-input/evaluations.tar.bz2 https://zenodo.org/records/15306169/files/evaluations.tar.bz2?download=1
tar -C data/00-input/evaluations/ -xaf data/00-input/evaluations.tar.bz2
rm data/00-input/evaluations.tar.bz2

# Prepare empty directories for GT
mkdir -p data/00-input/gt/rumsey data/00-input/gt/ign data/00-input/gt/twh
echo "WARNING: GT for test set is not public (yet), you need to save it manually under 'data/00-input/gt/test.json' and run '00-prepare-gt.ipynb'."
```

The **ground truth** for the test sets is **not available publicly**, so **you need to copy the secret files at the right place** under `data/00-input/gt/test.json`.
The notebook `00-prepare-gt.ipynb` will then split ground truth downloaded from the RRC platform in a separate file for each subset:
- `data/00-input/gt/rumsey/test.json` for the "rumsey" dataset
- `data/00-input/gt/ign/test.json` for the "ign" dataset (French land registers)
- `data/00-input/gt/twh/test.json` for the "twh" dataset (Taiwanese maps)

Without the test ground truth, you can still run the notebook `10-results-plots-tables.ipynb` to regenerate the ranking tables displayed in the report.

## Code
The code is tested with Python v3.10.
Python files are organized either under `maptext-analysis/` for utility Python code ("library" code), or as notebooks at the root of this repository.

Paths to default locations are stored under `maptext-analysis/paths.py`

To use this code, you should first make sure you have [uv](https://github.com/astral-sh/uv) installed, then you should install and activate the virtual environment with:
```sh
uv sync
```

You can then use `uv run ...` to run some code, or open your favorite notebook editor and point it to the right virtual environment (`.venv`).

Brief description of the notebooks:
- `00-prepare-gt.ipynb`: takes the secret GT file for the test set and splits it for each dataset.
- `10-list-valid-submissions.ipynb`: generates the list of valid submissions for each task and subset, along with their name. The output file is `valid_submissions.csv`. You do not have to regenerate it.
- `10-results-plots-tables.ipynb`: reads evaluation files, ground truth files, and metadata file about submissions to extract the global metrics about each {subset × task × method} to produce tables and bar plots for the report. Results are output under `data/10-tables-plots/`.
- `20-qualitative-results-raw-predictions.ipynb`: produces qualitative results, i.e., visualizations of the predictions for each {subset × task × method}, in order to better understand what makes some method good or bad. Results are output under `data/20-raw-predictions/`.
- `30-qualitative-results-evaluation.ipynb`: (WIP) produces qualitative results, including visualizations of the evaluation results for each {subset × task × method}, in order to better understand what makes some method good or bad. Results are output under `data/30-evaluated-predictions/`.
