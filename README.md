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
wget -O data/00-input/maptext24-submissions.tar.bz2 https://weinman.cs.grinnell.edu/tmp/maptext24-submissions.tar.bz2
tar -C data/00-input/ -xaf data/00-input/maptext24-submissions.tar.bz2
rm data/00-input/maptext24-submissions.tar.bz2

# Download and prepare evaluation results (both datasets)
wget -O data/00-input/maptext24-results.tar.xz https://weinman.cs.grinnell.edu/tmp/maptext24-results.tar.xz
tar -C data/00-input/ -xaf data/00-input/maptext24-results.tar.xz
rm data/00-input/maptext24-results.tar.xz

# Prepare empty directories for GT
mkdir -p data/00-input/gt/rumsey data/00-input/gt/ign
```

The **ground truth** for the test sets is **not available publicly**, so **you need to copy the secret files at the right places**:
- `data/00-input/gt/rumsey/test.json` for the "rumsey" dataset
- `data/00-input/gt/ign/test.json` for the "ign" dataset
The notebook `00-prepare-gt.ipynb` can be used to split ground truth for each subset.


## Code
Code is stored either under `maptext24-analysis/` for utility Python code ("library" code), or as notebooks at the root of this repository.

Paths to default locations are stored under `maptext24-analysis/paths.py`

To use this code, you should first make sure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed, then you should install and activate the virtual environment:
```sh
pipenv install --dev
pipenv shell  # optionnal if using vscode which will assist you in picking this environment 
```

The code uses Python v3.10.
