import utils
import subprocess

# ファイルは直接上書きするので，コピーしておく
utils.rm("./test/result")
utils.cp("./test/testcase", "./test/result")
_ = subprocess.run(["python3", "./ProofLeader/proofLeader.py", "--file", "./test/result"])
print("\n" + "-" * 30 + "\n")

path = utils.get_file_names("./test/result")

same_count = 0  # 正解数
failed_list = []  # 失敗リスト

# ProofLeaderにファイル探索機能があるけど，カウントとかしたいので一つ一つチェックする
for i, result_path in enumerate(path):
    testcase_path = result_path.replace("result", "ans")
    testcase_doc = utils.read_file(testcase_path)
    result_doc = utils.read_file(result_path)
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
    assert False