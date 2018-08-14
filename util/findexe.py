import stat
import sys

def _isExecutable(path):
    return path.stat().st_mode & stat.S_IXUSR != 0

def _findExeRecursive(dir, candidates):
    for i in dir.iterdir():
        if i.is_dir():
            _findExeRecursive(i, candidates)
        else:
            if _isExecutable(i):
                candidates.append(i)

def findExe(dir):
    if sys.platform == 'win32':
        candidates = list(dir.glob("**/*.bat"))
        candidates.extend(dir.glob("**/*.cmd"))
        if len(candidates) == 0:
            candidates = list(dir.glob("**/*.exe"))
    else:
        shs = list(dir.glob("**/*.sh"))
        candidates = [i for i in shs if _isExecutable(i)]
        if len(candidates) == 0:
            _findExeRecursive(dir, candidates)

    if len(candidates) == 0:
        print("実行ファイルないやんけ！！")
        return ""

    if len(candidates) > 1:
        print("どれを実行したらいいかわからんやんけ！！")
        return ""

    return candidates[0]

