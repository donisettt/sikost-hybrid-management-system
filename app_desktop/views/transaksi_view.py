import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app_desktop.models.transaksi import Transaksi
from app_desktop.controllers.transaksi_controller import TransaksiController
from app_desktop.controllers.transaksi_bulanan import TransaksiBulananController

class TransaksiApp(tk.Frame):
    def __init__(self, parent, kd_transaksi_bulanan=None, controller=None, user_role=None):
        super().__init__(parent)

        self.master = parent
        self.kd_transaksi_bulanan = kd_transaksi_bulanan
        self.controller = controller or TransaksiController()
        self.user_role = user_role

        self.bg_color = "#f0f4f8"
        self.fg_color = "#2c3e50"
        self.entry_bg = "#ffffff"
        self.header_bg = "#3498db"
        self.header_fg = "white"

        self.configure(bg=self.bg_color)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground=self.fg_color,
                        rowheight=25,
                        fieldbackground="white",
                        font=('Segoe UI', 10))
        style.map("Treeview", background=[('selected', '#2980b9')], foreground=[('selected', 'white')])
        style.configure("Treeview.Heading",
                        background=self.header_bg,
                        foreground=self.header_fg,
                        font=('Segoe UI', 10, 'bold'))

        # === Header Bar ===
        header_bar = tk.Frame(self, bg=self.bg_color)
        header_bar.pack(fill="x", padx=20, pady=(10, 5))

        btn_back = tk.Button(header_bar, text="Kembali", command=self.kembali_ke_transaksi_bulanan,
                             bg="#bdc3c7", fg="white", font=("Segoe UI", 10, "bold"))
        btn_back.pack(side="left")

        bulan_label = ""
        if self.kd_transaksi_bulanan:
            try:
                nama_bulan, tahun = self.controller.get_bulan_tahun_by_kd(self.kd_transaksi_bulanan)
                bulan_label = f" - Bulan {nama_bulan} {tahun}"
            except:
                bulan_label = " - Bulan Tidak Diketahui"

        judul = tk.Label(header_bar, text=f"Transaksi{bulan_label}", font=("Segoe UI", 16, "bold"),
                         bg=self.bg_color, fg=self.fg_color)
        judul.pack(side="top", pady=(5,5), padx=(0, 0))

        # === Form Transaksi ===
        frame_input = tk.LabelFrame(self, text="Form Transaksi", font=("Segoe UI", 12, "bold"),
                                    bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Transaksi", "Penyewa", "Kode Unit", "Tanggal Mulai", "Tanggal Selesai",
                  "Tanggal Transaksi", "Total Harga", "Status Transaksi"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=i // 2, column=(i % 2) * 2, sticky="w", pady=6, padx=(10, 10))
            ent = ttk.Entry(frame_input, width=30)
            ent.grid(row=i // 2, column=(i % 2) * 2 + 1, pady=6, sticky="w")
            self.entries[label_text.lower().replace(" ", "_")] = ent

        # === Tombol Aksi ===
        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=4, rowspan=4, padx=(15, 0))

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command=self.tambah_transaksi,
                                 fg="white", bg="#4CAF50", width=10)
        self.btn_update = tk.Button(frame_buttons, text="Update", command=self.update_transaksi,
                                    fg="white", bg="#2196F3", width=10)
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command=self.hapus_transaksi,
                                    fg="white", bg="#f44336", width=10)
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_form,
                                   fg="white", bg="#9E9E9E", width=10)

        self.btn_add.pack(pady=4)
        self.btn_delete.pack(pady=4)
        self.btn_update.pack(pady=4)
        self.btn_clear.pack(pady=4)

        # === Search Bar ===
        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Transaksi:", font=("Segoe UI", 10),
                              bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=50)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_transaksi)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        # === Table ===
        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_transaksi", "kd_penyewa", "kd_unit", "tanggal_mulai", "tanggal_selesai",
                   "tanggal_transaksi", "total_harga", "status_transaksi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        headers = ["Kode Transaksi", "Penyewa", "Kode Unit", "Tanggal Mulai", "Tanggal Selesai",
                   "Tanggal Transaksi", "Total Harga", "Status"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.generate_kode_otomatis()
        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        transaksi_list = self.controller.fetch_transaksi_by_bulanan(self.kd_transaksi_bulanan) if self.kd_transaksi_bulanan else self.controller.fetch_transaksi()
        for t in transaksi_list:
            self.tree.insert('', 'end', values=(
                t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_mulai,
                t.tanggal_selesai, t.tanggal_transaksi, t.total_harga, t.status_transaksi
            ))

    def tambah_transaksi(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data['kode_transaksi']:
            messagebox.showwarning("Peringatan", "Kode transaksi wajib diisi!")
            return
        transaksi = Transaksi(
            kd_transaksi=data['kode_transaksi'],
            kd_penyewa=data['penyewa'],
            kd_unit=data['kode_unit'],
            tanggal_mulai=data['tanggal_mulai'],
            tanggal_selesai=data['tanggal_selesai'],
            tanggal_transaksi=data['tanggal_transaksi'],
            total_harga=data['total_harga'],
            status_transaksi=data['status_transaksi'],
            kd_transaksi_bulanan=self.kd_transaksi_bulanan
        )
        self.controller.tambah_transaksi(transaksi)
        messagebox.showinfo("Sukses", "Transaksi berhasil dibuat")
        self.load_data()
        self.clear_form()

    def update_transaksi(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data['kode_transaksi']:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang akan diupdate!")
            return
        transaksi = Transaksi(
            kd_transaksi=data['kode_transaksi'],
            kd_penyewa=data['penyewa'],
            kd_unit=data['kode_unit'],
            tanggal_mulai=data['tanggal_mulai'],
            tanggal_selesai=data['tanggal_selesai'],
            tanggal_transaksi=data['tanggal_transaksi'],
            total_harga=data['total_harga'],
            status_transaksi=data['status_transaksi'],
            kd_transaksi_bulanan=self.kd_transaksi_bulanan
        )
        self.controller.update_transaksi(transaksi)
        messagebox.showinfo("Sukses", "Transaksi berhasil diupdate!")
        self.load_data()
        self.clear_form()

    def hapus_transaksi(self):
        kd_transaksi = self.entries['kode_transaksi'].get().strip()
        if not kd_transaksi:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang akan dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus transaksi?"):
            self.controller.hapus_transaksi(kd_transaksi)
            messagebox.showinfo("Sukses", "Transaksi berhasil dihapus.")
            self.load_data()
            self.clear_form()

    def clear_form(self):
        self.entries['kode_transaksi'].config(state='normal')
        for ent in self.entries.values():
            ent.delete(0, 'end')
        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            keys = ["kode_transaksi", "penyewa", "kode_unit", "tanggal_mulai", "tanggal_selesai",
                    "tanggal_transaksi", "total_harga", "status_transaksi"]
            for k, v in zip(keys, values):
                self.entries[k].config(state='normal')
                self.entries[k].delete(0, 'end')
                self.entries[k].insert(0, v)
                if k == 'kode_transaksi':
                    self.entries[k].config(state='disabled')

    def cari_transaksi(self, event):
        keyword = self.entry_search.get().strip()
        transaksi_list = self.controller.cari_transaksi(keyword) if keyword else self.controller.fetch_transaksi()
        self.tree.delete(*self.tree.get_children())
        for t in transaksi_list:
            self.tree.insert('', 'end', values=(
                t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_mulai,
                t.tanggal_selesai, t.tanggal_transaksi, t.total_harga, t.status_transaksi
            ))

    def generate_kode_otomatis(self):
        kd_baru = self.controller.generate_kode_transaksi()
        self.entries['kode_transaksi'].config(state='normal')
        self.entries['kode_transaksi'].delete(0, 'end')
        self.entries['kode_transaksi'].insert(0, kd_baru)
        self.entries['kode_transaksi'].config(state='disabled')

    def kembali_ke_transaksi_bulanan(self):
        from app_desktop.views.transaksi_bulanan import TransaksiBulananApp
        self.destroy()
        controller_bulanan = TransaksiBulananController()
        TransaksiBulananApp(self.master, controller_bulanan, self.user_role).pack(fill='both', expand=True)