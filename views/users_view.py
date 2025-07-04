import tkinter as tk
from tkinter import ttk, messagebox
from models.users import User
from controllers.users_controller import UsersController

class UserApp(tk.Frame):
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
        self.controller = UsersController()

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

        judul = tk.Label(self, text="Manajemen User 🧑️", font=("Segoe UI", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        judul.pack(pady=(10, 15))

        frame_input = tk.LabelFrame(self, text="Form User", font=("Segoe UI", 12, "bold"), bg=self.entry_bg, fg=self.fg_color, padx=20, pady=20)
        frame_input.pack(padx=20, pady=(0, 10), fill=tk.X)

        labels = ["Kode User", "Nama", "No HP", "Username", "Password","Role"]
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

            ent_key = label_text.lower().replace(" ", "_")

            if ent_key == "password":
                ent = ttk.Entry(frame_input, width=40, show="*")
                ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[ent_key] = ent

            elif ent_key == "kode_user":
                ent = ttk.Entry(frame_input, width=40, state='disabled')
                ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                self.entries[ent_key] = ent

            elif ent_key == "role":
                self.role_var = tk.StringVar(value="admin")
                frame_radio = tk.Frame(frame_input, bg=self.entry_bg)
                frame_radio.grid(row=i, column=1, pady=6, padx=(5, 0), sticky='w')

                rb_admin = ttk.Radiobutton(frame_radio, text="Admin", variable=self.role_var, value="admin")
                rb_petugas = ttk.Radiobutton(frame_radio, text="Petugas", variable=self.role_var, value="petugas")

                rb_admin.pack(side='left', padx=5)
                rb_petugas.pack(side='left', padx=5)

            else:
                if ent_key == "no_hp":
                    def hanya_angka(char):
                        return char.isdigit() or char == ""

                    vcmd = (self.register(hanya_angka), '%P')

                    ent = ttk.Entry(frame_input, width=40, validate='key', validatecommand=vcmd)
                    ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                    self.entries[ent_key] = ent

                    def validasi_nomor(e, entry_target):
                        nomor = entry_target.get().strip()
                        if nomor.startswith("0"):
                            nomor = "62" + nomor[1:]
                        elif not nomor.startswith("62"):
                            nomor = "62" + nomor
                        entry_target.delete(0, tk.END)
                        entry_target.insert(0, nomor)

                        if not (10 <= len(nomor) <= 15):
                            tk.messagebox.showwarning("Nomor Tidak Valid","Nomor HP harus terdiri dari 10 hingga 15 digit.")
                            entry_target.focus_set()  # Balikin fokus ke kolom
                            return

                    ent.bind("<FocusOut>", lambda e, entry_target=ent: validasi_nomor(e, entry_target))

                else:
                    ent = ttk.Entry(frame_input, width=40)
                    ent.grid(row=i, column=1, pady=6, padx=(5, 0))
                    self.entries[ent_key] = ent

        frame_buttons = tk.Frame(frame_input, bg=self.entry_bg)
        frame_buttons.grid(row=0, column=2, rowspan=5, padx=15, pady=(0, 33))

        self.btn_add = tk.Button(frame_buttons, text="Tambah", command=self.tambah_users, fg="white", bg="#4CAF50")
        self.btn_update = tk.Button(frame_buttons, text="Update", command=self.update_users, fg="white", bg="#2196F3")
        self.btn_delete = tk.Button(frame_buttons, text="Hapus", command=self.hapus_users, fg="white", bg="#f44336")
        self.btn_clear = tk.Button(frame_buttons, text="Clear", command=self.clear_form, fg="white", bg="#9E9E9E")

        self.btn_add.pack(fill='x', pady=4)
        self.btn_update.pack(fill='x', pady=4)
        self.btn_delete.pack(fill='x', pady=4)
        self.btn_clear.pack(fill='x', pady=4)

        frame_search = tk.Frame(self, bg=self.bg_color)
        frame_search.pack(fill='x', padx=20, pady=(5, 10))

        lbl_search = tk.Label(frame_search, text="🔍 Cari User:", font=("Segoe UI", 10), bg=self.bg_color, fg=self.fg_color)
        lbl_search.pack(side='left', padx=(0, 5))

        self.entry_search = ttk.Entry(frame_search, width=30)
        self.entry_search.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_search.bind("<KeyRelease>", self.cari_users)

        btn_reset = ttk.Button(frame_search, text="Reset", command=self.load_data)
        btn_reset.pack(side='left')

        table_frame = tk.Frame(self, bg=self.bg_color)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        columns = ("kode_user", "nama", "no_hp", "username", "password", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        header_names = ["Kode User", "Nama", "No HP", "Username", "Password", "Role"]
        for col, header in zip(columns, header_names):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=120, anchor='center')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.load_data()
        self.clear_form()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        user_list = self.controller.fetch_users()
        for user in user_list:
            self.tree.insert('', 'end', values=(
                user.kode_user,
                user.nama,
                user.username,
                "●●●●●●●",
                user.no_hp,
                user.role,
            ))

    def tambah_users(self):
        kd = self.controller.generate_kode_user()
        nama = self.entries['nama'].get().strip()
        username = self.entries['username'].get().strip()
        password = self.entries['password'].get().strip()
        no_hp = self.entries['no_hp'].get().strip()
        role = self.role_var.get()

        if not nama:
            messagebox.showwarning("Peringatan", "Nama user wajib diisi!")
            return

        user = User(kd, nama, username, password, no_hp, role)
        self.controller.tambah_users(user)
        messagebox.showinfo("Sukses", f"User {nama} berhasil ditambahkan dengan kode {kd}.")
        self.load_data()
        self.clear_form()

    def update_users(self):
        kd = self.entries['kode_user'].get().strip()
        nama = self.entries['nama'].get().strip()
        username = self.entries['username'].get().strip()
        password = self.entries['password'].get().strip()
        no_hp = self.entries['no_hp'].get().strip()
        role = self.role_var.get()

        if not kd:
            messagebox.showwarning("Peringatan", "Pilih User yang akan diupdate!")
            return

        user = User(kd, nama, username, password, no_hp, role)
        self.controller.update_users(user)
        messagebox.showinfo("Sukses", f"User {nama} berhasil diupdate.")
        self.load_data()
        self.clear_form()

    def hapus_users(self):
        kd = self.entries['kode_user'].get().strip()
        nama = self.entries['nama'].get().strip()
        if not kd:
            messagebox.showwarning("Peringatan", "Pilih user yang akan dihapus!")
            return
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus {nama}?")
        if confirm:
            self.controller.hapus_users(kd)
            messagebox.showinfo("Sukses", f"User {nama} berhasil dihapus.")
            self.load_data()
            self.clear_form()

    def clear_form(self):
        for ent_key, ent in self.entries.items():
            ent.config(state='normal')
            ent.delete(0, 'end')
        new_kode = self.controller.generate_kode_user()
        self.entries['kode_user'].insert(0, new_kode)
        self.entries['kode_user'].config(state='disabled')
        self.tree.selection_remove(self.tree.selection())

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.entries['kode_user'].config(state='normal')
            self.entries['kode_user'].delete(0, 'end')
            self.entries['kode_user'].insert(0, values[0])
            self.entries['kode_user'].config(state='disabled')

            self.entries['nama'].delete(0, 'end')
            self.entries['nama'].insert(0, values[1])

            self.entries['username'].delete(0, 'end')
            self.entries['username'].insert(0, values[2])

            self.entries['password'].delete(0, 'end')
            self.entries['password'].insert(0, values[3])

            self.entries['no_hp'].delete(0, 'end')
            self.entries['no_hp'].insert(0, values[4])

            role = self.role_var.get()

    def cari_users(self, event):
        keyword = self.entry_search.get().strip()
        if keyword == "":
            users_list = self.controller.fetch_users()
        else:
            users_list = self.controller.cari_users(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users_list:
            self.tree.insert('', 'end', values=(
                user.kode_user,
                user.nama,
                user.username,
                user.password,
                user.no_hp,
                user.role,
            ))