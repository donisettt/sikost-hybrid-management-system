class User:
    def __init__(self, kode_user, nama, username, password, role):
        self.kode_user = kode_user
        self.nama = nama
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "kode_user": self.kode_user,
            "nama": self.nama,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }