import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from controllers.laporan_controller import LaporanController

class LaporanApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = LaporanController()
        self.configure(bg="white")

        frame_laporan = tk.Frame(self, bg="white")
        frame_laporan.pack(pady=10, padx=10, fill="x")

        self.tgl_dari_var = tk.StringVar()
        self.tgl_sampai_var = tk.StringVar()
        self.kategori_periode_var = tk.StringVar()
        self._buat_form_laporan_periode(frame_laporan)

        self.bulan_var = tk.StringVar()
        self.tahun_bln_var = tk.StringVar()
        self.kategori_bln_var = tk.StringVar()
        self._buat_form_laporan_bulanan(frame_laporan)

        self.tahun_thn_var = tk.StringVar()
        self.kategori_thn_var = tk.StringVar()
        self._buat_form_laporan_tahunan(frame_laporan)

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
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_bln_var, values=["Semua", "Pemasukan", "Pengeluaran"], state="readonly", width=20)
        kategori_cb.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Buat Laporan", bg="green", fg="white", command=self.export_laporan_bulanan).grid(row=3, columnspan=2, pady=10, padx=(125, 0))

    def _buat_form_laporan_tahunan(self, parent):
        frame = tk.LabelFrame(parent, text="Laporan Tahunan", font=("Segoe UI", 10, "bold"), padx=10, pady=10, bg="white")
        frame.pack(side="left", padx=10)

        ttk.Label(frame, text="Tahun:", background="white").grid(row=0, column=0, sticky="w")
        tahun_cb = ttk.Combobox(frame, textvariable=self.tahun_thn_var, values=self._get_tahun_list(), state="readonly", width=20)
        tahun_cb.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Kategori:", background="white").grid(row=1, column=0, sticky="w")
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_thn_var, values=["Pemasukan", "Pengeluaran"], state="readonly", width=20)
        kategori_cb.grid(row=1, column=1, pady=5)

        tk.Button(frame, text="Buat Laporan", bg="green", fg="white", command="").grid(row=2, columnspan=2, pady=10, padx=(125, 0))

    def _buat_form_laporan_periode(self, parent):
        frame = tk.LabelFrame(parent, text="Laporan Periode", font=("Segoe UI", 10, "bold"), padx=10, pady=10, bg="white")
        frame.pack(side="left", padx=10)

        ttk.Label(frame, text="Dari Tanggal:", background="white").grid(row=0, column=0, sticky="w")
        self.dari_entry = DateEntry(frame, textvariable=self.tgl_dari_var, date_pattern='yyyy-mm-dd', width=18, state="readonly")
        self.dari_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Sampai Tanggal:", background="white").grid(row=1, column=0, sticky="w")
        self.sampai_entry = DateEntry(frame, textvariable=self.tgl_sampai_var, date_pattern='yyyy-mm-dd', width=18, state="readonly")
        self.sampai_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Kategori:", background="white").grid(row=2, column=0, sticky="w")
        kategori_cb = ttk.Combobox(frame, textvariable=self.kategori_periode_var, values=["Pemasukan", "Pengeluaran"], state="readonly", width=18)
        kategori_cb.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Buat Laporan", bg="green", fg="white", command="").grid(row=3, columnspan=2, pady=10, padx=(170, 0))

    def _get_bulan_list(self):
        return ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    def _get_tahun_list(self):
        return [str(year) for year in range(2020, datetime.now().year + 1)]

    # laporan_view.py (dalam class)

    def export_laporan_bulanan(self):
        bulan = self.bulan_var.get()
        tahun = self.tahun_bln_var.get()
        kategori = self.kategori_bln_var.get()

        if not bulan or not tahun or not kategori:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return

        data = self.controller.get_laporan_bulanan(bulan, tahun, kategori)
        if not data:
            messagebox.showinfo("Info", "Tidak ada data untuk laporan.")
            return

        # Pilih folder untuk simpan
        folder_path = filedialog.askdirectory(title="Pilih Folder untuk Simpan Laporan")
        if not folder_path:
            messagebox.showinfo("Batal", "Export laporan dibatalkan.")
            return

        # Buat nama file dan path lengkap
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_excel = f"laporan_{kategori.lower()}_{timestamp}.xlsx"
        full_path_excel = os.path.join(folder_path, filename_excel)

        # Header sesuai kategori
        if kategori == "Pengeluaran":
            headers = ["Kode", "Tanggal", "Kategori", "Deskripsi", "Jumlah", "Dibuat Oleh"]
        else:
            headers = ["Kode", "Penyewa", "Unit", "Tanggal", "Total", "Diskon", "Tambahan", "Bayar", "Uang", "Kembali",
                       "Status"]

        print("==== DEBUG DATA YANG DIEXPORT ====")
        for row in data:
            print(row)

        # Ekspor hanya ke Excel
        self.controller.export_excel(data, headers, full_path_excel)

        messagebox.showinfo("Sukses", f"Laporan berhasil diekspor ke:\n{full_path_excel}")