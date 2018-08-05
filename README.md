# rcauto
レイトレ合宿における作品を自動実行するやつ

## 必要なもの
* python3.5かpython3.6以上
現状ではpython3の標準ライブラリのみを使用。できるだけ依存関係を少なくしてインストールの手間を省く。

## 使い方
```
usage: python3 rcauto.py [-h] [--src URL] [--timelimit TIMELIMIT]

optional arguments:
  -h, --help            show this help message and exit
  --src URL             ダウンロードするファイルがあるページのURL
  --timelimit TIMELIMIT
                        レンダリングの制限時間(秒)
```

## 実行内容
1. --srcオプションして指定したwebページを読み込み, ダウンロードする作品の圧縮ファイルのURLのリストをdownloads.txtファイルに書き込む。
既にdownloads.txtが存在する場合はこのステップは実行されない。
1. downloads.txtを読み込んで作品すべてをdownディレクトリへダウンロードする。
downディレクトリに既にファイルが存在する場合は再ダウンロードされない。
1. 圧縮ファイルを解凍する。
1. 実行ファイルを特定する。
windowsでは.batファイルを最初に探し、もし見つかればそれを実行する。
なかった場合は.exeファイルが実行される。
Linuxでは.shファイルを最初に探し、次に実行権限のあるファイルを探す。
もし複数の.bat/.sh/.exeファイルがある場合はエラーになる。
1. 実行ファイルを実行する。
制限時間が経過すると強制終了される。
1. 出力画像ファイル(.bmpまたは.png)を探して、output/image/"圧縮ファイル名"ディレクトリ下にコピーする。

