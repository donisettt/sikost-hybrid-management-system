from datetime import datetime
from database.connection import Database

class DashboardController:
    def __init__(self):
        self.db = Database()

    def get_jumlah_penyewa(self):
        query = "SELECT COUNT(*) AS total FROM penyewa"
        self.db.execute(query)
        return self.db.fetchone()["total"]

    def get_jumlah_transaksi_bulan_ini(self):
        now = datetime.now()
        query = """
            SELECT COUNT(*) AS total FROM transaksi
            WHERE MONTH(tanggal_transaksi) = %s AND YEAR(tanggal_transaksi) = %s
        """
        self.db.execute(query, (now.month, now.year))
        return self.db.fetchone()["total"]

    def get_total_transaksi(self):
        self.db.execute("SELECT COUNT(*) AS total FROM transaksi")
        return self.db.fetchone()["total"]

    def get_total_pengeluaran(self):
        self.db.execute("SELECT SUM(jumlah) AS total FROM pengeluaran")
        result = self.db.fetchone()["total"]
        return result if result else 0

    def get_total_pendapatan_bulan_ini(self):
        now = datetime.now()
        query = """
            SELECT SUM(total_harga) AS total FROM transaksi
            WHERE MONTH(tanggal_transaksi) = %s AND YEAR(tanggal_transaksi) = %s
        """
        self.db.execute(query, (now.month, now.year))
        hasil = self.db.fetchone()["total"]
        return hasil if hasil else 0

    def get_transaksi_belum_lunas(self):
        self.db.execute("SELECT COUNT(*) AS total FROM transaksi WHERE status_transaksi != 'Lunas'")
        return self.db.fetchone()["total"]

    def get_transaksi_hari_ini(self):
        today = datetime.today().strftime('%Y-%m-%d')
        self.db.execute("SELECT COUNT(*) AS total FROM transaksi WHERE DATE(tanggal_transaksi) = %s", (today,))
        return self.db.fetchone()["total"]

    def get_top_penyewa(self, limit=5):
        query = """
            SELECT penyewa.nama, COUNT(*) AS total_transaksi
            FROM transaksi
            JOIN penyewa ON transaksi.kd_penyewa = penyewa.kd_penyewa
            GROUP BY transaksi.kd_penyewa
            ORDER BY total_transaksi DESC
            LIMIT %s
        """
        self.db.execute(query, (limit,))
        return self.db.fetchall()

    def get_tren_transaksi_perbulan(self, tahun):
        query = """
            SELECT MONTH(tanggal_transaksi) AS bulan, COUNT(*) AS total
            FROM transaksi
            WHERE YEAR(tanggal_transaksi) = %s
            GROUP BY bulan
            ORDER BY bulan
        """
        self.db.execute(query, (tahun,))
        return self.db.fetchall()

    def get_rasio_pemasukan_pengeluaran(self):
        self.db.execute("SELECT SUM(total_harga) as pemasukan FROM transaksi")
        pemasukan = self.db.fetchone()["pemasukan"] or 0

        self.db.execute("SELECT SUM(jumlah) as pengeluaran FROM pengeluaran")
        pengeluaran = self.db.fetchone()["pengeluaran"] or 0

        return pemasukan, pengeluaran

    def get_notifikasi_jatuh_tempo(self):
        query = """
            SELECT COUNT(*) AS total FROM transaksi 
            WHERE tanggal_selesai BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            AND status_transaksi != 'Lunas'
        """
        self.db.execute(query)
        return self.db.fetchone()["total"]