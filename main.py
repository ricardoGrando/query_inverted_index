#!/usr/bin/python3

import sys
from HTMLReader import *
from invertedIndex import *

class main:

    def __init__(self, pathDocs, pathStopwords):
        self.reader = HTMLReader(pathDocs, pathStopwords)
        self.db = Database()
        self.invertedIndex = InvertedIndex(self.db)
        self.createInvertedIndex()
        self.calculateTfidf()

        search_term = input("Enter term(s) to search: ")
        
        self.analiseQuery(search_term)    

    def highlight_term(self, id, term, text, similarity):
        replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
        return "--- document {id}: {replaced} -- similarity: {sim}".format(id=id, replaced=replaced_text, sim=similarity)

    def createInvertedIndex(self):
        for doc in self.reader.docs:
            self.invertedIndex.index_document(doc)

        print("##############################################")
        print("Inverted Index")
        print(self.invertedIndex)
        print("##############################################") 

    def calculateTfidf(self):
        self.invertedIndex.calc_tfidf()
        print("##############################################") 
        print("Tfidf")
        print(self.invertedIndex)
        print("##############################################") 

    def analiseQuery(self, search_term):
        similarity = self.invertedIndex.calc_similarity(search_term)

        result = self.invertedIndex.lookup_query(search_term)
        print("##############################################")
        print("Similarity")
        print(similarity)
        print("##############################################")

        if (sum(similarity) > 0):
            for term in result.keys():
                for appearance in result[term]:
                    # Belgium: { docId: 1, frequency: 1}
                    document = self.db.get(appearance.docId)
                    print(self.highlight_term(appearance.docId, term, document['text'], similarity[int(appearance.docId)]))
                print("-----------------------------")
        else:
            print("Term not found in the documents! ")

        ranking = similarity.copy()
        ranking.sort(reverse=True)

        for i in range(0, len(ranking)):
            for j in range(0, len(similarity)):
                if ranking[i] == similarity[j] and ranking[i] > 0:
                    print("Most similar: Doc("+str(j)+"), Similarity: "+str(ranking[i]))
m = main(sys.argv[1], sys.argv[2])
