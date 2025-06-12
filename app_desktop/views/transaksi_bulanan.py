import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app_desktop.controllers.transaksi_controller import TransaksiController
from app_desktop.views.transaksi_view import TransaksiApp


class TransaksiBulananApp(tk.Frame):
    def __init__(self, parent, controller, user_role):
        super().__init__(parent)
        self.controller = controller
        self.user_role = user_role  # Simpen role user di sini
        self.configure(bg="white")

        # Header
        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(side="top", anchor="w", pady=(10, 10), padx=20)

        self.title_label = tk.Label(
            self.header_frame,
            text="Halaman Transaksi Bulanan",
            font=("Segoe UI", 16, "bold"),
            bg="white"
        )
        self.title_label.pack(side="top", anchor="w")

        self.btn_tambah = tk.Button(
            self.header_frame,
            text="Tambah Transaksi",
            bg="#2ecc71",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.show_input_form
        )
        self.btn_tambah.pack(side="top", anchor="w", pady=(25, 0))

        self.form_frame = None

        # Card container
        self.card_frame = tk.Frame(self, bg="white")
        self.card_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_cards()

    def show_input_form(self):
        if self.form_frame:
            self.form_frame.destroy()

        self.form_frame = tk.Frame(self.header_frame, bg="#ecf0f1", pady=10)
        self.form_frame.pack(side="top", anchor="w", pady=(5, 0))

        tk.Label(self.form_frame, text="Bulan:", bg="#ecf0f1").grid(row=0, column=0, padx=5, pady=5)
        self.entry_bulan = ttk.Combobox(self.form_frame, values=[
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ], state="readonly")
        self.entry_bulan.grid(row=0, column=1, padx=5)

        tk.Label(self.form_frame, text="Tahun:", bg="#ecf0f1").grid(row=0, column=2, padx=5, pady=5)

        tahun_sekarang = datetime.now().year
        tahun_values = [str(tahun_sekarang - 1), str(tahun_sekarang)]
        self.entry_tahun = ttk.Combobox(self.form_frame, values=tahun_values, state="readonly")
        self.entry_tahun.grid(row=0, column=3, padx=5)
        self.entry_tahun.current(1)

        btn_buat = tk.Button(
            self.form_frame,
            text="Buat",
            command=self.buat_transaksi_bulanan,
            bg="#2980b9",
            fg="white"
        )
        btn_buat.grid(row=0, column=4, padx=10)

    def buat_transaksi_bulanan(self):
        bulan = self.entry_bulan.get()
        tahun = self.entry_tahun.get()

        if not bulan or not tahun:
            messagebox.showwarning("Peringatan", "Bulan dan Tahun wajib diisi!")
            return

        data_bulanan = self.controller.fetch_transaksi_bulanan()
        for row in data_bulanan:
            if row["nama_bulan"] == bulan and str(row["tahun"]) == tahun:
                messagebox.showwarning("Peringatan", f"Transaksi untuk {bulan} {tahun} sudah ada!")
                return

        kd_transaksi = self.controller.generate_kd_transaksi_bulanan()
        success = self.controller.insert_transaksi_bulanan(kd_transaksi, bulan, tahun)

        if success:
            messagebox.showinfo("Sukses", f"Transaksi bulan {bulan} {tahun} berhasil dibuat.")
            self.form_frame.destroy()
            self.load_cards()
        else:
            messagebox.showerror("Gagal", "Gagal menambahkan transaksi bulanan.")

    def load_cards(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        data_bulanan = self.controller.fetch_transaksi_bulanan()

        for i, row in enumerate(data_bulanan):
            bulan, tahun, jumlah_transaksi, kd_transaksi = row["nama_bulan"], row["tahun"], row["jumlah"], row[
                "kd_transaksi_bulanan"]
            warna = "#3498db" if i % 3 == 0 else "#95a5a6" if i % 3 == 1 else "#f1c40f"

            card = tk.Frame(self.card_frame, bg="white", bd=1, relief="solid")
            card.grid(row=i // 5, column=i % 5, padx=7, pady=10)

            header = tk.Label(card, text=f"Bulan {bulan} {tahun}", bg=warna, fg="white", font=("Segoe UI", 10, "bold"),
                              width=20)
            header.pack(padx=10, pady=(0, 5))

            jumlah_label_title = tk.Label(card, text="Jumlah Transaksi", font=("Segoe UI", 9), bg="white")
            jumlah_label_title.pack(pady=(5, 0))

            jumlah_label = tk.Label(card, text=str(jumlah_transaksi), font=("Segoe UI", 16, "bold"), bg="white")
            jumlah_label.pack(pady=(0, 5))

            detail = tk.Label(card, text="Selengkapnya >>", fg="blue", cursor="hand2", bg="white")
            detail.pack(pady=(0, 10))

            detail.bind("<Button-1>", lambda e, kd=kd_transaksi: self.lihat_detail_transaksi(kd))

            if self.user_role == "admin":
                btn_hapus = tk.Button(
                    card,
                    text="Hapus",
                    bg="#e74c3c",
                    fg="white",
                    font=("Segoe UI", 8, "bold"),
                    command=lambda kd=kd_transaksi, b=bulan, t=tahun: self.hapus_transaksi_bulanan(kd, b, t)
                )
                btn_hapus.pack(pady=(0, 10))

    def lihat_detail_transaksi(self, kd_transaksi_bulanan):
        from app_desktop.views.transaksi_view import TransaksiApp
        controller_transaksi = TransaksiController()
        self.destroy()
        detail_frame = TransaksiApp(self.master, kd_transaksi_bulanan, controller=controller_transaksi, user_role=self.user_role)
        detail_frame.pack(fill="both", expand=True)

    def show_transaksi_view(self):
        self.frame.pack_forget()
        self.transaksi_view = TransaksiApp(self.root)
        self.transaksi_view.pack(fill=tk.BOTH, expand=True)

    def hapus_transaksi_bulanan(self, kd_transaksi, nama_bulan, tahun):
        if messagebox.askyesno("Konfirmasi", f"Yakin mau hapus transaksi {nama_bulan} {tahun}?"):
            success = self.controller.delete_transaksi_bulanan(kd_transaksi)
            if success:
                messagebox.showinfo("Sukses", f"Transaksi {nama_bulan} {tahun} berhasil dihapus.")
                self.load_cards()
            else:
                messagebox.showerror("Gagal", f"Gagal menghapus transaksi {nama_bulan} {tahun}.")
