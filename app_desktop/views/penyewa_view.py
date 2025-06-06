import tkinter as tk
from tkinter import ttk, messagebox
from app_desktop.models.penyewa import Penyewa
from app_desktop.controllers.penyewa_controller import PenyewaController

class PenyewaApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg_color = "#f0f4f8"
        self.fg_color = "#2c3e50"
        self.entry_bg = "#ffffff"
        self.button_bg = "#3498db"
        self.button_hover = "#2980b9"
        self.header_bg = "#3498db"
        self.header_fg = "white"

        self.configure(bg=self.bg_color)
        self.controller = PenyewaController()

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

        judul = tk.Label(self, text="Manajemen Penyewa 🧑", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(pady=(10, 15))

        frame_input = tk.LabelFrame(self, text="Form Penyewa", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Penyewa", "Nama Penyewa", "Jenis Kelamin", "No HP", "Alamat", "Hunian"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10),
                           bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=i, column=0, sticky="w", pady=6)
            ent = ttk.Entry(frame_input, width=40)
            ent.grid(row=i, column=1, pady=6, padx=(5,0))
            self.entries[label_text.lower().replace(" ", "_")] = ent

        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=2, rowspan=5, padx=15)

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command="", fg="white", bg="#4CAF50")
        self.btn_update = tk.Button(frame_buttons, text="Update", command="", fg="white", bg="#2196F3")
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command="", fg="white", bg="#f44336")
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command="", fg="white", bg="#9E9E9E")

        self.btn_add.pack(fill='x', pady=4)
        self.btn_update.pack(fill='x', pady=4)
        self.btn_delete.pack(fill='x', pady=4)
        self.btn_clear.pack(fill='x', pady=4)

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Penyewa:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        #self.entry_search.bind("<KeyRelease>", self.cari_penyewa)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_penyewa", "nama", "jenis_kelamin", "no_hp", "alamat", "kd_kamar")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        header_names = ["Kode Penyewa", "Nama Penyewa", "Jenis Kelamin", "No HP", "Alamat", "Hunian"]
        for col, header in zip(columns, header_names):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        #self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        penyewa_list = self.controller.fetch_penyewa()
        for penyewa in penyewa_list:
            self.tree.insert('', 'end', values=(
                penyewa.kd_penyewa,
                penyewa.nama,
                penyewa.jenis_kelamin,
                penyewa.no_hp,
                penyewa.alamat,
                penyewa.kd_kamar
            ))

    # def tambah_penyewa(self):
    #     kd = self.entries['kode_penyewa'].get().strip()
    #     nama = self.entries['nama'].get().strip()
    #     jk = self.entries['jenis_kelamin'].get().strip()
    #     no_hp = self.entries['no_hp'].get().strip()
    #     alamat = self.entries['alamat'].get().strip()
    #     hunian = self.entries['kd_kamar'].get().strip()
    #
    #     if not kd or not nama:
    #         messagebox.showwarning("Peringatan", "Kode dan Nama penyewa wajib diisi!")
    #         return
    #
    #     try:
    #         no_hp = int(no_hp)
    #     except ValueError:
    #         messagebox.showwarning("Peringatan", "No HP harus berupa angka!")
    #         return