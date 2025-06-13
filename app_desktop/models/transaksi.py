class Transaksi:
    def __init__(self, kd_transaksi, kd_penyewa, kd_unit, tanggal_mulai, tanggal_selesai,tanggal_transaksi, total_harga, status_transaksi, diskon, biaya_tambahan, jumlah_bayar, uang_penyewa, kembalian,kd_transaksi_bulanan=None):
        self.kd_transaksi = kd_transaksi
        self.kd_transaksi_bulanan = kd_transaksi_bulanan
        self.kd_penyewa = kd_penyewa
        self.kd_unit = kd_unit
        self.tanggal_mulai = tanggal_mulai
        self.tanggal_selesai = tanggal_selesai
        self.tanggal_transaksi = tanggal_transaksi
        self.total_harga = total_harga
        self.status_transaksi = status_transaksi
        self.diskon = diskon
        self.biaya_tambahan = biaya_tambahan
        self.jumlah_bayar = jumlah_bayar
        self.uang_penyewa = uang_penyewa
        self.kembalian = kembalian

    def to_dict(self):
        return {
            "kd_transaksi": self.kd_transaksi,
            "kd_transaksi_bulanan": self.kd_transaksi_bulanan,
            "kd_penyewa": self.kd_penyewa,
            "kd_unit": self.kd_unit,
            "tanggal_mulai": self.tanggal_mulai,
            "tanggal_selesai": self.tanggal_selesai,
            "tanggal_transaksi": self.tanggal_transaksi,
            "total_harga": self.total_harga,
            "status_transaksi": self.status_transaksi,
            "diskon": self.diskon,
            "biaya_tambahan": self.biaya_tambahan,
            "jumlah_bayar": self.jumlah_bayar,
            "uang_penyewa": self.uang_penyewa,
            "kembalian": self.kembalian
        }
