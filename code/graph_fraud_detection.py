import numpy as np
import pandas as pd
from py2neo import Graph
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import KFold, train_test_split, StratifiedKFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.decomposition import PCA

# Functions to fetch network-based features
def load_degree(record):
    return records[record.split("'")[1]]['degree']

def load_community(record):
    return str(records[record.split("'")[1]]['community'])

def load_pagerank(record):
    return records[record.split("'")[1]]['pagerank']

banksim_df = pd.read_csv("../data/bs140513_032310.csv")

# Retrieving the class attribute from the dataframe
labels = banksim_df['fraud']


# Connecting to the Neo4j database
graph = Graph(password="root")

# Query to fetch the network features from Neo4j
query = """
MATCH (p:Placeholder)
RETURN p.id AS id, p.degree AS degree, p.pagerank as pagerank, p.community AS community
"""

data = graph.run(query)

records = {}

for record in data:
    records[record['id']] = {'degree': record['degree'], 'pagerank': record['pagerank'], 'community': record['community']}

# Merging the graph features with the banksim dataset
banksim_df['merchant_degree'] = banksim_df['merchant'].apply(load_degree)
banksim_df['customer_degree'] = banksim_df['customer'].apply(load_degree)
banksim_df['merchant_pagerank'] = banksim_df['merchant'].apply(load_pagerank)
banksim_df['customer_pagerank'] = banksim_df['customer'].apply(load_pagerank)
banksim_df['merchant_community'] = banksim_df['merchant'].apply(load_community)
banksim_df['customer_community'] = banksim_df['customer'].apply(load_community)

labels = banksim_df['fraud']

# Dropping the unnecessary columns including the age and gender attributes
feature_df = banksim_df.drop(['step', 'age', 'gender', 'customer', 'zipcodeOri', 'zipMerchant', 'fraud'], axis=1)

# One hot encoding the categorical variables
feature_df = pd.get_dummies(feature_df, columns=['category', 'merchant', 'merchant_community', 'customer_community'])

# Standardizing the features
standard_scaler = StandardScaler()
scaled_df = pd.DataFrame(standard_scaler.fit_transform(feature_df), columns = feature_df.columns)

scaled_df = scaled_df.values
labels = labels.values


# Training supervised learning models using intrinsic and network-based features

k_fold = StratifiedKFold(n_splits=5, shuffle=False)

# Initialising the three supervised learning models
random_forest = RandomForestClassifier(max_depth=20, n_estimators=150)
svm = SVC(gamma="auto")
logistic_regression = LogisticRegression(solver='lbfgs', max_iter=5000)


# Logistic Regression Classifier
print("\n\nBuilding Logistic Regression classifier with k=5 folds")
for train_index, test_index in k_fold.split(scaled_df, labels):

    X_train, X_test = scaled_df[train_index], scaled_df[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    # Handling the imbalance in the dataset using SMOTE
    sm = SMOTE()
    X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

    # Training the logistic regression classifier
    clf = logistic_regression.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    print(classification_report(y_test, predictions))

print("\n\nBuilding Random Forest classifier with k=5 folds")
for train_index, test_index in k_fold.split(scaled_df, labels):

    X_train, X_test = scaled_df[train_index], scaled_df[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    # Handling the imbalance in the dataset using SMOTE
    sm = SMOTE()
    X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

    # Training the logistic regression classifier
    clf = random_forest.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    print(classification_report(y_test, predictions))

print("\n\nBuilding SVM classifier with k=5 folds")
for train_index, test_index in k_fold.split(scaled_df, labels):

    X_train, X_test = scaled_df[train_index], scaled_df[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    # Handling the imbalance in the dataset using SMOTE
    sm = SMOTE()
    X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

    # Training the logistic regression classifier
    clf = svm.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    print(classification_report(y_test, predictions))
