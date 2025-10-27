import tkinter as tk
from src.gui.debate_gui import DebateGUI

def main():
    """程序入口函数"""
    root = tk.Tk()
    # 确保中文显示正常
    root.option_add("*Font", "SimHei")
    app = DebateGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()