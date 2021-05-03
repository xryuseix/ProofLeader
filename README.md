![Python](https://img.shields.io/github/pipenv/locked/python-version/xryuseix/ProofLeader)

# ProofLeader

![logo](./logo.png)

1. カレントディレクトリより深い位置にある.mdファイルの句読点や整数表記を修正します。

**(変換例)**
* `、`は`、`に変換されます。
* `。`は`。`に変換されます。
* ` 100111000 `は` 100,111,000 `に変換されます。
* `abc, def`は変換されません。
* `aは123です`は`a は 123 です`に変換されます。

2. 文章表現のミスや変な箇所の修正を警告します(設定は手動)。
3. 特定の文字列を探索します(設定は手動)。

## 使用方法

* 起動コマンド

```sh
python ProofLeader/proofLeader.py
または
python ProofLeader/proofLeader.py -f <FOLDER_NAME>
```

ただし、aliasを設定することで不特定のディレクトリから実行することも可能です。
```
alias ProofLeader="python /path/to/ProofLeader/proofLeader.py "
ProofLeader -f <FOLDER_NAME>
```

* コマンドラインオプション
```sh
Usage:
    {f} [-h | --help] [-v | --version] [-s | --search]
        [-t | --test <FOLDER_NAME>]
    {f} -h | --help
Options:
    -h --help                       ヘルプを表示
    -f --file <FOLDER_NAME>         ファイル/フォルダを指定して実行
    -v --version                    ProofLeaderのバージョンを表示
    -s --search                     特定の文字列を探索
```

* 期待される出力例

<pre>
folder_a/folder_b/README.md : <font color="LimeGreen">OK</font>
folder_c/README.md : <font color="LimeGreen">OK</font>
converter : <font color="LimeGreen">ALL OK</font>
<font color="LimeGreen">CHECK!!</font> -> https://competent-morse-3888be.netlify.app/
</pre>

## 英単語・数字の体裁修正機能

* `、`は`、`に変換します。(`ですが、あ`→`ですが、あ`)
* `。`は`。`に変換します。(`です。`→`です。`)
* 数字は前後にスペースを入れます。(`あいう123あいう`→`あいう 123 あいう`)
ただし、数字は正規表現`([\d.,^\+])+`で表すことのできるものとします。
* 数字は三桁ごとにカンマを入れます。(`1234`→`1,234`)
* 英単語は前後にスペースを入れます。(`あwordあ`→`あ word あ`)
ただし、英単語は正規表現`([A-Za-z_数字])+`で表すことのできるものとします。
* ただし、英単語または数字の前後にすでにスペースが入っている場合、スペースは追加しません。(`word あ`→`word あ`)

## 文章表現警告機能

* **文章表現の警告機能(ver 1.4 で書式が変更になりました)**
`/ProofLeader`に`word_list.csv`ファイルを作り、以下のように記述します。

<pre>
After1,Before1
After2,Before2_1,Before2_2,Before2_3
After3,Before3_1,Before3_2
</pre>

すると以下のようにBeforeが文章に入っていた場合Afterにした方がいいと警告します。
出力例は以下のようになります(Webページ上で文字色黄色は見えにくいので背景色を黒にしています)。

<pre>
<span style="background-color:#000000">
<font color="Yellow">WARNING</font><font color="White">: ファイル名:行数:行頭から何文字目: (致します) => (いたします)</font>
</span>
</pre>

またBeforeはOR指定ができます。

```
A,(B|C)
```

とすると、BまたはCのとき警告します。

### 補足

`<pre></pre>`または`` ``` ``または`` ` ``で囲われている内側の文字に関して、**変換はされません**。ですが、警告は出します。ただし、入れ子構造にするとエラーが発生する場合がございます。

(例)

```
<pre>
123,456 // 123,456 にはならない
</pre>
`11,111` // 1,111にはならない
```

```
<pre>
致します // WARNINGが表示されます。
</pre>
`致します` // WARNINGが表示されます。
```

## 除外ファイルの設定

本プログラムは実行ディレクトリ内の全てのファイルに対して校閲します。
ですが、`/ProofLeader`に`exclusion_list.csv`ファイルを作り、以下のように記述することで校閲対象から除外することができます。なお、正規表現は使えません。

```
SampleFolder/ex_list.md
ProofLeader/README.md
```

## ディレクトリの配置方法

現在`folder_a/`にいて、`folder_b/`内のREADME.mdを修正したいとします。
そのとき、以下のように配置し、**`folder_a/`で [使用方法の起動コマンド](#使用方法)を使用してください。**

```
folder_a/ -- folder_b/
          |- RroofLeader/ -- REAMDE.md
                          |- .version
                          |- XXX.py
```

## 文字列の探索

WARNINGを出すほどでもないけど、全ファイルから特定の文字列を探索したい場合に使用します。
コマンドラインオプションは`-s`または`--search`です。

```sh
python ProofLeader/proofLeader.py -s
```

`/ProofLeader`に`find_list.csv`ファイルを作り、以下のように記述することで校閲対象から除外することができます。なお、正規表現は使えません。

```
探索したい単語1
探索したい単語2
```

出力は以下のようになります。

<pre>
<font color="SteelBlue">FOUND!!</font>: ファイル名:行数:行頭から何文字目: (探索したい単語1)
<font color="SteelBlue">FOUND!!</font>: ファイル名:行数:行頭から何文字目: (探索したい単語2)
</pre>


## 必要なライブラリ及びパッケージ

* Python3 ( 3.6.4 で動作確認済み)
* docopt (v 2.0 以降)

## URL

[https://github.com/xryuseix/ProofLeader](https://github.com/xryuseix/ProofLeader)
