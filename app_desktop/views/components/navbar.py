import tkinter as tk
from PIL import Image, ImageTk
import datetime

class Navbar(tk.Frame):
    def __init__(self, master, user_data, on_dashboard_click, on_logout_click, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.user_data = user_data

        self.configure(bg="#5DADE2", height=50)
        left_frame = tk.Frame(self, bg="#5DADE2")
        left_frame.pack(side="left", padx=20, pady=10)

        hamburger = tk.Label(left_frame, text="≡", bg="#5DADE2", fg="white", font=("Segoe UI", 16, "bold"))
        hamburger.pack(side="left", padx=(0, 10))

        # Bikin frame khusus di kanan untuk time label + logout button
        right_frame = tk.Frame(self, bg="#5DADE2")
        right_frame.pack(side="right", pady=10, padx=15)

        # Logout button duluan biar nempel di kanan banget
        btn_logout = tk.Button(
            right_frame, text="Logout",
            bg="#e74c3c", fg="white", relief="flat",
            font=("Segoe UI", 11, "bold"), cursor="hand2",
            activebackground="#c0392b", activeforeground="white",
            command=on_logout_click
        )
        btn_logout.pack(side="right")

        # Time label muncul di kiri tombol logout
        self.time_label = tk.Label(right_frame, bg="#5DADE2", fg="white", font=("Segoe UI", 11, "bold"))
        self.time_label.pack(side="right", padx=(0, 15))
        self.update_time()

    def update_time(self):
        hari_indo = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }
        now = datetime.datetime.now()
        hari = hari_indo[now.strftime("%A")]
        tanggal = now.strftime("%d-%m-%Y")
        formatted_time = f"{hari}, {tanggal}"
        self.time_label.config(text=formatted_time)
        self.after(1000, self.update_time)
