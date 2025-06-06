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
                kd_kamar=row["kd_kamar"]
            )
            penyewa_list.append(penyewa)
        return penyewa_list

    def tambah_penyewa(self):
        kd = self.entries['kode_penyewa'].get().strip()
        nama = self.entries['nama'].get().strip()
        jk = self.entries['jenis_kelamin'].get().strip()
        no_hp = self.entries['no_hp'].get().strip()
        alamat = self.entries['alamat'].get().strip()
        hunian = self.entries['kd_kamar'].get().strip()

        if not kd or not nama:
            messagebox.showwarning("Peringatan", "Kode dan Nama Penyewa wajib diisi!")
            return

        try:
            harga_int = int(harga)
        except ValueError:
            messagebox.showwarning("Peringatan", "Harga harus berupa angka!")
            return