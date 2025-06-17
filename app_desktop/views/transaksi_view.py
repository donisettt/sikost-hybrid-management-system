import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from app_desktop.models.transaksi import Transaksi
from app_desktop.controllers.transaksi_controller import TransaksiController
from app_desktop.controllers.transaksi_bulanan import TransaksiBulananController

class TransaksiApp(tk.Frame):
    def __init__(self, parent, kd_transaksi_bulanan=None, controller=None, kembali_callback=None, user_role=None):
        super().__init__(parent)

        self.master = parent
        self.kd_transaksi_bulanan = kd_transaksi_bulanan
        self.controller = controller if controller else TransaksiController()
        self.kode_unit_list = self.controller.fetch_kode_unit_kosong()
        self.kode_penyewa_list = self.controller.fetch_penyewa_belum_transaksi(self.kd_transaksi_bulanan)
        self.nama_to_kode_penyewa = {
            data["nama"]: data["kd_penyewa"] for data in self.kode_penyewa_list
        }
        self.nama_penyewa_list = list(self.nama_to_kode_penyewa.keys())
        self.user_role = user_role
        self.kembali_callback = kembali_callback

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

        header_bar = tk.Frame(self, bg=self.bg_color)
        header_bar.pack(fill="x", padx=20, pady=(10, 5))

        bulan_label = ""
        if self.kd_transaksi_bulanan:
            try:
                nama_bulan, tahun = self.controller.get_bulan_tahun_by_kd(self.kd_transaksi_bulanan)
                bulan_label = f" - Bulan {nama_bulan} {tahun}"
            except:
                bulan_label = " - Bulan Tidak Diketahui"

        btn_kembali = tk.Button(header_bar, text="← Kembali", command=self.kembali_ke_transaksi_bulanan, bg="#bdc3c7", fg="black", font=("Segoe UI", 10), relief="flat", cursor="hand2")
        btn_kembali.pack(side="left", padx=(0, 10), pady=(5, 5))

        judul = tk.Label(header_bar, text=f"Transaksi{bulan_label}", font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(side="top", pady=(5, 5))

        frame_input = tk.LabelFrame(self, text="Form Transaksi", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode Transaksi", "Penyewa", "Kode Unit", "Tanggal Transaksi", "Tanggal Mulai",
                  "Tanggal Selesai", "Total Harga", "Status Transaksi", "Diskon", "Biaya Tambahan", "Jumlah Bayar",
                  "Uang Penyewa", "Kembalian"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            key = label_text.lower().replace(" ", "_")

            if key == "diskon":
                row = 3
                col = 0
            elif key == "uang_penyewa":
                row = 3
                col = 2
            elif key == "biaya_tambahan":
                row = 4
                col = 0
            elif key == "kembalian":
                row = 4
                col = 2
            elif key == "jumlah_bayar":
                row = 5
                col = 0
            else:
                row = i // 3
                col = (i % 3) * 2
                if i >= 10:
                    row += 3

            lbl = tk.Label(frame_input, text=label_text, font=("Segoe UI", 10), bg=self.entry_bg, fg=self.fg_color)
            lbl.grid(row=row, column=col, sticky="w", pady=6, padx=(10, 10))

            if key == "kode_unit":
                if not self.kode_unit_list:
                    cb = ttk.Combobox(frame_input, values=["Unit kamar penuh"], width=30, state="readonly")
                    cb.current(0)
                else:
                    unit_options = ["Pilih kode unit"] + self.kode_unit_list
                    cb = ttk.Combobox(frame_input, values=unit_options, width=30, state="readonly")
                    cb.current(0)
                cb.grid(row=row, column=col + 1, pady=6, padx=(1, 0), sticky="w")
                cb.bind("<<ComboboxSelected>>", self.unit_selected)
                self.entries[key] = cb

            elif key == "penyewa":
                if not self.nama_penyewa_list:
                    cb = ttk.Combobox(frame_input, values=["Sudah bayar semua"], width=30, state="readonly")
                    cb.current(0)
                else:
                    penyewa_options = ["Pilih penyewa"] + self.nama_penyewa_list
                    cb = ttk.Combobox(frame_input, values=penyewa_options, width=30, state="readonly")
                    cb.current(0)
                cb.grid(row=row, column=col + 1, pady=6, padx=(1, 0), sticky="w")
                cb.bind("<<ComboboxSelected>>", self.penyewa_selected)
                self.entries[key] = cb

            elif key in ["tanggal_mulai", "tanggal_selesai", "tanggal_transaksi"]:
                ent = DateEntry(frame_input, width=30, background='darkblue', foreground='white',
                                borderwidth=2, date_pattern='yyyy-mm-dd', state='readonly')
                ent.grid(row=row, column=col + 1, pady=6, sticky="w")
                if key == "tanggal_mulai":
                    ent.bind("<<DateEntrySelected>>", self.tanggal_mulai_changed)
                self.entries[key] = ent

            elif key == "status_transaksi":
                var = tk.StringVar(value="lunas")

                frame_status = tk.Frame(frame_input, bg=self.entry_bg)
                frame_status.grid(row=row, column=col + 1, pady=6, sticky="w")

                rb_lunas = tk.Radiobutton(frame_status, text="Lunas", variable=var, value="lunas", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_belum = tk.Radiobutton(frame_status, text="Belum Lunas", variable=var, value="belum_lunas", bg=self.entry_bg, fg=self.fg_color, font=("Segoe UI", 10))
                rb_lunas.pack(side="left", padx=(0, 10))
                rb_belum.pack(side="left")
                self.entries[key] = {
                    "var": var,
                    "widgets": [rb_lunas, rb_belum]
                }
            else:
                if key in ["diskon", "biaya_tambahan", "uang_penyewa"]:
                    vcmd = (self.register(self.hanya_angka), "%P")
                    ent = ttk.Entry(frame_input, width=30, validate="key", validatecommand=vcmd)
                else:
                    ent = ttk.Entry(frame_input, width=30)

                ent.grid(row=row, column=col + 1, pady=6, sticky="w")
                self.entries[key] = ent

                if key in ["total_harga", "diskon", "biaya_tambahan", "uang_penyewa"]:
                    ent.bind("<KeyRelease>", self.update_jumlah_bayar_otomatis)

                if key in ["diskon", "biaya_tambahan"]:
                    ent.insert(0, "0")

                if key in ["jumlah_bayar", "kembalian"]:
                    ent.config(state="readonly")

        self.entries["diskon"].bind("<KeyRelease>", self.update_jumlah_bayar_otomatis)
        self.entries["biaya_tambahan"].bind("<KeyRelease>", self.update_jumlah_bayar_otomatis)
        self.entries["uang_penyewa"].bind("<KeyRelease>", self.update_jumlah_bayar_otomatis)

        frame_add_clear = tk.Frame(frame_input, bg=self.entry_bg)
        frame_add_clear.grid(row=5, column=2, columnspan=2, sticky="w", padx=(10, 0), pady=(6, 0))

        self.btn_add = tk.Button(frame_add_clear, text="Batal", command=self.clear_form, fg="white", bg="#9E9E9E", width=8)
        self.btn_add.pack(side="left", padx=(152, 10))

        self.btn_clear = tk.Button(frame_add_clear, text="Bayar", command=self.tambah_transaksi, fg="white", bg="#4CAF50", width=8)
        self.btn_clear.pack(side="left")

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari Transaksi:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=50)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_transaksi)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data, width=8)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kd_transaksi", "kd_penyewa", "kd_unit",
                   "tanggal_transaksi", "status_transaksi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        headers = ["Kode Transaksi", "Penyewa", "Kode Unit",
                   "Tanggal Transaksi", "Status"]
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.generate_kode_otomatis()
        self.update_jumlah_bayar_otomatis()
        self.load_data()

    def hanya_angka(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False

    def kembali_ke_transaksi_bulanan(self):
        self.destroy()
        if self.kembali_callback:
            self.kembali_callback()

    def update_jumlah_bayar_otomatis(self, event=None):
        def safe_float(value):
            try:
                return float(value.strip()) if value.strip() != "" else 0.0
            except (ValueError, AttributeError):
                return 0.0

        total = safe_float(self.entries["total_harga"].get())
        diskon = safe_float(self.entries["diskon"].get())
        tambahan = safe_float(self.entries["biaya_tambahan"].get())
        uang_penyewa = safe_float(self.entries["uang_penyewa"].get())

        jumlah_bayar = total + tambahan - diskon
        kembalian = uang_penyewa - jumlah_bayar

        def format_idr(number):
            return f"{int(number):,}".replace(",", ".")

        self.entries["jumlah_bayar"].config(state="normal")
        self.entries["jumlah_bayar"].delete(0, "end")
        self.entries["jumlah_bayar"].insert(0, format_idr(jumlah_bayar))
        self.entries["jumlah_bayar"].config(state="readonly")

        self.entries["kembalian"].config(state="normal")
        self.entries["kembalian"].delete(0, "end")
        self.entries["kembalian"].insert(0, format_idr(kembalian))
        self.entries["kembalian"].config(state="readonly")

    def show_transaksi_detail(self, data):
        self.clear_container()
        self.current_frame = TransaksiApp(
            self.container,
            controller=TransaksiController(),
            transaksi_data=data,
            kembali_callback=self.show_transaksi_detail(),  # <== ini kunci
            user_role=self.user_data['role']
        )
        self.current_frame.pack(fill='both', expand=True)

    def tanggal_mulai_changed(self, event=None):
        try:
            tgl_mulai = self.entries["tanggal_mulai"].get_date()
            from dateutil.relativedelta import relativedelta
            tgl_selesai = tgl_mulai + relativedelta(months=1)
            self.entries["tanggal_selesai"].set_date(tgl_selesai)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengatur tanggal selesai otomatis: {e}")

    def penyewa_selected(self, event=None):
        nama_penyewa = self.entries["penyewa"].get()
        kd_penyewa = self.controller.get_kd_penyewa_by_name(nama_penyewa)

        if kd_penyewa:
            kd_unit, harga = self.controller.get_unit_dan_harga_by_penyewa(kd_penyewa)

            if kd_unit:
                self.entries["kode_unit"].set(kd_unit)
                self.entries["total_harga"].config(state="normal")
                self.entries["total_harga"].delete(0, tk.END)
                self.entries["total_harga"].insert(0, str(harga))
                self.entries["total_harga"].config(state="readonly")
            else:
                self.entries["kode_unit"].set("")
                self.entries["total_harga"].delete(0, tk.END)
        self.update_jumlah_bayar_otomatis()

    def refresh_penyewa_combobox(self):
        penyewa_data = self.controller.fetch_penyewa_belum_transaksi(self.kd_transaksi_bulanan)
        self.nama_to_kode_penyewa = {
            data["nama"]: data["kd_penyewa"] for data in penyewa_data
        }
        self.nama_penyewa_list = list(self.nama_to_kode_penyewa.keys())

        combobox = self.entries.get("penyewa")
        if combobox:
            combobox["values"] = ["Pilih penyewa"] + self.nama_penyewa_list
            combobox.current(0)

    def unit_selected(self, event=None):
        kd_unit = self.entries['kode_unit'].get()
        if kd_unit and kd_unit != "Pilih kode unit":
            harga = self.controller.get_harga_by_kode_unit(kd_unit)
            if harga is not None:
                self.entries['total_harga'].config(state='normal')
                self.entries['total_harga'].delete(0, tk.END)
                self.entries['total_harga'].insert(0, str(harga))
                self.entries['total_harga'].config(state='readonly')
            else:
                messagebox.showwarning("Tidak Ada Harga", f"Harga untuk unit {kd_unit} tidak ditemukan.")
        self.update_jumlah_bayar_otomatis()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        transaksi_list = self.controller.fetch_transaksi_bulanan(self.kd_transaksi_bulanan) if self.kd_transaksi_bulanan else self.controller.fetch_transaksi()
        for t in transaksi_list:
            self.tree.insert('', 'end', values=(
                t.kd_transaksi, t.kd_penyewa, t.kd_unit,
                t.tanggal_transaksi, t.status_transaksi
            ))

    def tambah_transaksi(self):
        data = {}
        for key, entry in self.entries.items():
            try:
                if isinstance(entry, (tk.Entry, ttk.Combobox)):
                    data[key] = entry.get()
                elif isinstance(entry, DateEntry):
                    data[key] = entry.get_date().strftime('%Y-%m-%d')
                elif isinstance(entry, dict) and "var" in entry:
                    # Spesial buat status_transaksi (radio button)
                    data[key] = entry["var"].get()
                elif isinstance(entry, tk.StringVar):
                    data[key] = entry.get()
                else:
                    data[key] = str(entry)  # fallback darurat
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat mengambil data input: {e}")
                return

        if data["penyewa"] == "Pilih penyewa" or data["kode_unit"] == "Pilih kode unit":
            messagebox.showwarning("Input tidak lengkap", "Pilih penyewa dan kode unit.")
            return

        tgl_mulai = datetime.datetime.strptime(data["tanggal_mulai"], "%Y-%m-%d").date()
        tgl_selesai = datetime.datetime.strptime(data["tanggal_selesai"], "%Y-%m-%d").date()
        if tgl_mulai >= tgl_selesai:
            messagebox.showwarning("Tanggal Salah", "Tanggal selesai harus setelah tanggal mulai.")
            return

        try:
            transaksi = Transaksi(
                kd_transaksi=data["kode_transaksi"],
                kd_transaksi_bulanan=self.kd_transaksi_bulanan,
                kd_penyewa=self.nama_to_kode_penyewa.get(data["penyewa"]),
                kd_unit=data["kode_unit"],
                tanggal_mulai=data["tanggal_mulai"],
                tanggal_selesai=data["tanggal_selesai"],
                tanggal_transaksi=data["tanggal_transaksi"],
                total_harga=self.bersihkan_angka(data["total_harga"]),
                status_transaksi=data["status_transaksi"],
                diskon=self.bersihkan_angka(data["diskon"]),
                biaya_tambahan=self.bersihkan_angka(data["biaya_tambahan"]),
                jumlah_bayar=self.bersihkan_angka(data["jumlah_bayar"]),
                uang_penyewa=self.bersihkan_angka(data["uang_penyewa"]),
                kembalian=self.bersihkan_angka(data["kembalian"])
            )

            self.controller.tambah_transaksi(transaksi)
            messagebox.showinfo("Sukses", "Transaksi berhasil ditambahkan.")
            self.clear_form()
            self.load_data()
            self.refresh_penyewa_combobox()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan transaksi: {e}")

    def update_transaksi(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data['kode_transaksi']:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang akan diupdate!")
            return
        tgl_mulai = datetime.datetime.strptime(data["tanggal_mulai"], "%Y-%m-%d").date()
        tgl_selesai = datetime.datetime.strptime(data["tanggal_selesai"], "%Y-%m-%d").date()
        if tgl_mulai > tgl_selesai:
            messagebox.showwarning("Tanggal Salah", "Tanggal mulai harus lebih awal dari tanggal selesai.")
            return

        transaksi = Transaksi(
            kd_transaksi=data['kode_transaksi'],
            kd_penyewa=self.nama_to_kode_penyewa.get(data['penyewa'], ""),
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
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dihapus.")
            return
        item = self.tree.item(selected_item)
        kd_transaksi = item["values"][0]

        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus transaksi {kd_transaksi}?")
        if confirm:
            try:
                self.controller.hapus_transaksi(kd_transaksi)
                messagebox.showinfo("Sukses", "Transaksi berhasil dihapus.")
                self.clear_form()
                self.load_data()
                self.refresh_penyewa_combobox()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus transaksi: {e}")

    def clear_form(self):
        self.refresh_penyewa_combobox()
        self.entries['kode_transaksi'].config(state='normal')

        for key, ent in self.entries.items():
            if isinstance(ent, ttk.Combobox):
                ent.config(state='readonly')
                ent.current(0)
            elif isinstance(ent, DateEntry):
                ent.set_date(datetime.date.today())
            elif isinstance(ent, tk.Entry) or isinstance(ent, tk.Text):
                ent.config(state='normal')
                ent.delete(0, 'end')
                if key in ["diskon", "biaya_tambahan", "kembalian"]:
                    ent.insert(0, "0")
                elif key in ["jumlah_bayar", "kembalian"]:
                    ent.insert(0, "0")
                    ent.config(state="readonly")
            elif isinstance(ent, tk.StringVar):
                if key == "status_transaksi":
                    ent.set("lunas")
                else:
                    ent.set("")
            else:
                pass

        self.tree.selection_remove(self.tree.selection())
        self.generate_kode_otomatis()

        if isinstance(self.entries['kode_unit'], ttk.Combobox):
            self.entries['kode_unit'].config(state='readonly')
            self.entries['kode_unit'].set("Pilih kode unit")
            unit_kosong = self.controller.fetch_kode_unit_kosong()
            self.entries['kode_unit']['values'] = ["Pilih kode unit"] + unit_kosong
            self.entries['kode_unit'].set("Pilih kode unit")

    def bersihkan_angka(self, str_angka):
        try:
            return int(str_angka.replace('.', '').strip()) if str_angka else 0
        except ValueError:
            return 0

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            kode_transaksi = self.tree.item(selected, 'values')[0]
            detail_data = self.controller.get_detail_transaksi(kode_transaksi)

            for k, v in detail_data.items():
                entry = self.entries.get(k)
                if not entry:
                    continue

                if isinstance(entry, tk.Entry):
                    entry.config(state='normal')
                    entry.delete(0, 'end')
                    if k == "penyewa":
                        nama = next((nama for nama, kode in self.nama_to_kode_penyewa.items() if kode == v), v)
                        entry.insert(0, nama)
                    else:
                        entry.insert(0, str(v))
                    entry.config(state='readonly')

                elif isinstance(entry, ttk.Combobox):
                    entry.config(state='readonly')
                    entry.set(v)

                elif isinstance(entry, DateEntry):
                    try:
                        entry.set_date(v)
                    except:
                        pass
                    entry.config(state='disabled')

                elif isinstance(entry, tk.StringVar):
                    entry.set(v)

            if "status_transaksi" in self.entries:
                for widget in self.entries["status_transaksi"]["widgets"]:
                    widget.config(state="disabled")

            print("Treeview item values:", self.tree.item(selected, 'values'))
            print("Detail dari DB:", detail_data)

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
        kd_baru = self.controller.generate_kode_transaksi(self.kd_transaksi_bulanan)
        self.entries['kode_transaksi'].config(state='normal')
        self.entries['kode_transaksi'].delete(0, 'end')
        self.entries['kode_transaksi'].insert(0, kd_baru)
        self.entries['kode_transaksi'].config(state='disabled')
