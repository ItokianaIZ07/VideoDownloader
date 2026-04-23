import subprocess
import re


class Downloader:
    def __init__(self):
        self.yt_dlp_path = "./bin/yt-dlp.exe"

    def download(self, url, format="mp4", output_path=".", progress_callback=None):
        command = [self.yt_dlp_path, "--newline"]

        # Format
        if format == "mp3":
            command += ["-x", "--audio-format", "mp3"]
        else:
            command += ["-f", "mp4"]

        # Output path
        command += ["-o", f"{output_path}/%(title)s.%(ext)s"]

        command.append(url)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            percent = self._extract_progress(line)

            if percent is not None and progress_callback:
                progress_callback(percent)

    def _extract_progress(self, text):
        match = re.search(r'(\d+\.\d+)%', text)
        if match:
            return float(match.group(1)) / 100  # 0 → 1
        return None