from app_desktop.database.connection import Database
from app_desktop.models.unit_kamar import UnitKamar
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UnitKamarController:
    def __init__(self):
        self.db = Database()

    def fetch_unitKamar(self):
        query = """
            SELECT uk.kd_unit, uk.kd_kamar, k.nama_kamar, uk.status
            FROM unit_kamar uk
            JOIN kamar k ON uk.kd_kamar = k.kd_kamar
            ORDER BY uk.kd_unit
        """
        try:
            self.db.execute(query)
            rows = self.db.fetchall()
            unitKamar_list = [
                {
                    "kd_unit": row["kd_unit"],
                    "kd_kamar": row["kd_kamar"],
                    "nama_kamar": row["nama_kamar"],
                    "status": row["status"]
                } for row in rows
            ]
            return unitKamar_list
        except Exception as e:
            logging.error(f"Error fetching unit kamar: {e}")
            return []

    def fetch_kamar(self):
        query = "SELECT kd_kamar, nama_kamar FROM kamar ORDER BY kd_kamar"
        try:
            self.db.execute(query)
            rows = self.db.fetchall()
            return [{"kd_kamar": row["kd_kamar"], "nama_kamar": row["nama_kamar"]} for row in rows]
        except Exception as e:
            logging.error(f"Error fetching kamar records: {e}")
            return []

    def fetch_kamar_combobox(self):
        kamar_list = self.fetch_kamar()
        return [f"{k['kd_kamar']} | {k['nama_kamar']}" for k in kamar_list]

    def tambah_unitKamar(self, unitKamar: UnitKamar):
        if self.cek_kd_unit_exists(unitKamar.kd_unit):
            logging.warning(f"kd_unit {unitKamar.kd_unit} sudah ada, tidak bisa tambah.")
            raise ValueError(f"Unit kamar dengan kd_unit '{unitKamar.kd_unit}' sudah ada.")
        query = """
            INSERT INTO unit_kamar (kd_unit, kd_kamar, status) VALUES (%s, %s, %s)
        """
        params = (unitKamar.kd_unit, unitKamar.kd_kamar, unitKamar.status)
        try:
            self.db.execute(query, params)
            self.db.commit()
            logging.info(f"Added unit kamar with kd_unit={unitKamar.kd_unit}")
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error adding unit kamar: {e}")
            raise

    def update_unitKamar(self, unitKamar: UnitKamar):
        query = """
            UPDATE unit_kamar
            SET kd_kamar = %s, status = %s
            WHERE kd_unit = %s
        """
        params = (unitKamar.kd_kamar, unitKamar.status, unitKamar.kd_unit)
        try:
            self.db.execute(query, params)
            self.db.commit()
            logging.info(f"Updated unit kamar with kd_unit={unitKamar.kd_unit}")
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error updating unit kamar: {e}")
            raise

    def update_status_unitKamar(self, kd_unit, status):
        query = "UPDATE unit_kamar SET status = %s WHERE kd_unit = %s"
        params = (status, kd_unit)
        try:
            self.db.execute(query, params)
            self.db.commit()
            logging.info(f"Updated status unit kamar kd_unit={kd_unit} to {status}")
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error updating status unit kamar: {e}")
            raise

    def hapus_unitKamar(self, kd_unit):
        try:
            query_update_penyewa = "UPDATE penyewa SET kd_unit = NULL WHERE kd_unit = %s"
            self.db.execute(query_update_penyewa, (kd_unit,))

            query_delete_unit = "DELETE FROM unit_kamar WHERE kd_unit = %s"
            self.db.execute(query_delete_unit, (kd_unit,))

            self.db.commit()
            logging.info(f"Unit kamar {kd_unit} berhasil dihapus dan kd_unit di tabel penyewa di-set NULL")

        except Exception as e:
            self.db.rollback()
            logging.error(f"Gagal hapus unit kamar {kd_unit}: {e}")
            raise

    def cari_unitKamar(self, keyword):
        query = """
            SELECT * FROM unit_kamar
            WHERE kd_unit LIKE %s OR status LIKE %s OR kd_kamar LIKE %s
            ORDER BY kd_unit
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword)
        try:
            self.db.execute(query, params)
            rows = self.db.fetchall()
            unitKamar_list = [
                UnitKamar(
                    kd_unit=row["kd_unit"],
                    kd_kamar=row["kd_kamar"],
                    status=row["status"]
                ) for row in rows
            ]
            logging.info(f"Found {len(unitKamar_list)} unit kamar matching keyword '{keyword}'.")
            return unitKamar_list
        except Exception as e:
            logging.error(f"Error searching unit kamar: {e}")
            return []

    def cek_kd_unit_exists(self, kd_unit):
        query = "SELECT 1 FROM unit_kamar WHERE kd_unit = %s LIMIT 1"
        params = (kd_unit,)
        try:
            self.db.execute(query, params)
            row = self.db.fetchone()
            return row is not None
        except Exception as e:
            logging.error(f"Error checking kd_unit existence: {e}")
            return False

    def get_jumlah_kamar(self, kd_kamar):
        query = "SELECT jumlah_kamar FROM kamar WHERE kd_kamar = %s"
        params = (kd_kamar,)
        result = self.db.query_one(query, params)
        if result:
            return result['jumlah_kamar']
        else:
            raise ValueError("Kode kamar tidak ditemukan")

    def count_unit_kamar(self, kd_kamar):
        query = "SELECT COUNT(*) as total FROM unit_kamar WHERE kd_kamar = %s"
        params = (kd_kamar,)
        result = self.db.query_one(query, params)
        return result['total'] if result else 0

    def close_connection(self):
        try:
            self.db.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error closing database connection: {e}")
