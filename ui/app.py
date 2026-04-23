import customtkinter as ctk
import os
import threading
from tkinter import filedialog
from tkinter import messagebox
from core.downloader import Downloader
from core.validator import LinkValidator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


#  UTIL : dossier téléchargement par défaut
def get_default_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

class NavBar(ctk.CTkFrame):
    def __init__(self, parent, on_nav_change):
        super().__init__(parent, width=120)
        self.pack_propagate(False)

        self.on_nav_change = on_nav_change

        self.home_btn = ctk.CTkButton(self, text="🏠 Home",
                                     command=lambda: self.on_nav_change("home"))
        self.home_btn.pack(fill="x", padx=10, pady=10)

        self.settings_btn = ctk.CTkButton(self, text="⚙️ Paramètres",
                                         command=lambda: self.on_nav_change("settings"))
        self.settings_btn.pack(fill="x", padx=10, pady=10)

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

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.url_input = URLInput(self)
        self.url_input.pack(fill="x", pady=5)

        self.format_selector = FormatSelector(self)
        self.format_selector.pack(fill="x", pady=5)

        self.progress = ProgressBar(self)
        self.progress.pack(fill="x", pady=5)

        self.button = ctk.CTkButton(self, text="Télécharger", command=self.on_download)
        self.button.pack(fill="x", padx=10, pady=10)

    def on_download(self):
        downloader = Downloader()

        def update_progress(value):
            self.progress_bar.set_progress(value)

        def run():
            downloader.download(
                url=self.url_input.get_url(),
                format=self.format_selector.get_format(),
                output_path=self.app.pages["settings"].get_download_path(),
                progress_callback=update_progress
            )

        url = self.url_input.get_url()

        if url.strip() == "":
            messagebox.showerror("Erreur", "Veuillez entrer un lien")
            return

        if LinkValidator.is_valid_url(url):
            threading.Thread(target=run).start()
        else:
            messagebox.showerror("Erreur","Veuillez saisir un lien valide")


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Paramètres", font=("Arial", 16)).pack(
            anchor="w", padx=10, pady=10
        )

        ctk.CTkLabel(self, text="Dossier de téléchargement").pack(
            anchor="w", padx=10, pady=(10, 5)
        )

        self.path_var = ctk.StringVar(value=get_default_download_path())

        self.path_entry = ctk.CTkEntry(self, textvariable=self.path_var)
        self.path_entry.pack(fill="x", padx=10, pady=5)

        self.browse_btn = ctk.CTkButton(
            self, text="Choisir un dossier", command=self.choose_folder
        )
        self.browse_btn.pack(padx=10, pady=10, anchor="w")

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
        self.geometry("700x400")

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
