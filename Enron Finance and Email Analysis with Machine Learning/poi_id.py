#!/usr/bin/python

import sys
from copy import copy

import pickle
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

sys.path.append("tools")
from feature_format import featureFormat, targetFeatureSplit
import new_features
from scatplot import scatplot
from tester import dump_classifier_and_data


### Task 1: Select features
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
### 
### Financial features: all units are in US dollars
poi_label = ['poi']
financial_features = ['salary',
                      'deferral_payments',
                      'total_payments',
                      'loan_advances',
                      'bonus',
                      'restricted_stock_deferred',
                      'deferred_income',
                      'total_stock_value',
                      'expenses',
                      'exercised_stock_options',
                      'other',
                      'long_term_incentive',
                      'restricted_stock',
                      'director_fees',
                      'total_comp'] #created from 'new_features' function
### Units are generally number of emails messages;
### notable exception is ‘email_address’, which is a text string
email_features = ['to_messages',
                  'from_poi_to_this_person',
                  'from_messages',
                  'from_this_person_to_poi',
                  'shared_receipt_with_poi',
                  'fraction_to_poi'] #created from 'new_features' function
features_list = poi_label + financial_features + email_features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)
#scatplot(data_dict, 'salary', 'bonus')

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = copy(data_dict)
my_dataset = new_features.add_poi_email_fraction(my_dataset)
my_dataset = new_features.total_comp(my_dataset)


### This section identifies the top 8 features in features_list and disregards
### all other features.  The classifier will proceed using the reduced
### features list below.
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)
dtc_clf = tree.DecisionTreeClassifier()
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)
dtc_clf.fit(features_train, labels_train)
pred = dtc_clf.predict(features_test)
features_list_post_DTC = ['poi']
try:
    importances = dtc_clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print 'Feature Ranking: '
    for i in range(8):
        print "{} feature Number {} ({}) Feature: {}".format(
        i+1, 
        indices[i],
        importances[indices[i]],
        features_list[indices[i]] )
        if features_list != 'poi':
            features_list_post_DTC.append(features_list[indices[i]])
except AttributeError:
    print "*** Not DecisionTreeClassifier"

print "New Features List: ", features_list_post_DTC


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list_post_DTC, sort_keys=True)
labels, features = targetFeatureSplit(data)


### Task 4: Try a varity of classifiers
clf_gaussian = GaussianNB()
clf_kmeans = KMeans(n_clusters=2)
clf_svc = SVC(kernel='rbf', C=100)

clf = clf_kmeans

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

accuracy = []
precision = []
recall = []
for n in range(1000):
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    accuracy.append(accuracy_score(labels_test, pred))
    precision.append(precision_score(labels_test, pred))
    recall.append(recall_score(labels_test, pred))


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

print "Accuracy score: ", mean(accuracy)
print "Precision: ", mean(precision)
print "Recall: ", mean(recall)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)