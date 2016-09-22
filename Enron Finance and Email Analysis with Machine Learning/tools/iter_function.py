#!/usr/bin/python

import numpy as np

from pprint import pprint
import numpy as np
from sklearn import preprocessing
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from feature_format import featureFormat, targetFeatureSplit

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


"""
Function utilizes Decision Tree Classifier to identify top features for a
given data set.
"""
def top_features(my_dataset, features_list, iterations=1000, features_qty=8):
    data = featureFormat(my_dataset, features_list, sort_keys=True)
    labels, features = targetFeatureSplit(data)
    dtc_clf = tree.DecisionTreeClassifier()
    features_list_post_DTC = ['poi']
    
    features_list_tally = {'poi' : []}
    for k in features_list[1:]:
        features_list_tally[k] = []
    
    for n in range(iterations):
        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size=0.3, random_state=42)
        dtc_clf.fit(features_train, labels_train)
        #pred = dtc_clf.predict(features_test)
        importances = dtc_clf.feature_importances_
        indices = np.argsort(importances)[::-1]
        for i in range(len(indices)):
            key = features_list[indices[i]]
            val = importances[indices[i]]
            features_list_tally[key].append(val)
    
    features_list_tally.pop('poi', 0)
    for k in features_list[1:]:
        features_list_tally[k] = mean(features_list_tally[k])
    features_list_tally = sorted(features_list_tally, key=features_list_tally.__getitem__)
    for n in range(features_qty):
        features_list_post_DTC.append(features_list_tally[n])
    
    return features_list_post_DTC
    

"""
Function runs through mutliple classifying iterations to get a better reading
on accuracy, precision, and recall.
"""
def clf_stats(clf, features, labels, iterations=1000):
    accuracy = []
    precision = []
    recall = []
    for n in range(iterations):
        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size=0.3, random_state=42)
        clf.fit(features_train, labels_train)
        pred = clf.predict(features_test)
        accuracy.append(accuracy_score(labels_test, pred))
        precision.append(precision_score(labels_test, pred))
        recall.append(recall_score(labels_test, pred))
    
    return mean(accuracy), mean(precision), mean(recall)