import pathlib
import os
import read_file as File
import converter


def dfs(dir="", search=False):
    exFiles = File.readFile("./ProofLeader/exclusion_list.csv").split("\n")

    files = []

    def recursive(path):  # dfs
        for po in path.iterdir():
            if po.is_dir():
                recursive(po)
            elif po.is_file() & po.match("*.md"):
                if not str(po) in exFiles:
                    files.append(str(po))

    root = "./"+dir
    recursive(pathlib.Path(root))

    for file in files:
        converter.converter(file, search)
        print(file + " : \033[32mOK\033[0m")

    print("converter : \033[32mALL OK\033[0m")
