# from core.downloader import Downloader

# downloader = Downloader()

# downloader.download_video("https://www.youtube.com", "mp3")

from ui.app import App

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))
        