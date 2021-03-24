# tmpディレクトリをtestcaseからコピーする形で作成
import os, glob
from pathlib import Path

# ファイル一覧を取得する
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


# ファイルを読み込む
def read_file(path):
    with open(path) as f:
        return f.read()


# ファイルは直接上書きするので，コピーしておく
os.system("sudo rm -rf ./test/result")
os.system("sudo cp -r ./test/testcase ./test/result")
os.system("sudo python3 ./ProofLeader/proofLeader.py --file ./test/result")
print("\n" + "-" * 30 + "\n")

path = get_file_names("./test/result")

same_count = 0  # 正解数
failed_list = []  # 失敗リスト

# ProofLeaderにファイル探索機能があるけど，カウントとかしたいので一つ一つチェックする
for i, result_path in enumerate(path):
    testcase_path = result_path.replace("result", "ans")
    testcase_doc = read_file(testcase_path)
    result_doc = read_file(result_path)
    if testcase_doc == result_doc:
        same_count += 1
    else:
        failed_list.append(testcase_path)

# 正誤チェック
if same_count == len(path):
    print("\033[32m[PASSED]\033[0m ", end="")
else:
    print("\033[31m[FAILED]\033[0m ", end="")
print("test : ({} / {}) passed!".format(same_count, len(path)))

# 失敗したファイルがある時，失敗リストを出力
if same_count != len(path):
    for f in failed_list:
        print("\033[33mWARNING\033[0m : {}".format(f))
