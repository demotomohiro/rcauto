import argparse
import pathlib
import shutil
import urllib.parse
import urllib.request
from util.downloadlist  import *
from util.findexe       import *
from util.render        import *
from util.path          import *

parser = argparse.ArgumentParser(description="レイトレ合宿における作品を自動実行するやつ")
parser.add_argument("--src", help = "ダウンロードするファイルがあるページのURL", metavar="URL")
parser.add_argument("--timelimit", type=int, help = "制限時間(秒)")
args = parser.parse_args()

downloadsTxt = pathlib.Path("downloads.txt")
if not downloadsTxt.exists() or args.src != None:
    if args.src == None:
        parser.print_help()
        parser.exit()
    writeDownloadList(args.src, downloadsTxt)
    print("webページからダウンロードする作品のリストを取ってきた。")

with downloadsTxt.open() as downloadsFile:
    downloads = [i for i in [i.strip() for i in downloadsFile.readlines()] if len(i) != 0 and not i.startswith("#")]

downloadDir = mkdir("down")
workDir     = mkdir("work")
outputDir   = mkdir("out")
archives    = []
for i in downloads:
    path = download(i, getDownloadDestPath(i, downloadDir))
    archives.append(path)

for path in archives:
    prodName = path.stem.split('.')[0]
    prodDir = workDir / prodName
    if isFinished(outputDir, prodName):
        print(prodName + "のレンダリングはもうしなくていいんだ。")
        continue
    if prodDir.exists():
        try:
            shutil.rmtree(str(prodDir))
        except OSError:
            time.sleep(4)
            shutil.rmtree(str(prodDir))
    shutil.unpack_archive(str(path), str(prodDir))
    if not copySlides(prodDir, outputDir, prodName):
        print(prodName + "のスライドが無いんですが")
    exe = findExe(prodDir)
    if not exe:
        print(prodName + "のレイトレは実行しようがない")
        continue
    startTime = time.time()
    #ファイルのタイムスタンプを見て元からあるファイルなのか出力ファイルなのかを区別する。
    #なので確実に出力ファイルのタイムがstartTimeより後になるようsleepする。
    time.sleep(4)
    render(exe, args.timelimit, outputDir/prodName)
    if not copyOutputs(prodDir, outputDir, prodName, startTime):
        print(str(exe) + "の出力画像が無い。なにかがおかしい。")

