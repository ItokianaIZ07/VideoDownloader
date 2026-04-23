import os
import sys

class Ressource:
    
    def __ressource_path(relative_path):
        try:
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)
    
    @staticmethod
    def getYTDLP():
        return Ressource.__ressource_path("./bin/yt-dlp.exe")
    
    @staticmethod
    def getIcon():
        return Ressource.__ressource_path("./assets/icon.ico")