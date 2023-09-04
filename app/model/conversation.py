import nltk 
from fuzzywuzzy import fuzz
import re
import json
from app.func.func import audioToText

class Dataset():
    def __init__(self, instruction, input, output):
        self.instruction = instruction
        self.input = input
        self.output = output         
    
    def display(self):
        print(self._text,\
        self._token,\
        self._annotations,\
        self._roll)

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
        
class Conver():
    def __init__(self):
        self.bot_, self.user_, self.score = [], [], []
        self.length = 0
    
    def processingUserText(self, index):
        self.bot_.append(None)
        self.score.append(None)
        database_embedded = readEmbeddedDatabase()
        Max_score = 0
        Max_score = fuzz.ratio(self.user_[index], database_embedded[0].instruction)
        for item in database_embedded:
            if fuzz.fuzz(self.user_[index], item.instruction) >= Max_score:
                self.bot_[index] = item
                Max_score = fuzz.ratio(self.user_[index], item.instruction)
        self.score[index] = Max_score
    
    def addConver(self, text):
        self.length +=1
        self.user_.append(text)
        self.processingUserText(self.length - 1)
        
    def getConver(self):
        return self.bot_[self.length -1]
        
if __name__ == "__main__":
    pass
# python3 app/model/conversation.py


        
    