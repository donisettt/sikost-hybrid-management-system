class TransaksiBulanan:
    def __init__(self, kd_transaksi, nama_bulan, tahun):
        self.kd_transaksi = kd_transaksi
        self.nama_bulan = nama_bulan
        self.tahun = tahun

    def to_dict(self):
        return {
            "kd_transaksi": self.kd_transaksi,
            "nama_bulan": self.nama_bulan,
            "tahun": self.tahun
        }