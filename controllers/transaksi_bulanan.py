from database.connection import Database
from models.transaksi_bulanan import TransaksiBulanan

class TransaksiBulananController:
    def __init__(self):
        self.db = Database()

    def fetch_transaksi_bulanan(self):
        query = """
        SELECT 
            tb.nama_bulan,
            tb.tahun,
            COUNT(t.kd_transaksi) AS jumlah,
            tb.kd_transaksi_bulanan
        FROM transaksi_bulanan tb
        LEFT JOIN transaksi t ON tb.kd_transaksi_bulanan = t.kd_transaksi_bulanan
        GROUP BY tb.kd_transaksi_bulanan, tb.nama_bulan, tb.tahun
        ORDER BY tb.tahun DESC
        """
        return self.db.fetchall_query(query)

    def insert_transaksi_bulanan(self, kd_transaksi_bulanan, bulan, tahun):
        try:
            query = "INSERT INTO transaksi_bulanan (kd_transaksi_bulanan, nama_bulan, tahun) VALUES (%s, %s, %s)"
            self.db.execute(query, (kd_transaksi_bulanan, bulan, tahun))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def generate_kd_transaksi_bulanan(self):
        query = "SELECT MAX(kd_transaksi_bulanan) as max_kd FROM transaksi_bulanan"
        self.db.execute(query)
        result = self.db.fetchone()

        if result and result["max_kd"]:
            last_kd = result["max_kd"]
            number = int(last_kd[2:]) + 1
        else:
            number = 1

        return f"TB{number:03d}"

    def delete_transaksi_bulanan(self, kd_transaksi_bulanan):
        try:
            delete_transaksi_query = "DELETE FROM transaksi WHERE kd_transaksi_bulanan = %s"
            self.db.execute(delete_transaksi_query, (kd_transaksi_bulanan,))

            delete_bulanan_query = "DELETE FROM transaksi_bulanan WHERE kd_transaksi_bulanan = %s"
            self.db.execute(delete_bulanan_query, (kd_transaksi_bulanan,))

            delete_detail_transaksi_query = "DELETE FROM detail_transaksi WHERE kd_transaksi_bulanan = %s"
            self.db.execute(delete_detail_transaksi_query, (kd_transaksi_bulanan,))

            self.db.commit()
            return True
        except Exception as e:
            print(f"Error delete: {e}")
            self.db.rollback()
            return False