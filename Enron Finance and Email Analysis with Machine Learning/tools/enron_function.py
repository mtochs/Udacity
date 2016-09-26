#!/usr/bin/python

from pprint import pprint
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


from feature_format import featureFormat, targetFeatureSplit

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


"""
   Function utilizes SelectKBest to identify top features for a given data set.
"""
def getKey(item):
    return item[1]

from sklearn.feature_selection import SelectKBest
def skb(data_dict, features_list, k):
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)
    clf = SelectKBest(k=k)
    clf.fit(features, labels)
    scores = clf.scores_
    f = zip(features_list[1:], scores)
    f = list(sorted(f, key=getKey, reverse=True))
    print "\n\nFeatures sorted by highest SelectKBase score:"
    for n in range(k):
        print "#{} {} with score {}".format(n+1, f[n][0], f[n][1])
    return dict(f[:k]).keys()



"""
   Function finds all NaN's of a feature list within a data set
"""
def find_nans(data_dict, f):
    total_nans = {}
    for key in f[1:]:
        i = 0
        for name in data_dict:
            if data_dict[name][key] == 'NaN':
                i = i + 1
        total_nans[key] = i
    return total_nans





"""
Function runs through mutliple classifying iterations to get a better reading
on accuracy, precision, and recall.
"""

def clf_stats(clf, features, labels):
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    accuracy = accuracy_score(labels_test, pred)
    precision = precision_score(labels_test, pred)
    recall = recall_score(labels_test, pred)
    return accuracy, precision, recall


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
"""