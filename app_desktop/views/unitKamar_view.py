import tkinter as tk
from tkinter import ttk, messagebox
from app_desktop.models.unit_kamar import UnitKamar
from app_desktop.controllers.unitKamar_controller import UnitKamarController

class UnitKamarApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = UnitKamarController()

        self.bg_color = "#f0f4f8"
        self.fg_color = "#2c3e50"
        self.entry_bg = "#ffffff"
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
                        background="#3498db",
                        foreground="white",
                        font=('Segoe UI', 10, 'bold'))

        tk.Label(self, text="Manajemen Unit Kamar 🛏️", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=(10, 15))

        self.create_form_section()
        self.create_search_section()
        self.create_table_section()

        self.data_unit_kamar = []
        self.load_data()

    def create_form_section(self):
        form = tk.LabelFrame(self, text="Form Unit Kamar", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        form.pack(padx=20, pady=(0, 10), fill=tk.X)

        self.entries = {}
        labels = ["Kode Kamar", "Kode Unit"]
        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color).grid(row=i, column=0,
                                                                                                       sticky="w",
                                                                                                       pady=6)
            key = label.lower().replace(" ", "_")
            if label == "Kode Kamar":
                kamar_list = self.controller.fetch_kamar()
                if kamar_list:
                    kamar_options = ["Pilih data kamar"] + [f"{k['kd_kamar']} | {k['nama_kamar']}" for k in kamar_list]
                else:
                    kamar_options = ["Tidak ada data"]
                combo = ttk.Combobox(form, values=kamar_options, state="readonly", width=37)
                combo.grid(row=i, column=1, pady=6, padx=(5, 0))
                combo.set(kamar_options[0])
                combo.bind("<<ComboboxSelected>>", self.generate_kode_unit_otomatis)  # Tambahkan ini
                self.entries[key] = combo
            else:
                entry = ttk.Entry(form, width=40)
                entry.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = entry

        tk.Label(form, text="Status", font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color).grid(row=2, column=0, sticky="w", pady=6)

        self.status_var = tk.StringVar(value="kosong")
        status_frame = tk.Frame(form, bg=self.entry_bg)
        status_frame.grid(row=2, column=1, pady=6, sticky="w")
        tk.Radiobutton(status_frame, text="Kosong", variable=self.status_var, value="kosong", bg=self.entry_bg, font=("Segoe UI", 10)).pack(side='left', padx=(0, 10))
        tk.Radiobutton(status_frame, text="Terisi", variable=self.status_var, value="terisi", bg=self.entry_bg, font=("Segoe UI", 10)).pack(side='left')

        btn_frame = tk.Frame(form, bg=self.entry_bg)
        btn_frame.grid(row=0, column=2, rowspan=3, padx=15)
        ttk.Button(btn_frame, text="Tambah", command=self.tambah_unitKamar).pack(fill='x', pady=4)
        ttk.Button(btn_frame, text="Update", command=self.update_unitKamar).pack(fill='x', pady=4)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_unitKamar).pack(fill='x', pady=4)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(fill='x', pady=4)

    def create_search_section(self):
        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        tk.Label(frame_search, text="🔍 Cari Unit Kamar:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color).pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_unitKamar)

        ttk.Button(frame_search, text="Reset", command=self.load_data).pack(side='left')

    def create_table_section(self):
        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_unit", "kd_kamar", "nama_kamar", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        unitKamar_list = self.controller.fetch_unitKamar()
        self.data_unit_kamar = unitKamar_list  # simpan data untuk cari
        kamar_dict = {k['kd_kamar']: k['nama_kamar'] for k in self.controller.fetch_kamar()}

        for uk in unitKamar_list:
            nama_kamar = kamar_dict.get(uk["kd_kamar"], "Tidak Diketahui")
            self.tree.insert('', 'end', values=(uk["kd_unit"], uk["kd_kamar"], nama_kamar, uk["status"]))

        kamar_list = self.controller.fetch_kamar()
        kamar_options = [f"{k['kd_kamar']} | {k['nama_kamar']}" for k in kamar_list]
        self.entries['kode_kamar']['values'] = kamar_options

        self.entry_search.delete(0, tk.END)

    def tambah_unitKamar(self):
        kd_unit = self.entries['kode_unit'].get().strip()
        kd_kamar_full = self.entries['kode_kamar'].get().strip()
        status = self.status_var.get()

        if not kd_unit or not kd_kamar_full:
            messagebox.showwarning("Peringatan", "Semua field harus diisi.")
            return

        kd_kamar = kd_kamar_full.split("|")[0].strip()

        try:
            # Ambil kuota kamar dari controller
            jumlah_kamar = self.controller.get_jumlah_kamar(kd_kamar)
            # Hitung jumlah unit kamar yang sudah ada untuk kd_kamar ini
            jumlah_unit = self.controller.count_unit_kamar(kd_kamar)

            if jumlah_unit >= jumlah_kamar:
                messagebox.showwarning("Peringatan", "Jumlah kamar maksimal.")
                return

            unit = UnitKamar(kd_unit, kd_kamar, status)
            self.controller.tambah_unitKamar(unit)
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan.")
            self.load_data()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal menambahkan data.\n{e}")

    def update_unitKamar(self):
        kd_unit = self.entries['kode_unit'].get().strip()
        kd_kamar_full = self.entries['kode_kamar'].get().strip()
        status = self.status_var.get()

        if not kd_unit or not kd_kamar_full:
            messagebox.showwarning("Peringatan", "Semua field harus diisi.")
            return

        kd_kamar = kd_kamar_full.split("|")[0].strip()

        try:
            unit = UnitKamar(kd_unit, kd_kamar, status)
            self.controller.update_unitKamar(unit)
            messagebox.showinfo("Sukses", "Data berhasil diupdate.")
            self.load_data()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal update data.\n{e}")

    def hapus_unitKamar(self):
        kd_unit = self.entries['kode_unit'].get().strip()
        if not kd_unit:
            messagebox.showwarning("Peringatan", "Pilih data dulu untuk dihapus.")
            return

        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus unit {kd_unit}?"):
            try:
                self.controller.hapus_unitKamar(kd_unit)
                messagebox.showinfo("Sukses", "Data berhasil dihapus.")
                self.load_data()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Gagal", f"Gagal hapus data.\n{e}")

    def clear_form(self):
        self.entries['kode_unit'].delete(0, tk.END)
        self.entries['kode_kamar'].set('')
        self.status_var.set('kosong')

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            kd_unit, kd_kamar, nama_kamar, status = item['values']
            self.entries['kode_unit'].config(state='normal')  # pastikan bisa diedit dulu
            self.entries['kode_unit'].delete(0, tk.END)
            self.entries['kode_unit'].insert(0, kd_unit)
            self.entries['kode_unit'].config(state='disabled')  # lalu nonaktifkan
            # Set combobox berdasarkan kd_kamar
            kamar_list = self.entries['kode_kamar']['values']
            for kamar in kamar_list:
                if kamar.startswith(kd_kamar):
                    self.entries['kode_kamar'].set(kamar)
                    break
            self.status_var.set(status)

    def cari_unitKamar(self, event):
        keyword = self.entry_search.get().lower()
        filtered = []
        kamar_dict = {k['kd_kamar']: k['nama_kamar'] for k in self.controller.fetch_kamar()}

        for uk in self.data_unit_kamar:
            nama_kamar = kamar_dict.get(uk["kd_kamar"], "").lower()
            if (keyword in uk["kd_unit"].lower() or
                keyword in uk["kd_kamar"].lower() or
                keyword in nama_kamar or
                keyword in uk["status"].lower()):
                filtered.append((uk["kd_unit"], uk["kd_kamar"], kamar_dict.get(uk["kd_kamar"], ""), uk["status"]))

        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            self.tree.insert('', 'end', values=row)

    def generate_kode_unit_otomatis(self, event):
        kd_kamar_full = self.entries['kode_kamar'].get()
        if kd_kamar_full == "Pilih data kamar" or kd_kamar_full == "Tidak ada data" or not kd_kamar_full:
            self.entries['kode_unit'].config(state='normal')
            self.entries['kode_unit'].delete(0, tk.END)
            return

        # ambil nama kamar dari pilihan combobox (format: "KVH-001 | Kamar Mawar")
        parts = kd_kamar_full.split("|")
        if len(parts) < 2:
            return
        nama_kamar = parts[1].strip()  # contoh: "Kamar Mawar"

        # ambil kata terakhir nama kamar untuk jadi prefix kode unit, misal "Mawar" dari "Kamar Mawar"
        # atau kamu bisa ambil nama kamar tanpa kata "Kamar" dulu, ini contoh ambil kata terakhir:
        nama_terakhir = nama_kamar.split()[-1].upper()  # "MAWAR"

        # cari data unit kamar yang sudah ada dengan prefix nama_terakhir
        existing_units = [uk['kd_unit'] for uk in self.data_unit_kamar if uk['kd_unit'].startswith(nama_terakhir)]

        # ambil nomor urut terbesar
        nomor_terbesar = 0
        for unit in existing_units:
            # format kode unit: NAMA-XXX, ambil angka XXX
            try:
                nomor = int(unit.split("-")[-1])
                if nomor > nomor_terbesar:
                    nomor_terbesar = nomor
            except:
                pass

        nomor_baru = nomor_terbesar + 1
        kode_unit_baru = f"{nama_terakhir}-{nomor_baru:03d}"

        # set kode unit otomatis di entry
        self.entries['kode_unit'].config(state='normal')
        self.entries['kode_unit'].delete(0, tk.END)
        self.entries['kode_unit'].insert(0, kode_unit_baru)
