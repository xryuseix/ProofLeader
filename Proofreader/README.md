# Proofreader
カレントディレクトリより深い位置にいあるREADME.mdの句読点や整数表記を修正します．

* `，`は`、`に変換されます．
* `．`は`。`に変換されます．
* `100111000`は`100,111,000`に変換されます．
* `abc, def`は変換されません．

## 使用方法

* 起動コマンド

```sh
sh Proofreader/proofreader.sh
```

* 期待される出力例

```zsh
folder_a/folder_b/README.md : OK
folder_c/README.md : OK
converter : ALL OK
CHECK!! -> https://competent-morse-3888be.netlify.app/
```

* 文章表現の警告機能
同一ディレクトリに`word_list.csv`ファイルを作り，以下のように記述します．

```
Before,After
Before,After
Before,After
```

するとBeforeが文章に入っていた場合Afterにした方がいいと警告します．
~Before,Afterは正規表現で記述してください．~
正規表現で書きたいのですが，現在`(|)`の三文字くらいしか使えません．ごめんなさい><

## ディレクトリの配置方法

現在`folder_a/`にいて，`folder_b/`内のREADME.mdを修正したいとします．
その時，以下のように配置し，**`folder_a/`で [使用方法の起動コマンド](#使用方法)を使用してください．**

```
folder_a/ -- folder_b/
          |- Rroofreader/
```

## 必要なライブラリ及びパッケージ

* Python3(3.6.4以上)
* pathlib
* sys
* scv
* os
* re