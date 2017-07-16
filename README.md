![project logo](https://github.com/flashxyz/DNA_sequencing_learning/blob/master/img/1.png)
# DNA sequencing learning
[![Trello](https://github.com/flashxyz/DNA_sequencing_learning/blob/master/img/trello.png)](https://trello.com/b/2tHwzFtL/-)

## Getting Started

This is a project about Machine Learning of NGS DNA samples from breast cancer patients using FREEC.
Right now we are in Prototype stage, and just learning our tools before using the real data, so in this current code will mimic the real data and use PCA, Logistic Regression and Random Projection using sklearn library with python.

## Directories
- /DataSavedInCSV - CSV files that were generated from hospital results.
- /DeepLearning - contains all the code that use Machine Learning for trying characterize tumor sample.
- /Script To Hospital - contain the script we built to extract the data from DNA files at Hospital. 
- /VectorToHistograms - convert SAMPLE file that was extracted from BAM file with FREEC to Histogram.
- /custom FREEC 10.3 src - contain our custom FREEC for extracting the expected results from Hospital in minimum time.
- /img - contains images for the git.
- /res - contains results that presented in the report.
- main.py - The implementation of PCA, Logistic Regression and Random Projection (Prototype stage).
