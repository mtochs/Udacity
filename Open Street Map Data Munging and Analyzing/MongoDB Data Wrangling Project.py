# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 10:44:12 2016

@author: mykel
"""

OSM_FILE = "denver-boulder_colorado.osm"
JSON_FILE = "{0}.json".format(OSM_FILE)

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

# ********** Iterative Parse **********
def count_tags(filename):
	tags = {}
	for e, element in ET.iterparse(filename):
		u_tag = element.tag
		if u_tag in tags:
			tags[u_tag] = tags[u_tag] + 1
		elif u_tag not in tags:
			tags[u_tag] = 1
	return tags


# ********** Tag Types **********
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
	if element.tag == "tag":
		if lower.match(element.attrib['k']):
			keys["lower"] += 1
		elif lower_colon.match(element.attrib['k']):
			keys["lower_colon"] += 1
		elif problemchars.search(element.attrib['k']):
			keys["problemchars"] += 1
		else:
			keys["other"] += 1
		pass
		
	return keys

def process_map(filename):
	keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
	for _, element in ET.iterparse(filename):
		keys = key_type(element, keys)
	return keys


def process_users(filename):
	users = set()
	for _, element in ET.iterparse(filename):
		try:
			users.add(element.attrib['user'])
		except:
			pass

	return users

# ********** Improving Street Names **********
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# These are expected road tags
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
			"Trail", "Parkway", "Commons", "Circle", "North", "South", "East", "West", "Way",
			"Broadway", "Terrace", "Highway", "Center", "Row", "Point", "Loop", "Plaza", "Run"]

# Dictionary for fixing inconsistent road tags
mapping = {
			# Road tag inconsistencies and errors
			"Ace": "Avenue",
			"Av": "Avenue",
			"Ave": "Avenue",
			"Blvd": "Boulevard",
			"Dr": "Drive",
			"Cir": "Circle",
			"Ct": "Court",
			"Ln": "Lane",
			"Pkwy": "Parkway",
			"Pky": "Parkway",
			"Pl": "Plaza",
			"Rd": "Road",
			"St": "Street",
			# General name errors.  This fixes misspellings, 
			# single-word entries, etc.
			"68th": "68th Street",
			"88th": "88th Street",
			"Arapahoe": "Arapahoe Road",
			"Baselin": "Baseline Road",
			"Baseline": "Baseline Road",
			"Colfax": "Colfax Avenue",
			"Grant": "Grant Street",
			"Lincoln": "Lincoln Street",
			"Main": "Main Street",
			"Mainstreet": "Main Street",
			"Osage": "Osage Street",
			"Pennsylvania": "Pennsylvania Street",
			"Raod": "Road",
			"Speer": "Speer Boulevard",
			"Strret": "Street",
			"Tennyson": "Tennyson Street",
			"Walnut": "Walnut Street"
			}

# **********************
# Audit street names
def audit_street_type(street_types, street_name):
	m = street_type_re.search(street_name)
	if m:
		street_type = m.group()
		if street_type.title() not in expected and street_name.split()[-1].strip('.').title() not in mapping:
			street_types[street_type].add(street_name)

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
	osm_file = open(osmfile, "r")
	street_types = defaultdict(set)
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])
	osm_file.close()
	return street_types
# End street name audit
# **********************

# **********************
# Audit phone numbers
phone_dashed = re.compile(r'^(\d{3})-(\d{3})-(\d{4})$')

def audit_phone_number(bad_phones, phone):
	m = phone_dashed.search(phone)
	if not m:
		return bad_phones.add(phone)
	else: 
		return bad_phones
		

def is_phone(elem):
	return (elem.attrib['k'] == "phone")

def audit_phone(osmfile):
	osm_file = open(osmfile, "r")
	bad_phones = set()
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_phone(tag):
					audit_phone_number(bad_phones, tag.attrib['v'])
	osm_file.close()
	return bad_phones
# End phone number audit
# **********************



# Function standarizes street naming convention with known
# errors in data.
def update_name(name, mapping):
	words = name.title().split()
	try:
		w = words[-1].strip('.')
		words[-1] = mapping[w]
	except:
		pass
	name = " ".join(words)
	return name

#********** Preparing for Database **********

# Array used to store bad data.  Variable used for
# identifying bad entries and cleaning errors.
#bad_data = []

# Simple function to test if a variable is present 
# in XML string.
def try_or_not(element, wc):
	try:
		return element.attrib[wc]
	except:
		return None

def shape_element(element):
	node = {}
	if element.tag == "node" or element.tag == "way" :
		# Check to see if latitude exists in the string of data
		if try_or_not(element, 'lat'):
			pos = [float(element.attrib['lat']), float(element.attrib['lon'])]
		else:
			pos = None
		
		node = {
			"id": element.attrib['id'],
			"type": element.tag,
			"visible": element.get("visible"),
			"created": {
				"version": element.attrib['version'],
				"changeset": element.attrib['changeset'],
				"timestamp": element.attrib['timestamp'],
				"user": element.attrib['user'],
				"uid": element.attrib['uid']
			},
			"pos": pos
		}
		cats = ["amenity", "cuisine", "name", "phone"]
		address = {
		  "address": {
			"housenumber": None,
			"street": None
			}
		}
		#*****************************************
		# Creates nodes for 'tag' entries
		for tag in element.iter("tag"):
			k_value = tag.attrib["k"]
			v_value = tag.attrib["v"]
			
			# A colon is added to the IF statement to avoid index errors.
			# Five entries contained a redundant "address" k_value.  Thus,
			# triggering an error when using k_value.split(":")[1].  The 
			# split would not create an array if no ':' is present.
			if "addr:" in k_value:
				addr = k_value.split(":")[1]
				if addr in address["address"] and len(k_value.split(":")) == 2:
					try:
						address["address"][addr] = update_name(str(v_value), mapping)
					except UnicodeEncodeError:
						# There were only two Unicode errors in the data.
						# Thus, this 'except' fixes the 2 known ascii bugs.
						if str(v_value.encode('ascii', 'ignore'))[0:2] is "Pea":
							address["address"][addr] = "Peña Boulevard"
						else:
							address["address"][addr] = update_name(str(v_value.encode('ascii', 'ignore')), mapping)
						#bad_data.append(node)
			elif k_value in cats:
				node[k_value] = v_value

		if address["address"]["housenumber"]:
			node.update(address)
		#*****************************************
		# Creates nodes for 'way' entries
		if element.tag == "way":
			node_refs = []
			for nd in element.iter("nd"):
				if "ref" in nd.keys():
					node_refs.append(nd.get("ref"))
			if node_refs[0]:
				node["node_refs"] = node_refs
		#******************************************
		return node
	else:
		return None

#******************************************
# Function used for collecting problem data.
# Problem data writen to a .json file for 
# further inspection
#******************************************
def bad_data_to_json(element, pretty = False):
	file_out = "{0}.problems.json".format(OSM_FILE)
	with codecs.open(file_out, "w") as fo:
		for el in element:
			if pretty:
				fo.write(json.dumps(el, indent=2)+"\n")
			else:
				fo.write(json.dumps(el) + "\n")


def process_data(file_in, pretty = False):
	# You do not need to change this file
	file_out = JSON_FILE
	data = []
	with codecs.open(file_out, "w") as fo:
		for _, element in ET.iterparse(file_in):
			el = shape_element(element)
			if el:
				data.append(el)
				if pretty:
					fo.write(json.dumps(el, indent=2)+"\n")
				else:
					fo.write(json.dumps(el) + "\n")

		# ***** Bad data report *****
		# This was used during data audit process to 
		# identify problematic data.
		# 
		#if bad_data:
		#	bad_data_to_json(bad_data, True)
		# ***************************
	return data


# ********** MongoDB for Data Analysis **********
from pymongo import MongoClient
def mongo_ip():
	return MongoClient("192.168.1.15", 32774)

# Function for getting database from MongoDB docker container
def get_db(db_name = "denver"):
	client = mongo_ip()
	db = client[db_name]
	return db

def insert_data(data, db):
	db.denver.insert(data)
	pass

def make_pipeline(element = "number_of_unique_users"):
	# complete the aggregation pipeline
	if element is "number_of_unique_users":
		pipeline = [
			{ "$group" : { "_id" : "$created.uid",
							"count" : { "$sum" : 1 } } },
			{ "$sort" : { "count" : -1 } }
			]
	
	elif element is "number_of_amenities":
		pipeline = [
			{ "$match" : { "type" : "node" } },
			{ "$group" : { "_id" : "$amenity",
							"count" : { "$sum" : 1 } } },
			{ "$sort" : { "count" : -1 } }
			]
	elif element is "addresses_listed":
		pipeline = [
			{ "$group" : { "_id" : "$address.street",
							"count" : { "$sum" : 1 } } },
			{ "$sort" : { "count" : -1 } }
			]
	elif element is "names_listed":
		pipeline = [
			{ "$group" : { "_id" : "$name",
							"count" : { "$sum" : 1 } } },
			{ "$sort" : { "count" : -1 } }
			]
	
	#pprint.pprint(pipeline)
	return pipeline

def data_sources(db, pipeline):
	return [doc for doc in db.udacity.aggregate(pipeline)]




if __name__ == "__main__":
	#tags = count_tags(OSM_FILE)
	#pprint.pprint(tags)

	#keys = process_map(OSM_FILE)
	#pprint.pprint(keys)

	#users = process_users(OSM_FILE)
	#pprint.pprint(users)

	# Audit street types from OSM file data
	#st_types = audit(OSM_FILE)
	#pprint.pprint(dict(st_types))

	# Audit phone numbers from OSM file data
	#phone_types = audit_phone(OSM_FILE)
	#pprint.pprint(phone_types)

	# Convert OSM to JSON
	#data = process_data(OSM_FILE, False)
	#pprint.pprint(data)

	# Test DB connectivity
	#client = mongo_ip()
	#print client.server_info()

	# Load JSON into MongoDB
	# Ran shell command from windows machine:
	# mongoimport /host:192.168.1.15:32774 /db:denver /collection:udacity /file:denver-boulder_colorado.osm.json

	# Command initiates the data base connection
	#db = get_db()
	
	# Pipeline retrieves the query that will be sent to the data base
	#pipeline = make_pipeline("names_listed")

	# result stores the array of the data sent from MongoDB after the query
	#result = data_sources(db, pipeline)

	#pprint.pprint(len(result))
	#pprint.pprint(result[0:6])
	

"""
{u'_id': ObjectId('57b1fe24ac0813b0fbfb079a'),
 u'created': {u'changeset': u'7551724',
			u'timestamp': u'2011-03-14T04:12:27Z',
			u'uid': u'117055',
			u'user': u'GPS_dr',
			u'version': u'6'},
 u'id': u'25676629',
 u'pos': [39.9822661, -105.2638756],
 u'type': u'node',
 u'visible': None}
"""