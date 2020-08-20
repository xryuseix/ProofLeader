# -*- coding: utf-8 -*-
__doc__ = """{f}
Usage:
    {f} [-v | --version] [-s | --search]
        [-f | --file <FOLDER_NAME>]
    {f} -h | --help
Options:
    -h --help                       ヘルプを表示
    -f --file <FOLDER_NAME>         ファイル/フォルダを指定して実行
    -v --version                    ProofLeaderのバージョンを表示
    -s --search                     特定の文字列を探索
""".format(
    f=__file__
)

import sys
import os
import readme_dfs
from docopt import docopt

args = docopt(__doc__)

if args['--version']:
    with open('ProofLeader/.version') as f:
        print(f.read())

if args['--file']:
    readme_dfs.dfs(args['--file'][0], search = args['--search'])
else:
    readme_dfs.dfs(search = args['--search'])
    

print("\033[32mCHECK!!\033[0m -> https://competent-morse-3888be.netlify.app/")

