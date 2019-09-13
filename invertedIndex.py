# https://medium.com/@fro_g/writing-a-simple-inverted-index-in-python-3c8bcb52169a

import math

ALFA = 0.5

class Appearance:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """
    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency
        self.tfidf = 0.0
        self.idf = 0.0
        
    def __repr__(self):
        """
        String representation of the Appearance object
        """
        return str(self.__dict__)

class Database:
    """
    In memory database representing the already indexed documents.
    """
    def __init__(self):
        self.db = dict()
    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.__dict__)
    
    def get(self, id):
        return self.db.get(id, None)
    
    def add(self, document):
        """
        Adds a document to the DB.
        """
        return self.db.update({document['id']: document})
    def remove(self, document):
        """
        Removes document from DB.
        """
        return self.db.pop(document['id'], None)

class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        self.index = dict()
        self.db = db
    def __repr__(self):
        """
        String representation of the Database object
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
        return list(dict.keys())
    
    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        This is a very naive search since it will just split the terms and show
        the documents where they appear.
        """
        return { term: self.index[term] for term in query.split(' ') if term in self.index }

    def get_highest_frequency(self, docId, termsList):
        max_freq = 0
        for term in termsList:
            for key in self.index[term]:
                if int(key.docId) == docId and int(key.frequency) > max_freq:
                    max_freq = int(key.frequency)
        return max_freq

    def calc_tfidf(self):
        # List of all terms sorted
        self.termsList = sorted(self.getList(self.index))

        for term in self.termsList:
            for key in self.index[term]:
                key.idf = math.log10(float(len(self.db.db))/float(len(self.index[term])))                                
                key.tfidf = (float(key.frequency)/self.get_highest_frequency(int(key.docId), self.termsList))*key.idf

    def calc_D(self):
        D = [0.0]*int(len(self.db.db))

        for docId in range (0, int(len(self.db.db))):
            for term in self.termsList:
                for key in self.index[term]:
                    if int(key.docId) == docId:
                        D[docId] += key.tfidf**2
                        
            D[docId] = math.sqrt(D[docId])
            
        return D

    def calc_freq_query(self, wordsQuery):
        fq = [0]*int(len(self.termsList))       
        
        for i in range(0, len(self.termsList)):
            for word in wordsQuery:
                if word == self.termsList[i]:
                    fq[i] += 1

        return fq

    def calc_q_2(self, fq):
        Q_2 = [0.0]*int(len(self.termsList))

        for i in range(0, len(self.termsList)):
            if fq[i] > 0:
                Q_2[i] = ((ALFA + ((1-ALFA)*fq[i])/max(fq))*self.index[self.termsList[i]][0].idf)**2

        return Q_2

    def calc_tfidf_q(self, Q_2):
        tfidf_Q = [0.0]*int(len(self.db.db))

        for i in range(0, len(self.db.db)):            
            for j in range(0, len(self.termsList)):
                for key in self.index[self.termsList[j]]:                    
                    if (int(key.docId) == i):
                        tfidf_Q[i] +=  math.sqrt(Q_2[j])*key.tfidf

        return tfidf_Q

    def calc_similarity(self, search_tearm):
        
        D = self.calc_D()

        fq = self.calc_freq_query(search_tearm.split(" "))        

        Q_2 = self.calc_q_2(fq)
                   
        tfidf_Q = self.calc_tfidf_q(Q_2)

        sim_q = [0.0]*int(len(self.db.db))

        for i in range(0, len(self.db.db)):
            if (math.sqrt(sum(Q_2))*D[i]) > 0:
                sim_q[i] = tfidf_Q[i]/(math.sqrt(sum(Q_2))*D[i])

        return sim_q
        # for term in termsList:
