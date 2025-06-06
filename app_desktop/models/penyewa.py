class Penyewa:
    def __init__(self, kd_penyewa, nama, jenis_kelamin, no_hp, alamat, kd_kamar):
        self.kd_penyewa = kd_penyewa
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp
        self.alamat = alamat
        self.kd_kamar = kd_kamar

    def to_dict(self):
        return {
            "kd_penyewa": self.kd_penyewa,
            "nama": self.nama,
            "jenis_kelamin": self.jenis_kelamin,
            "no_hp": self.no_hp,
            "alamat": self.alamat,
            "kd_kamar": self.kd_kamar
        }