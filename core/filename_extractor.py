import subprocess
import os
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
        
        # command += ["--cookies-from-browser", "chrome"]
        if os.path.exists("./assets/cookies.txt"):
            command += ["--cookies", "./assets/cookies.txt"]
        
        command += ["--js-runtimes", "node"]

        command.append(url)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(
            command,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            startupinfo=startupinfo,
            shell=False
        )

        # stdout, stderr = result.communicate()

        if result.returncode != 0:
            raise Exception(result.stderr)
        

        return result.stdout.strip()