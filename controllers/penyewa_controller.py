from database.connection import Database
from models.penyewa import Penyewa

class PenyewaController:
    def __init__(self):
        self.db = Database()

    def fetch_kode_unit(self):
        query = """
            SELECT kd_unit FROM unit_kamar
            WHERE status = 'kosong'
        """
        self.db.execute(query)
        result = self.db.fetchall()
        kode_units = [row["kd_unit"] for row in result]
        return kode_units

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
                status=row["status"],
                kd_unit=row["kd_unit"]
            )
            penyewa_list.append(penyewa)
        return penyewa_list

    def tambah_penyewa(self, penyewa: Penyewa):
        penyewa.status = penyewa.status.strip()

        if penyewa.status not in ["Aktif", "Non-Aktif"]:
            raise ValueError("Status penyewa tidak valid.")

        query = """
            INSERT INTO penyewa (kd_penyewa, nama, jenis_kelamin, no_hp, alamat, status, kd_unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        params = (
            penyewa.kd_penyewa,
            penyewa.nama,
            penyewa.jenis_kelamin,
            penyewa.no_hp,
            penyewa.alamat,
            penyewa.status,
            penyewa.kd_unit
        )
        self.db.execute(query, params)
        self.db.commit()

        query_update_status = """
            UPDATE unit_kamar SET status = 'terisi' WHERE kd_unit = %s
        """
        self.db.execute(query_update_status, (penyewa.kd_unit,))
        self.db.commit()

    def update_penyewa(self, penyewa: Penyewa):
        query_get_old_kd_unit = "SELECT kd_unit FROM penyewa WHERE kd_penyewa = %s"
        self.db.execute(query_get_old_kd_unit, (penyewa.kd_penyewa,))
        result = self.db.fetchone()

        if result:
            old_kd_unit = result["kd_unit"]
            query = """
                UPDATE penyewa
                SET nama = %s, jenis_kelamin = %s, no_hp = %s, alamat = %s, status = %s, kd_unit = %s
                WHERE kd_penyewa = %s
            """
            params = (
                penyewa.nama,
                penyewa.jenis_kelamin,
                penyewa.no_hp,
                penyewa.alamat,
                penyewa.status,
                penyewa.kd_unit,
                penyewa.kd_penyewa
            )
            self.db.execute(query, params)
            query_update_old_unit = "UPDATE unit_kamar SET status = 'kosong' WHERE kd_unit = %s"
            self.db.execute(query_update_old_unit, (old_kd_unit,))
            query_update_new_unit = "UPDATE unit_kamar SET status = 'terisi' WHERE kd_unit = %s"
            self.db.execute(query_update_new_unit, (penyewa.kd_unit,))
            self.db.commit()

    def hapus_penyewa(self, kd_penyewa):
        query_get_kd_unit = "SELECT kd_unit FROM penyewa WHERE kd_penyewa = %s"
        self.db.execute(query_get_kd_unit, (kd_penyewa,))
        result = self.db.fetchone()

        if result:
            kd_unit = result["kd_unit"]
            query_delete = "DELETE FROM penyewa WHERE kd_penyewa = %s"
            self.db.execute(query_delete, (kd_penyewa,))
            query_update_status = "UPDATE unit_kamar SET status = 'kosong' WHERE kd_unit = %s"
            self.db.execute(query_update_status, (kd_unit,))
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
                status=row["status"],
                kd_unit=row["kd_unit"]
            )
            penyewa_list.append(penyewa)
        return penyewa_list

    def get_all_penyewa(self):
        query = self.db.cursor
        query.execute("SELECT kd_penyewa, nama, jenis_kelamin, no_hp, alamat, status, kd_unit FROM penyewa")
        data = query.fetchall()
        return [dict(row) for row in data]

    def generate_kd_penyewa(self):
        query = "SELECT kd_penyewa FROM penyewa ORDER BY kd_penyewa DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_code = result["kd_penyewa"]
            last_number = int(last_code.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1
        new_code = f"VH-{new_number:03d}"
        return new_code

    def close_connection(self):
        self.db.close()