import sys
import os

if len(sys.argv) > 1:
    os.system("python ProofLeader/readme_dfs.py {}".format(sys.argv[1]))
else:
    os.system("python ProofLeader/readme_dfs.py")

print("\033[32mCHECK!!\033[0m -> https://competent-morse-3888be.netlify.app/")

