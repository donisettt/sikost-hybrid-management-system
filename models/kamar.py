class Kamar:
    def __init__(self, kd_kamar, nama_kamar, tipe, jumlah_kamar, kuota, harga, fasilitas):
        self.kd_kamar = kd_kamar
        self.nama_kamar = nama_kamar
        self.tipe = tipe
        self.jumlah_kamar = jumlah_kamar
        self.kuota = kuota
        self.harga = harga
        self.fasilitas = fasilitas

    def to_dict(self):
        return {
            "kd_kamar": self.kd_kamar,
            "nama_kamar": self.nama_kamar,
            "tipe": self.tipe,
            "jumlah_kamar": self.jumlah_kamar,
            "kuota": self.kuota,
            "harga": self.harga,
            "fasilitas": self.fasilitas
        }