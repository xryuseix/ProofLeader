import glob
import read_file as File
import converter as Conv
from pathlib import Path

# ファイル一覧を取得する
def get_file_names(path):
    # 末尾の修正
    if path[-1] == "/":
        path = path[:-1]
    
    if Path(path).is_dir():
        return glob.glob("%s/*.md"%(path))
    else:
        return [path]

# mdファイルを探索し，converterに渡す
def dfs(root="/", dir="", search=False):
    ex_files_prot = File.readFile("%s/exclusion_list.csv"%(root)).split("\n")

    files = get_file_names(dir)
    
    # 除外リストに記載されていないファイルパス一覧
    valid_filepath = []

    for f in files:
        p = Path(f)
        is_exclusion = False
        for e in ex_files_prot:
            if p.samefile(e):
                is_exclusion = True
                break
        if not is_exclusion:
            valid_filepath.append(f)

    for file in valid_filepath:
        Conv.converter(file, search)
        print(file + " : \033[32mOK\033[0m")

    print("converter : \033[32mALL SUCCEEDED\033[0m")
