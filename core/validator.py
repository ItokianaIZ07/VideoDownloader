import re
import subprocess
from core.ressource import Ressource

class LinkValidator:

    YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"

    @staticmethod
    def is_valid_url(url: str) :
        return re.match(LinkValidator.YOUTUBE_REGEX, url) is not None
    
    @staticmethod
    def is_accessible(url: str) -> bool:
        yt_dlp_path = Ressource.getYTDLP()
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            result = subprocess.run(
                [yt_dlp_path, "--simulate", "--quiet", url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo,
                shell=False
            )

            return result.returncode == 0   

        except Exception:
            return False
        
    @staticmethod
    def is_playList(url: str)->bool:
        return url.__contains__("list")
        
import socket
class NetworkValidator:
    @staticmethod
    def is_connected():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=20)
            return True
        except OSError:
            return False