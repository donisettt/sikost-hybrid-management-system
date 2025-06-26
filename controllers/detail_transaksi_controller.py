from database.connection import Database
from models.detail_transaksi import DetailTransaksi

class DetailTransaksiController:
    def __init__(self):
        self.db = Database()
        self.cursor = self.db

    def get_filter_options(self):
        self.cursor.execute("SELECT nama FROM penyewa")
        penyewa = [row["nama"] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT DISTINCT nama_bulan FROM transaksi_bulanan")
        bulan = [row["nama_bulan"] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT DISTINCT tahun FROM transaksi_bulanan")
        tahun = [row["tahun"] for row in self.cursor.fetchall()]

        return penyewa, bulan, tahun

    def get_detail_transaksi(self, nama_penyewa, bulan, tahun):
        query = """
            SELECT 
                dt.kd_detail_transaksi AS kode_detail_transaksi,
                dt.kd_transaksi AS kode_transaksi, 
                p.nama AS nama_penyewa, 
                uk.kd_unit AS nama_unit, 
                dt.tanggal_transaksi, 
                dt.tanggal_mulai, 
                dt.tanggal_selesai,
                dt.total_harga, 
                dt.diskon, 
                dt.biaya_tambahan, 
                dt.jumlah_bayar, 
                dt.uang_penyewa, 
                dt.kembalian, 
                dt.status_transaksi AS status_bayar
            FROM detail_transaksi dt
            JOIN penyewa p ON dt.kd_penyewa = p.kd_penyewa
            JOIN unit_kamar uk ON dt.kd_unit = uk.kd_unit
            JOIN transaksi_bulanan tb ON dt.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
            WHERE p.nama = %s AND tb.nama_bulan = %s AND tb.tahun = %s
        """
        self.cursor.execute(query, (nama_penyewa, bulan, tahun))
        rows = self.cursor.fetchall()
        return rows

    def hapus_detail_transaksi(self, kd_detail_transaksi):
        try:
            query_get = "SELECT kd_transaksi FROM detail_transaksi WHERE kd_detail_transaksi = %s"
            self.cursor.execute(query_get, (kd_detail_transaksi,))
            result = self.cursor.fetchone()

            if result:
                kd_transaksi = result['kd_transaksi']
                query_detail = "DELETE FROM detail_transaksi WHERE kd_detail_transaksi = %s"
                self.cursor.execute(query_detail, (kd_detail_transaksi,))
                query_transaksi = "DELETE FROM transaksi WHERE kd_transaksi = %s"
                self.cursor.execute(query_transaksi, (kd_transaksi,))
                self.db.commit()
                return True
            else:
                print("[DEBUG] Tidak ditemukan: kd_detail_transaksi =", kd_detail_transaksi)
                return False
        except Exception as e:
            print("[ERROR] Saat hapus detail transaksi:", e)
            return False