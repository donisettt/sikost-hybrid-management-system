import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import Database
from PIL import Image, ImageTk
import io

class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, bg="white")
        self.master = master
        self.on_login_success = on_login_success
        self.db = Database()

        self.pack_propagate(False)
        self.config(width=600, height=400, bg="white")

        self.center_frame = tk.Frame(self, bg="white")
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background="white")
        style.configure("TLabel", font=("Segoe UI", 12), background="white")
        style.configure("TEntry", font=("Segoe UI", 12))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#007ACC", background="white")

        style.configure("Green.TButton",
                        background="#4CAF50",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"),
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor='none')
        style.map("Green.TButton",
                  background=[("active", "#45a049"), ("!disabled", "#4CAF50")],
                  foreground=[("disabled", "gray")])

        image_url = "C:/Users/Lutfi  Mahesa/Documents/Pi/01STTB/Tugas Kuliah/Semester 4/PBO2/Project UAS Kelompok 3/sikost-hybrid-management-system/image/logos.png"
        try:
            with open(image_url, 'rb') as f:
                raw_data = f.read()
            try:
                resample_mode = Image.Resampling.LANCZOS
            except AttributeError:
                resample_mode = Image.ANTIALIAS
            im = Image.open(io.BytesIO(raw_data)).resize((200, 200), resample_mode)
            self.photo = ImageTk.PhotoImage(im)
        except Exception as e:
            print(f"Gagal load gambar: {e}")
            self.photo = None

        self.center_frame = tk.Frame(self, bg="white", padx=30, pady=30, relief=tk.RIDGE, borderwidth=2)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        if self.photo:
            image_label = tk.Label(self.center_frame, image=self.photo, bg="white")
            image_label.pack(pady=(0, 15))

        header = ttk.Label(self.center_frame, text="SIkost VibeHouse", style="Header.TLabel")
        header.pack(pady=(0, 15))

        form_frame = tk.Frame(self.center_frame, bg="white")
        form_frame.pack()

        tk.Label(form_frame, text="👤 Username:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, sticky=tk.W, pady=6, padx=5)
        self.entry_user = ttk.Entry(form_frame, width=30)
        self.entry_user.grid(row=0, column=1, pady=6, padx=5)

        tk.Label(form_frame, text="🔒 Password:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, sticky=tk.W, pady=6, padx=5)
        self.entry_pass = ttk.Entry(form_frame, show="*", width=30)
        self.entry_pass.grid(row=1, column=1, pady=6, padx=5)

        self.entry_pass.bind("<Return>", self.on_enter_pressed)

        login_btn = ttk.Button(form_frame, text="🚀 Login", command=self.login, style="Green.TButton")
        login_btn.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

    def on_enter_pressed(self, event):
        if self.entry_pass.get().strip():
            self.login()

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        user_data = self.db.cek_login(username, password)
        if user_data:
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")