# Predictive Analysis
This directory contains scripts notebooks for predictive analysis of the dataset. Scripts implement the same codes and functions provided in the notebooks but allow running from terminal with arguments (except for cross-validation).

### Directory Files
  - **[ProcessDataPrediction.ipynb](./ProcessDataPrediction.ipynb):** This notebook prepares the dataset for predictive analysis. See the entry below for `processDataPrediction.py` for more information about preprocessing. 
  - **[PatientPrediction.ipynb](./PatientPrediction.ipynb):** This notebook implements linear regression algorithms and recursive feature elimination. See the entry below for `patientPrediction.py` for more information about predictive analysis. The notebook also includes a section for cross-validation, which is not included in `patientPrediction.py`.
  - **[processDataPrediction.py](./processDataPrediction.py):** This script prepares the dataset for predictive analysis. It encodes categorical features with One-Hot encoding, imputes and normalizes numerical values, maps health facility numbers to cities and longitude&latitude information using [get_locations.py](../utils/get_locations.py), parses temporal information, and copies diagnoses labels. Then it concatanates of these features and construct a new dataset. Furthermore, it dumps `metadata_patient_pred.json` containing information about the generated dataset (i.e. column names, normalization statistics, etc.)

    Usage
    ``` shell
    python processDataClustering.py --data_path DATA_CSV --save_path SAVE_DIRECTORY
    ```

      Arguments:
    * `--data_path`: Path to dataset file (should be .csv)
    * `--save_path`: Path for storing processed dataset. If no path is provided, file will be dumped the directory of the input dataset.
    

  - **[patientPrediction.py](./patientPrediction.py):** This script trains a linear classifier per diagnosis. It first loads the dataset and the corresponding metadata file. Then it fits the data to binary classifiers to predict diagnosis of healthcare workers and prints accuracy and F1-scores of the trained models. Then, it executes recursive feature elimination method to find most important features and prints out a comparion of F1-scores of both the full model and the pruned model.

  Usage
  ``` shell
  python processDataClustering.py --data_path DATA_CSV  --n_features 4 --step 10 --verbose 1
  ```

  Arguments:
  * `--data_path`: Path to dataset file (should be .csv)
  * `--n_features`: The number of features to select.'
  * `--step`: Number of features to eliminate at every iteration.
  * `--verbose`: Verbosity level.


To test scripts, just type (after changing paths for the dataset)
  ``` shell
  sh predAnalysis.sh
  ```
