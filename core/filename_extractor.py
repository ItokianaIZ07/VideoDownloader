import subprocess
from core.ressource import Ressource


class FilenameExtractor:

    def __init__(self):
        self.yt_dlp_path = Ressource.getYTDLP()

    def get_filename(self, url, format="mp4"):
        command = [
            self.yt_dlp_path,
            "--print", "filename",
            "-o", "%(title)s.%(ext)s",
        ]

        if format == "mp3":
            command += ["-x", "--audio-format", "mp3"]

        command.append(url)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            startupinfo=startupinfo,
            shell=False
        )

        return result.stdout.strip()