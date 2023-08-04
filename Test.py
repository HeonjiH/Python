import pandas as pd
import json
from flask import Flask, request
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from konlpy.tag import Okt

class ExcelHelper:
    def __init__(self, path="", fileName=""):
        self._fileName = fileName
        self._path = path
        self.dataset = pd.read_excel(f"{path}/{fileName}", index_col=0)
    
    def classifyData(self, key):
        filterData = self.dataset[self.dataset["구분"] == key][["질문", "답변"]]
        return filterData


class SentenceBleu:
    def __init__(self):
        self.reference = []
        self.generate = []
        self.refDict = {}
        self.okt = Okt()

    def setReference(self, ref):
        for sentence in ref:
            arr = self.okt.nouns(sentence)
            self.reference.append([arr])
            self.refDict[" ".join(arr)] = sentence

    def setGenerate(self, gen):
        self.generate = self.okt.nouns(gen)
    
    def getPrecision(self):
        tmpRef = ""
        tmpScore = 0
        for refStr in self.reference:
            score = sentence_bleu(refStr, self.generate, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method4)
            if score > 0 and score <= 1 :
                if(score > tmpScore): 
                    tmpScore = score
                    tmpRef = " ".join(refStr[0])
        
        print(tmpScore)
        return self.refDict[tmpRef]
        


class MainClass:
    def __init__(self, keys):
        self.keys = keys
        self.questionBleu = SentenceBleu()
        self.answerBleu = SentenceBleu()
        self.qnaDict = {}
        self.correctAnswer = ""
    
    #qna data excel파일에서 읽어오기
    def importExcel(self, path, fileName):
        excel = ExcelHelper(path, fileName)
        
        for key in self.keys:
            data = excel.classifyData(key)
            for col, ser in data.iterrows():
                qKey = str(ser.values[0])
                aVal = str(ser.values[1])
                self.qnaDict[qKey] = aVal
            
        #bleu에 레퍼런스 문장 세팅 (질문, 답변)
        self.questionBleu.setReference(self.qnaDict.keys())
        self.answerBleu.setReference(self.qnaDict.values())
            
    def question(self, sentence):
        self.questionBleu.setGenerate(sentence)
        return self.questionBleu.getPrecision()
    
    def getCorrectAnswer(self, sentence):
        result = self.question(sentence)
        return self.qnaDict[result]
    
    def answer(self, sentence):
        self.answerBleu.setGenerate(sentence)
        return self.answerBleu.getPrecision()
    
    def inputSet(self):
        _input = ""
        while True:
            _input = input("질문: ")
            if(_input == "exit"): break;
            result = self.question(_input)
            print(f"{self.qnaDict[result]}")
        
_main = MainClass(["공지", "문자 초안 작성"])
_main.importExcel("C:/Users/dalsa/OneDrive/Desktop/study/Python", "test.xlsx")

#restful api
app = Flask(__name__)

@app.route("/question", methods=["POST"])
def getCorrectAnswer():
    post_result = json.loads(request.get_data())
    _question = post_result["question"]
    answer = _main.getCorrectAnswer(_question)
    
    _genAnswer = post_result["answer"]
    _result = _main.answer(_genAnswer)
    
    isTrue = False
    if(answer == _result):
        isTrue = True
    
    print("======================================")
    print("======================================")
    print(_result)    
    print(isTrue)
    print("======================================")
    print("======================================")
    
    return answer

app.run(host="localhost", port=8080)
