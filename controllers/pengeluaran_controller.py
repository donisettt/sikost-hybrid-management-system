from database.connection import Database
from models.pengeluaran import Pengeluaran
from datetime import datetime

class PengeluaranController:
    def __init__(self):
        self.db = Database()

    def fetch_pengeluaran(self):
        query = "SELECT * FROM pengeluaran"
        self.db.execute(query)
        result = self.db.fetchall()

        pengeluaran_list = []
        for row in result:
            pengeluaran = Pengeluaran(
                kd_pengeluaran=row["kd_pengeluaran"],
                tanggal=row["tanggal"],
                kategori=row["kategori"],
                deskripsi=row["deskripsi"],
                jumlah=row["jumlah"],
                dibuat_oleh=row["dibuat_oleh"],
                bukti=row["bukti"]
            )
            pengeluaran_list.append(pengeluaran)
        return pengeluaran_list

    def tambah_pengeluaran(self, pengeluaran: Pengeluaran):
        query = """
            INSERT INTO pengeluaran (kd_pengeluaran, tanggal, kategori, deskripsi, jumlah,
            dibuat_oleh, bukti) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            pengeluaran.kd_pengeluaran,
            pengeluaran.tanggal,
            pengeluaran.kategori,
            pengeluaran.deskripsi,
            pengeluaran.jumlah,
            pengeluaran.dibuat_oleh,
            pengeluaran.bukti
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_pengeluaran(self, pengeluaran: Pengeluaran):
        query = """
            UPDATE penyewa
            SET tanggal = %s, kategori = %s, deskripsi = %s, jumlah = %s, dibuat_oleh = %s, bukti = %s
            WHERE kd_pengeluaran = %s
        """
        params = (
            pengeluaran.tanggal,
            pengeluaran.kategori,
            pengeluaran.deskripsi,
            pengeluaran.jumlah,
            pengeluaran.dibuat_oleh,
            pengeluaran.bukti,
            pengeluaran.kd_pengeluaran
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_pengeluaran(self, kd_pengeluaran):
        query = "DELETE FROM pengeluaran WHERE kd_pengeluaran = %s"
        self.db.execute(query, (kd_pengeluaran,))
        self.db.commit()

    def cari_pengeluaran(self, keyword):
        query = """
            SELECT * FROM pengeluaran
            WHERE kd_pengeluaran LIKE %s OR kategori LIKE %s OR jumlah LIKE %s OR dibuat_oleh LIKE %s
        """
        like_keyword = f"%{keyword}"
        params = (like_keyword, like_keyword, like_keyword, like_keyword)
        self.db.execute(query, params)
        result = self.db.fetchall()

        pengeluaran_list = []
        for row in result:
            pengeluaran = Pengeluaran(
                kd_pengeluaran=row["kd_pengeluaran"],
                tanggal=row["tanggal"],
                kategori=row["kategori"],
                deskripsi=row["deskripsi"],
                jumlah=row["jumlah"],
                dibuat_oleh=row["dibuat_oleh"],
                bukti=row["bukti"]
            )
            pengeluaran_list.append(pengeluaran)
        return pengeluaran_list

    def generate_kode_pengeluaran(self):
        query = "SELECT kd_pengeluaran FROM pengeluaran ORDER BY kd_pengeluaran DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_code = result["kd_pengeluaran"]
            # Misal: VH-009
            last_number = int(last_code.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_code = f"PGN-{new_number:03d}"
        return new_code

    def close_connection(self):
        self.db.close()