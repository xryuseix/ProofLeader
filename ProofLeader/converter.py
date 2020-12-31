# -*- coding: utf-8 -*-
import re
import os
import read_file as File


# ．，を、。に変換
def dot_to_comma(text):
    replacedText = re.sub("，", r"、", text)
    return re.sub("．", r"。", replacedText)


# word_listを参照して警告
def word_to_word(text, file, search):
    if not os.path.isfile("./ProofLeader/word_list.csv"):
        return text
    wordList = File.readFile("./ProofLeader/word_list.csv", True)
    # find_listを開く
    if search:
        findListPath = "./ProofLeader/find_list.csv"
        if not os.path.isfile(findListPath):
            search = False
        with open(findListPath) as f:
            findList = [s.strip() for s in f.readlines()]

    textArr = text.splitlines()
    wordOut = []
    findOut = []
    for i, text in enumerate(textArr):
        for li in wordList:  # 文字列警告
            reObj = re.search(li[0], text)
            if reObj:
                wordOut.append([i + 1, reObj.start(), reObj.group(), li[1]])
        if search:  # 文字列探索
            for li in findList:
                reObj = re.search(li, text)
                if reObj:
                    findOut.append([i + 1, reObj.start(), li])
    for c in wordOut:
        print(
            "\033[33mWARNING\033[0m: {}:{}:{}: ({}) => ({})".format(
                file, c[0], c[1], c[2], c[3]
            )
        )
    for c in findOut:
        print("\033[36mFOUND!!\033[0m: {}:{}:{}: ({})".format(file, c[0], c[1], c[2]))
    return "\n".join(textArr)


# 数字を三桁ごとに区切ってカンマ
def digit_comma(num):
    beforeCommaNum = num.count(",")
    s = num.split(".")
    ret = re.sub("(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s[0])
    if len(s) > 1:
        ret += "." + s[1]
    return ret, ret.count(",") - beforeCommaNum


# 前後に空白を入れる
def space(text):
    resText = ""
    delIndex = [m.span() for m in re.finditer("<pre>|</pre>|```|`|「|」{1}", text)]
    delIndex.insert(0, [0, 0])
    delIndex.append([len(text), len(text)])

    for i in range(len(delIndex) - 1):
        subText = text[delIndex[i][1] : delIndex[i + 1][0]]

        if i % 2 == 0 or (  # 「英記号列(プログラム)」は除外
            delIndex[i][1] > 0
            and text[delIndex[i][1] - 1] == "「"
            and not re.fullmatch("[^亜-熙ぁ-んァ-ヶ]*", subText)
        ):
            # 数値の前に空白
            subText = re.sub(
                "([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", subText
            )
            # 数値の後ろに空白
            subText = re.sub(
                "([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", subText
            )
            # 先頭英字の後ろに空白
            subText = re.sub("(\n[a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", subText)

            numPoses = re.finditer("([+-]?(?:\d+\.?\d*|\.\d+))", subText)
            shift = 0  # カンマを置いた回数
            for p in numPoses:  # 三桁ごとにカンマ
                s, tmpShift = digit_comma(
                    subText[p.span()[0] + shift : p.span()[1] + shift]
                )
                subText = (
                    subText[0 : p.span()[0] + shift]
                    + s
                    + subText[p.span()[1] + shift :]
                )
                shift += tmpShift
            if i + 1 < len(delIndex):
                resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
            else:
                resText += subText
        else:
            resText += subText + text[delIndex[i + 1][0] : delIndex[i + 1][1]]
    return resText


# 数値の前後と行頭にスペースを入れる
class SpaceConvert:
    def __init__(self, text: str):
        self.text = text

    # 数値の前後と行頭にスペースを入れる
    def add_space(self, text: str):
        print(text)
        # 数値の前に空白
        text = re.sub("([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", text)
        # 数値の後ろに空白
        text = re.sub("([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", text)
        # 先頭英字の後ろに空白
        text = re.sub("(\n[a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", text)
        print(text + "\n")
        return text

    # 文字列を除外パターンで分離
    def split_text(self):
        converted_text = ""
        # 変換対象外にするパターン一覧
        rm_patterns = ["</{0,1}pre>", "</{0,1}code>", "```"]
        # 除外パターンでテキストを分割
        text_arr = re.split("|".join(rm_patterns), self.text)
        text_arr.pop()
        # text_arrの各文字列がどのパターンの中にあるか
        ptns_in_text = [
            self.text[m.span()[0] : m.span()[1]]
            for m in re.finditer("|".join(rm_patterns), self.text)
        ]

        # 現在囲まれているタグ一覧
        ptn_state = []

        for doc, ptn in zip(text_arr, ptns_in_text):
            ptn = ptn.replace("/", "")  # 終了タグと開始タグを一緒にする
            if not ptn_state:  # 除外パターンに囲われていない時
                doc = self.add_space(doc)
            converted_text += doc
            if not ptn in ptn_state:  # 除外パターンの開始
                ptn_state.append(ptn)
            else:  # 除外パターンの終了
                ptn_state.remove(ptn)
            converted_text += ptn
        return converted_text


def converter(file, search):
    text = File.readFile(file)

    if not search:
        text = dot_to_comma(text)
        text = space(text)
    text = word_to_word(text, file, search)

    with open(file, mode="w") as f:
        f.write(text)


if __name__ == "__main__":
    sc = SpaceConvert("AAA<pre>ZZ123Z</pre>CC1234C```ZZZ```")
    print(sc.split_text())
