import argparse
import pathlib
import shutil
import subprocess
from util.path          import *

parser = argparse.ArgumentParser(description="rcauto.pyのテストの準備をする。")
parser.add_argument("--clean", action='store_true')
args = parser.parse_args()

downloadDir = mkdir("down")

if args.clean:
    print("Clean up")
    pathlib.Path("tested.txt").unlink(True)
    if getOutputDir().exists():
        shutil.rmtree(getOutputDir())
    if pathlib.Path("work").exists():
        shutil.rmtree("work")

shutil.make_archive(downloadDir / "testrender", "zip", ".", "testrender")
subprocess.run(["g++", "-o", "test", "test.cpp"], cwd = "testrender2")
shutil.make_archive(downloadDir / "testrender2", "zip", ".", "testrender2")

(pathlib.Path(__file__).parent / "downloads.txt").write_text(
    str(downloadDir / "testrender.zip") + "\n" +
    str(downloadDir / "testrender2.zip")
)
