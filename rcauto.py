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
parser.add_argument("--timelimit", default = 123, type = int, help = "制限時間(秒)")
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
outputDir   = getOutputDir()
archives    = []
testedListFile = pathlib.Path("tested.txt")
testeds     = set()
with testedListFile.open() as f:
    for i in f.readlines():
        l = i.strip()
        if len(l) == 0 or l.startswith("#"):
            continue
        testeds.add(l)

for i in downloads:
    path = getDownloadDestPath(i, downloadDir)
    if path.name in testeds:
        continue
    download(i, path)
    archives.append(path)

for path in archives:
    prodName = path.stem.split('.')[0]
    prodDir = workDir / prodName
    if isFinished(prodName):
        print(prodName + "のレンダリングはもうしなくていいんだ。")
        continue
    if prodDir.exists():
        try:
            shutil.rmtree(str(prodDir))
        except OSError:
            time.sleep(4)
            shutil.rmtree(str(prodDir))
    shutil.unpack_archive(str(path), str(prodDir))
    with testedListFile.open('at') as f:
        print(path.name, file = f)
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
    render(exe, args.timelimit, getStdoutDir() / prodName)
    if not copyOutputs(prodDir, prodName, startTime):
        print(str(exe) + "の出力画像が無い。なにかがおかしい。")

