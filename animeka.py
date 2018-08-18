import shutil
import subprocess
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

    animeBase = animeDir / i.name
    concatFile = animeBase.with_suffix(".con.txt")
    animeFile = animeBase.with_suffix(".apng")

    with concatFile.open('w') as fcon:
        print("ffconcat version 1.0", file = fcon)
        for img in images:
            print("file", "'" + str(img) + "'", file = fcon)

    subprocess.run(["ffmpeg", "-r", "3", "-safe", "0", "-i", str(concatFile), "-plays", "0", str(animeFile)], cwd = str(i), check = True)

