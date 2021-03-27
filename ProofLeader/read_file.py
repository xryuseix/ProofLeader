import csv


def readFile(path, isCsv=False):
    text = ""
    wordList = []
    with open(path) as f:
        if isCsv:
            reader = csv.reader(f)
            for row in reader:
                for i, r in enumerate(row):
                    if i:
                        wordList.append([r, row[0]])
        else:
            text += f.read()
    if isCsv:
        return wordList
    else:
        return text
