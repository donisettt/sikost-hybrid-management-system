class DetailTransaksi:
    def __init__(self, kd_detail_transaksi, kd_transaksi, nama_penyewa, nama_unit, tanggal_transaksi,
                 tanggal_mulai, tanggal_selesai, total_harga, diskon, biaya_tambahan, jumlah_bayar,
                 uang_penyewa, kembalian, status_transaksi):
        self.kd_detail = kd_detail_transaksi
        self.kd_transaksi = kd_transaksi
        self.nama_penyewa = nama_penyewa
        self.nama_unit = nama_unit
        self.tgl_transaksi = tanggal_transaksi
        self.tgl_mulai = tanggal_mulai
        self.tgl_selesai = tanggal_selesai
        self.total_harga = total_harga
        self.diskon = diskon
        self.biaya_tambahan = biaya_tambahan
        self.jumlah_bayar = jumlah_bayar
        self.uang_penyewa = uang_penyewa
        self.kembalian = kembalian
        self.status_transaksi = status_transaksi

    def to_dict(self):
        return {
            "kd_detail_transaksi": self.kd_detail,
            "kd_transaksi": self.kd_transaksi,
            "nama_penyewa": self.nama_penyewa,
            "nama_unit": self.nama_unit,
            "tanggal_transaksi": self.tgl_transaksi,
            "tanggal_mulai": self.tgl_mulai,
            "tanggal_selesai": self.tgl_selesai,
            "total_harga": self.total_harga,
            "diskon": self.diskon,
            "biaya_tambahan": self.biaya_tambahan,
            "jumlah_bayar": self.jumlah_bayar,
            "uang_penyewa": self.uang_penyewa,
            "kembalian": self.kembalian,
            "status_transaksi": self.status_transaksi
        }