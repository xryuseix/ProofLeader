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


def digit_comma(num):
    beforeCommaNum = num.count(",")
    s = num.split(".")
    ret = re.sub("(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s[0])
    if len(s) > 1:
        ret += "." + s[1]
    return ret, ret.count(",") - beforeCommaNum


# 数字を三桁ごとに区切ってカンマ
class DigitComma:
    def __init__(self, text: str):
        self.text = text

    # 数字を三桁ごとに区切ってカンマ
    def __digit_comma(self, num: str):
        num = num.group()
        integer_decimal = num.split(".")
        commad_num = re.sub(
            "(\d)(?=(\d\d\d)+(?!\d))", r"\1,", integer_decimal[0]
        )  # 整数部
        if len(integer_decimal) > 1:
            commad_num += "." + integer_decimal[1]  # 小数部
        return commad_num

    # textから数値の場所のみを切り出す
    def cut_out(self):
        # 数値を切り出してカンマを挿入
        return re.sub(r"\d+[.,\d]*\d+", self.__digit_comma, self.text)


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
    def __add_space(self, text: str):
        # 数値の前に空白
        text = re.sub("([^\n\d, \.])([+-]?(?:\d+\.?\d*|\.\d+))", r"\1 \2", text)
        # 数値の後ろに空白
        text = re.sub("([+-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", text)
        # 先頭英字の後ろに空白
        text = re.sub("(\n[a-zA-Z]+)([亜-熙ぁ-んァ-ヶ])", r"\1 \2", text)
        return text

    # 前後に空白が入ってはいけない場合，削除する
    def __erase_invalid_spaces(self, text: str):
        invalid_space_list = [r"_", r"-", r"+", r"^"]
        # 累乗記号 : 前後のスペースを消す(xor記号の場合は^を使わない)
        text = text.replace(" ^ ", "^")
        # プラスマイナス : 式ではない場合のみ前のスペースを消す
        text = re.sub(r"([^(\d\s)])([+-])\s(\d)", r"\1 \2\3", text)
        # アンダーバー : 前後またはその片方のスペースを消す
        text = text.replace("_ ", "_")
        text = text.replace(" _", "_")
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
            m.group() for m in re.finditer("|".join(rm_patterns), self.text)
        ]

        # 現在囲まれているタグ一覧
        ptn_state = []

        for doc, ptn in zip(text_arr, ptns_in_text):
            # 終了タグと開始タグを一緒にする
            ptn = ptn.replace("/", "")

            # 除外パターンに囲われていない時
            if not ptn_state:
                doc = self.__add_space(doc)
            converted_text += doc

            # 数値にカンマを入れる
            dc = DigitComma(converted_text)
            converted_text = dc.cut_out()
            converted_text = self.__erase_invalid_spaces(converted_text)

            # 除外パターンの開始
            if not ptn in ptn_state:
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
    s = "A12 ^ 12AA<pre>Z_ 1Z 1 _ 23 - 456 Z</pre>CC- 1234C+ 12```ZZZ```"
    sc = SpaceConvert(s)
    print(sc.split_text())
