import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime  # ✅ Perbaikan di sini
from app_desktop.controllers.laporan_controller import LaporanController

class LaporanApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = LaporanController()
        self.configure(bg="white")

        # === Frame Utama ===
        frame_laporan = tk.Frame(self, bg="white")
        frame_laporan.pack(pady=10, padx=10, fill="x")

        # --- Laporan Bulanan ---
        self.bulan_var = tk.StringVar()
        self.tahun_bln_var = tk.StringVar()
        self.kategori_bln_var = tk.StringVar()
        self._buat_form_laporan_bulanan(frame_laporan)

        # --- Laporan Tahunan ---
        self.tahun_thn_var = tk.StringVar()
        self.kategori_thn_var = tk.StringVar()
        self._buat_form_laporan_tahunan(frame_laporan)

        # --- Laporan Periode ---
        self.tgl_dari_var = tk.StringVar()
        self.tgl_sampai_var = tk.StringVar()
        self.kategori_periode_var = tk.StringVar()
        self._buat_form_laporan_periode(frame_laporan)

        # === Tombol Clear dan Print ===
        frame_btn = tk.Frame(self, bg="white")
        frame_btn.pack(fill="x", padx=20, pady=10)

        self.btn_clear = tk.Button(frame_btn, text="Clear", bg="#aaa", fg="white", command=self.clear)
        self.btn_clear.pack(side="right", padx=5)

        self.btn_print = tk.Button(frame_btn, text="Print", bg="#007bff", fg="white", command=self.cetak_laporan)
        self.btn_print.pack(side="right", padx=5)

        # === Tempat Menampilkan Laporan ===
        self.text_area = tk.Text(self, height=20, font=("Segoe UI", 10))
        self.text_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _buat_form_laporan_bulanan(self, parent):
        frame = tk.LabelFrame(parent, text="Laporan Bulanan", font=("Segoe UI", 10, "bold"), padx=10, pady=10, bg="white")
        frame.pack(side="left", padx=10)

        ttk.Label(frame, text="Bulan:", background="white").grid(row=0, column=0, sticky="w")
        bulan_cb = ttk.Combobox(frame, textvariable=self.bulan_var, values=self._get_bulan_list(), state="readonly", width=20)
        bulan_cb.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Tahun:", background="white").grid(row=1, column=0, sticky="w")
        tahun_cb = ttk.Combobox(frame, textvariable=self.tahun_bln_var, values=self._get_tahun_list(), state="readonly", width=20)
        tahun_cb.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Kategori:", background="white").grid(row=2, column=0, sticky="w")
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_bln_var, values=["Pemasukan", "Pengeluaran"], state="readonly", width=20)
        kategori_cb.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Lihat Laporan", bg="green", fg="white", command=self.lihat_laporan_bulanan).grid(row=3, columnspan=2, pady=10)

    def _buat_form_laporan_tahunan(self, parent):
        frame = tk.LabelFrame(parent, text="Laporan Tahunan", font=("Segoe UI", 10, "bold"), padx=10, pady=10, bg="white")
        frame.pack(side="left", padx=10)

        ttk.Label(frame, text="Tahun:", background="white").grid(row=0, column=0, sticky="w")
        tahun_cb = ttk.Combobox(frame, textvariable=self.tahun_thn_var, values=self._get_tahun_list(), state="readonly", width=20)
        tahun_cb.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Kategori:", background="white").grid(row=1, column=0, sticky="w")
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_thn_var, values=["Pemasukan", "Pengeluaran"], state="readonly", width=20)
        kategori_cb.grid(row=1, column=1, pady=5)

        tk.Button(frame, text="Lihat Laporan", bg="green", fg="white", command=self.lihat_laporan_tahunan).grid(row=2, columnspan=2, pady=10)

    def _buat_form_laporan_periode(self, parent):
        frame = tk.LabelFrame(parent, text="Laporan Periode", font=("Segoe UI", 10, "bold"), padx=10, pady=10, bg="white")
        frame.pack(side="left", padx=10)

        ttk.Label(frame, text="Dari Tanggal:", background="white").grid(row=0, column=0, sticky="w")
        self.dari_entry = DateEntry(frame, textvariable=self.tgl_dari_var, date_pattern='yyyy-mm-dd', width=18)
        self.dari_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Sampai Tanggal:", background="white").grid(row=1, column=0, sticky="w")
        self.sampai_entry = DateEntry(frame, textvariable=self.tgl_sampai_var, date_pattern='yyyy-mm-dd', width=18)
        self.sampai_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Kategori:", background="white").grid(row=2, column=0, sticky="w")
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_periode_var, values=["Pemasukan", "Pengeluaran"], state="readonly", width=20)
        kategori_cb.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Lihat Laporan", bg="green", fg="white", command=self.lihat_laporan_periode).grid(row=3, columnspan=2, pady=10)

    def _get_bulan_list(self):
        return ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    def _get_tahun_list(self):
        return [str(year) for year in range(2020, datetime.now().year + 1)]  # ✅ Fixed di sini

    def lihat_laporan_bulanan(self):
        kategori = self.kategori_bln_var.get()
        if kategori == "Pemasukan":
            hasil = self.controller.get_laporan_bulanan(self.bulan_var.get(), self.tahun_bln_var.get(), "Semua")
        elif kategori == "Pengeluaran":
            hasil = self.controller.get_pengeluaran_periode(
                f"{self.tahun_bln_var.get()}-{self._get_bulan_angka(self.bulan_var.get())}-01",
                f"{self.tahun_bln_var.get()}-{self._get_bulan_angka(self.bulan_var.get())}-31"
            )
        else:
            hasil = []
        self._tampilkan_laporan(hasil)

    def lihat_laporan_tahunan(self):
        kategori = self.kategori_thn_var.get()
        if kategori == "Pemasukan":
            hasil = self.controller.get_laporan_tahunan(self.tahun_thn_var.get(), "Semua")
        elif kategori == "Pengeluaran":
            hasil = self.controller.get_pengeluaran_periode(f"{self.tahun_thn_var.get()}-01-01",
                                                            f"{self.tahun_thn_var.get()}-12-31")
        else:
            hasil = []
        self._tampilkan_laporan(hasil)

    def lihat_laporan_periode(self):
        kategori = self.kategori_periode_var.get()
        if kategori == "Pemasukan":
            hasil = self.controller.get_laporan_periode(self.tgl_dari_var.get(), self.tgl_sampai_var.get(), "Semua")
        elif kategori == "Pengeluaran":
            hasil = self.controller.get_pengeluaran_periode(self.tgl_dari_var.get(), self.tgl_sampai_var.get())
        else:
            hasil = []
        self._tampilkan_laporan(hasil)

    def _tampilkan_laporan(self, data):
        self.text_area.delete(1.0, tk.END)
        if not data:
            self.text_area.insert(tk.END, "Tidak ada data untuk ditampilkan.")
        else:
            for item in data:
                self.text_area.insert(tk.END, f"{item}\n")

    def _get_bulan_angka(self, nama_bulan):
        bulan_map = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
            "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
            "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        return bulan_map.get(nama_bulan, "01")

    def clear(self):
        self.text_area.delete(1.0, tk.END)

    def cetak_laporan(self):
        messagebox.showinfo("Cetak", "Fitur cetak bisa menggunakan export ke PDF atau printer langsung nanti.")
