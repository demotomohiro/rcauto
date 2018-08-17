import pathlib
import shutil

def abspath(path):
    return pathlib.Path(path).resolve()

def mkdir(path):
    p = pathlib.Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return abspath(p)

_outputDir   = mkdir("out")
def getOutputDir():
    return _outputDir

_stdoutDir  = mkdir(getOutputDir() / "stdout")
def getStdoutDir():
    return _stdoutDir

def _copyfile(src, dst):
    return shutil.copy2(str(src), str(dst))

def _copyOutputs(dir, startTime, prodOutputDir, prodImageDir, foundImage = False):
    for i in dir.iterdir():
        if i.is_dir():
            if _copyOutputs(i, startTime, prodOutputDir, prodImageDir, foundImage):
                foundImage = True
        else:
            if i.stat().st_mtime > startTime:
                if i.suffix == '.bmp' or i.suffix == '.png':
                    if foundImage == False:
                        mkdir(prodImageDir)
                        print(str(dir) + "内のレンダリング画像をコピー中。")
                    foundImage = True
                    _copyfile(i, prodImageDir)
                else:
                    mkdir(prodOutputDir)
                    _copyfile(i, prodOutputDir)
    return foundImage

def _getProdOutputDir(prodName):
    return getOutputDir() / "output" / prodName

def _getProdImageDir(prodName):
    return getOutputDir() / "image" / prodName

def _getProdSlideDir(prodOutputDirBase, prodName):
    return prodOutputDirBase / "slide" / prodName

def isFinished(prodName):
    return _getProdImageDir(prodName).exists()

def copyOutputs(dir, prodName, startTime):
    return _copyOutputs(dir, startTime, _getProdOutputDir(prodName), _getProdImageDir(prodName))

def copySlides(dir, prodOutputDirBase, prodName):
    dstDir = _getProdSlideDir(prodOutputDirBase, prodName)
    srcs = []
    for i in ["*.pdf", "*.pptx", "*.key"]:
        srcs.extend(dir.rglob(i))
    if len(srcs) == 0:
        return False
    mkdir(dstDir)
    for i in srcs:
        _copyfile(i, dstDir)

    return True
