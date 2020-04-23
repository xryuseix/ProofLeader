import pathlib
import os

files = []

def recursive(path): # dfs
    for po in path.iterdir():
        if po.is_dir():
            recursive(po)
        elif po.is_file() & po.match('*/README.md'):
            files.append(str(po))

recursive(pathlib.Path('.'))

for file in files:
    os.system('python Proofreader/converter.py ' + file)
    print(file + ' : OK')

print('converter : ALL OK')