import sys
import re

file = sys.argv[1]
text = ""

with open(file) as f:
    s = f.read()
    text = s

replacedText = text
replacedText = re.sub(r'([亜-熙ぁ-んァ-ヶ])，', r'\1、', replacedText)
replacedText = re.sub(r'([亜-熙ぁ-んァ-ヶ])．', r'\1。', replacedText)

replacedText = re.sub(r'(\d)(?=(\d{3})+(?!\d))', r'\1,', replacedText)

print(text)
print('\n================\n')
print(replacedText)
