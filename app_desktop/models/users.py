class User:
    def __init__(self, kd_user, nama, username, password):
        self.kd_user = kd_user
        self.nama = nama
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "kd_user": self.kd_user,
            "nama": self.nama,
            "username": self.username,
            "password": self.password
        }