class Transaksi:
    def __init__(self, kd_transaksi, kd_penyewa, kd_kamar, tanggal_bayar, nominal, metode_bayar):
        self.kd_transaksi = kd_transaksi
        self.kd_penyewa = kd_penyewa
        self.kd_kamar = kd_kamar
        self.tanggal_bayar = tanggal_bayar
        self.nominal = nominal
        self.metode_bayar = metode_bayar

    def to_dict(self):
        return {
            "kd_transaksi": self.kd_transaksi,
            "kd_penyewa": self.kd_penyewa,
            "kd_kamar": self.kd_kamar,
            "tanggal_bayar": self.tanggal_bayar,
            "nominal": self.nominal,
            "metode_bayar": self.metode_bayar
        }