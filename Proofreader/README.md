#  Proofre a  e      r カレントディレクトリより深い位置にいある m d     ファイルの句読点や整数表記を修正します。

* `，`は`、`に変換されます。
* `．`は`。`に変換されます。
* `                          10              ,                          11              ,                          00              `は`                          10              ,                          11              ,                          00              `に変換されます。
* ` a  c     ,  d  f     `は変換されません。

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
同一ディレクトリに` w o  d     _ l i  t     . c  v     `ファイルを作り、以下のように記述します。

```
Before,After
Before,After
Before,After
```

すると Bef o  e     が文章に入っていた場合 Af t  r     にした方がいいと警告します。
B     ef o  e     は正規表現で記述できます。

## ディレクトリの配置方法

現在` fol d  r     _ a     /`にいて、` fol d  r     _ b     /`内の REA D  E     . m d     を修正したいとします。
その時、以下のように配置し、**` fol d  r     _ a     /`で [使用方法の起動コマンド](#使用方法)を使用してください。**

```
folder_a/ -- folder_b/
          |- Rroofreader/
```

## 必要なライブラリ及びパッケージ

*  Pyt h  n                               3             (                          3             .                          6             .                          4             以上)
*  pat h  i      b *  s y      s *  s c      v *  o      s *  r      e
