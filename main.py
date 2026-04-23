from ui.app import App
from core.ressource import Ressource
import os
import sys

if __name__ == "__main__":
    try:
        # ytDlp = Ressource.getYTDLP()
        # print("PATH ",ytDlp)
        # print("EXISTS ",os.path.exists(ytDlp))
        # print("BASE ",sys._MEIPASS if hasattr(sys, "_MEIPASS") else "NO MEIPASS")
        app = App()
        app.mainloop()
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))
        