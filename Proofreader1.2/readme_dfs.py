import pathlib
import sys
import os

files = []

def recursive(path): # dfs
    for po in path.iterdir():
        if po.is_dir():
            recursive(po)
        elif po.is_file() & po.match('*.md'):
            files.append(str(po))

root = './'
if len(sys.argv) == 2:
    root += sys.argv[1]
recursive(pathlib.Path(root))

for file in files:
    os.system('python Proofreader/converter.py ' + file)
    print(file + ' : OK')

print('converter : ALL OK')