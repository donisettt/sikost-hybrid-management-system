from app_desktop.database.connection import Database
from app_desktop.models.transaksi import Transaksi

class TransaksiController:
    def __init__(self):
        self.db = Database()

    def fetch_transaksi(self):
        query = """
            SELECT tr.kd_transaksi, p.nama, uk.kd_unit, tr.tanggal_mulai, tr.tanggal_selesai, tr.tanggal_transaksi, tr.total_harga, tr.status_transaksi
            FROM transaksi tr
            JOIN penyewa p ON tr.kd_penyewa = p.kd_penyewa
            JOIN unit_kamar uk ON tr.kd_unit = uk.kd_unit
        """