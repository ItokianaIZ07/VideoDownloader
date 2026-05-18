import subprocess
import re
import sys
import os
from core.ressource import Ressource


class Downloader:
    def __init__(self):
        self.yt_dlp_path = Ressource.getYTDLP()
        self.cookies = Ressource.getCookies()
        self.process = None

    def start_download_process(self, url, format="mp4", output_path=".", progress_callback=None):

        command = [self.yt_dlp_path, "--newline"]

        # Format
        if format == "mp3":
            command += ["-x", "--audio-format", "mp3"]
        else:
            command += ["-f", "mp4"]

        # command += ["--cookies-from-browser", "edge"]
        if os.path.exists(self.cookies):
            command += ["--cookies", self.cookies]

        command += ["--js-runtimes", "node"]
        

        # Output path
        command += ["-o", f"{output_path}/%(title)s.%(ext)s"]

        command.append(url)

        self.process = self.__run_process(command)

        return self.process

    def wait_process(self, process, stop_event=None, progress_callback=None):

        while True:
            if stop_event and stop_event.is_set():
                process.terminate()
                return False

            line = process.stdout.readline()
            if not line:
                break

            # percent = self._extract_progress(line)

            # if percent is not None and progress_callback:
            #     progress_callback(percent)

            info = self._extract_download_info(line)

            if info and progress_callback:
                progress_callback(info)

        process.wait()
        return process.returncode == 0

    def download(self, url, format="mp4", output_path=".", progress_callback=None):

        process = self.start_download_process(url, format, output_path, progress_callback)

        return self.wait_process(process, False, progress_callback)


    def _extract_progress(self, text):
        match = re.search(r'(\d+\.\d+)%', text)
        if match:
            return float(match.group(1)) / 100
        return None

    def __run_process(self, command):
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo,
                shell=False
            )
        else:
            return subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=False
            )

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def _extract_download_info(self, text):
        # Exemple ligne yt-dlp :
        # [download]  45.3% of 120.50MiB at 1.20MiB/s ETA 00:32

        match = re.search(
            r'(\d+(?:\.\d+)?)%\s+of\s+([\S]+).*?at\s+([\S]+).*?ETA\s+([\S]+)',
            text
        )

        if match:
            percent = float(match.group(1)) / 100
            total_size = match.group(2).strip()
            speed = match.group(3).strip()
            eta = match.group(4).strip()

            return {
                "percent": percent,
                "total": total_size,
                "speed": speed,
                "eta": eta
            }

        # fallback si ligne partielle (yt-dlp n'affiche pas toujours tout)
        match_simple = re.search(
            r'(\d+(?:\.\d+)?)%\s+of\s+([\d\.]+\s*\w+)',
            text
        )

        if match_simple:
            percent = float(match_simple.group(1)) / 100
            total_size = match_simple.group(2).strip()

            return {
                "percent": percent,
                "total": total_size,
                "speed": "N/A",
                "eta": "N/A"
            }

        return None