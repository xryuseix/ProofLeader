# -*- coding: utf-8 -*-
import sys
import csv
import re
import os

def readFile(path, isCsv=False):
    text = ""
    wordList = []
    with open(path) as f:
        if isCsv:
            reader = csv.reader(f)
            for row in reader:
                wordList.append(row)
        else:
            text += f.read()
    if isCsv:
        return wordList
    else:
        return text

def dotComma(text):
    ja = '[亜-熙ぁ-んァ-ヶ]'
    replacedText = re.sub('({})，'.format(ja), r'\1、', text)
    return re.sub('({})．'.format(ja), r'\1。', replacedText)

def word2Word(text, file):
    if not os.path.isfile('./Proofreader/word_list.csv'):
        return text
    wordList = readFile('./Proofreader/word_list.csv', True)
    textArr = text.split('```')

    for arr in range(0, len(textArr), 2):
        textList = textArr[arr].split('\n')
        for i, text in enumerate(textList):
            for k in wordList:
                reObj = re.search(k[0], text)
                if reObj:
                    print("WARNING: {}:{}:{}: ({}) => ({})".format(file, arr+i+1, reObj.start(), reObj.group(), k[1]))
    return '```'.join(textArr)

def numComma(text):
    digit = '(\d)(?=(\d{3})+(?!\d))'
    textArr = text.split('```')
    for i in range(0, len(textArr), 2):
        textArr[i] = re.sub(digit, r'\1,', textArr[i])
    return '```'.join(textArr)

file = sys.argv[1]
text = readFile(file)

text = dotComma(text)
text = numComma(text)
text = word2Word(text, file)

with open(file, mode='w') as f:
    f.write(text)