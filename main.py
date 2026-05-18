from ui.app import App
from core.ressource import Ressource
from datetime import datetime

if __name__ == "__main__":
    try:
        # ytDlp = Ressource.getYTDLP()
        # print("PATH ",ytDlp)
        # print("EXISTS ",os.path.exists(ytDlp))
        # print("BASE ",sys._MEIPASS if hasattr(sys, "_MEIPASS") else "NO MEIPASS")
        app = App()
        app.mainloop()
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"[{now}] ERROR LOG\n")
            f.write("-----------------\n")
            f.write(str(e) + "\n")