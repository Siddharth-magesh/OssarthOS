import subprocess
import webbrowser
import time

CONDA_PATH = r"C:\Users\Siddharth\anaconda3\condabin\conda.bat"

process = subprocess.Popen(
    f'cmd.exe /c "{CONDA_PATH} activate d:/smart && pip install -r D:/OssarthOS/requirements.txt && python D:/OssarthOS/app.py"',
    shell=True
)
time.sleep(10)

webbrowser.open("http://127.0.0.1:3000")

process.wait()
