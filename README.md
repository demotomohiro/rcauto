# rcauto
レイトレ合宿における作品を自動実行するやつ。
作品の圧縮形式は基本的にpython3のshutil.unpack_archiveが対応しているものなら解凍できる。(zip, tar, tar.gz, tar.bz2, tar.xz)

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
このプログラムから出力されるファイルとディレクトリはカレントディレクトリ下に作られる。
1. --srcオプションして指定したwebページを読み込み, ダウンロードする作品の圧縮ファイルのURLのリストをdownloads.txtファイルに書き込む。
既にdownloads.txtが存在する場合はこのステップは実行されない。
1. downloads.txtを読み込んで作品すべてをdownディレクトリへダウンロードする。
downディレクトリに既にファイルが存在する場合は再ダウンロードされない。
1. out/image/"圧縮ファイル名"ディレクトリが既に存在する場合は既にレンダリングが完了したものと見なし以下の処理は実行されない。
1. 圧縮ファイルをworkディレクトリ下に解凍する。
1. 発表スライドのファイルをout/slide/"圧縮ファイル名"ディレクトリ下にコピーする。
1. 実行ファイルを特定する。
windowsでは.bat/.cmdファイルを最初に探し、もし見つかればそれを実行する。
なかった場合は.exeファイルが実行される。
Linuxでは.shファイルを最初に探し、次に実行権限のあるファイルを探す。
もし複数の.bat/.sh/.exeファイルがある場合はエラーになる。
1. レンダラーを実行する。
制限時間が経過すると強制終了される。
stdoutとstderrはout/"圧縮ファイル名".stdout.txtとout/"圧縮ファイル名".stderr.txtに保存する。
1. 出力画像ファイル(.bmpまたは.png)を探して、out/image/"圧縮ファイル名"ディレクトリ下にコピーする。
1. 出力画像ファイル以外に生成されたファイル(ログファイル等)があればout/output/"圧縮ファイル名"ディレクトリ下にコピーする。
