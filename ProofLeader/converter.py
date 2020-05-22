# -*- coding: utf-8 -*-
import re
import os
import read_file as File


# ．，を、。に変換
def dotComma(text):
    ja = "[亜-熙ぁ-んァ-ヶ]"
    replacedText = re.sub("({})，".format(ja), r"\1、", text)
    return re.sub("({})．".format(ja), r"\1。", replacedText)


# word_listを参照して警告
def word2Word(text, file):
    if not os.path.isfile("./ProofLeader/word_list.csv"):
        return text
    wordList = File.readFile("./ProofLeader/word_list.csv", True)
    textArr = text.splitlines()
    for i, text in enumerate(textArr):
        for li in wordList:
            reObj = re.search(li[0], text)
            if reObj:
                print(
                    "\033[33mWARNING\033[0m: {}:{}:{}: ({}) => ({})".format(
                        file, i + 1, reObj.start(), reObj.group(), li[1]
                    )
                )
    return "\n".join(textArr)


# 数字を三桁ごとに区切ってカンマ&前後に空白を入れる
def numComma(text):
    resText = ""
    digit = "(\d)(?=(\d{3})+(?!\d))"
    delIndex = [m.span() for m in re.finditer("<pre>|</pre>|```", text)]
    delIndex.insert(0, [0, 0])
    delIndex.append([len(text), len(text)])

    for i in range(len(delIndex) - 1):
        subText = text[delIndex[i][1] : delIndex[i + 1][0]]
        if not i % 2:
            subText = re.sub("([^\n\d, ])(\d+)", r"\1 \2", subText)  # 数値の前に空白
            subText = re.sub("(\d)([^\n\d, ])", r"\1 \2", subText)  # 数値の後ろに空白
            subText = re.sub("(\n[a-zA-Z]+)[亜-熙ぁ-んァ-ヶ]", r"\1 ", subText)  # 先頭英字の後ろに空白
            subText = re.sub(digit, r"\1,", subText)
            if i + 1 < len(delIndex):
                resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
            else:
                resText += subText
        else:
            resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
    return resText

def converter(file):
    text = File.readFile(file)

    text = dotComma(text)
    text = numComma(text)
    text = word2Word(text, file)

    with open(file, mode="w") as f:
        f.write(text)
