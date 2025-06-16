from app_desktop.models.detail_transaksi import DetailTransaksi
from app_desktop.database.connection import Database
import time, random

class DetailTransaksiController:
    def __init__(self):
        self.conn = Database()

    def generate_kd_detail(self):
        return f"DT{int(time.time())}{random.randint(100,999)}"

    def tambah_detail_dari_transaksi(self, transaksi_obj):
        """
        transaksi_obj: instance dari class transaksi (atau dict) yg berisi data transaksi,
        lalu convert dan insert ke detail_transaksi.
        """
        kd_detail = self.generate_kd_detail()
        detail = DetailTransaksi(
            kd_detail_transaksi=kd_detail,
            kd_transaksi=transaksi_obj.kd_transaksi,
            nama_penyewa=transaksi_obj.nama_penyewa,
            nama_unit=transaksi_obj.nama_unit,
            tanggal_transaksi=transaksi_obj.tanggal_transaksi,
            tanggal_mulai=transaksi_obj.tanggal_mulai,
            tanggal_selesai=transaksi_obj.tanggal_selesai,
            total_harga=transaksi_obj.total_harga,
            diskon=transaksi_obj.diskon,
            biaya_tambahan=transaksi_obj.biaya_tambahan,
            jumlah_bayar=transaksi_obj.jumlah_bayar,
            uang_penyewa=transaksi_obj.uang_penyewa,
            kembalian=transaksi_obj.kembalian,
            status_transaksi=transaksi_obj.status_transaksi
        )
        self.insert_detail(detail)

    def insert_detail(self, detail: DetailTransaksi):
        sql = """
        INSERT INTO detail_transaksi (
            kd_detail_transaksi, kd_transaksi, nama_penyewa, nama_unit,
            tanggal_transaksi, tanggal_mulai, tanggal_selesai, total_harga,
            diskon, biaya_tambahan, jumlah_bayar, uang_penyewa, kembalian, status_transaksi
        ) VALUES (
            %(kd_detail_transaksi)s, %(kd_transaksi)s, %(nama_penyewa)s, %(nama_unit)s,
            %(tanggal_transaksi)s, %(tanggal_mulai)s, %(tanggal_selesai)s, %(total_harga)s,
            %(diskon)s, %(biaya_tambahan)s, %(jumlah_bayar)s, %(uang_penyewa)s, %(kembalian)s, %(status_transaksi)s
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, detail.to_dict())
        self.conn.commit()
        cursor.close()

    def edit_detail(self, kd_detail_transaksi, update_data: dict):
        """
        update_data contoh: {"nama_penyewa": "Doni", "diskon": 5000, ...}
        """
        set_clause = ", ".join([f"{k} = %({k})s" for k in update_data.keys()])
        sql = f"UPDATE detail_transaksi SET {set_clause} WHERE kd_detail_transaksi = %(kd)s"
        params = update_data.copy()
        params['kd'] = kd_detail_transaksi

        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        cursor.close()

    def hapus_detail(self, kd_detail_transaksi):
        sql = "DELETE FROM detail_transaksi WHERE kd_detail_transaksi = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql, (kd_detail_transaksi,))
        self.conn.commit()
        cursor.close()

    def get_detail_by_kd(self, kd_detail_transaksi):
        sql = "SELECT * FROM detail_transaksi WHERE kd_detail_transaksi = %s"
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, (kd_detail_transaksi,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return DetailTransaksi(**row)
        return None

    def cetak_struk(self, kd_detail_transaksi):
        detail = self.get_detail_by_kd(kd_detail_transaksi)
        if not detail:
            raise ValueError("Data detail transaksi tidak ditemukan")

        struk = (
            f"--- STRUK TRANSAKSI ---\n"
            f"Kode Detail: {detail.kd_detail}\n"
            f"Penyewa: {detail.nama_penyewa}\n"
            f"Unit: {detail.nama_unit}\n"
            f"Tanggal Transaksi: {detail.tgl_transaksi}\n"
            f"Total Harga: Rp{detail.total_harga}\n"
            f"Diskon: Rp{detail.diskon}\n"
            f"Biaya Tambahan: Rp{detail.biaya_tambahan}\n"
            f"Jumlah Bayar: Rp{detail.jumlah_bayar}\n"
            f"Uang Penyewa: Rp{detail.uang_penyewa}\n"
            f"Kembalian: Rp{detail.kembalian}\n"
            f"Status: {detail.status_transaksi}\n"
            f"-----------------------"
        )
        print(struk)