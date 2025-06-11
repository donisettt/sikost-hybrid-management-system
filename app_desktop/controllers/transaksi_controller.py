from app_desktop.database.connection import Database
from app_desktop.models.transaksi import Transaksi

class TransaksiController:
    def __init__(self):
        self.db = Database()

    def get_unit_kamar(self):
        query = """
            SELECT unit_kamar.*, kamar.harga
            FROM unit_kamar
            JOIN kamar ON unit_kamar.kd_kamar = kamar.kd_kamar;
        """
        results = self.db.execute(query)
        if results:
            return results
        else:
            return []

    def fetch_transaksi(self):
        query = """
            SELECT tr.kd_transaksi, tr.kd_transaksi_bulanan, p.nama AS kd_penyewa, uk.kd_unit,
                   tr.tanggal_mulai, tr.tanggal_selesai, tr.tanggal_transaksi,
                   tr.total_harga, tr.status_transaksi
            FROM transaksi tr
            JOIN penyewa p ON tr.kd_penyewa = p.kd_penyewa
            JOIN unit_kamar uk ON tr.kd_unit = uk.kd_unit
        """
        self.db.execute(query)
        result = self.db.fetchall()

        transaksi_list = []
        for row in result:
            transaksi = Transaksi(
                kd_transaksi=row["kd_transaksi"],
                kd_transaksi_bulanan=row["kd_transaksi_bulanan"],
                kd_penyewa=row["kd_penyewa"],
                kd_unit=row["kd_unit"],
                tanggal_mulai=row["tanggal_mulai"],
                tanggal_selesai=row["tanggal_selesai"],
                tanggal_transaksi=row["tanggal_transaksi"],
                total_harga=row["total_harga"],
                status_transaksi=row["status_transaksi"]
            )
            transaksi_list.append(transaksi)
        return transaksi_list

    def tambah_transaksi(self, transaksi: Transaksi):
        query = """
            INSERT INTO transaksi (
                kd_transaksi, kd_transaksi_bulanan, kd_penyewa, kd_unit,
                tanggal_mulai, tanggal_selesai, tanggal_transaksi,
                total_harga, status_transaksi
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            transaksi.kd_transaksi,
            transaksi.kd_transaksi_bulanan,
            transaksi.kd_penyewa,
            transaksi.kd_unit,
            transaksi.tanggal_mulai,
            transaksi.tanggal_selesai,
            transaksi.tanggal_transaksi,
            transaksi.total_harga,
            transaksi.status_transaksi
        )
        self.db.execute(query, params)
        self.db.commit()

    def update_transaksi(self, transaksi: Transaksi):
        query = """
            UPDATE transaksi
            SET kd_transaksi_bulanan = %s, kd_penyewa = %s, kd_unit = %s,
                tanggal_mulai = %s, tanggal_selesai = %s, tanggal_transaksi = %s,
                total_harga = %s, status_transaksi = %s
            WHERE kd_transaksi = %s
        """
        params = (
            transaksi.kd_transaksi_bulanan,
            transaksi.kd_penyewa,
            transaksi.kd_unit,
            transaksi.tanggal_mulai,
            transaksi.tanggal_selesai,
            transaksi.tanggal_transaksi,
            transaksi.total_harga,
            transaksi.status_transaksi,
            transaksi.kd_transaksi
        )
        self.db.execute(query, params)
        self.db.commit()

    def hapus_transaksi(self, kd_transaksi):
        query = "DELETE FROM transaksi WHERE kd_transaksi = %s"
        self.db.execute(query, (kd_transaksi,))
        self.db.commit()

    def cari_transaksi(self, keyword):
        query = """
            SELECT * FROM transaksi
            WHERE kd_transaksi LIKE %s OR kd_penyewa LIKE %s OR kd_unit LIKE %s OR tanggal_mulai LIKE %s
            OR tanggal_transaksi LIKE %s OR status_transaksi LIKE %s
        """
        like = f"%{keyword}%"
        params = (like, like, like, like, like, like)
        self.db.execute(query, params)
        result = self.db.fetchall()

        transaksi_list = []
        for row in result:
            transaksi = Transaksi(
                kd_transaksi=row["kd_transaksi"],
                kd_transaksi_bulanan=row.get("kd_transaksi_bulanan"),
                kd_penyewa=row["kd_penyewa"],
                kd_unit=row["kd_unit"],
                tanggal_mulai=row["tanggal_mulai"],
                tanggal_selesai=row["tanggal_selesai"],
                tanggal_transaksi=row["tanggal_transaksi"],
                total_harga=row.get("total_harga"),
                status_transaksi=row["status_transaksi"]
            )
            transaksi_list.append(transaksi)
        return transaksi_list

    def generate_kode_transaksi(self):
        query = "SELECT kd_transaksi FROM transaksi WHERE kd_transaksi LIKE 'TRX-VH-%' ORDER BY kd_transaksi DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_kode = result['kd_transaksi']
            last_number = int(last_kode.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_kode = f"TRX-VH-{new_number:03d}"
        return new_kode

    def fetch_transaksi_by_bulanan(self, kd_transaksi_bulanan):
        query = """
            SELECT tr.kd_transaksi, tr.kd_transaksi_bulanan, p.nama AS kd_penyewa, uk.kd_unit,
                   tr.tanggal_mulai, tr.tanggal_selesai, tr.tanggal_transaksi,
                   tr.total_harga, tr.status_transaksi
            FROM transaksi tr
            JOIN penyewa p ON tr.kd_penyewa = p.kd_penyewa
            JOIN unit_kamar uk ON tr.kd_unit = uk.kd_unit
            WHERE tr.kd_transaksi_bulanan = %s
        """
        self.db.execute(query, (kd_transaksi_bulanan,))
        result = self.db.fetchall()

        transaksi_list = []
        for row in result:
            transaksi = Transaksi(
                kd_transaksi=row["kd_transaksi"],
                kd_transaksi_bulanan=row["kd_transaksi_bulanan"],
                kd_penyewa=row["kd_penyewa"],
                kd_unit=row["kd_unit"],
                tanggal_mulai=row["tanggal_mulai"],
                tanggal_selesai=row["tanggal_selesai"],
                tanggal_transaksi=row["tanggal_transaksi"],
                total_harga=row["total_harga"],
                status_transaksi=row["status_transaksi"]
            )
            transaksi_list.append(transaksi)
        return transaksi_list

    def get_bulan_tahun_by_kd(self, kd_transaksi_bulanan):
        query = "SELECT nama_bulan, tahun FROM transaksi_bulanan WHERE kd_transaksi_bulanan = %s"
        self.db.execute(query, (kd_transaksi_bulanan,))
        result = self.db.fetchone()
        if result:
            return result["nama_bulan"], result["tahun"]
        return "Tidak Diketahui", ""

    def close_connection(self):
        self.db.close()