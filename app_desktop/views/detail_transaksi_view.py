import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
import tempfile
import os
import platform
from reportlab.lib.units import mm
import re
from datetime import datetime

class DetailTransaksiApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.entries = {}
        self.create_form_detail()
        self.create_detail_transaksi()

    def create_form_detail(self):
        frame_form = tk.LabelFrame(self, text="Form Detail Transaksi", font=("Segoe UI", 10, "bold"), bg="white")
        frame_form.pack(padx=10, pady=(10, 5), fill="x")

        tk.Label(frame_form, text="Nama Penyewa", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, padx=(25, 25), pady=(10, 10), sticky="w")
        self.cb_penyewa = ttk.Combobox(frame_form, state="readonly", width=25)
        self.cb_penyewa.grid(row=0, column=1, padx=(0, 20), pady=(10, 10))

        tk.Label(frame_form, text="Bulan", bg="white", font=("Segoe UI", 10)).grid(row=0, column=2, padx=(25, 25), pady=(10, 10), sticky="w")
        self.cb_bulan = ttk.Combobox(frame_form, state="readonly", width=15)
        self.cb_bulan.grid(row=0, column=3, padx=(10, 20), pady=(10, 10))

        tk.Label(frame_form, text="Tahun", bg="white", font=("Segoe UI", 10)).grid(row=0, column=4, padx=(25, 25), pady=(10, 10), sticky="w")
        self.cb_tahun = ttk.Combobox(frame_form, state="readonly", width=15)
        self.cb_tahun.grid(row=0, column=5, padx=(10, 20), pady=(10, 10))

        penyewa_list, bulan_list, tahun_list = self.controller.get_filter_options()
        self.cb_penyewa["values"] = ["Pilih Penyewa"] + penyewa_list
        self.cb_bulan["values"] = ["Pilih Bulan"] + bulan_list
        self.cb_tahun["values"] = ["Pilih Tahun"] + tahun_list
        self.cb_penyewa.current(0)
        self.cb_bulan.current(0)
        self.cb_tahun.current(0)

        btn_lihat = tk.Button(
            frame_form, text="Lihat Transaksi", bg="#4CAF50", fg="white",
            font=("Segoe UI", 8, "bold"), command=self.lihat_transaksi
        )
        btn_lihat.grid(row=0, column=6, padx=(25, 20), pady=(10, 10))

    def create_detail_transaksi(self):
        frame_detail = tk.LabelFrame(self, text="Detail Transaksi", font=("Segoe UI", 10, "bold"), bg="white")
        frame_detail.pack(padx=10, pady=(5, 10), fill="both", expand=True)

        frame_form = tk.Frame(frame_detail, bg="white")
        frame_form.pack(fill="both", expand=True, padx=10, pady=10)

        labels = [
            "Kode Transaksi", "Nama Penyewa", "Nama Unit",
            "Tanggal Transaksi", "Tanggal Mulai", "Tanggal Selesai",
            "Total Harga", "Diskon", "Biaya Tambahan",
            "Jumlah Bayar", "Uang Penyewa", "Kembalian",
            "Status Bayar"
        ]

        row = 0
        col = 0
        for i, label in enumerate(labels):
            tk.Label(frame_form, text=label, bg="white", font=("Segoe UI", 10)).grid(
                row=row, column=col * 2, sticky="w", padx=(30, 30), pady=10
            )
            ent = tk.Entry(frame_form, width=22, state="readonly", readonlybackground="white", fg="black")
            ent.grid(row=row, column=col * 2 + 1, padx=(0, 20), pady=5, sticky="w")
            self.entries[label.lower().replace(" ", "_")] = ent

            col += 1
            if col == 3:
                col = 0
                row += 1

        button_row = row + 1
        action_preview_container = tk.Frame(frame_form, bg="white")
        action_preview_container.grid(row=button_row, column=0, columnspan=6, pady=(20, 0), sticky="w")

        frame_tombol = tk.Frame(action_preview_container, bg="white")
        frame_tombol.pack(side="left", padx=30, pady=(0, 220))

        btn_cetak = tk.Button(frame_tombol, text="Cetak Struk", bg="#4CAF50", fg="white", font=("Segoe UI", 9, "bold"), width=14, command=self.cetak_struk_pdf)
        btn_cetak.pack(pady=3)

        btn_hapus = tk.Button(frame_tombol, text="Hapus", bg="#f44336", fg="white", font=("Segoe UI", 9, "bold"), width=14)
        btn_hapus.pack(pady=3)

        preview = tk.LabelFrame(action_preview_container, text="Preview Struk", bg="white", width=240, height=300,
                                font=("Segoe UI", 9, "bold"))
        preview.pack(side="left")
        preview.pack_propagate(False)
        self.preview_text = tk.Label(preview, bg="white", justify="left", anchor="nw", font=("Courier New", 7))
        self.preview_text.pack(fill="both", expand=True)

    def lihat_transaksi(self):
        nama_penyewa = self.cb_penyewa.get()
        bulan = self.cb_bulan.get()
        tahun = self.cb_tahun.get()

        if "Pilih" in nama_penyewa or "Pilih" in bulan or "Pilih" in tahun:
            messagebox.showwarning("Peringatan", "Harap pilih penyewa, bulan, dan tahun.")
            return

        data = self.controller.get_detail_transaksi(nama_penyewa, bulan, tahun)
        if not data:
            messagebox.showinfo("Info", "Data tidak ditemukan.")
            return

        detail = data[0]

        for key, entry in self.entries.items():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(detail.get(key, "")))
            self.tampilkan_preview_struk()
            entry.config(state="readonly")

    def tampilkan_preview_struk(self):
        e = self.entries  # biar singkat

        struk = f"""
              SIkost VibeHouse
      Jl. Buah Batu No. 12 Kota Bandung
               0823-2030-8986
    --------------------------------------
    Tanggal     : {e['tanggal_transaksi'].get()}
    Kode Trans  : {e['kode_transaksi'].get()}
    --------------------------------------
    Penyewa     : {e['nama_penyewa'].get()}
    Unit        : {e['nama_unit'].get()}
    Periode     : {e['tanggal_mulai'].get()} - {e['tanggal_selesai'].get()}
    --------------------------------------
    Total Bayar : Rp. {e['jumlah_bayar'].get()}
    Diskon      : Rp. {e['diskon'].get()}
    Tambahan    : Rp. {e['biaya_tambahan'].get()}
    Bayar (Cash): Rp. {e['uang_penyewa'].get()}
    Kembalian   : Rp. {e['kembalian'].get()}
    Status      : {e['status_bayar'].get()}
    --------------------------------------
              ~~ TERIMA KASIH ~~
    """
        self.preview_text.config(text=struk)

    def cetak_struk_pdf(self):
        e = self.entries

        struk_lines = [
            "SIkost VibeHouse",
            "Jl. Buah Batu No. 12 Kota Bandung",
            "0823-2030-8986",
            "-" * 40,
            f"Tanggal     : {e['tanggal_transaksi'].get()}",
            f"Kode Trans  : {e['kode_transaksi'].get()}",
            "-" * 40,
            f"Penyewa     : {e['nama_penyewa'].get()}",
            f"Unit        : {e['nama_unit'].get()}",
            f"Periode     : {e['tanggal_mulai'].get()} - {e['tanggal_selesai'].get()}",
            "-" * 40,
            f"Total Bayar : Rp. {e['jumlah_bayar'].get()}",
            f"Diskon      : Rp. {e['diskon'].get()}",
            f"Tambahan    : Rp. {e['biaya_tambahan'].get()}",
            f"Bayar (Cash): Rp. {e['uang_penyewa'].get()}",
            f"Kembalian   : Rp. {e['kembalian'].get()}",
            f"Status      : {e['status_bayar'].get()}",
            "-" * 40,
            "~~ TERIMA KASIH ~~"
        ]

        width, height = (80 * mm, 80 * mm)
        nama_penyewa = e['nama_penyewa'].get()
        nama_unit = e['nama_unit'].get()
        nama_penyewa_clean = re.sub(r'\W+', '_', nama_penyewa.strip())
        nama_unit_clean = re.sub(r'\W+', '_', nama_unit.strip())
        tanggal_str = datetime.now().strftime("%Y%m%d")
        filename = f"Struk_Transaksi_{tanggal_str}_{nama_penyewa_clean}_{nama_unit_clean}.pdf"
        pdf_path = os.path.join(tempfile.gettempdir(), filename)

        c = canvas.Canvas(pdf_path, pagesize=(width, height))
        c.setFont("Courier", 8)

        y = height - 15
        for i, line in enumerate(struk_lines):
            if i <= 2 or i == len(struk_lines) - 1:
                text_width = c.stringWidth(line, "Courier", 8)
                c.drawString((width - text_width) / 2, y, line)
            else:
                c.drawString(10, y, line)
            y -= 10

        c.save()

        if platform.system() == "Windows":
            os.startfile(pdf_path)
        elif platform.system() == "Darwin":
            os.system(f"open '{pdf_path}'")
        else:
            os.system(f"xdg-open '{pdf_path}'")
