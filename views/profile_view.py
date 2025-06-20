import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProfileApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Judul
        tk.Label(self, text="Profile", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=10)

        container = tk.Frame(self, bg="white")
        container.pack(padx=20, pady=10, fill="x")

        # Frame Data Profile
        frame_profile = tk.LabelFrame(container, text="Data Profile", font=("Segoe UI", 10), padx=15, pady=10)
        frame_profile.grid(row=0, column=0, padx=10, sticky="n")
        self.nama_var = tk.StringVar()
        self.username_var = tk.StringVar()

        self.kode_user_var = tk.StringVar()
        tk.Label(frame_profile, text="Kode User", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        kode_user_entry = tk.Entry(frame_profile, textvariable=self.kode_user_var, width=30, state="readonly")
        kode_user_entry.grid(row=0, column=1, pady=5)

        fields = [
            ("Nama", self.nama_var),
            ("Username", self.username_var)
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(frame_profile, text=label, font=("Segoe UI", 10)).grid(row=i + 1, column=0, sticky="w", pady=5)
            tk.Entry(frame_profile, textvariable=var, width=30).grid(row=i + 1, column=1, pady=5)

        # Tombol Simpan & Batal
        frame_btn = tk.Frame(frame_profile)
        frame_btn.grid(row=len(fields) + 1, columnspan=2, pady=10, padx=(104, 0))

        tk.Button(frame_btn, text="Batal", width=8, bg="lightgray", command=self.clear_form).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Simpan", width=8, bg="green", fg="white", command=self.save_profile).pack(side="left", padx=5)

        # Frame Password
        frame_password = tk.LabelFrame(container, text="Data Password", font=("Segoe UI", 10), padx=15, pady=10)
        frame_password.grid(row=0, column=1, padx=10, sticky="n")

        self.old_pass_var = tk.StringVar()
        self.new_pass_var = tk.StringVar()

        tk.Label(frame_password, text="Password", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame_password, textvariable=self.old_pass_var, show="*", width=30).grid(row=0, column=1, pady=5)

        tk.Label(frame_password, text="New Password", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame_password, textvariable=self.new_pass_var, show="*", width=30).grid(row=1, column=1, pady=5)

        tk.Button(frame_password, text="Ubah Password", bg="green", fg="white", width=13, command=self.change_password)\
            .grid(row=2, column=1, sticky="e", pady=10)

        self.load_profile_data()

    def load_profile_data(self):
        user_data = self.controller.get_user_profile()
        if user_data:
            self.kode_user_var.set(user_data["kode_user"])
            self.nama_var.set(user_data["nama"])
            self.username_var.set(user_data["username"])

    def clear_form(self):
        self.nama_var.set("")
        self.username_var.set("")

    def save_profile(self):
        success = self.controller.update_profile(
            self.kode_user_var.get(),  # 👈 Tambahkan ini
            self.nama_var.get(),
            self.username_var.get()
        )
        if success:
            messagebox.showinfo("Berhasil", "Data profil berhasil diperbarui.")
        else:
            messagebox.showerror("Gagal", "Gagal memperbarui profil.")

    def change_password(self):
        if not self.old_pass_var.get() or not self.new_pass_var.get():
            messagebox.showwarning("Peringatan", "Mohon isi semua kolom password.")
            return
        success = self.controller.update_password(
            self.old_pass_var.get(),
            self.new_pass_var.get()
        )
        if success:
            messagebox.showinfo("Berhasil", "Password berhasil diperbarui.")
            self.old_pass_var.set("")
            self.new_pass_var.set("")
        else:
            messagebox.showerror("Gagal", "Password lama salah atau gagal mengubah password.")