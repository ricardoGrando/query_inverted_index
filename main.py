#!/usr/bin/python3

import sys
from HTMLReader import *
from invertedIndex import *
import matplotlib.pyplot as plt
import numpy as np

class main:

    def __init__(self, pathDocs, pathStopwords):
        self.reader = HTMLReader(pathDocs, pathStopwords)
        self.db = Documents()
        self.invertedIndex = InvertedIndex(self.db)
        self.createInvertedIndex()
        #self.calculateTfidf()

        #search_term = input("Enter term(s) to search: ")
        #self.analiseQuery(search_term)   
        #self.selectDocs() 
        #self.calcPrecRecallF()
        #self.calcAvgPrec()
        #self.calcCompInterInter11()
        #self.calculateArea()
        #self.plotGraphs()

        self.calc_PR()

    def createInvertedIndex(self):
        """
        Creates the inverted index dict
        """
        for doc in self.reader.docs:
            self.invertedIndex.index_document(doc)

        print("##############################################")
        print("Inverted Index")
        print(self.invertedIndex)
        print("##############################################") 

    def calculateTfidf(self):
        """
        Calculates the Tfidf of the terms related to the docs
        """
        self.invertedIndex.calc_tfidf()
        print("##############################################") 
        print("Tfidf")
        print(self.invertedIndex)
        print("##############################################") 
        print(self.invertedIndex.index.keys())
        
    def analiseQuery(self, search_term):
        """
        Analise the queryin relation to the docs. Shows the docs with each word of the querys and the most similar docs with the input
        """
        similarity = self.invertedIndex.calc_similarity(search_term)

        result = self.invertedIndex.lookup_query(search_term)
        print("##############################################")
        print("Similarity")
        print(similarity)
        print("##############################################")

        if (sum(similarity) == 0):
            print("Term not found in the documents! ")

        self.ranking = similarity.copy()
        self.ranking.sort(reverse=True)

        self.retrieved = []

        for i in range(0, len(self.ranking)):
            for j in range(0, len(similarity)):
                if self.ranking[i] == similarity[j] and self.ranking[i] > 0:
                    print("Most similar: Doc("+str(j)+"), Similarity: "+str(self.ranking[i]))
                    self.retrieved.append(j)

    def selectDocs(self):
        """
        Get the number of relevant docs and the user selected docs
        """
        print("\nInsert the number of relevant Docs that you are looking for: (e.i. 10 )")
        self.numberRelevant = float(input())

        print("\nInsert the relevant Docs: (e.i. 0,1,2 )")
        self.relevant = input()
        self.relevant = [int(i) for i in self.relevant.split(",")]
        self.relevant.sort()
        
    def calcPrecRecallF(self):
        """
        Calculates the precision, Recall and F-measure
        """
        totalRelevant = 0.0
        for doc in self.relevant:
            if doc in self.retrieved:
                totalRelevant += 1

        self.precision = totalRelevant/float(len(self.retrieved))    
        self.recall = float(totalRelevant)/self.numberRelevant
        self.fmseasure = 2.0*(self.precision*self.recall)/(self.precision+self.recall)

        print("##############################################") 
        print("Precision:")
        print(self.precision)
        print("Recall:")
        print(self.recall)
        print("F-measure:")
        print(self.fmseasure)
        print("##############################################") 

    def calcAvgPrec(self):
        """
        Calculates the average precision. It also calculates the complete recall, which is equal to the interpolate recall, and the complete precision of the docs
        """
        avg = 0.0
        counter = 0
        self.recallCompInter = []
        self.precComplete = []
        for i in range (0, len(self.retrieved)):
            if self.retrieved[i] in self.relevant:
                counter += 1  
                avg += ((float(counter)/(i+1)))
            
            self.recallCompInter.append(float(counter)/(self.numberRelevant))
            self.precComplete.append(float(counter)/(i+1))        

        avg = avg/counter

        print("##############################################") 
        print("AvgPrecision:")
        print(avg)
        print("##############################################")
  
    def calcCompInterInter11(self):
        """
        Calculates the intepolate precison and the interpolate precision and recall
        """
        self.precInter = []
        self.selectedIndex = []
        for i in range(0, len(self.precComplete)):
            self.precInter.append(max(self.precComplete[i:]))
            if self.recallCompInter[i] != self.recallCompInter[i-1]:
                self.selectedIndex.append(i)

        self.prec11 = []
        self.recall11 = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  
        i = 0
        j = 1

        while (len(self.selectedIndex) > j-1):
            self.prec11.append(self.precInter[self.selectedIndex[j-1]])

            i += self.numberRelevant*0.1            
            j = math.ceil(i)           

        while (len(self.prec11) < len(self.recall11)):
            self.prec11.append(0.0)
            print(len(self.prec11), len(self.recall11))

        print("##############################################")
        print("Recallcompinter:")
        print(self.recallCompInter)
        print("preccomp:")
        print(self.precComplete)  
        print("precinter:")
        print(self.precInter)
        print("prec11:")
        print(self.prec11)
        print("recall11:")
        print(self.recall11)    

    def calculateArea(self):
        self.completeArea = np.trapz(self.precComplete, x=self.recallCompInter)
        self.interpolateArea = np.trapz(self.precInter, x=self.recallCompInter)
        self.interpolate11Area = np.trapz(self.prec11, x=self.recall11)

        print("##############################################")
        print("CompleteArea:")
        print(self.completeArea)
        print("InterpolateArea:")
        print(self.interpolateArea)
        print("Interpolate11Area:")
        print(self.interpolate11Area)

    def plotGraphs(self):
        """
        Plot'em
        """
        plt.ylim([0.0,1.0])
        plt.xlim([0.0,1.0])
        plt.plot(self.recallCompInter, self.precComplete, label='Complete')
        plt.plot(self.recallCompInter, self.precInter, label='Interpolate')
        plt.plot(self.recall11, self.prec11, label='Interpolate11')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.legend(framealpha=1, frameon=True)
        plt.show()

    def calc_PR(self):
        """
        Calculates the PR of the terms related to the docs
        """

        self.PR = np.zeros(shape=(len(self.invertedIndex.db.db)))
        self.PR[:] = 1.0/len(self.invertedIndex.db.db)
        self.alpha = 0.1
        self.e = 0.000000001
        self.invertedIndex.calc_PR(self.alpha, self.e, self.PR)

m = main(sys.argv[1], sys.argv[2])
