import tkinter as tk
from tkinter import messagebox

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

class Sidebar(tk.Frame):
    def __init__(self, master, user_data, icons, callback_dict):
        super().__init__(master, width=220, bg="#34495e")
        self.pack(side="left", fill="y")

        self.user_data = user_data
        self.icons = icons
        self.callback_dict = callback_dict

        self.profile_frame = tk.Frame(self, bg="#34495e")
        self.profile_frame.pack(pady=20)

        self.profile_icon_label = tk.Label(self.profile_frame, image=self.icons.get("profile"), bg="#34495e")
        self.profile_icon_label.pack()

        self.profile_text = tk.Label(
            self.profile_frame,
            text=f"Halo, {self.user_data['nama']}",
            bg="#34495e",
            fg="white",
            font=("Segoe UI", 12, "bold")
        )
        self.profile_text.pack(pady=(5, 0))

        self.separator = tk.Frame(self, height=1, bg="#2c3e50")
        self.separator.pack(fill="x", padx=15, pady=10)

        btn_params = {
            "fg": "white", "bg": "#2c3e50", "relief": "flat", "compound": "left",
            "anchor": "w", "padx": 15, "font": ("Segoe UI", 11, "bold"),
            "cursor": "hand2", "borderwidth": 0,
            "activebackground": "#1abc9c", "activeforeground": "white",
        }

        role = self.user_data.get('role', '').lower()

        if role == 'admin':
            self.btn_dashboard = HoverButton(self, icon=self.icons.get("dashboard"), text=" Dashboard", command=callback_dict['dashboard'], **btn_params)
            self.btn_dashboard.pack(fill="x", pady=6, padx=10)

            self.btn_user = HoverButton(self, icon=self.icons.get("user"), text=" Kelola User", command=callback_dict['user'], **btn_params)
            self.btn_user.pack(fill="x", pady=6, padx=10)

            self.btn_kelola_kamar = HoverButton(self, icon=self.icons.get("kamar"), text=" Kelola Kamar ▼", command=self.toggle_kelola_kamar, **btn_params)
            self.btn_kelola_kamar.pack(fill="x", pady=6, padx=10)

            self.submenu_kelola_kamar = tk.Frame(self, bg="#3b4a59")
            btn_submenu_params = {
                "fg": "white", "bg": "#3b4a59", "relief": "flat", "anchor": "w",
                "padx": 30, "font": ("Segoe UI", 10), "cursor": "hand2", "borderwidth": 0,
                "activebackground": "#1abc9c", "activeforeground": "white",
            }

            self.btn_kamar = tk.Button(self.submenu_kelola_kamar, text="🛏  Kamar", command=callback_dict['kamar'], **btn_submenu_params)
            self.btn_kamar.pack(fill="x", pady=2)

            self.btn_unit_kamar = tk.Button(self.submenu_kelola_kamar, text="📦  Unit Kamar", command=callback_dict['unit_kamar'], **btn_submenu_params)
            self.btn_unit_kamar.pack(fill="x", pady=2)

            self.btn_penyewa = HoverButton(self, icon=self.icons.get("penyewa"), text=" Manajemen Penyewa", command=callback_dict['penyewa'], **btn_params)
            self.btn_penyewa.pack(fill="x", pady=6, padx=10)

            self.btn_kelola_transaksi = HoverButton(self, icon=self.icons.get("transaksi"), text=" Transaksi ▼", command=self.toggle_kelola_transaksi, **btn_params)
            self.btn_kelola_transaksi.pack(fill="x", pady=6, padx=10)

            self.submenu_kelola_transaksi = tk.Frame(self, bg="#3b4a59")
            self.btn_transaksi = tk.Button(self.submenu_kelola_transaksi, text="💰  Transaksi Bulanan", command=callback_dict['transaksi'], **btn_submenu_params)
            self.btn_transaksi.pack(fill="x", pady=2)

            self.btn_detail_transaksi = tk.Button(self.submenu_kelola_transaksi, text="📤  Detail Transaksi", command=callback_dict['detail'], **btn_submenu_params)
            self.btn_detail_transaksi.pack(fill="x", pady=2)

            self.btn_pengeluaran = tk.Button(self.submenu_kelola_transaksi, text="📤  Pengeluaran", command=callback_dict['pengeluaran'], **btn_submenu_params)
            self.btn_pengeluaran.pack(fill="x", pady=2)

        elif role == 'petugas':
            self.btn_dashboard = HoverButton(self, icon=self.icons.get("dashboard"), text=" Dashboard", command=callback_dict['dashboard'], **btn_params)
            self.btn_dashboard.pack(fill="x", pady=6, padx=10)

            self.btn_penyewa = HoverButton(self, icon=self.icons.get("penyewa"), text=" Manajemen Penyewa", command=callback_dict['penyewa'], **btn_params)
            self.btn_penyewa.pack(fill="x", pady=6, padx=10)

            self.btn_kelola_transaksi = HoverButton(self, icon=self.icons.get("transaksi"), text=" Transaksi ▼", command=self.toggle_kelola_transaksi, **btn_params)
            self.btn_kelola_transaksi.pack(fill="x", pady=6, padx=10)

            btn_submenu_params = {
                "fg": "white", "bg": "#3b4a59", "relief": "flat", "anchor": "w",
                "padx": 30, "font": ("Segoe UI", 10), "cursor": "hand2", "borderwidth": 0,
                "activebackground": "#1abc9c", "activeforeground": "white",
            }

            self.submenu_kelola_transaksi = tk.Frame(self, bg="#3b4a59")
            self.btn_transaksi = tk.Button(self.submenu_kelola_transaksi, text="💰  Transaksi Bulanan", command=callback_dict['transaksi'], **btn_submenu_params)
            self.btn_transaksi.pack(fill="x", pady=2)

            self.btn_detail_transaksi = tk.Button(self.submenu_kelola_transaksi, text="📤  Detail Transaksi", command=callback_dict['detail'], **btn_submenu_params)
            self.btn_detail_transaksi.pack(fill="x", pady=2)

            self.btn_pengeluaran = tk.Button(self.submenu_kelola_transaksi, text="📤  Pengeluaran", command=callback_dict['pengeluaran'], **btn_submenu_params)
            self.btn_pengeluaran.pack(fill="x", pady=2)

        else:
            info_label = tk.Label(self, text="Role tidak dikenali.\nHubungi administrator.", fg="white", bg="#34495e", font=("Segoe UI", 10, "italic"))
            info_label.pack(padx=15, pady=20)

        self.footer_frame = tk.Frame(self, bg="#34495e")
        self.footer_frame.pack(side='bottom', fill='x', pady=10, padx=10)

        self.footer_label = tk.Label(self.footer_frame, text="© 2025 - Kelompok 3 TIF SB 23", bg="#34495e", fg="white", font=("Segoe UI", 7))
        self.footer_label.pack()

    def toggle_kelola_kamar(self):
        if self.submenu_kelola_kamar.winfo_ismapped():
            self.submenu_kelola_kamar.pack_forget()
        else:
            self.submenu_kelola_kamar.pack(fill="x", padx=20, after=self.btn_kelola_kamar)

    def toggle_kelola_transaksi(self):
        if self.submenu_kelola_transaksi.winfo_ismapped():
            self.submenu_kelola_transaksi.pack_forget()
        else:
            self.submenu_kelola_transaksi.pack(fill="x", padx=20, after=self.btn_kelola_transaksi)