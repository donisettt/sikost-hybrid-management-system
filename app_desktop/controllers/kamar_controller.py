from app_desktop.database.connection import Database
from app_desktop.models.kamar import Kamar

class KamarController:
    def __init__(self):
        self.db = Database()

    def fetch_kamar(self):
        query = "SELECT * FROM kamar"
        self.db.execute(query)
        result = self.db.fetchall()

        kamar_list = []
        for row in result:
            kamar = Kamar(
                kd_kamar=row["kd_kamar"],
                nama_kamar=row["nama_kamar"],
                tipe=row["tipe"],
                jumlah_kamar=row["jumlah_kamar"],
                kuota=row["kuota"],
                harga=row["harga"],
                fasilitas=row["fasilitas"]
            )
            kamar_list.append(kamar)
        return kamar_list

    def tambah_kamar(self, kamar: Kamar):
        query = """
            INSERT INTO kamar (kd_kamar, nama_kamar, tipe, jumlah_kamar, kuota, harga, fasilitas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        params = (
            kamar.kd_kamar,
            kamar.nama_kamar,
            kamar.tipe,
            kamar.jumlah_kamar,
            kamar.kuota,
            kamar.harga,
            kamar.fasilitas
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_kamar(self, kamar: Kamar):
        query = """
        UPDATE kamar
        SET nama_kamar = %s, tipe = %s, jumlah_kamar = %s, kuota = %s, harga = %s, fasilitas = %s
        WHERE kd_kamar = %s
        """
        params = (
            kamar.nama_kamar,
            kamar.tipe,
            kamar.jumlah_kamar,
            kamar.kuota,
            kamar.harga,
            kamar.fasilitas,
            kamar.kd_kamar
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_kamar(self, kd_kamar):
        query = "DELETE FROM kamar WHERE kd_kamar = %s"
        self.db.execute(query, (kd_kamar,))
        self.db.commit()

    def cari_kamar(self, keyword):
        query = """
        SELECT * FROM kamar
        WHERE kd_kamar LIKE %s OR nama_kamar LIKE %s OR tipe LIKE %s OR kuota LIKE %s
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword, like_keyword)
        self.db.execute(query, params)
        result = self.db.fetchall()

        kamar_list = []
        for row in result:
            kamar = Kamar(
                kd_kamar=row["kd_kamar"],
                nama_kamar=row["nama_kamar"],
                tipe=row["tipe"],
                jumlah_kamar=row["jumlah_kamar"],
                kuota=row["kuota"],
                harga=row["harga"],
                fasilitas=row["fasilitas"]
            )
            kamar_list.append(kamar)
        return kamar_list

    def generate_kd_kamar(self):
        query = "SELECT kd_kamar FROM kamar ORDER BY kd_kamar DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_code = result["kd_kamar"]
            last_number = int(last_code.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_code = f"KVH-{new_number:03d}"
        return new_code

    def close_connection(self):
        self.db.close()