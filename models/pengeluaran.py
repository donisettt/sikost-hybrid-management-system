class Pengeluaran:
    def __init__(self, kd_pengeluaran, tanggal, kategori, deskripsi, jumlah_harga, dibuat_oleh, bukti):
        self.kd_pengeluaran = kd_pengeluaran
        self.tanggal = tanggal
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.jumlah_harga = jumlah_harga
        self.dibuat_oleh = dibuat_oleh
        self.bukti = bukti

    def to_dict(self):
        return {
            "kd_pengeluaran": self.kd_pengeluaran,
            "tanggal": self.tanggal,
            "kategori": self.kategori,
            "deskripsi": self.deskripsi,
            "jumlah": self.jumlah_harga,
            "dibuat_oleh": self.dibuat_oleh,
            "bukti": self.bukti
        }