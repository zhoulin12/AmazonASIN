import PyInstaller.__main__
import os
import sys
import subprocess
import playwright

base_path = os.path.dirname(os.path.abspath(__file__))
pw_dir = os.path.dirname(playwright.__file__)
browsers_dir = os.path.join(pw_dir, "driver", "package", ".local-browsers")

env = os.environ.copy()
env["PLAYWRIGHT_BROWSERS_PATH"] = "0"
if not os.path.exists(browsers_dir) or not os.listdir(browsers_dir):
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, env=env)

add_data = f"{browsers_dir};playwright/driver/package/.local-browsers"

PyInstaller.__main__.run([
    "asin.py",
    "--name=AmazonSpider",
    "--onefile",
    "--console",
    "--clean",
    "--collect-all=playwright",
    "--collect-all=openpyxl",
    "--collect-all=xlsxwriter",
    "--collect-all=pandas",
    "--collect-all=bs4",
    "--collect-all=PIL",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.PngImagePlugin",
    "--hidden-import=PIL.JpegImagePlugin",
    "--add-data", add_data,
])
