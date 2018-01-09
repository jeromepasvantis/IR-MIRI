import sys
from pymongo import MongoClient
from bson.code import Code

conn = MongoClient()
db = conn.groceries

def countPerItem():
	mapper = Code("""
	function() {
	    for (var i = 0; i < this.items.length; i++) {
	        emit(this.items[i],1);
	        }
	    }
	              """)

	reducer = Code("""
	function(key,values) {
	    var total = 0;
	    for (var i = 0; i < values.length; i++) {
	        total += values[i];
	        }
	        return total;
	    }
	               """)  

	r = db.basket.map_reduce(mapper, reducer, "counts")

def countCombinations():
	mapper = Code(""" 
		function () {
			for (var i = 0; i < this.items.length; i++) { 
				for (var j = i+1; j < this.items.length; j++) {
					emit([this.items[i], this.items[j]].sort().join(), 1);
				}
			}
		}""");

	reducer = Code("""
	function(key,values) {
	    var total = 0;
	    for (var i = 0; i < values.length; i++) {
	        total += values[i];
	        }
	        return total;
	    }
	               """) 

	r = db.basket.map_reduce(mapper, reducer, "countsComb")

def main(argv=None):
	countPerItem()
	countCombinations()

if __name__ == "__main__":
	sys.exit(main())