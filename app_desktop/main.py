import tkinter as tk
from app_desktop.views.login_view import LoginFrame
from app_desktop.views.dashboard import DashboardApp

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SIkost VibeHouse")
        self.root.geometry("900x600")

        self.login_frame = LoginFrame(self.root, self.show_main_menu)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_menu(self, user_data):
        self.login_frame.pack_forget()
        self.dashboard = DashboardApp(self.root, self.show_login, user_data)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

    def show_login(self):
        self.dashboard.pack_forget()
        self.login_frame = LoginFrame(self.root, self.show_main_menu)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")
    app = App(root)
    root.mainloop()
