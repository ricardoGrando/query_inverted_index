import math
from Appearance import *
from Documents import *
import numpy as np

ALFA = 0.5

class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        self.index = dict()
        self.db = db
    def __repr__(self):
        """
        String representation of the Documents object
        """
        return str(self.index)
        
    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """
        
        # Remove punctuation from the text.
        terms = document['text'].split(' ')
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if term != '':
                term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
                appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
            
        # Update the inverted index
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    def getList(self, dict):    
        """
        Returns the dict as a list
        """   
        return list(dict.keys())
    
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        return { term: self.index[term] for term in query.split(' ') if term in self.index }

    def get_highest_frequency(self, docId, termsList):
        """
        Returns the max frequency of all terms in a docid document
        """
        max_freq = 0
        for term in termsList:
            for key in self.index[term]:
                if int(key.docId) == docId and int(key.frequency) > max_freq:
                    max_freq = int(key.frequency)
        return max_freq

    def calc_tfidf(self):
        """
        Calculate the tfidf of all keys of each term in the appearance dictionary
        """
        # List of all terms sorted
        self.termsList = sorted(self.getList(self.index))

        for term in self.termsList:
            for key in self.index[term]:
                key.idf = math.log10(float(len(self.db.db))/float(len(self.index[term])))                                
                key.tfidf = (float(key.frequency)/self.get_highest_frequency(int(key.docId), self.termsList))*key.idf

    def calc_D(self):
        """
        Calculate the D of all keys of each term in the appearance dictionary of each document
        """        
        D = [0.0]*int(len(self.db.db))

        for docId in range (0, int(len(self.db.db))):
            for term in self.termsList:
                for key in self.index[term]:
                    if int(key.docId) == docId:
                        D[docId] += key.tfidf**2
                        
            D[docId] = math.sqrt(D[docId])
            
        return D

    def calc_freq_query(self, wordsQuery):
        """
        Calculate the D of all keys of each term in the appearance dictionary of each document
        """
        fq = [0]*int(len(self.termsList))       
        
        for i in range(0, len(self.termsList)):
            for word in wordsQuery:
                if word == self.termsList[i]:
                    fq[i] += 1

        return fq

    def calc_q_2(self, fq):
        """
        Calculate the Q^2 list of the query related to each term
        """
        Q_2 = [0.0]*int(len(self.termsList))

        for i in range(0, len(self.termsList)):
            if fq[i] > 0:
                Q_2[i] = ((ALFA + ((1-ALFA)*fq[i])/max(fq))*self.index[self.termsList[i]][0].idf)**2

        return Q_2

    def calc_tfidf_q(self, Q_2):
        """
        Calculate the tfidf*Q list related to each document
        """
        tfidf_Q = [0.0]*int(len(self.db.db))

        for i in range(0, len(self.db.db)):            
            for j in range(0, len(self.termsList)):
                for key in self.index[self.termsList[j]]:                    
                    if (int(key.docId) == i):
                        tfidf_Q[i] +=  math.sqrt(Q_2[j])*key.tfidf

        return tfidf_Q

    def calc_similarity(self, search_tearm):
        """
        Calculate the similarity of the query with every document
        """
        D = self.calc_D()

        fq = self.calc_freq_query(search_tearm.split(" "))        

        Q_2 = self.calc_q_2(fq)
                   
        tfidf_Q = self.calc_tfidf_q(Q_2)

        sim_q = [0.0]*int(len(self.db.db))

        for i in range(0, len(self.db.db)):
            if (math.sqrt(sum(Q_2))*D[i]) > 0:
                sim_q[i] = tfidf_Q[i]/(math.sqrt(sum(Q_2))*D[i])

        return sim_q

    def get_sum_pr_l(self, id):

        termsList = sorted(self.getList(self.index))

        counter = 0

        for term in termsList:  
            for key in self.index[term]:
                if key.docId == id:
                    counter += 1

        return counter
                    

    def calc_PR(self, alpha, epsilon, pr_list):
        """
        Calculate the PR of each HTML file
        """
        # List of all terms sorted
        self.termsList = sorted(self.getList(self.index))

        last_pr_list = np.zeros(shape=pr_list.shape)

        counter = 0

        while (max(abs(last_pr_list-pr_list)) > epsilon):
            last_pr_list = pr_list.copy()
            for i in range(0, len(self.termsList)): 
                sum = 0.0 
                for key in self.index[self.termsList[i]]: 
                    sum += pr_list[int(key.docId)]/self.get_sum_pr_l(key.docId)
                    
                pr_list[i] = alpha/len(pr_list) + (1-alpha)*sum

                #print(max(abs(last_pr_list-pr_list)))

            print(pr_list)

            counter += 1  

        print("##############################################")
        print("Final PR: ")
        print(pr_list)
        print("Number of iterations: "+str(counter))
              