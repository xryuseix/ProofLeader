import csv


def readFile(path, is_csv=False):
    text = ""
    word_list = []
    with open(path) as f:
        if is_csv:
            reader = csv.reader(f)
            for row in reader:
                for i, r in enumerate(row):
                    if i:
                        word_list.append([r, row[0]])
        else:
            text += f.read()
    if is_csv:
        return word_list
    else:
        return text
