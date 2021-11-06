import glob
import read_file as File
import converter as Conv
from pathlib import Path

# ファイル一覧を取得する
def get_file_names(current_path):
    # 末尾の修正
    if current_path[-1] == "/":
        current_path = current_path[:-1]

    res = []
    path_list = glob.glob("%s/*" % (current_path))
    
    # 与えられたのがフォルダではなくてファイルなら追加
    if(Path(current_path).is_file()):
        path_list.append(current_path)
    
    # ディレクトリならさらに探索
    for path in path_list:
        if Path(path).is_dir():
            res.extend(get_file_names(path))
        else:
            if path[-3:] == ".md":
                res.append(path)
    return res


# mdファイルを探索し，converterに渡す
def file_search(root="/", dir="", search=False):
    ex_files_prot = File.readFile("%s/exclusion_list.csv" % (root)).split("\n")

    files = get_file_names(dir)

    # 除外リストに記載されていないファイルパス一覧
    valid_filepath = []

    for f in files:
        p = Path(f)
        is_exclusion = False
        for e in ex_files_prot:
            # 除外リストのファイルがない場合
            if not Path(e).exists():
                continue
            # 除外リストのファイルと一致した場合
            if p.samefile(e):
                is_exclusion = True
                break
        if not is_exclusion:
            valid_filepath.append(f)

    for file in valid_filepath:
        Conv.converter(file, search)
        print(file + " : \033[32mOK\033[0m")

    print("converter : \033[32mALL SUCCEEDED\033[0m")
