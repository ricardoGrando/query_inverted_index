# -*- coding: utf-8 -*-

import glob
import os
import codecs
import string

import requests
from inscriptis import get_text

class HTMLReader:
    def __init__(self, pathDocs, pathStopwords):
        self.pathDocs = pathDocs
        self.pathStopwords = pathStopwords
        self.readStopwords()
        self.readDocs()

    def readDocs(self):
        DataPathList = glob.glob(self.pathDocs+'*.html')
        DataPathList.sort()

        self.docs = []
        
        h = 0
        for docPath in DataPathList:
            f = codecs.open(docPath, 'r')
            text = get_text(f.read())
    
            # print(text_raw)
            # text = text_raw.split("\n")[3]

            self.docs.append({
                'id': str(h),
                'text': self.removePonctuation(text.split(" "))
            })

            h += 1

    def removePonctuation(self, doc):  
        i = 0
        while( i < len(doc)):
            doc[i] = doc[i].translate(str.maketrans('', '', '.!,?*%0123456789/;><~^'))
            doc[i] = doc[i].lower()
            if (doc[i] in self.stopwords):
                doc.pop(i)
            else:
                i += 1
        
        return ' '.join(doc)
   
    def readStopwords(self):
        fp = open(self.pathStopwords, "r")        
        first_line = fp.readline()

        self.stopwords = first_line.split(';')[:-1]