import shutil
import subprocess
import time
from util.path          import *

if shutil.which("ffmpeg") == None:
    raise FileNotFoundError("ffmpegぐらい入れとけや")

imageDir = getImageDir()
if not imageDir.is_dir():
    raise NotADirectoryError(str(imageDir) + "がないぞ")

animeDir = mkdir(getAnimeDir())

for i in imageDir.iterdir():
    if not i.is_dir():
        print(str(imageDir) + "に不審なファイルがあるぞ")
        continue

    images = list(i.glob('*.png'))
    images.extend(i.glob('*.bmp'))
    images.extend(i.glob('*.jpg'))
    images.sort()

    fpsFilePath = i / "fps.txt"
    try:
        fps = int(fpsFilePath.read_text())
    except ValueError:
        # powershellでecho 30 > fps.txtとするとBOMつきのutf-16-leになる。
        # その場合encodingを指定しないと正しく読み込めない。
        fps = int(fpsFilePath.read_text(encoding='utf-16'))

    animeBase = animeDir / i.name
    concatFile = animeBase.with_suffix(".con.txt")
    animeFile = animeBase.with_suffix(".mp4")

    with concatFile.open('w') as fcon:
        print("ffconcat version 1.0", file = fcon)
        for img in images:
            print("file", "'" + str(img) + "'", file = fcon)

    print(f"[{time.strftime('%X')}] {str(i)}にあるファイルから動画を作成開始。")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-r", str(fps), "-safe", "0", "-i", str(concatFile), "-plays", "0", "-c:v", "libx264", "-crf", "18", str(animeFile)], cwd = str(i), check = True)
    print(f"[{time.strftime('%X')}] {str(i)}にあるファイルから動画を作成した。")
