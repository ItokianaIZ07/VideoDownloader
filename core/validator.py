import re
import subprocess

class LinkValidator:

    YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"

    @staticmethod
    def is_valid_url(url: str) :
        return re.match(LinkValidator.YOUTUBE_REGEX, url) is not None
    
    @staticmethod
    def is_accessible(self, url: str) -> bool:
        yt_dlp_path = "./bin/yt-dlp.exe"
        try:
            result = subprocess.run(
                [yt_dlp_path, "--simulate", "--quiet", url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            return result.returncode == 0

        except Exception:
            return False