from database.connection import Database

class LaporanController:
    def __init__(self):
        self.conn = Database()

    def get_laporan_bulanan(self, bulan: str, tahun: str, kategori: str = "Semua"):
        cursor = self.conn.cursor
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            JOIN transaksi_bulanan tb ON t.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
            WHERE tb.nama_bulan = %s AND tb.tahun = %s
        """
        params = [bulan, tahun]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_laporan_tahunan(self, tahun: str, kategori: str = "Semua"):
        cursor = self.conn.cursor
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            JOIN transaksi_bulanan tb ON t.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
            WHERE tb.tahun = %s
        """
        params = [tahun]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_laporan_periode(self, dari_tanggal: str, sampai_tanggal: str, kategori: str = "Semua"):
        cursor = self.conn.cursor
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            WHERE t.tanggal_transaksi BETWEEN %s AND %s
        """
        params = [dari_tanggal, sampai_tanggal]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_pengeluaran_periode(self, dari_tanggal: str, sampai_tanggal: str):
        cursor = self.conn.cursor
        query = """
            SELECT kd_pengeluaran, tanggal, kategori, deskripsi, jumlah, dibuat_oleh, bukti
            FROM pengeluaran
            WHERE tanggal BETWEEN %s AND %s
        """
        cursor.execute(query, (dari_tanggal, sampai_tanggal))
        return cursor.fetchall()