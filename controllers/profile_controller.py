from database.connection import Database
from models.users import User

class ProfileController:
    def __init__(self, kode_user):
        self.db = Database()
        self.kode_user = kode_user

    def get_user_profile(self):
        query = self.db.cursor
        query.execute("SELECT kode_user, nama, username FROM users WHERE kode_user = %s", (self.kode_user,))
        user = query.fetchone()
        return dict(user) if user else None

    def update_profile(self, kode_user, nama, username):
        try:
            query = self.db.cursor
            query.execute("""
                UPDATE users SET nama = %s, username = %s
                WHERE kode_user = %s
            """, (nama, username, kode_user))  # ✅ 3 parameter dikirim
            self.db.commit()
            return query.rowcount > 0
        except Exception as e:
            print("Error update profile:", e)
            return False

    def update_password(self, old_password, new_password):
        query = self.db.cursor
        query.execute("SELECT password FROM users WHERE kode_user = %s", (self.kode_user,))
        user = query.fetchone()

        if user and user["password"] == old_password:  # Bisa diganti dengan hash comparison
            query.execute("""
                UPDATE users SET password = %s WHERE kode_user = %s
            """, (new_password, self.kode_user))
            self.db.commit()
            return True
        return False