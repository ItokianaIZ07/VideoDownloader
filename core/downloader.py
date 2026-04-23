import subprocess


class Downloader:

    def __init__(self):
        self.__downloader = "./bin/yt-dlp.exe"

    def download_video(self, url, format="mp4"):
        if format == "mp3":
            cmd = [f"{self.__downloader}", "-x", "--audio-format", "mp3", url]
        else:
            cmd = [f"{self.__downloader}", "-f", "mp4", url]

        subprocess.run(cmd)