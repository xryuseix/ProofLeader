import pathlib
import sys
import os
import read_file as File

exFiles = File.readFile("./ProofLeader/exclusion_list.csv").split(',\n')

files = []


def recursive(path):  # dfs
    for po in path.iterdir():
        if po.is_dir():
            recursive(po)
        elif po.is_file() & po.match("*.md"):
            if not str(po) in exFiles:
                files.append(str(po))


root = "./"
if len(sys.argv) == 2:
    root += sys.argv[1]
recursive(pathlib.Path(root))

for file in files:
    os.system("python ProofLeader/converter.py " + file)
    print(file + " : \033[32mOK\033[0m")

print("converter : \033[32mALL OK\033[0m")