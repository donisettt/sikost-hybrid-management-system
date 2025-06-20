import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from datetime import datetime
from io import BytesIO
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from app_desktop.views.kamar_view import KamarApp
from app_desktop.views.unitKamar_view import UnitKamarApp
from app_desktop.views.penyewa_view import PenyewaApp
from app_desktop.views.users_view import UserApp
from app_desktop.views.components.sidebar import Sidebar
from app_desktop.views.components.navbar import Navbar
from app_desktop.views.transaksi_bulanan import TransaksiBulananApp
from app_desktop.views.transaksi_view import TransaksiApp
from app_desktop.views.pengeluaran_view import PengeluaranApp
from app_desktop.views.detail_transaksi_view import DetailTransaksiApp
from app_desktop.views.profile_view import ProfileApp
from app_desktop.views.laporan_view import LaporanApp
from app_desktop.controllers.transaksi_bulanan import TransaksiBulananController
from app_desktop.controllers.detail_transaksi_controller import DetailTransaksiController
from app_desktop.controllers.profile_controller import ProfileController
from app_desktop.controllers.dashboard_controller import DashboardController

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
    def __init__(self, master, on_logout_callback, user_data, on_profile_callback):
        super().__init__(master)
        self.master = master
        self.on_logout_callback = on_logout_callback
        self.on_profile_callback = on_profile_callback

        self.user_data = user_data
        self.current_frame = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.configure(bg="#ecf0f1")

        self.icons = {}
        self.load_icon("profile", "https://cdn-icons-png.flaticon.com/512/2922/2922510.png", (64, 64))
        self.load_icon("dashboard", "https://cdn-icons-png.flaticon.com/512/1828/1828859.png",(24, 24))
        self.load_icon("user", "https://cdn-icons-png.flaticon.com/512/847/847969.png", (24, 24))
        self.load_icon("kamar", "https://cdn-icons-png.flaticon.com/512/1946/1946436.png", (24, 24))
        self.load_icon("penyewa", "https://cdn-icons-png.flaticon.com/512/921/921347.png",(24, 24))
        self.load_icon("transaksi", "https://cdn-icons-png.flaticon.com/512/833/833524.png",(24, 24))

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
                'penyewa': self.show_penyewa,
                'transaksi': self.show_transaksi,
                'pengeluaran': self.show_pengeluaran,
                'detail': self.show_detail_transaksi,
                'laporan': self.show_laporan,
                'profile': self.show_profile,
                'logout': self.confirm_exit,
            }
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # --- NAVBAR ---
        self.navbar = Navbar(
            self,
            user_data=self.user_data,
            on_dashboard_click=self.show_dashboard,
            on_profile_click=self.show_profile,
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

    def show_profile(self):
        self.clear_container()
        kode_user = self.user_data.get("kode_user")  # pastikan ini ada di user_data saat login
        controller = ProfileController(kode_user)  # controller dibuat dulu
        profile_frame = ProfileApp(self.container, controller=controller)  # lalu dikirim ke view
        profile_frame.pack(fill="both", expand=True)
        self.current_frame = profile_frame
        self.on_profile_callback()

    def show_dashboard(self):
        self.clear_container()

        frame = tk.Frame(self.container, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        title_label = tk.Label(frame, text="Dashboard", font=("Segoe UI", 18, "bold"), bg="#ecf0f1", anchor="w")
        title_label.pack(anchor="w", pady=(0, 20))

        card_frame = tk.Frame(frame, bg="#ecf0f1")
        card_frame.pack(fill="x", pady=(0, 10))

        def create_card(parent, title, value, color):
            card = tk.Frame(parent, bg="white", width=200, height=110, highlightbackground="#ccc", highlightthickness=1)
            card.pack_propagate(False)

            header = tk.Label(card, text=title, font=("Segoe UI", 10, "bold"), bg=color, fg="white")
            header.pack(fill="x")

            value_label = tk.Label(card, text=str(value), font=("Segoe UI", 15, "bold"), bg="white", fg="#2c3e50")
            value_label.pack(expand=True)

            return card

        def format_rupiah(angka):
            return "Rp {:,}".format(angka).replace(",", ".")

        # Ambil data dari controller
        dashboard_ctrl = DashboardController()
        jumlah_penyewa = dashboard_ctrl.get_jumlah_penyewa()
        jumlah_transaksi_bulan_ini = dashboard_ctrl.get_jumlah_transaksi_bulan_ini()
        total_transaksi = dashboard_ctrl.get_total_transaksi()
        total_pengeluaran = dashboard_ctrl.get_total_pengeluaran()
        total_pendapatan = dashboard_ctrl.get_total_pendapatan_bulan_ini()
        belum_lunas = dashboard_ctrl.get_transaksi_belum_lunas()
        transaksi_hari_ini = dashboard_ctrl.get_transaksi_hari_ini()
        penyewa_teraktif = dashboard_ctrl.get_top_penyewa()
        grafik_bulanan = dashboard_ctrl.get_tren_transaksi_perbulan(datetime.now().year)
        pemasukan, pengeluaran = dashboard_ctrl.get_rasio_pemasukan_pengeluaran()
        notif_jatuh_tempo = dashboard_ctrl.get_notifikasi_jatuh_tempo()

        # === Card ===
        card1 = create_card(card_frame, "Jumlah Penyewa", jumlah_penyewa, "#2980b9")
        card2 = create_card(card_frame, "Transaksi Bulan Ini", jumlah_transaksi_bulan_ini, "#e67e22")
        card3 = create_card(card_frame, "Total Transaksi", total_transaksi, "#27ae60")
        card4 = create_card(card_frame, "Total Pengeluaran", format_rupiah(total_pengeluaran), "#c0392b")

        card5 = create_card(card_frame, "Pendapatan Bulan Ini", format_rupiah(total_pendapatan), "#8e44ad")
        card6 = create_card(card_frame, "Belum Lunas", belum_lunas, "#f39c12")
        card7 = create_card(card_frame, "Hari Ini", transaksi_hari_ini, "#16a085")
        card8 = create_card(card_frame, "Jatuh Tempo", notif_jatuh_tempo, "#d35400")

        card1.grid(row=0, column=0, padx=10, pady=4)
        card2.grid(row=0, column=1, padx=10, pady=5)
        card3.grid(row=0, column=2, padx=10, pady=5)
        card4.grid(row=0, column=3, padx=10, pady=5)
        card5.grid(row=1, column=0, padx=10, pady=5)
        card6.grid(row=1, column=1, padx=10, pady=5)
        card7.grid(row=1, column=2, padx=10, pady=5)
        card8.grid(row=1, column=3, padx=10, pady=5)

        # === Notifikasi Reminder ===
        if notif_jatuh_tempo > 0:
            tk.Label(frame, text=f"Ada {notif_jatuh_tempo} transaksi yang akan jatuh tempo minggu ini!",
                     fg="red", bg="#ecf0f1", font=("Segoe UI", 10, "italic")).pack(pady=(10, 0))

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

    def show_transaksi(self):
        print("Menampilkan halaman transaksi bulanan")  # debug log
        self.clear_container()
        transaksi_bulanan = TransaksiBulananController()
        user_role = self.user_data.get('role', 'petugas')
        transaksi_frame = TransaksiBulananApp(self.container, transaksi_bulanan, user_role=user_role)
        transaksi_frame.pack(fill="both", expand=True)
        self.current_frame = transaksi_frame

    def show_transaksi_view(self):
        self.clear_container()
        transaksi_bulanan = TransaksiBulananController()
        transaksi_view_frame = TransaksiApp(
            self.container,
            kembali_callback=self.show_transaksi
        )
        transaksi_view_frame.pack(fill="both", expand=True)
        self.current_frame = transaksi_bulanan

    def show_pengeluaran(self):
        self.clear_container()
        pengeluaran_frame = PengeluaranApp(self.container)
        pengeluaran_frame.pack(fill="both", expand=True)
        self.current_frame = pengeluaran_frame

    def show_detail_transaksi(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        controller = DetailTransaksiController()
        detail_frame = DetailTransaksiApp(self.container, controller)
        detail_frame.pack(fill="both", expand=True)
        self.current_frame = detail_frame

    def show_laporan(self):
        self.clear_container()
        laporan_frame = LaporanApp(self.container)
        laporan_frame.pack(fill="both", expand=True)
        self.current_frame = laporan_frame

    def clear_container(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def set_current_frame(self, frame):
        self.current_frame = frame