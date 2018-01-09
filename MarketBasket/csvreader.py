import sys
from os import path
from codecs import encode, decode
from pymongo import MongoClient


conn = MongoClient()
db = conn.groceries


def readCsv(fd):
	singleItems = list([])

	with open(fd, "r") as file:
	    for transaction in file:
	        items = []    
	        for item in transaction.strip().split(','):
	        	item = decode(item.strip(),'latin2','ignore')
	        	items.append(item)
	        	if item not in singleItems: singleItems.append(item)
	        t = {}
	        t['items'] = items
	        db.basket.insert(t)

	s = {}
	s['items'] = singleItems
	db.items.insert(s)


def main(argv=None):
	if argv:
		fd = argv[1]
	else:
		fd = "groceries.csv"
	readCsv(fd)

if __name__ == "__main__":
	sys.exit(main())