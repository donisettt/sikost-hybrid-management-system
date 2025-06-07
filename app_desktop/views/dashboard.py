import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from app_desktop.views.kamar_view import KamarApp
from app_desktop.views.unitKamar_view import UnitKamarApp
from app_desktop.views.penyewa_view import PenyewaApp
from app_desktop.views.users_view import UserApp

class HoverButton(tk.Button):
    def __init__(self, master=None, icon=None, **kw):
        super().__init__(master=master, **kw)
        self.default_bg = self["bg"]
        self.default_fg = self["fg"]
        self.icon = icon
        if icon:
            self.config(image=icon, compound="left")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = '#1abc9c'
        self['fg'] = 'white'

    def on_leave(self, e):
        self['bg'] = self.default_bg
        self['fg'] = self.default_fg

class DashboardApp(tk.Frame):
    def __init__(self, master, on_logout_callback, user_data):
        super().__init__(master)
        self.master = master
        self.on_logout_callback = on_logout_callback
        self.user_data = user_data

        self.pack(fill="both", expand=True)
        self.configure(bg="#ecf0f1")

        self.icons = {}
        self.load_icon("profile", "https://cdn-icons-png.flaticon.com/512/2922/2922510.png", (64, 64))
        self.load_icon("dashboard", "https://cdn-icons-png.flaticon.com/512/1077/1077035.png", (24, 24))
        self.load_icon("kamar", "https://cdn-icons-png.flaticon.com/512/681/681494.png", (24, 24))
        self.load_icon("penyewa", "https://cdn-icons-png.flaticon.com/512/1946/1946429.png", (24, 24))
        self.load_icon("keluar", "https://cdn-icons-png.flaticon.com/512/159/159707.png", (24, 24))

        self.sidebar = tk.Frame(self, width=220, bg="#34495e")
        self.sidebar.pack(side="left", fill="y")

        self.profile_frame = tk.Frame(self.sidebar, bg="#34495e")
        self.profile_frame.pack(pady=20)

        self.profile_icon_label = tk.Label(self.profile_frame, image=self.icons["profile"], bg="#34495e")
        self.profile_icon_label.pack()

        self.profile_text = tk.Label(
            self.profile_frame,
            text=f"Halo, {self.user_data['nama']}",
            bg="#34495e",
            fg="white",
            font=("Segoe UI", 12, "bold")
        )
        self.profile_text.pack(pady=(5, 0))

        self.separator = tk.Frame(self.sidebar, height=1, bg="#2c3e50")
        self.separator.pack(fill="x", padx=15, pady=10)

        btn_params = {
            "fg": "white",
            "bg": "#2c3e50",
            "relief": "flat",
            "compound": "left",
            "anchor": "w",
            "padx": 15,
            "font": ("Segoe UI", 11, "bold"),
            "cursor": "hand2",
            "borderwidth": 0,
            "activebackground": "#1abc9c",
            "activeforeground": "white",
        }

        self.btn_dashboard = HoverButton(self.sidebar, icon=self.icons["dashboard"], text=" Dashboard", command=self.show_dashboard, **btn_params)
        self.btn_dashboard.pack(fill="x", pady=6, padx=10)

        self.btn_dashboard = HoverButton(self.sidebar, icon=self.icons["kamar"], text=" Kelola User", command=self.show_user, **btn_params)
        self.btn_dashboard.pack(fill="x", pady=6, padx=10)

        self.btn_kelola_kamar = HoverButton(self.sidebar, icon=self.icons["kamar"], text=" Kelola Kamar ▼", command=self.toggle_kelola_kamar, **btn_params)
        self.btn_kelola_kamar.pack(fill="x", pady=6, padx=10)

        self.submenu_kelola_kamar = tk.Frame(self.sidebar, bg="#3b4a59")

        btn_submenu_params = {
            "fg": "white",
            "bg": "#3b4a59",
            "relief": "flat",
            "anchor": "w",
            "padx": 30,
            "font": ("Segoe UI", 10),
            "cursor": "hand2",
            "borderwidth": 0,
            "activebackground": "#1abc9c",
            "activeforeground": "white",
        }

        self.btn_kamar = tk.Button(self.submenu_kelola_kamar, text="🛏  Kamar", command=self.show_kamar, **btn_submenu_params)
        self.btn_kamar.pack(fill="x", pady=2)

        self.btn_unit_kamar = tk.Button(self.submenu_kelola_kamar, text="📦  Unit Kamar", command=self.show_unitKamar, **btn_submenu_params)
        self.btn_unit_kamar.pack(fill="x", pady=2)

        self.btn_penyewa = HoverButton(self.sidebar, icon=self.icons["penyewa"], text=" Manajemen Penyewa", command=self.show_penyewa, **btn_params)
        self.btn_penyewa.pack(fill="x", pady=6, padx=10)

        self.btn_keluar = HoverButton(self.sidebar, icon=self.icons["keluar"], text=" Keluar", command=self.confirm_exit, **btn_params)
        self.btn_keluar.config(bg="#e74c3c", activebackground="#c0392b")
        self.btn_keluar.default_bg = "#e74c3c"
        self.btn_keluar.pack(fill="x", pady=6, padx=10)

        self.footer_frame = tk.Frame(self.sidebar, bg="#34495e")
        self.footer_frame.pack(side='bottom', fill='x', pady=10, padx=10)

        self.footer_label = tk.Label(self.footer_frame, text="© 2025 - Kelompok 3 TIF SB 23", bg="#34495e", fg="white", font=("Segoe UI", 7))
        self.footer_label.pack()

        self.container = tk.Frame(self, bg="#ecf0f1")
        self.container.pack(side="left", fill="both", expand=True)

        self.current_frame = None
        self.show_dashboard()

    def toggle_kelola_kamar(self):
        if self.submenu_kelola_kamar.winfo_ismapped():
            self.submenu_kelola_kamar.pack_forget()
        else:
            self.submenu_kelola_kamar.pack(fill="x", padx=20, after=self.btn_kelola_kamar)

    def load_icon(self, name, url, size):
        try:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize(size, Image.Resampling.LANCZOS)
            self.icons[name] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Gagal load icon {name} dari {url}: {e}")
            self.icons[name] = None

    def confirm_exit(self):
        if messagebox.askyesno("Konfirmasi Logout", "Apakah anda yakin ingin keluar?"):
            self.on_logout_callback()

    def clear_container(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_dashboard(self):
        self.clear_container()
        frame = tk.Frame(self.container, bg="#ecf0f1")
        frame.pack(fill="both", expand=True)
        label = tk.Label(frame, text="Selamat datang di Dashboard", font=("Arial", 24), bg="#ecf0f1")
        label.pack(pady=20)
        self.current_frame = frame

    def show_kamar(self):
        self.clear_container()
        kamar_frame = KamarApp(self.container)
        kamar_frame.pack(fill="both", expand=True)
        self.current_frame = kamar_frame

    def show_unitKamar(self):
        self.clear_container()
        unitKamar_frame = UnitKamarApp(self.container)
        unitKamar_frame.pack(fill="both", expand=True)
        self.current_frame = unitKamar_frame

    def show_penyewa(self):
        self.clear_container()
        penyewa_frame = PenyewaApp(self.container)
        penyewa_frame.pack(fill="both", expand=True)
        self.current_frame = penyewa_frame

    def show_user(self):
        self.clear_container()
        user_frame = UserApp(self.container)
        user_frame.pack(fill="both", expand=True)
        self.current_frame = user_frame