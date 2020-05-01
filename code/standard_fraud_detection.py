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


banksim_df = pd.read_csv("../data/bs140513_032310.csv")

# Retrieving the class attribute from the dataframe
labels = banksim_df['fraud']

'''
Removing unwanted columns
Since zipcodeOri and zipMerchant have the same value for all the rows, these columns are redundant
'''

feature_df = banksim_df.drop(['step', 'customer', 'zipcodeOri', 'zipMerchant', 'fraud'], axis=1)


# One hot encoding the categorical variables
feature_df = pd.get_dummies(feature_df, columns=['age', 'gender', 'category', 'merchant'])

# Standardizing the features
standard_scaler = StandardScaler()
scaled_df = pd.DataFrame(standard_scaler.fit_transform(feature_df), columns = feature_df.columns)


# Performing dimensionality reduction using PCA

# Limiting the number of components such that 95% of the variance is explained
pca = PCA(0.95, svd_solver='full')
scaled_df = pca.fit_transform(scaled_df)


# Training supervised learning models using intrinsic features from the dataset
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
    #X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

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
    #X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

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
    #X_after_smote, Y_after_smote = sm.fit_resample(X_train, y_train)

    # Training the logistic regression classifier
    clf = svm.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    print(classification_report(y_test, predictions))
