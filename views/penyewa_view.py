import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import ttk, messagebox
from datetime import datetime
from models.penyewa import Penyewa
from controllers.penyewa_controller import PenyewaController

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
        self.kode_unit_list = self.controller.fetch_kode_unit()

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

        frame_input = tk.LabelFrame(self, text="Form Penyewa", font=("Segoe UI", 12, "bold"), bg=self.entry_bg,
                                    fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Penyewa", "Nama", "Jenis Kelamin", "No HP", "Alamat", "Status", "Kode Unit"]
        self.entries = {}

        def validasi_nomor(event, ent):
            nomor = ent.get().strip()
            if nomor.startswith("0"):
                nomor = "62" + nomor[1:]
            elif not nomor.startswith("62"):
                nomor = "62" + nomor
            ent.delete(0, tk.END)
            ent.insert(0, nomor)

        for i, label_text in enumerate(labels):
            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=i, column=0, sticky="w", pady=6)

            key = label_text.lower().replace(" ", "_")

            if key == "kode_unit":
                if not self.kode_unit_list:
                    cb = ttk.Combobox(frame_input, values=["Tidak ada data"], state="disabled", width=38)
                    cb.current(0)
                else:
                    unit_options = ["Silahkan pilih kode unit"] + self.kode_unit_list
                    cb = ttk.Combobox(frame_input, values=unit_options, state="disabled", width=38)
                    cb.current(0)
                cb.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = cb

            elif key == "jenis_kelamin":
                self.jk_var = tk.StringVar()
                jk_frame = tk.Frame(frame_input, bg=self.entry_bg)
                jk_frame.grid(row=i, column=1, pady=6, padx=(5, 0), sticky="w")

                rb_l = tk.Radiobutton(jk_frame, text="Laki-laki", variable=self.jk_var, value="Laki-laki", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_p = tk.Radiobutton(jk_frame, text="Perempuan", variable=self.jk_var, value="Perempuan", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_l.pack(side="left", padx=5)
                rb_p.pack(side="left", padx=5)
                self.entries[key] = self.jk_var
                self.jk_var.set("Laki-laki")

            elif key == "status":
                self.status_var = tk.StringVar()
                status_frame = tk.Frame(frame_input, bg=self.entry_bg)
                status_frame.grid(row=i, column=1, pady=6, padx=(5, 0), sticky="w")

                rb_a = tk.Radiobutton(status_frame, text="Aktif", variable=self.status_var, value="Aktif", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_n = tk.Radiobutton(status_frame, text="Non-Aktif", variable=self.status_var, value="Non-Aktif", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_a.pack(side="left", padx=5)
                rb_n.pack(side="left", padx=5)
                self.entries[key] = self.status_var
                self.status_var.set("Aktif")

            else:
                ent = ttk.Entry(frame_input, width=40)
                ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[key] = ent

                if key == "no_hp":
                    def hanya_angka(new_value):
                        return new_value.isdigit() or new_value == ""

                    vcmd = (self.register(hanya_angka), '%P')

                    ent = ttk.Entry(frame_input, width=40, validate="key", validatecommand=vcmd)
                    ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                    self.entries[key] = ent

                    def validasi_nomor(e, entry_target):
                        nomor = entry_target.get().strip()
                        if nomor.startswith("0"):
                            nomor = "62" + nomor[1:]
                        elif not nomor.startswith("62"):
                            nomor = "62" + nomor

                        if not (10 <= len(nomor) <= 15):
                            messagebox.showwarning("Nomor Tidak Valid", "Nomor HP harus terdiri dari 10 hingga 15 digit angka.")
                            entry_target.focus_set()
                            return

                        entry_target.delete(0, tk.END)
                        entry_target.insert(0, nomor)

                    ent.bind("<FocusOut>", lambda e, entry_target=ent: validasi_nomor(e, entry_target))

        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=2, rowspan=5, padx=15, pady=(0, 27))

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command=self.tambah_penyewa, fg="white", bg="#4CAF50")
        self.btn_update = tk.Button(frame_buttons, text="Update", command=self.update_penyewa, fg="white", bg="#2196F3")
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command=self.hapus_penyewa, fg="white", bg="#f44336")
        self.btn_export = tk.Button(frame_buttons, text="Export", command=self.export_data, fg="white", bg="#FF9800")
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_form, fg="white", bg="#9E9E9E")

        self.btn_add.pack(fill='x', pady=4)
        self.btn_update.pack(fill='x', pady=4)
        self.btn_delete.pack(fill='x', pady=4)
        self.btn_export.pack(fill='x', pady=4)
        self.btn_clear.pack(fill='x', pady=4)

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Penyewa:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_penyewa)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_penyewa", "nama", "jenis_kelamin", "no_hp", "alamat", "status", "kd_unit")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        header_names = ["Kode Penyewa", "Nama", "Jenis Kelamin", "No HP", "Alamat", "Status", "Kode Unit"]
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
        penyewa_list = self.controller.fetch_penyewa()
        for penyewa in penyewa_list:
            self.tree.insert('', 'end', values=(
                penyewa.kd_penyewa,
                penyewa.nama,
                penyewa.jenis_kelamin,
                penyewa.no_hp,
                penyewa.alamat,
                penyewa.status,
                penyewa.kd_unit
            ))

    def tambah_penyewa(self):
        kd = self.entries['kode_penyewa'].get().strip()
        nama = self.entries['nama'].get().strip()
        jk = self.entries['jenis_kelamin'].get()
        no_hp = self.entries['no_hp'].get().strip()
        alamat = self.entries['alamat'].get().strip()
        status = self.entries['status'].get()
        kd_unit = self.entries['kode_unit'].get().strip()

        if not kd or not nama:
            messagebox.showwarning("Peringatan", "Nama Penyewa wajib diisi!")
            return
        elif not jk:
            messagebox.showwarning("Peringatan", "Pilih jenis kelamin penyewa!")

        penyewa = Penyewa(kd, nama, jk, no_hp, alamat, status, kd_unit)
        self.controller.tambah_penyewa(penyewa)
        messagebox.showinfo("Sukses", f"Berhasil menambahkan {nama} sebagai penyewa.")
        self.load_data()
        self.clear_form()

    def update_penyewa(self):
        kd = self.entries['kode_penyewa'].get().strip()
        nama = self.entries['nama'].get().strip()
        jk = self.entries['jenis_kelamin'].get()
        no_hp = self.entries['no_hp'].get().strip()
        alamat = self.entries['alamat'].get().strip()
        status = self.entries['status'].get()
        kd_unit = self.entries['kode_unit'].get().strip()

        if not kd or not nama:
            messagebox.showwarning("Peringatan", "Pilih penyewa yang akan diupdate!")
            return

        penyewa = Penyewa(kd, nama, jk, no_hp, alamat, status, kd_unit)
        self.controller.update_penyewa(penyewa)
        messagebox.showinfo("Sukses", f"Penyewa {nama} berhasil diupdate.")
        self.load_data()
        self.clear_form()

    def hapus_penyewa(self):
        kd = self.entries['kode_penyewa'].get().strip()
        nama = self.entries['nama'].get().strip()
        if not kd:
            messagebox.showwarning("Peringatan", "Pilih penyewa yang akan dihapus!")
            return
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus {nama} sebagai penyewa?")
        if confirm:
            self.controller.hapus_penyewa(kd)
            messagebox.showinfo("Sukses", "Data penyewa berhasil dihapus.")
            print("Debug: Data berhasil disimpan")
            self.load_data()
            self.clear_form()

    def export_data(self):
        data_penyewa = self.controller.get_all_penyewa()

        if not data_penyewa:
            messagebox.showwarning("Kosong", "Tidak ada data penyewa untuk diekspor.")
            return

        df = pd.DataFrame(data_penyewa)

        bulan_tahun = datetime.now().strftime("%B_%Y")
        default_filename = f"data_penyewa_{bulan_tahun}.xlsx"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=default_filename,
            title="Simpan Data Penyewa"
        )

        if not file_path:
            return

        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Berhasil", f"Data berhasil diekspor ke:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal mengekspor data:\n{e}")

    def clear_form(self):
        self.entries['kode_penyewa'].config(state='normal')

        for key, widget in self.entries.items():
            if key in ['nama', 'no_hp', 'alamat']:
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, 'end')

            elif key == 'kode_unit':
                widget.set('Silahkan pilih kode unit')
                widget.config(state='disabled')

            elif key == 'kode_penyewa':
                continue

        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.entries['kode_penyewa'].config(state='normal')
            self.entries['kode_penyewa'].delete(0, 'end')
            self.entries['kode_penyewa'].insert(0, values[0])
            self.entries['kode_penyewa'].config(state='disabled')

            self.entries['nama'].delete(0, 'end')
            self.entries['nama'].insert(0, values[1])

            self.entries['jenis_kelamin'].set(values[2])

            self.entries['no_hp'].delete(0, 'end')
            self.entries['no_hp'].insert(0, values[3])

            self.entries['alamat'].delete(0, 'end')
            self.entries['alamat'].insert(0, values[4])

            self.entries["status"].set(values[5])

            self.entries['kode_unit'].config(state='readonly')
            self.entries['kode_unit'].set(values[6])

    def cari_penyewa(self, event):
        keyword = self.entry_search.get().strip()
        if keyword == "":
            penyewa_list = self.controller.fetch_penyewa()
        else:
            penyewa_list = self.controller.cari_penyewa(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for penyewa in penyewa_list:
            self.tree.insert('', 'end', values=(
                penyewa.kd_penyewa,
                penyewa.nama,
                penyewa.jenis_kelamin,
                penyewa.no_hp,
                penyewa.alamat,
                penyewa.status,
                penyewa.kd_unit
            ))

    def generate_kode_otomatis(self):
        kd_baru = self.controller.generate_kd_penyewa()
        self.entries['kode_penyewa'].config(state='normal')
        self.entries['kode_penyewa'].delete(0, 'end')
        self.entries['kode_penyewa'].insert(0, kd_baru)
        self.entries['kode_penyewa'].config(state='disabled')