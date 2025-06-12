import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from app_desktop.views.kamar_view import KamarApp
from app_desktop.views.unitKamar_view import UnitKamarApp
from app_desktop.views.penyewa_view import PenyewaApp
from app_desktop.views.users_view import UserApp
from app_desktop.views.components.sidebar import Sidebar
from app_desktop.views.components.navbar import Navbar
from app_desktop.views.transaksi_bulanan import TransaksiBulananApp
from app_desktop.controllers.transaksi_bulanan import TransaksiBulananController

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
        self.current_frame = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.configure(bg="#ecf0f1")

        self.icons = {}
        self.load_icon("profile", "https://cdn-icons-png.flaticon.com/512/2922/2922510.png", (64, 64))
        self.load_icon("dashboard", "https://cdn-icons-png.flaticon.com/512/1828/1828859.png",(24, 24))  # Dashboard icon
        self.load_icon("user", "https://cdn-icons-png.flaticon.com/512/847/847969.png", (24, 24))  # Kelola User
        self.load_icon("kamar", "https://cdn-icons-png.flaticon.com/512/1946/1946436.png", (24, 24))  # Kelola Kamar
        self.load_icon("penyewa", "https://cdn-icons-png.flaticon.com/512/921/921347.png",(24, 24))  # Manajemen Penyewa
        self.load_icon("transaksi", "https://cdn-icons-png.flaticon.com/512/833/833524.png",(24, 24))  # Icon transaksi, aku pilih yg kasir/ticket vibes

        # --- SIDEBAR ---
        self.sidebar = Sidebar(
            self,
            user_data=self.user_data,
            icons=self.icons,
            callback_dict={
                'dashboard': self.show_dashboard,
                'user': self.show_user,
                'kamar': self.show_kamar,
                'unit_kamar': self.show_unitKamar,
                'fasilitas': self.show_fasilitas,
                'penyewa': self.show_penyewa,
                'transaksi': self.show_transaksi,
                'logout': self.confirm_exit,
            }
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # --- NAVBAR ---
        self.navbar = Navbar(
            self,
            user_data=self.user_data,
            on_dashboard_click=self.show_dashboard,
            on_logout_click=self.confirm_exit
        )
        self.navbar.grid(row=0, column=1, sticky="ew")

        # --- CONTAINER UTAMA ---
        self.container = tk.Frame(self, bg="#ecf0f1")
        self.container.grid(row=1, column=1, sticky="nsew")

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
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(frame, text="Selamat datang di Dashboard", font=("Segoe UI", 20, "bold"), bg="#ecf0f1")
        title_label.pack(pady=(0, 20))

        # Group info card
        card_group = tk.Frame(frame, bg="white", bd=2, relief="groove", padx=15, pady=15)
        card_group.pack(fill="x", pady=(0, 20))

        group_title = tk.Label(card_group, text="Kelompok 3 - TIF SB 23", font=("Segoe UI", 14, "bold"), bg="white",
                               fg="#2c3e50")
        group_title.pack(anchor="w", pady=(0, 10), padx=7)

        anggota_list = [
            "Doni Setiawan Wahyono 23552011146 | Lead Full Stack Developer",
            "Lutfi Mahesa Abdul K - 23552011147 | UI/UX Designer & Database Architect",
            "Aisah Gandari Rahmah - 23552011127 | UI/UX Designer & Database Architect",
            "Ariyan Kusharthanto - 23552011168 | Project Administrator & Research Analyst",
            "Indri Rohmawati - 23552011128 | Project Administrator & Research Analyst",
        ]

        for anggota in anggota_list:
            label = tk.Label(card_group, text=anggota, font=("Segoe UI", 11), bg="white", fg="#34495e")
            label.pack(anchor="w", padx=10)

        # Teknologi yang Digunakan card
        card_tech = tk.Frame(frame, bg="white", bd=2, relief="groove", padx=15, pady=15)
        card_tech.pack(fill="x")

        tech_title = tk.Label(card_tech, text="Teknologi yang Digunakan", font=("Segoe UI", 14, "bold"), bg="white",
                              fg="#2c3e50")
        tech_title.pack(anchor="w", pady=(0, 10), padx=7)

        tech_list = [
            "Bahasa pemrograman: Python (Tkinter)",
            "Database: MySQL (mysql-connector)",
            "Tools aplikasi: Laragon, PyCharm, Git, Balsamiq",
        ]

        for tech in tech_list:
            label = tk.Label(card_tech, text=tech, font=("Segoe UI", 11), bg="white", fg="#34495e")
            label.pack(anchor="w", padx=10)

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

    def show_fasilitas(self):
        self.clear_container()
        fasilitas_frame = FasilitasApp(self.container)
        fasilitas_frame.pack(fill="both", expand=True)
        self.current_frame = fasilitas_frame

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

    def show_transaksi(self):
        self.clear_container()
        transaksi_controller = TransaksiBulananController()

        user_role = self.user_data.get('role', 'petugas')

        transaksi_frame = TransaksiBulananApp(self.container, transaksi_controller, user_role=user_role)
        transaksi_frame.pack(fill="both", expand=True)
        self.current_frame = transaksi_frame
