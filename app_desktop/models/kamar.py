class Kamar:
    def __init__(self, kd_kamar, nama_kamar, tipe, kuota, harga, fasilitas):
        self.kd_kamar = kd_kamar
        self.nama_kamar = nama_kamar
        self.tipe = tipe
        self.kuota = kuota
        self.harga = harga
        self.fasilitas = fasilitas

    def to_dict(self):
        return {
            "kd_kamar": self.kd_kamar,
            "nama_kamar": self.nama_kamar,
            "tipe": self.tipe,
            "kuota": self.kuota,
            "harga": self.harga,
            "fasilitas": self.fasilitas
        }