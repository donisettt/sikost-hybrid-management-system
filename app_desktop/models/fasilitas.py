class Fasilitas:
    def __init__(self, kd_fasilitas, nama, status):
        self.kd_fasilitas = kd_fasilitas
        self.nama = nama
        self.status = status

    def to_dict(self):
        return {
            "kd_fasilitas": self.kd_fasilitas,
            "nama": self.nama,
            "status": self.status
        }