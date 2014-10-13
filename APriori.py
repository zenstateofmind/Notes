# 1) read a line


import sys
import re

class APriori(object):

	def __init__(self):
		self.itemCount = {}
		self.filename = ''
		self.threshold = 0
		self.frequentItemTable = []
		self.triangularMatrix = []
		self.m = 0
		self.frequentPairs = {}
		self.triples = {}
		self.frequentOnes = {}
		self.frequentTriples = {}
		self.transactions = 0
		self.frequentItemSet = []

	def readFile(self, currPass):
		file = open(self.filename)
		currTransactions = 0 
		for basket in file:
			if currTransactions < self.transactions:
				stringBasket = basket.strip().split()
				intBasket = [int(x) for x in stringBasket]
				if currPass == 1:
					self.firstPassProcessing(intBasket)
				elif currPass == 2 :
					self.secondPassProcessing(intBasket)
				else:
					self.thirdPassProcessing(intBasket)
			else:
				break;
			currTransactions = currTransactions + 1
		file.close()

	def defaultTransactions(self):
		file = open(self.filename)
		for line in file:
			self.transactions = self.transactions + 1
		file.close()

	def firstPass(self) :
		self.readFile(1)
		self.frequentOnes = {items:frequency for (items, frequency) in self.itemCount.iteritems() if frequency > self.threshold}
		self.frequentItemSet = self.frequentItemSet + [items for (items, frequency) in self.itemCount.iteritems() if frequency > self.threshold]
		print "Frequent 1sets: ", self.frequentOnes



	def secondPass(self):
		self.triangularMatrix = map(lambda item : [0 for x in range(0, item+1)], range(0, max(self.frequentItemTable)+1))
		self.readFile(2)
		for row in range(0, len(self.triangularMatrix)):
			for column in range(0, len(self.triangularMatrix[row])):
				if self.triangularMatrix[row][column] > self.threshold:
					self.frequentPairs[(self.frequentItemTable.index(row), self.frequentItemTable.index(column))] = self.triangularMatrix[row][column]
					self.frequentItemSet.append((self.frequentItemTable.index(row), self.frequentItemTable.index(column)))
		print 'Frequent 2sets: ', self.frequentPairs

	def thirdPass(self):
		self.readFile(3)	
		self.frequentTriples = {items:frequency for (items, frequency) in self.triples.iteritems() if frequency > self.threshold}
		self.frequentItemSet = self.frequentItemSet + [items for (items, frequency) in self.triples.iteritems() if frequency > self.threshold]
		print 'Frequent 3sets: ', self.frequentTriples


	def firstPassProcessing(self, basket):
		for item in set(basket):
			self.itemCount[item] = self.itemCount.get(item, 0) + 1


	def betweenThePasses(self):
		# This function creates initializes a list whose size is as big as the itemCount keyset with all elements being 0
		self.frequentItemTable = map(lambda x: x * 0, range(0, len(self.itemCount.keys())))
		for item, frequency in self.itemCount.iteritems():
			if frequency >= self.threshold :
				self.frequentItemTable[item] = self.m
				self.m = self.m+1
			else:	
				self.frequentItemTable[item] = -1
		self.m = self.m - 1 #this is because right after you add m to the array the final time, you increment it

	def secondPassProcessing(self, basket):
		freqItems = filter(lambda x : self.frequentItemTable[x] != -1, basket)
		freqItemPairs = [(x, y) for x in freqItems for y in freqItems if freqItems.index(y) > freqItems.index(x)]
		for (item1, item2) in freqItemPairs:
			currentItem = (item1, item2) if item1 > item2 else (item2, item1)
			indexForTMatrix1 = self.frequentItemTable[currentItem[0]]
			indexForTMatrix2 = self.frequentItemTable[currentItem[1]]
			# print ' index1 : ', indexForTMatrix1
			# print  'index2: ', indexForTMatrix2
			self.triangularMatrix[indexForTMatrix1][indexForTMatrix2] =  self.triangularMatrix[indexForTMatrix1][indexForTMatrix2] + 1

	def thirdPassProcessing(self, basket):
		freqItems = filter(lambda x : self.frequentItemTable[x] != -1, basket)
		frequentTriples = [(x, y, z) for x in freqItems for y in freqItems for z in freqItems if freqItems.index(y) > freqItems.index(x) and freqItems.index(z) > freqItems.index(y)]
		for (item1, item2, item3) in frequentTriples:
			currentItemsSet = (item1, item2, item3)
			currentItemList = list(currentItemsSet)
			item1 = max(currentItemList)
			currentItemList.remove(item1)
			item2 = max(currentItemList)
			currentItemList.remove(item2)
			item3 = max(currentItemList)
			currentItemList.remove(item3)
			currentItemsSet = (item1, item2, item3)
			self.triples[currentItemsSet] = self.triples.get(currentItemsSet, 0) + 1

	def main(self, name, filename = 'retail.dat',  threshold=.02, transactions = 0):
		self.filename = filename
		self.transactions = int(transactions)
		if self.transactions == 0:
			self.defaultTransactions()
			
		self.threshold = int(float(threshold) * self.transactions)
		self.firstPass()
		self.betweenThePasses()
		self.secondPass()
		self.thirdPass()
		print 'Item Set: ', self.frequentItemSet


if __name__ == '__main__':
	APriori = APriori()
	APriori.main(*sys.argv)
