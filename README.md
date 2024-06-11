# Analysis of ICDAR24 MapText results
Collections of tools to produce tables, graphs and figures for the report, from submissions, evaluations and dataset.


## Prepare local data
We need to gather:
- images for the test sets ("rumsey" and "ign" datasets)
- submissions from participants
- evaluation results
- ground truth for test sets ("rumsey" and "ign" datasets)

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
wget -O data/00-input/images/test-ign.zip https://zenodo.org/records/10732281/files/test.zip?download=1
unzip data/00-input/images/test-ign.zip -d data/00-input/images/
rm data/00-input/images/test-ign.zip

# Download and prepare participants' submissions (both datasets)
mkdir -p data/00-input/submissions/
wget -O data/00-input/maptext24-submissions.tar.bz2 https://zenodo.org/records/11518609/files/submissions.tar.bz2?download=1
tar -C data/00-input/submissions -xaf data/00-input/maptext24-submissions.tar.bz2
rm data/00-input/maptext24-submissions.tar.bz2
wget -O data/00-input/submissions.csv https://zenodo.org/records/11518609/files/submissions.csv?download=1


# Download and prepare evaluation results (both datasets)
mkdir -p data/00-input/evaluations/
wget -O data/00-input/evaluations.tar.bz2 https://zenodo.org/records/11549943/files/evaluations.tar.bz2?download=1
tar -C data/00-input/evaluations/ -xaf data/00-input/evaluations.tar.bz2
rm data/00-input/evaluations.tar.bz2

# Prepare empty directories for GT
mkdir -p data/00-input/gt/rumsey data/00-input/gt/ign
echo "WARNING: GT for test set is not public (yet), you need to save it manually under 'data/00-input/gt/test.json' and run '00-prepare-gt.ipynb'."
```

The **ground truth** for the test sets is **not available publicly**, so **you need to copy the secret files at the right place** under `data/00-input/gt/test.json`.
The notebook `00-prepare-gt.ipynb` will then split ground truth downloaded from the RRC platform in a separate file for each subset:
- `data/00-input/gt/rumsey/test.json` for the "rumsey" dataset
- `data/00-input/gt/ign/test.json` for the "ign" dataset (French land registers)

Without the test ground truth, you can still run the notebook `10-results-plots-tables.ipynb` to regenerate the ranking tables displayed in the report.

## Code
The code is tested with Python v3.10.
It is stored either under `maptext24-analysis/` for utility Python code ("library" code), or as notebooks at the root of this repository.

Paths to default locations are stored under `maptext24-analysis/paths.py`

To use this code, you should first make sure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed, then you should install and activate the virtual environment:
```sh
pipenv install --dev
pipenv shell  # optional if using vscode which will assist you in picking this environment 
```

Brief description of the notebooks:
- `00-prepare-gt.ipynb`: takes the secret GT file for the test set and splits it for each dataset.
- `10-list-valid-submissions.ipynb`: generates the list of valid submissions for each task and subset, along with their name. The output file is `valid_submissions.csv`. You do not have to regenerate it.
- `10-results-plots-tables.ipynb`: reads evaluation files, ground truth files, and metadata file about submissions to extract the global metrics about each {subset × task × method} to produce tables and bar plots for the report. Results are output under `data/10-tables-plots/`.
- `20-qualitative-results-raw-predictions.ipynb`: produces qualitative results, i.e., visualizations of the predictions for each {subset × task × method}, in order to better understand what makes some method good or bad. Results are output under `data/20-raw-predictions/`.
- `30-qualitative-results-evaluation.ipynb`: (WIP) produces qualitative results, including visualizations of the evaluation results for each {subset × task × method}, in order to better understand what makes some method good or bad. Results are output under `data/30-evaluated-predictions/`.
