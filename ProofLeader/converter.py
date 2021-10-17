# -*- coding: utf-8 -*-
import os, sys, re
import read_file as File


# ．，を、。に変換
def dot_to_comma(text):
    replacedText = re.sub("，", r"、", text)
    return re.sub("．", r"。", replacedText)


# word_listを参照して警告
def word_to_word(text, file, search, root):
    if not os.path.isfile("%sword_list.csv" % (root)):
        return text
    wordList = File.readFile("%sword_list.csv" % (root), True)
    # find_listを開く
    if search:
        findListPath = "%sfind_list.txt" % (root)
        if not os.path.isfile(findListPath):
            findListPath = []
        else:
            findListPath = File.readFile(findListPath).split("\n")

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
            "\033[33mWARNING\033[0m: %s:%s:%s: (%s) => (%s)"
            % (file, c[0], c[1], c[2], c[3])
        )
    for c in findOut:
        print("\033[36mFOUND!!\033[0m: %s:%s:%s: (%s)" % (file, c[0], c[1], c[2]))
    return "\n".join(textArr)


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


# 数値の前後と行頭にスペースを入れる
class SpaceConvert:
    def __init__(self, text: str, special_noun_list: list):
        self.text = text
        self.special_noun_list = special_noun_list

    # 数値の前後と行頭にスペースを入れる
    def __add_space(self, text: str):
        # 数値の前に空白
        text = re.sub(r"([^\n\d, \.])((?:\d+\.?\d*|\.\d+))", r"\1 \2", text)
        # 数値の後ろに空白
        text = re.sub(r"([\+\-]?(?:\d+\.?\d*|\.\d+))([^\n\d, \.])", r"\1 \2", text)

        # 記号の前後に空白
        op = r"\+\-\*"
        text = re.sub(r"([^%s\n ])([%s]+)" % (op, op), r"\1 \2", text)
        text = re.sub(r"([%s]+)([^%s ])" % (op, op), r"\1 \2", text)

        # 英字の後ろに空白
        symbol = r'_\.\^,:\/%<>"\'=\[\]\(\)'
        word = r"a-zA-Z\d" + symbol
        text = re.sub(r"([a-zA-Z][%s]*)([^\n%s ])" % (word, word), r"\1 \2", text)
        # 先頭以外の英字の前に空白
        text = re.sub(r"([^\n%s ])([a-zA-Z][%s]*)" % (word, word), r"\1 \2", text)

        # "[日本語][スペース]?[演算子][スペース][数値]"を"[日本語][スペース][演算子][数値]"にする (あ+ 1 → あ +1)
        ja = r"亜-熙ぁ-んァ-ヶ"
        text = re.sub(r"([%s]) ?([%s]+) (\d)" % (ja, op), r"\1 \2\3", text)
        # "[改行][スペース]?[演算子][スペース][数値]"を"[改行][演算子][数値]"にする (+ 1 → +1)
        text = re.sub(r"\n ?([%s]+) (\d)" % (op), r"\n\1\2", text)

        return text

    # 前後に空白が入ってはいけない場合，削除する
    def __erase_invalid_spaces(self, text: str):
        # 累乗記号 : 前後のスペースを消す(xor記号の場合は^を使わない)
        text = text.replace(r" ^ ", r"^")

        # アンダーバー : 前後またはその片方のスペースを消す
        text = text.replace("_ ", "_").replace(" _", "_")

        # Python 3 を Python3 にする
        text = re.sub(r"([A-Za-z]) (\d)", r"\1\2", text)

        # special_noun_listに入っている，間に不要な空白が入っている単語を修正する
        for noun in self.special_noun_list:
            # 入力をエスケープ
            need_escape = r"\\\*\+\.\?\(\)\{\}\[\]\^\$\|"
            noun_invalid_reg: str = re.sub("([%s])" % (need_escape), r"\\\1", noun)
            noun_invalid_reg = re.sub(r"(?<!\\)(.)", r" ?\1", noun_invalid_reg)[2:]
            # 置換
            text = re.sub(noun_invalid_reg, noun, text)

        return text

    # タグ前後の不要なスペースを削除
    def __erase_invalid_before_patterns_spaces(self, text: str):
        text = re.sub(r" +<", r" <", text)  # タグの前
        text = re.sub(r"> +", r"> ", text)  # タグの後
        return text

    # 文字列を除外パターンで分離
    def split_text(self):
        converted_text = ""
        # 変換対象外にするパターン一覧
        rm_patterns_range = [r"</?pre>", r"</?code>", "```"]
        # 除外パターンでテキストを分割
        text_arr = re.split("|".join(rm_patterns_range), self.text)
        # text_arrの各文字列がどのパターンの中にあるか
        ptns_in_text = [
            m.group() for m in re.finditer("|".join(rm_patterns_range), self.text)
        ]

        # 現在囲まれているタグ一覧
        ptn_state = []

        for doc, ptn in zip(text_arr, ptns_in_text):
            # 終了タグと開始タグを一緒にする
            ptn_prot = ptn.replace("/", "")

            # 除外パターンに囲われていない時
            if not ptn_state:
                # 数値にスペースを入れる
                doc = self.__add_space(doc)
                # 数値にカンマを入れる
                dc = DigitComma(doc)
                doc = dc.cut_out()
                doc = self.__erase_invalid_spaces(doc)

            converted_text += doc

            # 除外パターンの開始
            if not ptn_prot in ptn_state:
                ptn_state.append(ptn_prot)
                # <code>の前にスペースを入れる
                if ptn_prot == "<code>" and converted_text[-1] != "\n":
                    converted_text += " "
                # タグを整形結果に追加
                converted_text += ptn
            # 除外パターンの終了
            else:
                ptn_state.remove(ptn_prot)
                # タグを整形結果に追加
                converted_text += ptn
                # <code>の後にスペースを入れる
                if ptn_prot == "<code>":
                    converted_text += " "
        else:
            # テキストのブロック数と除外パターンの数が不一致の場合
            if len(text_arr) > len(ptns_in_text) and not ptn_state:
                # 数値にスペースを入れる
                doc = self.__add_space(text_arr[-1])
                # 数値にカンマを入れる
                dc = DigitComma(doc)
                doc = dc.cut_out()
                converted_text += self.__erase_invalid_spaces(doc)
        # タグ前後の不要なスペースを削除
        converted_text = self.__erase_invalid_before_patterns_spaces(converted_text)
        return converted_text


def converter(file, search):
    text = File.readFile(file)
    root = sys.argv[0][:-14]

    if not os.path.isfile("%sspecial_noun_list.txt" % (root)):
        special_noun_list = []
    else:
        special_noun_list = File.readFile("%sspecial_noun_list.txt" % (root)).split(
            "\n"
        )

    if not search:
        # 数値の前後，行頭の英単語の後にスペースを入れる
        sc = SpaceConvert(text, special_noun_list)
        text = sc.split_text()
        # ，を、に変更する
        text = dot_to_comma(text)
    # 指定した単語のWARNINGを出す
    text = word_to_word(text, file, search, root)

    with open(file, mode="w") as f:
        f.write(text)


if __name__ == "__main__":
    #     s = "A12 ^ 12AA<pre>Z_ 1Z 1 _ 23 - 456 Z</pre>CC- 1234C+ 12```ZZZ```AAA"
    s = "abc1d_aaa貼り付けco11111deでき入1123.456888 力 <code>る </code> よ\n<code></code>あっっ"
    print(s)
    sc = SpaceConvert(s)
    print(sc.split_text())
