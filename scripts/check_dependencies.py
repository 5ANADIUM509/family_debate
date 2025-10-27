"""检查并确保所有依赖项都已安装"""

import importlib
import subprocess
import sys

REQUIREMENTS = [
    "dotenv",
    "requests",
    "tkinter"
]

def check_dependencies():
    missing = []
    for pkg in REQUIREMENTS:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"检测到缺失的依赖项：{', '.join(missing)}")
        confirm = input("是否安装这些依赖项？(y/n) ")
        if confirm.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("依赖项安装完成")
        else:
            print("请手动安装缺失的依赖项后再运行程序")
            sys.exit(1)
    else:
        print("所有依赖项都已正确安装")

if __name__ == "__main__":
    check_dependencies()