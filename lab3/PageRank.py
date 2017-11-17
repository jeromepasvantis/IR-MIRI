#!/usr/bin/python

from collections import namedtuple
import time
import sys
import numpy as np

class Edge:
    def __init__ (self, origin=None, destination=None):
        self.origin = origin 
        self.destination = destination
        self.weight = 1 

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.destination, self.weight)

    def increaseWeight(self):
        self.weight = self.weight + 1
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0
        self.pageIndex = 0 # I don't know....
        self.listPosition = 0

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)
        #return "{0}\t{1}\t{2}".format(self.code, self.name, self.outweight)

    def __cmp__(self, other):
        if self.pageIndex < other.pageIndex:
            return -1
        elif self.pageIndex > other.pageIndex:
            return 1
        else:
            return 0

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match (key: IATA1 concat IATA2)
edgeHash2 = dict() # hash key: origin -> List of incoming edges
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.listPosition=cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r");
    countDifferent = 0
    countTotal = 0
    for line in routesTxt.readlines():
        try:
            countTotal += 1
            temp = line.split(',')
            if (len(temp[2]) != 3 and len(temp[4]) != 3) :
                raise Exception('not an IATA code')
            # Extract i and j
            origin = temp[2]
            destination = temp[4]
            # Increase Out(i)
            airportHash[origin].outweight += 1
            # Check if Route already in Edges
            if origin+destination in edgeHash:
                # Just increase the weight
                edgeHash[origin+destination].increaseWeight()
            else:
                # Add new edge
                countDifferent += 1
                e = Edge(origin, destination)
                edgeList.append(e)
                edgeHash[origin+destination] = e
                # Maintain second dict
                if destination in edgeHash2:
                    edgeHash2[destination].append(e)
                else:
                    edgeHash2[destination] = [e]
        except Exception as inst:
            pass
    routesTxt.close()
    print "There were {0} different routes out of {1} in total".format(countDifferent, countTotal)

def computeDifference(A, B):
    A = np.array(A)
    B = np.array(B)
    return np.sqrt(((A - B) ** 2).mean())

def computePageRanks():
    n = len(airportList)
    P = [1.0/n for i in xrange(n)]
    L = 0.85
    diff = 1000000
    th = 1.0e-06
    iterations = 0
    
    while (diff > th):
        Q = [0 for i in xrange(n)]

        for i in airportList:
            #compute sum
            s=0
            
            if i.code in edgeHash2:
                for e in edgeHash2[i.code]:
                    s += (P[airportHash[e.origin].listPosition] * e.weight) / airportHash[e.origin].outweight
                    Q[i.listPosition] = L * s + (1.0-L)/n  
            else:
                #Deal with edges without outgoing nodes
                Q[i.listPosition] = 1.0/n

        diff = computeDifference(P,Q)
        #Check if sum = 1
        #print sum(i for i in P)
        P = Q
        iterations += 1    
    for i in airportList:
        i.pageIndex = P[i.listPosition]
    return iterations

def outputPageRanks(n=10):
    ranking = sorted(airportList, reverse=True)
    print ranking[0:n]
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks(10)
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1

if __name__ == "__main__":
    sys.exit(main())
