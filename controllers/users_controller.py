from database.connection import Database
from models.users import User

class UsersController:
    def __init__(self):
        self.db = Database()

    def fetch_users(self):
        query = "SELECT * FROM users"
        self.db.execute(query)
        result = self.db.fetchall()

        users_list = []
        for row in result:
            users = User(
                kode_user=row["kode_user"],
                nama=row["nama"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            )
            users_list.append(users)
        return users_list

    def tambah_users(self, user: User):
        query = """
            INSERT INTO users (kode_user, nama, username, password, role) VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            user.kode_user,
            user.nama,
            user.username,
            user.password,
            user.role
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_users(self, user: User):
        query = """
            UPDATE users
            SET nama = %s, username = %s, password = %s, role = %s
            WHERE kode_user = %s
        """
        params = (
            user.nama,
            user.username,
            user.password,
            user.role,
            user.kode_user
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_users(self, kode_user):
        query = "DELETE FROM users WHERE kode_user = %s"
        self.db.execute(query, (kode_user,))
        self.db.commit()

    def cari_users(self, keyword):
        query = """
            SELECT * FROM users
            WHERE kode_user LIKE %s OR nama LIKE %s OR username LIKE %s OR role LIKE %s
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword, like_keyword)
        self.db.execute(query, params)
        result = self.db.fetchall()

        users_list = []
        for row in result:
            user = User(
                kode_user=row["kode_user"],
                nama=row["nama"],
                username=row["username"],
                password=row["password"],
                role=row["role"]
            )
            users_list.append(user)
        return users_list

    def generate_kode_user(self):
        query = "SELECT kode_user FROM users WHERE kode_user LIKE 'USR-VH-%' ORDER BY kode_user DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_kode = result['kode_user']
            last_number = int(last_kode.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_kode = f"USR-VH-{new_number:03d}"
        return new_kode

    def close_connection(self):
        self.db.close()