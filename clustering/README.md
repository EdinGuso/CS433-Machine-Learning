# Clustering
This directory contains notebooks and scripts for preparation of a dataset for clustering and performing the clustering algorithms. Scripts implement the same codes and functions provided in the notebooks but allow running from terminal with arguments (except for determining the optimal number of clusters).

### Directory Files
  - **[ProcessDataClustering.ipynb](./ProcessDataClustering.ipynb):** This notebook prepares the dataset for clustering. See the entry below for `processDataClustering.py` for more information about preprocessing. 
  - **[PatientClustering.ipynb](./PatientClustering.ipynb):** This notebook implements clustering algorithms. See the entry below for `patientClustering.py` for more information about clustering. In order to determine a good number of clusters, the notebook also examines and plots the loss of K-Prototypes and AIC/BIC of GMM as a function of number of clusters, which is not included in `patientClustering.py`.
  - **[processDataClustering.py](./processDataClustering.py):** This script prepares the dataset for clustering. It groups categorical features with a predefined set of rules, imputes and normalizes numerical values, maps health facility numbers to cities and longitude&latitude information using [get_locations.py](../utils/get_locations.py), parses temporal information. Then it concatanates of these features and construct a new dataset. Furthermore, it dumps `metadata_patient.json` containing information about the generated dataset (i.e. column names, normalization statistics, etc.)

    Usage
    ``` shell
    python processDataClustering.py --data_path DATA_CSV --save_path SAVE_DIRECTORY
    ```

      Arguments:
    * `--data_path`: Path to dataset file (should be .csv)
    * `--save_path`: Path for storing processed dataset. If no path is provided, file will be dumped the directory of the input dataset.
    

  - **[patientClustering.py](./patientClustering.py):** This script perfoms clustering of the preprocessed dataset. It first loads the dataset and the corresponding metadata file. Then it fits the data to the user defined clustering algotihm and predicts the cluster assignments. Then, it creates and saves a new dataframe with cluster assignments of data samples and another dataframe with cluster representatives. Finally, it saves the clustering model to the output path as a pickle file.

  Usage
  ``` shell
  python processDataClustering.py --data_path DATA_CSV --save_path SAVE_DIRECTORY --method 0 --n_clusters 8 --n_init 5 --max_iter 10
  ```

  Arguments:
  * `--data_path`: Path to dataset file (should be .csv)
  * `--save_path`: Path for storing resuls. If no path is provided, file will be dumped the directory of the input dataset.
  * `--method`: Clustering method. Either 0 for a Gaussian Mixture Model (default, fast) or 1 for KPrototypes (slow, better cluster interpretability).
  * `--n_clusters`: Number of clusters.
  * `--n_init`: Number of initializations of the clustering algorith. The best result is kept.
  * `--max_iter`: Maximum number of iterations.

To test scripts, just type (after changing paths for the dataset)
  ``` shell
  sh clustering.sh
  ```