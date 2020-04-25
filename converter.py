# -*- coding: utf-8 -*-
import sys
import re

def readFile(path, csv=False):
    text = ""
    wordList = []
    with open(path) as f:
        if csv:
            wordList.append(f.read().split(','))
        else:
            text += f.read()
    if csv:
        return wordList
    else:
        return text

def dotComma(text):
    ja = '[亜-熙ぁ-んァ-ヶ]'
    replacedText = re.sub('({})，'.format(ja), r'\1、', text)
    return re.sub('({})．'.format(ja), r'\1。', replacedText)

def word2Word(text, file):
    wordList = readFile('./word_list.csv', True)
    textArr = text.split('```')

    for arr in range(0, len(textArr), 2):
        textList = textArr[arr].split('\n')
        for i, text in enumerate(textList):
            for k in wordList:
                reObj = re.search(k[0], text)
                if reObj:
                    print(file,arr+i,k[0],k[1],reObj.start())
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

print(text)

