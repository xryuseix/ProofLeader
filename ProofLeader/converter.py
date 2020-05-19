# -*- coding: utf-8 -*-
import sys
import re
import os
import readFile as File


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
    textArr = text.split("```")

    for arr in range(0, len(textArr), 2):
        textList = textArr[arr].split("\n")
        for i, text in enumerate(textList):
            for k in wordList:
                reObj = re.search(k[0], text)
                if reObj:
                    print(
                        "\033[33mWARNING\033[0m: {}:{}:{}: ({}) => ({})".format(
                            file, arr + i + 1, reObj.start(), reObj.group(), k[1]
                        )
                    )
    return "```".join(textArr)


# 数字を三桁ごとに区切ってカンマ&前後に空白を入れる
def numComma(text):
    digit = "(\d)(?=(\d{3})+(?!\d))"
    textArr = re.split("<pre>|<\/pre>", text)
    returnStr = ""
    for i, crrText in enumerate(textArr):
        if not i % 2:
            crrText = re.sub("([^\n\d, ])(\d+)", r"\1 \2", crrText)  # 数値の前に空白
            crrText = re.sub("(\d)([^\n\d, ])", r"\1 \2", crrText)  # 数値の後ろに空白
            crrText = re.sub("(\n[a-zA-Z]+)[亜-熙ぁ-んァ-ヶ]", r"\1 ", crrText)  # 先頭英字の後ろに空白
            crrText = re.sub(digit, r"\1,", crrText)
            if i > 0:
                crrText = "</pre>" + crrText
        else:
            crrText = "<pre>" + crrText
        returnStr += crrText
    return returnStr


file = sys.argv[1]
text = File.readFile(file)

text = dotComma(text)
text = numComma(text)
text = word2Word(text, file)

with open(file, mode="w") as f:
    f.write(text)
