# -*- coding: utf-8 -*-

import glob
import os
import codecs
import string
import re

import requests
from inscriptis import get_text

class HTMLReader:
    def __init__(self, pathDocs, pathStopwords):
        self.pathDocs = pathDocs
        self.pathStopwords = pathStopwords
        self.readStopwords()
        self.readDocs()

    def readDocs(self):
        """
        Read all documents of the path and set them in the Docs list
        """
        DataPathList = glob.glob(self.pathDocs+'*.html')
        DataPathList.sort()

        self.docs = []
        
        h = 0
        for docPath in DataPathList:
            f = codecs.open(docPath, 'r')
            text = get_text(f.read())

            self.docs.append({
                'id': str(h),
                'text': self.removePonctuation(re.split('\s|\n',text))
            })

            print(re.split('\s|\n',text))
            # print(re.split('\s|, |\*|\n',text))

            h += 1

    def removePonctuation(self, doc):  
        """
        Remove pontuation and set lower case in the text. Also removes the stopwords of the text
        """
        i = 0
        while( i < len(doc)):
            doc[i] = doc[i].translate(str.maketrans('.!,?“*%0123456789/:°\|]}º[ª{=+-_)(&¨$#@);"><~^\n', '                                               '))
            doc[i] = doc[i].replace(' ','')

            doc[i] = doc[i].lower()
            if (doc[i] in self.stopwords):
                # doc.pop(i)
                doc.remove(doc[i])
            else:
                i += 1

        return ' '.join(doc)
   
    def readStopwords(self):
        """
        Read the stopwords configuration file
        """
        fp = open(self.pathStopwords, "r")        
        first_line = fp.readline()

        self.stopwords = first_line.split(';')[:-1]