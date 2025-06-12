from app_desktop.database.connection import Database
from app_desktop.models.fasilitas import Fasilitas

class FasilitasController:
    def __init__(self):
        self.db = Database()

    def fetch_fasilitas(self):
        query = "SELECT * FROM fasilitas"
        self.db.execute(query)
        result = self.db.fetchall()

        fasilitas_list = []
        for row in result:
            fasilitas = Fasilitas(
                kd_fasilitas=row["kd_fasilitas"],
                nama=row["nama"],
                status=row["status"]
            )
            fasilitas_list.append(fasilitas)
        return fasilitas_list

    def tambah_fasilitas(self, fasilitas: Fasilitas):
        query = """
            INSERT INTO fasilitas (kd_fasilitas, nama, status) VALUES (%s, %s, %s)
        """
        params = (
            fasilitas.kd_fasilitas,
            fasilitas.nama,
            fasilitas.status
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_fasilitas(self, fasilitas: Fasilitas):
        query = """
            UPDATE fasilitas SET nama = %s, status = %s WHERE kd_fasilitas = %s
        """
        params = (
            fasilitas.nama,
            fasilitas.status,
            fasilitas.kd_fasilitas
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_fasilitas(self, kd_fasilitas):
        query = "DELETE FROM fasilitas WHERE kd_fasilitas = %s"
        self.db.execute(query, (kd_fasilitas,))
        self.db.commit()

    def cari_fasilitas(self, keyword):
        query = """
            SELECT * FROM fasilitas
            WHERE kd_fasilitas LIKE %s OR nama LIKE %s OR status LIKE %s
        """
        like_keyword = f"%{keyword}"
        params = (like_keyword, like_keyword, like_keyword)
        self.db.execute(query, params)
        result = self.db.fetchall()

        fasilitas_list = []
        for row in result:
            fasilitas = Fasilitas(
                kd_fasilitas=row["kd_fasilitas"],
                nama=row["nama"],
                status=row["status"]
            )
            fasilitas_list.append(fasilitas)
        return fasilitas_list

    def generate_kd_fasilitas(self):
        query = "SELECT kd_fasilitas FROM fasilitas ORDER BY kd_fasilitas DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_code = result["kd_fasilitas"]
            last_number = int(last_code.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_code = f"FVH-{new_number:03d}"
        return new_code

    def close_connection(self):
        self.db.close()