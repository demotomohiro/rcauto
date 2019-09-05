import os
import signal
import subprocess
import sys
import time
from util.path          import *

def _run(exe, timeout, logPath):
    print(str(exe) + "を実行中")
    cwd = str(exe.parent)
    pathStdout = logPath.with_suffix('.stdout.txt')
    pathStderr = logPath.with_suffix('.stderr.txt')
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
    with pathStdout.open('wb') as fstdout, pathStderr.open('wb') as fstderr:
        #実行ファイルが.batとか.shだとそこから呼び出される実行ファイルは新しいプロセスとして実行されるようなので
        #subprocess.run()だと子プロセスを終了させることはできない。
        #新しいプロセスグループを作り, 終了させるときはプロセスグループのリーダーにシグナルを送って, グループ全体を終了させる。
        with subprocess.Popen(
            [str(exe)],
            stdout = fstdout, stderr = fstderr,
            cwd = cwd,
            start_new_session = True, creationflags = creationflags) as proc:
            startTime = time.time()
            endTime = 0
            try:
                proc.wait(timeout)
                endTime = time.time()
            except subprocess.TimeoutExpired:
                print("Time out!!!")
            finally:
                if proc.poll() == None:
                    print("Killing process")
                    if sys.platform == 'win32':
                        proc.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        os.killpg(proc.pid, signal.SIGKILL)
                    proc.kill()
                #proc.poll() != Noneでも子プロセスが終了したかどうかは確認できないけど・・・
                print(str(exe) + "を実行した。ふぅ")
                if endTime >= startTime:
                    print("実行時間: " + str(endTime - startTime) + "秒")

    if pathStderr.stat().st_size == 0:
        for i in range(5):
            try:
                pathStderr.unlink()
            except PermissionError:
                time.sleep(1)
                continue
            break

def render(exe, timeout, logPath):
    _run(exe, timeout, logPath)
