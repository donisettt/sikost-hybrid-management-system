import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import pandas as pd
from app_desktop.models.kamar import Kamar
from app_desktop.controllers.kamar_controller import KamarController

class KamarApp(tk.Frame):
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
        self.controller = KamarController()
        self.register_validations()

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

        judul = tk.Label(self, text="Manajemen Kamar 🛏️", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(pady=(10, 15))

        frame_input = tk.LabelFrame(self, text="Form Kamar", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Kamar", "Nama Kamar", "Tipe", "Jumlah Kamar", "Maksimal Penghuni", "Harga", "Fasilitas"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10),
                           bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=i, column=0, sticky="w", pady=6)

            key = label_text.lower().replace(" ", "_")

            if key == "tipe":
                combo = ttk.Combobox(frame_input, values=["ekonomi", "standar", "eksklusif"], state="readonly", width=38)
                combo.set("Pilih Tipe Kamar")
                combo.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = combo
            else:
                ent_kwargs = {"width": 40}
                if key in ["jumlah_kamar", "maksimal_penghuni", "harga"]:
                    ent_kwargs.update({
                        "validate": "key",
                        "validatecommand": self.validasi_angka
                    })

                ent = ttk.Entry(frame_input, **ent_kwargs)
                ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = ent

        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=2, rowspan=5, padx=15)

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command=self.tambah_kamar, fg="white", bg="#4CAF50")
        self.btn_update = tk.Button(frame_buttons, text="Update", command=self.update_kamar, fg="white", bg="#2196F3")
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command=self.hapus_kamar, fg="white", bg="#f44336")
        self.btn_import = tk.Button(frame_buttons, text="Import", command=self.import_kamar, fg="white", bg="#FF9800")
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_form, fg="white", bg="#9E9E9E")

        self.btn_add.pack(fill='x', pady=4)
        self.btn_update.pack(fill='x', pady=4)
        self.btn_delete.pack(fill='x', pady=4)
        self.btn_import.pack(fill='x', pady=4)
        self.btn_clear.pack(fill='x', pady=4)

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5,10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Kamar:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0,5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0,5))
        self.entry_search.bind("<KeyRelease>", self.cari_kamar)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_kamar", "nama_kamar", "tipe", "jumlah_kamar", "kuota", "harga", "fasilitas")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        header_names = ["Kode Kamar", "Nama Kamar", "Tipe", "Jumlah Kamar", "Maksimal Penghuni","Harga", "Fasilitas"]
        for col, header in zip(columns, header_names):
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
        for item in self.tree.get_children():
            self.tree.delete(item)
        kamar_list = self.controller.fetch_kamar()
        for kamar in kamar_list:
            self.tree.insert('', 'end', values=(
                kamar.kd_kamar,
                kamar.nama_kamar,
                kamar.tipe,
                kamar.jumlah_kamar,
                f"{kamar.kuota} orang",
                kamar.harga,
                kamar.fasilitas
            ))

    def validate_integer(self, input):
        return input.isdigit() or input == ""

    def register_validations(self):
        vcmd = (self.register(self.validate_integer), "%P")
        self.validasi_angka = vcmd

    def tambah_kamar(self):
        kd = self.entries['kode_kamar'].get().strip()
        nama = self.entries['nama_kamar'].get().strip()
        tipe = self.entries['tipe'].get().strip()
        jumlah_kamar = self.entries['jumlah_kamar'].get().strip()
        kuota = self.entries['maksimal_penghuni'].get().strip()
        harga = self.entries['harga'].get().strip()
        fasilitas = self.entries['fasilitas'].get().strip()

        if not nama:
            messagebox.showwarning("Peringatan", "Nama kamar wajib diisi!")
            return
        elif not tipe:
            messagebox.showwarning("Peringatan", "Tipe kamar wajib diisi!")
            return
        elif not jumlah_kamar:
            messagebox.showwarning("Peringatan", "Jumlah kamar wajib diisi!")
            return
        elif not kuota:
            messagebox.showwarning("Peringatan", "Maksimal penghuni wajib diisi!")
            return
        elif not harga:
            messagebox.showwarning("Peringatan", "Harga kamar wajib diisi!")
            return
        elif not fasilitas:
            messagebox.showwarning("Peringatan", "Fasilitas kamar wajib diisi!")
            return

        try:
            harga_int = int(harga)
        except ValueError:
            messagebox.showwarning("Peringatan", "Harga harus berupa angka!")
            return

        kamar = Kamar(kd, nama, tipe, jumlah_kamar, kuota, harga_int, fasilitas)
        self.controller.tambah_kamar(kamar)
        messagebox.showinfo("Sukses", f"{nama} berhasil ditambahkan.")
        self.load_data()
        self.clear_form()

    def update_kamar(self):
        kd = self.entries['kode_kamar'].get().strip()
        nama = self.entries['nama_kamar'].get().strip()
        tipe = self.entries["tipe"].get().strip()
        if tipe == "Pilih Tipe Kamar" or tipe == "":
            messagebox.showwarning("Peringatan", "Silakan pilih tipe kamar yang valid.")
            return
        jumlah_kamar = self.entries['jumlah_kamar'].get().strip()
        kuota = self.entries['maksimal_penghuni'].get().strip()
        harga = self.entries['harga'].get().strip()
        fasilitas = self.entries['fasilitas'].get().strip()

        if not kd:
            messagebox.showwarning("Peringatan", "Pilih kamar yang akan diupdate!")
            return
        try:
            harga_int = int(harga)
        except ValueError:
            messagebox.showwarning("Peringatan", "Harga harus berupa angka!")
            return

        kamar = Kamar(kd, nama, tipe, jumlah_kamar, kuota, harga_int, fasilitas)
        self.controller.update_kamar(kamar)
        messagebox.showinfo("Sukses", f"{nama} berhasil diupdate.")
        self.load_data()
        self.clear_form()

    def hapus_kamar(self):
        kd = self.entries['kode_kamar'].get().strip()
        nama = self.entries['nama_kamar'].get().strip()
        if not kd:
            messagebox.showwarning("Peringatan", "Pilih kamar yang akan dihapus!")
            return
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus {nama}?")
        if confirm:
            self.controller.hapus_kamar(kd)
            messagebox.showinfo("Sukses", f"{nama} berhasil dihapus.")
            self.load_data()
            self.clear_form()

    def clear_form(self):
        self.entries['kode_kamar'].config(state='normal')
        for ent in self.entries.values():
            ent.delete(0, 'end')
        for key, entry in self.entries.items():
            if isinstance(entry, ttk.Combobox):
                entry.set("Pilih Tipe Kamar")  # reset combobox ke default
            else:
                entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.entries['kode_kamar'].config(state='normal')
            self.entries['kode_kamar'].delete(0, 'end')
            self.entries['kode_kamar'].insert(0, values[0])
            self.entries['kode_kamar'].config(state='disabled')

            self.entries['nama_kamar'].delete(0, 'end')
            self.entries['nama_kamar'].insert(0, values[1])

            self.entries['tipe'].set(values[2])

            self.entries['jumlah_kamar'].delete(0, 'end')
            self.entries['jumlah_kamar'].insert(0, values[3])

            self.entries['maksimal_penghuni'].delete(0, 'end')
            kuota_bersih = str(values[4]).replace(" orang", "").strip()
            self.entries['maksimal_penghuni'].insert(0, kuota_bersih)

            self.entries['harga'].delete(0, 'end')
            self.entries['harga'].insert(0, values[5])

            self.entries['fasilitas'].delete(0, 'end')
            self.entries['fasilitas'].insert(0, values[6])

    def cari_kamar(self, event):
        keyword = self.entry_search.get().strip()
        if keyword == "":
            kamar_list = self.controller.fetch_kamar()
        else:
            kamar_list = self.controller.cari_kamar(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for kamar in kamar_list:
            self.tree.insert('', 'end', values=(
                kamar.kd_kamar,
                kamar.nama_kamar,
                kamar.tipe,
                kamar.jumlah_kamar,
                kamar.kuota,
                kamar.harga,
                kamar.fasilitas
            ))

    def import_kamar(self):
        file_path = filedialog.askopenfilename(
            title="Pilih File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                self.controller.import_kamar_dari_file(file_path)
            else:
                df = pd.read_excel(file_path)

                required_columns = {"nama_kamar", "tipe", "jumlah_kamar", "kuota", "harga", "fasilitas"}
                if not required_columns.issubset(df.columns):
                    messagebox.showerror("Error",
                                         "Format file tidak valid. Pastikan kolom: " + ", ".join(required_columns))
                    return

                for _, row in df.iterrows():
                    kamar = Kamar(
                        kd_kamar=self.controller.generate_kd_kamar(),
                        nama_kamar=row["nama_kamar"],
                        tipe=row["tipe"],
                        jumlah_kamar=int(row["jumlah_kamar"]),
                        kuota=int(row["kuota"]),
                        harga=int(row["harga"]),
                        fasilitas=row["fasilitas"]
                    )
                    self.controller.tambah_kamar(kamar)

            messagebox.showinfo("Sukses", "Import data kamar berhasil.")
            self.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengimpor data: {e}")

    def generate_kode_otomatis(self):
        kd_baru = self.controller.generate_kd_kamar()
        self.entries['kode_kamar'].config(state='normal')
        self.entries['kode_kamar'].delete(0, 'end')
        self.entries['kode_kamar'].insert(0, kd_baru)
        self.entries['kode_kamar'].config(state='disabled')