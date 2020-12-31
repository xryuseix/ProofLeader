# tmpディレクトリをtestcaseからコピーする形で作成
# cd
import os, glob

# ファイル一覧を取得する
def get_file_names(path):
    allfile = glob.glob(path + "/*")
    return allfile


# ファイルを読み込む
def read_file(path):
    with open(path) as f:
        return f.read()


os.system("sudo rm -rf ./test/result")
os.system("sudo cp -r ./test/testcase ./test/result")
os.system("sudo python3 ./ProofLeader/proofLeader.py --file ./test/result")
print("\n" + "-" * 30 + "\n")

path = get_file_names("./test/result")

same_count = 0
failed_list = []

for i, result_path in enumerate(path):
    testcase_path = result_path.replace("result", "ans")
    testcase_doc = read_file(testcase_path)
    result_doc = read_file(result_path)
    if testcase_doc == result_doc:
        same_count += 1
    else:
        failed_list.append(testcase_path)


if same_count == len(path):
    print("\033[32m[PASSED]\033[0m ", end="")
else:
    print("\033[31m[FAILED]\033[0m ", end="")
print("test : ({} / {}) passed!".format(same_count, len(path)))

if same_count != len(path):
    for f in failed_list:
        print("\033[33mWARNING\033[0m : {}".format(f))
