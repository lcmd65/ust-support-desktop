import re
import nltk 
import numpy 
import os
import gensim
import transformers
import torch
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import json
from fuzzywuzzy import fuzz
from app.func.func import audioToText
from app.func.database import connectMongoEmbedded

class Dataset():
    def __init__(self, instruction, input, output):
        self.instruction = instruction
        self.input = input
        self.output = output         
    
    def display(self):
        print(self.instruction,\
        self.input,\
        self.output)
        
def readEmbeddedDatabase():
    database = []
    with open("app/embedded/promp.json", "r+") as file:
        data = json.load(file)
        for item in data: 
            item_data = Dataset(\
                item["instruction"],
                item["input"],
                item["output"])
            database.append(item_data)
    return database

def readMongoEmbeddedDatabase():
    data = connectMongoEmbedded()
    database = []
    for item in data: 
            item_data = Dataset(\
                item["instruction"],
                item["input"],
                item["output"])
            database.append(item_data)
    return database
        
class Conver():
    def __init__(self):
        self.bot_, self.user_, self.score = [], [], []
        self.length = 0
        self.output = [] # topscore list
        self.model = self.sementicWord2Vec()
        self.llm_model = AutoModelForQuestionAnswering.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
        self.tokenizer = AutoTokenizer.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
        self.pipeline = pipeline("question-answering", model=self.llm_model, tokenizer=self.tokenizer)
    
    ## fuzzy matching 
    def processingUserText(self, index):
        self.bot_.append(None)
        self.score.append(None)
        database_embedded = readMongoEmbeddedDatabase()
        Max_score = 0
        Max_score = fuzz.ratio(self.user_[index], database_embedded[0].instruction)
        for item in database_embedded:
            if fuzz.ratio(self.user_[index], item.instruction) >= 0.8:
                self.bot_[index] = item.output
                Max_score = fuzz.ratio(self.user_[index], item.instruction)
        self.score[index] = Max_score
    
    def topScoreList(self, index):
        self.output.append([])
        self.bot_.append(None)
        self.score.append(None)
        database_embedded = readMongoEmbeddedDatabase()
        for item in database_embedded:
            if fuzz.ratio(self.user_[index], item.instruction) >= 0.8:
                self.bot_[index] = item.output
                break
            if fuzz.ratio(self.user_[index], item.instruction) >= 0.3:
                string1_embedding = self.model.wv[self.user_[index]]
                string2_embedding = self.model.wv[item.instruction]
                similar =  self.model.wv.similarity(string1_embedding, string2_embedding)
                if similar >= 0.3:
                    self.output[index].append(item)    
    
    def questionAnswering(self, question_, context_):
        answer = self.pipeline(question=question_, context=context_)
        return answer
        
    def processingTopScoreList(self, index):
        max_score = 0
        for item in self.output[index]:
            answer_ = self.questionAnswering(self.user_[index], item["output"])
            if answer_['score'] > max_score:
                self.bot_[index] = answer_['answer']
                max_score = answer_['score']
        self.score[index] = (self.score[index]*0.5) + max_score*0.5
    
    def answerGenerate(self, index):
        if self.bot_[index] != None:
            return self.bot_[index]
        else:
            self.processingTopScoreList(index)
            return self.bot_[index]
            
    def sementicWord2Vec(self):
        model = 'app/data/vnex.model.bin'
        if os.path.isfile(model):
            from packaging import version
            if version.parse(gensim.__version__) >= version.parse("1.0.1"):
                from gensim.models import KeyedVectors
                word2vec_model = KeyedVectors.load_word2vec_format(model, binary=True)
                return word2vec_model
            else:
                from gensim.models import Word2Vec
                word2vec_model = Word2Vec.load_word2vec_format(model, binary=True)
                return word2vec_model
    
    def addConver(self, text):
        self.length +=1
        self.user_.append(text)
        self.topScoreList(self.length - 1)
        
    def getConver(self):
        self.answerGenerate(self.length - 1)        


        
    