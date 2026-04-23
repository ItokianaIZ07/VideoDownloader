import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox

from core.downloader import Downloader
from core.validator import LinkValidator, NetworkValidator
from core.filename_extractor import FilenameExtractor
from core.ressource import Ressource

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def get_default_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")


class NavBar(ctk.CTkFrame):
    def __init__(self, parent, on_nav_change):
        super().__init__(parent, width=120)
        self.pack_propagate(False)

        self.on_nav_change = on_nav_change

        ctk.CTkButton(self, text="🏠 Home",
                      command=lambda: self.on_nav_change("home")).pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(self, text="⚙️ Paramètres",
                      command=lambda: self.on_nav_change("settings")).pack(fill="x", padx=10, pady=10)


class URLInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Lien YouTube").pack(anchor="w", padx=10, pady=(10, 5))

        self.entry = ctk.CTkEntry(self, placeholder_text="https://youtube.com/...")
        self.entry.pack(fill="x", padx=10, pady=(0, 10))

    def get_url(self):
        return self.entry.get()


class FormatSelector(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Format").pack(anchor="w", padx=10, pady=(10, 5))

        self.var = ctk.StringVar(value="mp4")

        ctk.CTkOptionMenu(self, variable=self.var, values=["mp4", "mp3"]).pack(
            padx=10, pady=(0, 10), anchor="w"
        )

    def get_format(self):
        return self.var.get()


class ProgressBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Progression").pack(anchor="w", padx=10, pady=(10, 5))

        self.bar = ctk.CTkProgressBar(self)
        self.bar.pack(fill="x", padx=10, pady=(0, 10))
        self.bar.set(0)

    def set_progress(self, value):
        self.bar.set(value)


class FilenameDisplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Vidéo").pack(anchor="w", padx=10, pady=(10, 5))

        self.label = ctk.CTkLabel(self, text="Aucune vidéo sélectionnée")
        self.label.pack(anchor="w", padx=10, pady=(0, 10))

    def set_filename(self, name):
        self.label.configure(text=name)


class StatusDisplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Statut").pack(anchor="w", padx=10, pady=(10, 5))

        self.label = ctk.CTkLabel(self, text="En attente...")
        self.label.pack(anchor="w", padx=10, pady=(0, 10))

    def set_status(self, text, color="white"):
        self.label.configure(text=text)

        colors = {
            "green": "lightgreen",
            "red": "red",
            "orange": "orange",
            "white": "white"
        }

        self.label.configure(text_color=colors.get(color, "white"))


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.downloader_process = None
        self.downloading = False

        self.url_input = URLInput(self)
        self.url_input.pack(fill="x", pady=5)

        self.format_selector = FormatSelector(self)
        self.format_selector.pack(fill="x", pady=5)

        self.filename_display = FilenameDisplay(self)
        self.filename_display.pack(fill="x", pady=5)

        self.progress = ProgressBar(self)
        self.progress.pack(fill="x", pady=5)

        self.status = StatusDisplay(self)
        self.status.pack(fill="x", pady=5)

        self.downloadButton = ctk.CTkButton(self, text="Télécharger", command=self.on_download)

        
        self.downloadButton.pack(fill="x", padx=10, pady=10)

    # =========================
    # Pour modifier les composants sans crash
    # =========================
    def safe_ui(self, func):
        self.after(0, func)

    def reset_button(self):
            self.downloadButton.configure(text="Télécharger")
            self.downloading = False
            self.stop_download = False

    def on_download(self):
        if self.downloading:
            self.stop_download = True

            if self.downloader_process:
                self.downloader_process.terminate()

            self.downloadButton.configure(text="Télécharger")
            self.downloading = False
            self.status.set_status("Annulation...", "orange")
            return

        self.stop_download = False
        self.downloading = True
        self.downloadButton.configure(text="Annuler")

        downloader = Downloader()
        extractor = FilenameExtractor()

        url = self.url_input.get_url().strip()
        fmt = self.format_selector.get_format()

        self.progress.set_progress(0)
        self.status.set_status("Chargement...", "orange")

        if url == "":
            messagebox.showerror("Erreur", "Veuillez entrer un lien")
            self.reset_button()
            return

        if not LinkValidator.is_valid_url(url):
            messagebox.showerror("Erreur", "Lien invalide")
            self.reset_button()
            return

        if not NetworkValidator.is_connected():
            messagebox.showerror("Erreur", "Pas de connexion internet")
            self.reset_button()
            return

        def update_progress(value):
            self.safe_ui(lambda: self.progress.set_progress(value))

        def run():
            try:
                filename = extractor.get_filename(url, fmt)

                self.safe_ui(lambda: self.filename_display.set_filename(filename))
                self.safe_ui(lambda: self.status.set_status("Téléchargement en cours...", "orange"))

                self.downloader_process = downloader.start_download_process(
                    url=url,
                    format=fmt,
                    output_path=self.app.pages["settings"].get_download_path(),
                    progress_callback=update_progress
                )

                success = downloader.wait_process(self.downloader_process, self.stop_download, update_progress) # ty no modification(nampiana update_progress)

                if self.stop_download:
                    self.safe_ui(lambda: self.status.set_status("Annulé ❌", "red"))
                elif success:
                    self.safe_ui(lambda: self.status.set_status("Téléchargement terminé ✅", "green"))
                else:
                    self.safe_ui(lambda: self.status.set_status("Échec ❌", "red"))

            except Exception as e:
                with open("error.log", "w") as f:
                    f.write(str(e))

                self.safe_ui(lambda: self.status.set_status("Erreur ❌", "red"))

            finally:
                self.safe_ui(self.reset_button)

        threading.Thread(target=run).start()
    


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Paramètres", font=("Arial", 16))\
            .pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(self, text="Dossier de téléchargement")\
            .pack(anchor="w", padx=10, pady=(10, 5))

        self.path_var = ctk.StringVar(value=get_default_download_path())

        self.entry = ctk.CTkEntry(self, textvariable=self.path_var)
        self.entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(self, text="Choisir un dossier", command=self.choose_folder)\
            .pack(anchor="w", padx=10, pady=10)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def get_download_path(self):
        return self.path_var.get()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.iconbitmap(Ressource.getIcon())
        self.geometry("800x550")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navbar = NavBar(self, self.switch_page)
        self.navbar.grid(row=0, column=0, sticky="ns")

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")

        self.pages = {
            "home": HomePage(self.container, self),
            "settings": SettingsPage(self.container, self)
        }

        self.current_page = None
        self.switch_page("home")

    def switch_page(self, name):
        if self.current_page:
            self.current_page.pack_forget()

        self.current_page = self.pages[name]
        self.current_page.pack(fill="both", expand=True)