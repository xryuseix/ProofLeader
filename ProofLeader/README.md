# ProofLeader
カレントディレクトリより深い位置にある.mdファイルの句読点や整数表記を修正します。

(変換例)
* `，`は`、`に変換されます。
* `．`は`。`に変換されます。
* ` 100111000 `は` 100,111,000 `に変換されます。
* `abc, def`は変換されません。
* `aは123です`は`a は 123 です`に変換されます。

何がどう変換されるのか、厳密なことはそのうち記述します。

## 使用方法

* 起動コマンド

<pre>
python ProofLeader/proofLeader.py
または
python ProofLeader/proofLeader.py TARGET_DIR/
</pre>

* 期待される出力例

<pre>
folder_a/folder_b/README.md : OK
folder_c/README.md : OK
converter : ALL OK
CHECK!! -> https://competent-morse-3888be.netlify.app/
</pre>

## 機能

* **文章表現の警告機能(ver 1.4で書式が変更になりました)**
`/ProofLeader`に`word_list.csv`ファイルを作り、以下のように記述します。

<pre>
After1,Before1
After2,Before2_1,Before2_2,Before2_3
After3,Before3_1,Before3_2
</pre>

すると以下のようにBeforeが文章に入っていた場合Afterにした方がいいと警告します。

<pre>
WARNING: ファイル名:行数:何文字: (致します) => (いたします)
</pre>

またBeforeはOR指定ができます．
<pre>
A,(B|C)
</pre>
とすると，BまたはCのとき警告します．

### 補足
`<pre></pre>`または` ``` `で囲われている内側の文字に関して、**変換はされません**．ですが、警告は出します。

(例)
```
<pre>
123456 // 123,456にはならない
</pre>
```

```
<pre>
致します // WARNINGが表示されます。
</pre>
```

## 除外ファイルの設定

本プログラムは実行ディレクトリ内の全てのファイルに対して校閲します。
ですが、`/ProofLeader`に`exclusion_list.csv`ファイルを作り、以下のように記述することで校閲対象から除外することができます。なお、正規表現は使えません。

<pre>
SampleFolder/ex_list.md,
ProofLeader/README.md
</pre>

## ディレクトリの配置方法

現在`folder_a/`にいて、`folder_b/`内のREADME.mdを修正したいとします。
そのとき、以下のように配置し、**`folder_a/`で [使用方法の起動コマンド](#使用方法)を使用してください。**

<pre>
folder_a/ -- folder_b/
          |- RroofLeader/ -- REAMDE.md
                          |- .version
                          |- XXX.py
</pre>

## 必要なライブラリ及びパッケージ

* Python3 (3.6.4で動作確認済み)
* pathlib
* sys
* scv
* os
* re

## URL

[https://github.com/xryuseix/ProofLeader](https://github.com/xryuseix/ProofLeader)