from app_desktop.database.connection import Database
from app_desktop.models.penyewa import Penyewa

class PenyewaController:
    def __init__(self):
        self.db = Database()

    def fetch_penyewa(self):
        query = "SELECT * FROM penyewa"
        self.db.execute(query)
        result = self.db.fetchall()

        penyewa_list = []
        for row in result:
            penyewa = Penyewa(
                kd_penyewa=row["kd_penyewa"],
                nama=row["nama"],
                jenis_kelamin=row["jenis_kelamin"],
                no_hp=row["no_hp"],
                alamat=row["alamat"],
                kd_unit=row["kd_unit"]
            )
            penyewa_list.append(penyewa)
        return penyewa_list

    def tambah_penyewa(self, penyewa: Penyewa):
        query = """
            INSERT INTO penyewa (kd_penyewa, nama, jenis_kelamin, no_hp, alamat, kd_unit)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        params = (
            penyewa.kd_penyewa,
            penyewa.nama,
            penyewa.jenis_kelamin,
            penyewa.no_hp,
            penyewa.alamat,
            penyewa.kd_unit
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_penyewa(self, penyewa: Penyewa):
        query = """
            UPDATE penyewa
            SET nama = %s, jenis_kelamin = %s, no_hp = %s, alamat = %s, kd_unit = %s
            WHERE kd_penyewa = %s
        """
        params = (
            penyewa.nama,
            penyewa.jenis_kelamin,
            penyewa.no_hp,
            penyewa.alamat,
            penyewa.kd_unit,
            penyewa.kd_penyewa
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_penyewa(self, kd_penyewa):
        query = "DELETE from penyewa where kd_penyewa = %s"
        self.db.execute(query, (kd_penyewa,))
        self.db.commit()

    def cari_penyewa(self, keyword):
        query = """
            SELECT * FROM penyewa
            where kd_penyewa LIKE %s OR nama LIKE %s OR kd_unit LIKE %s
            """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword)
        self.db.execute(query, params)
        result = self.db.fetchall()

        penyewa_list = []
        for row in result:
            penyewa = Penyewa(
                kd_penyewa=row["kd_penyewa"],
                nama=row["nama"],
                jenis_kelamin=row["jenis_kelamin"],
                no_hp=row["no_hp"],
                alamat=row["alamat"],
                kd_unit=row["kd_unit"]
            )
            penyewa_list.append(penyewa)
        return penyewa_list

    def close_connection(self):
        self.db.close()