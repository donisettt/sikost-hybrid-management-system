import tkinter as tk
from tkinter import ttk, messagebox

class DetailTransaksiApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # === Form Filter ===
        form_frame = tk.LabelFrame(self, text="Form Detail Transaksi", bg="white")
        form_frame.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(form_frame, text="Nama Penyewa", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nama_penyewa_cb = ttk.Combobox(form_frame, values=["Pilih Penyewa"])
        self.nama_penyewa_cb.current(0)
        self.nama_penyewa_cb.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Bulan", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.bulan_cb = ttk.Combobox(form_frame, values=["Pilih Bulan"])
        self.bulan_cb.current(0)
        self.bulan_cb.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Tahun", bg="white").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.tahun_cb = ttk.Combobox(form_frame, values=["Pilih Tahun"])
        self.tahun_cb.current(0)
        self.tahun_cb.grid(row=0, column=5, padx=5)

        self.btn_lihat = tk.Button(form_frame, text="Lihat Transaksi", bg="green", fg="white", width=15)
        self.btn_lihat.grid(row=0, column=6, padx=10)

        # === Detail Transaksi ===
        detail_frame = tk.LabelFrame(self, text="Detail Transaksi", bg="white")
        detail_frame.pack(fill="x", padx=10, pady=(5, 10))

        # Kolom kiri
        labels_kiri = [
            ("Kode Transaksi", "TRX-JAN25-001"),
            ("Nama Penyewa", "Doni Setiawan Wahyono"),
            ("Nama Unit", "MAWAR-001"),
            ("Tanggal Transaksi", "2025-12-12"),
            ("Tanggal Mulai", "2025-12-12"),
            ("Tanggal Selesai", "2026-01-12"),
            ("Total Harga", "650000")
        ]

        # Kolom kanan
        labels_kanan = [
            ("Diskon", "0"),
            ("Biaya Tambahan", "0"),
            ("Jumlah Bayar", "650000"),
            ("Uang Penyewa", "650000"),
            ("Kembalian", "0"),
            ("Status Transaksi", "lunas")
        ]

        for i, (label, value) in enumerate(labels_kiri):
            tk.Label(detail_frame, text=label, bg="white").grid(row=i, column=0, sticky="w", padx=10, pady=2)
            tk.Label(detail_frame, text=value, bg="white", font=("Segoe UI", 10)).grid(row=i, column=1, sticky="w")

        for i, (label, value) in enumerate(labels_kanan):
            tk.Label(detail_frame, text=label, bg="white").grid(row=i, column=2, sticky="w", padx=(40,10), pady=2)
            tk.Label(detail_frame, text=value, bg="white", font=("Segoe UI", 10)).grid(row=i, column=3, sticky="w")

        # Tombol Aksi
        btn_frame = tk.Frame(detail_frame, bg="white")
        btn_frame.grid(row=0, column=4, rowspan=3, padx=40, pady=10)

        tk.Button(btn_frame, text="Cetak Struk", bg="green", fg="white", width=12).pack(pady=5)
        tk.Button(btn_frame, text="Update", bg="dodgerblue", fg="white", width=12).pack(pady=5)
        tk.Button(btn_frame, text="Hapus", bg="red", fg="white", width=12).pack(pady=5)

        # Placeholder area (seperti canvas)
        canvas = tk.Canvas(detail_frame, width=120, height=120, bg="white", highlightbackground="black")
        canvas.grid(row=3, column=4, padx=40)
        canvas.create_oval(55, 55, 65, 65, fill="red")  # Red dot