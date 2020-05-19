import csv


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
