#!/usr/bin/python

""" 
Simple function that displays a scatter plot with two feature inputs
from data_dict
"""


import numpy as np
from feature_format import featureFormat, targetFeatureSplit

def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """
    fraction = 0.
    if poi_messages != "NaN" or all_messages != "NaN":
        fraction = float(poi_messages)/float(all_messages)

    return fraction


def add_poi_email_fraction(data):
    for name in data:
        data_point = data[name]
        from_poi_to_this_person = data_point["from_poi_to_this_person"]
        to_messages = data_point["to_messages"]
        fraction_from_poi = computeFraction(from_poi_to_this_person, to_messages)
        #print fraction_from_poi
        data_point["fraction_from_poi"] = fraction_from_poi


        from_this_person_to_poi = data_point["from_this_person_to_poi"]
        from_messages = data_point["from_messages"]
        fraction_to_poi = computeFraction(from_this_person_to_poi, from_messages)
        #print fraction_to_poi
        data[name]["fraction_to_poi"] = fraction_to_poi
    return data


def total_comp(data):
    for name in data:
        financials = ['salary', 'bonus', 'total_stock_value', 'exercised_stock_options']
        dollars = 0
        for f in financials:
            try:
                dollars = dollars + int(data[name][f])
            except:
                continue
        data[name]['total_comp'] = dollars
    return data
