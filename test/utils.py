import os, glob
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree


def cp(from_path: str, to_path: str):
    assert os.path.exists(from_path), f"[ERROR] {from_path} is not found"
    if os.path.isdir(from_path):
        copy_tree(from_path, to_path)
        assert os.path.exists(to_path), f"[ERROR] {to_path} is not found"
        assert os.path.isdir(to_path), f"[ERROR] {to_path} is not dir"
    else:
        shutil.copyfile(from_path, to_path)
        assert os.path.exists(to_path), f"[ERROR] {to_path} is not found"
        assert os.path.isfile(to_path), f"[ERROR] {to_path} is not dir"


def rm(path: str):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            assert not os.path.exists(path), f"[ERROR] {path} is not found"
        else:
            os.remove(path)
            assert not os.path.exists(path), f"[ERROR] {path} is not found"


def read_file(path: str):
    with open(path) as f:
        return f.read()


# md ファイル一覧を取得する
def get_file_names(current_path):
    # 末尾の修正
    if current_path[-1] == "/":
        current_path = current_path[:-1]

    res = []
    path_list = glob.glob("%s/*" % (current_path))
    for path in path_list:
        if Path(path).is_dir():
            res.extend(get_file_names(path))
        else:
            if path[-3:] == ".md":
                res.append(path)
    return res
