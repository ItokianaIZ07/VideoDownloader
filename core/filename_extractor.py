import subprocess


class FilenameExtractor:

    def __init__(self):
        self.yt_dlp_path = "./bin/yt-dlp.exe"

    def get_filename(self, url, format="mp4"):
        command = [
            self.yt_dlp_path,
            "--print", "filename",
            "-o", "%(title)s.%(ext)s",
        ]

        if format == "mp3":
            command += ["-x", "--audio-format", "mp3"]

        command.append(url)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()