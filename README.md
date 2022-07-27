# CS433-Machine Learning

This repo includes the group project I worked on for the CS433: Machine Learning course at EPFL during Fall 2021 semester.

It consists of scripts and notebooks to preprocess and analyze MSF eCARE patient dataset.

To run the scripts properly one should have `Python 3.8.12` and install the libraries in [requirements.txt](./requirements.txt). 

Each directory has its own `README.md` file explaning what scripts and notebooks do and how to use them.

Unfortunately we cannot share the dataset comprising of patient records due to privacy reasons.

### Directories
  - **[clustering](./clustering/):** This directory contains the code for preparing the dataset for clustering and performing the clustering algorithms.
  - **[predictiveAnalysis](./predictiveAnalysis/):** This folder consists of scripts and notebooks to preprocess the dataset for supervised training to predict diagnoses and codes implementing the recursive feature elimination analysis.
  - **[dataExploration](./dataExploration/):** This folder has the notebooks used for preliminary data analysis.
  - **[utils](./utils/):** This folder has only one script file which maps health facility codes to city names and geographic coordinates.
