# Fraud  Detection  With  Graph  Databases  and  Machine  Learning

This course has been implemented as part of the CSE 573 (Semantic Web Mining) course at Arizona State University for the Spring 2020 semester. In this project, we aim to detect fraudulent behavior in bank transactions using graph databases and machine learning models.
The dataset used for this project is the BankSim dataset which is a simulated dataset created using a sample of transactional data provided by a bank in Spain (https://www.kaggle.com/ntnu-testimon/banksim1).

## Folder Structure 
    .
    ├── data                    # BankSim data files
    ├── code                    # Source files (Python scripts and notebooks)
    ├── app                     # UI files
    └── README.md

## Source Files

- code/standard_fraud_detection.py : This script contains the code to build fraud detection models using intrinsic features obtained from the BankSim dataset.
- code/graph_fraud_detection.py: This script contains the code to build fraud detection models using both intrinsic features and graph-based features pertaining to the BankSim dataset.
- code/graphdb_creation.cyp: This file contains the necessary Neo4j queries to create a graph model using the BankSim dataset and work with the data.
- code/fraud_detection.ipynb : This Jupyter notebook contains the code from both standard_fraud_detection.py and graph_fraud_detection.py in a more interactive format.
- app/swm.html : This HTML document contains the code pertaining to the customer profile dashboard.
- app/index.js : This JS file contains the essential JavaScript code required for the dashboard.

## Instructions to run the code

All the instructions mentioned below must be run from a terminal session.


To build and test the performance of classifiers using just intrinsic features from the dataset, the following command can be used to run the standard_fraud_detection.py script:

```
python -W ignore standard_fraud_detection.py
```

Inorder to make use of graph-based features, a graph model must first be constructed in Neo4j. The necessary code to build the same is available in the graphdb_creation.cyp file.


To build and test the performance of classifiers using both intrinsic and graph-based features from the dataset, the following command can be used to run the graph_fraud_detection.py script:

```
python -W ignore graph_fraud_detection.py
```

To launch the Customer Profile dashboard, a server must be launched in the local system with the following command:
```
python -m SimpleHTTPServer 8000
```
The dashboard can then be accessed on the browser using this URL - http://localhost:8000/


## Python libraries used
- NumPy - v1.18.1
- Pandas - v0.25.3
- scikit-learn - v0.22.2.post1
- Py2neo - v4.3.0
- imblearn - 0.6.2
