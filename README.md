# rcauto
レイトレ合宿における作品を自動実行するやつ。

作品の圧縮形式は基本的にpython3のshutil.unpack_archiveが対応しているものなら解凍できる。(zip, tar, tar.gz, tar.bz2, tar.xz)

rcauto.pyはwebページから作品リストの取得、作品のダウンロードから実行と出力ファイルを一か所に纏める処理を行う。

animeka.pyは画像ファイルのリストをffmpegを使って1つの動画ファイルに変換する。

Linux用レンダラは実行ファイルの特定ができるように実行ファイルには実行権限をつけ、ファイルのパーミッションが保存されるように圧縮して提出してもらわないと困る。

## 必要なもの
* python3.5かpython3.6以上

現状ではpython3の標準ライブラリのみを使用。できるだけ依存関係を少なくしてインストールの手間を省く。

## 使い方
```
python3 rcauto.py [-h] [--src URL] [--timelimit TIMELIMIT]

optional arguments:
  -h, --help            show this help message and exit
  --src URL             ダウンロードするファイルがあるページのURL
  --timelimit TIMELIMIT
                        レンダリングの制限時間(秒)
```

animeka.pyはrcauto.pyを実行した後に同じディレクトリで実行する
```
python3 animeka.py
```

## 実行内容
### rcauto.py
このプログラムから出力されるファイルとディレクトリはカレントディレクトリ下に作られる。
1. --srcオプションして指定したwebページを読み込み、ダウンロードする作品の圧縮ファイルのURLのリストをdownloads.txtファイルに書き込む。
   - 既にdownloads.txtが存在する場合はこのステップは実行されない。
1. downloads.txtを読み込んで作品すべてをdownディレクトリへダウンロードする。
   - downディレクトリに既にファイルが存在する場合は再ダウンロードされない。
1. out/image/"圧縮ファイル名"ディレクトリが既に存在する場合は既にレンダリングが完了したものと見なし以下の処理は実行されない。
1. 圧縮ファイルをworkディレクトリ下に解凍する。
1. 発表スライドのファイルをout/slide/"圧縮ファイル名"ディレクトリ下にコピーする。
1. 実行ファイルを特定する。
   - windowsでは.bat/.cmdファイルを最初に探し、もし見つかればそれを実行する。なかった場合は.exeファイルを探す。
   - Linuxでは.shファイルを最初に探し、次に実行権限のあるファイルを探す。
   - もし複数の.bat/.sh/.exeファイルがあればエラーになる。
1. レンダラーを実行する。
   - 制限時間が経過すると強制終了される。
   - stdoutとstderrはout/stdout/"圧縮ファイル名".stdout.txtとout/stdout/"圧縮ファイル名".stderr.txtに保存する。
1. 出力画像ファイル(.bmpまたは.png)を探して、out/image/"圧縮ファイル名"ディレクトリ下にコピーする。
1. 出力画像ファイル以外に生成されたファイル(ログファイル等)があればout/output/"圧縮ファイル名"ディレクトリ下にコピーする。

### animeka.py
1. out/imageディレクトリ下にある各ディレクトリに対して以下の処理を行う。
1. ディレクトリ内の.png, .bmpファイルのリストを取得する。
1. リストの内容を元に.con.txtファイルをout/animeディレクトリに作成する。
   - .con.txtファイルはffmpegのconcat Demuxerで使われる(https://www.ffmpeg.org/ffmpeg-formats.html#concat-1)。
1. ffmpegを使ってレンダリング経過画像を一つの動画ファイルに変換し、out/animeディレクトリに出力する。
