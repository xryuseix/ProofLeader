import sys
import os
import readme_dfs

if len(sys.argv) > 1:
    readme_dfs.dfs(sys.argv[1])
else:
    readme_dfs.dfs()
    

print("\033[32mCHECK!!\033[0m -> https://competent-morse-3888be.netlify.app/")

