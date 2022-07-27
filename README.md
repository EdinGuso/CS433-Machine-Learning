# CS433-2021-eCARE2
This repository has been created by Abdulkadir Gokce, Edin Guso and Güneş Başak Özgün for CS433 Project 2.

It consists of scripts and notebooks to preprocess and analyze MSF eCARE patient dataset.

To run the scripts properly one should have `Python 3.8.12` and install the libraries in [requirements.txt](./requirements.txt). 

Each directory has its own `README.md` file explaning what scripts and notebooks do and how to use them.

Unfortunately we cannot share the dataset comprising of patient records due to privacy reasons.

### Directories
  - **[clustering](./clustering/):** This directory contains the code for preparing the dataset for clustering and performing the clustering algorithms.
  - **[predictiveAnalysis](./predictiveAnalysis/):** This folder consists of scripts and notebooks to preprocess the dataset for supervised training to predict diagnoses and codes implementing the recursive feature elimination analysis.
  - **[dataExploration](./dataExploration/):** This folder has the notebooks used for preliminary data analysis.
  - **[utils](./utils/):** This folder has only one script file which maps health facility codes to city names and geographic coordinates.
