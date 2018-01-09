from __future__ import division
import sys
from pymongo import MongoClient
from bson.code import Code

conn = MongoClient()
db = conn.groceries

def compute(th_sup, th_conf, printRules=False):
	totalTrans = db.basket.count()
	found = 0
	# Go through each element in collection countsComb
	combinations = db.countsComb.find()
	for c in combinations:
		#print c
		# Compute support (equal for a->b and b->a)
		support = c['value'] / totalTrans
		# If support smaller than threshold continue
		if support < th_sup: continue
		# Separate the two items and calculate confidence for both directions
		item1, item2 = c['_id'].split(',')
		# For both directions check if confidence greater than threshold, if so increase found
		countItem1 = db.counts.find_one({"_id":item1})['value']
		countItem2 = db.counts.find_one({"_id":item2})['value']
		confidence1 = c['value'] / countItem1
		confidence2 = c['value'] / countItem2
		if confidence1 >= th_conf:
			found += 1
			if printRules: print "{0} --> {1}".format(item1, item2)
		if confidence2 >= th_conf: 
			found += 1
			if printRules: print "{1} --> {0}".format(item1, item2)

	return found

def main(argv=None):
	support = [0.01, 0.01, 0.01, 0.01, 0.05, 0.07, 0.20, 0.5]
	confidence = [0.01, 0.25, 0.5, 0.75, 0.25, 0.25, 0.25, 0.25]
	found = list([])
	#Task 1: print table
	print "TASK 1"
	print "-"*30
	for i in range(len(support)):
		found.append(compute(support[i], confidence[i], False))
		print "{0} \t {1} \t {2}".format(support[i], confidence[i], found[i])

	#Task 2: print rules
	print "TASK 2"
	print "-"*30
	print "Association Rules for Row 4: "
	compute(support[3], confidence[3], True)
	print "Association Rules for Row 5: "
	compute(support[4], confidence[4], True)
	print "Association Rules for Row 6: "
	compute(support[5], confidence[5], True)

if __name__ == "__main__":
	sys.exit(main())