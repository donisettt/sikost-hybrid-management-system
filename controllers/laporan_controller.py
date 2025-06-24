import openpyxl
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from database.connection import Database

class LaporanController:
    def __init__(self):
        self.conn = Database()

    def export_excel(self, data, headers, filename):
        import pandas as pd
        from openpyxl import load_workbook
        from openpyxl.utils import get_column_letter

        # Deteksi apakah data list of dict atau list of tuple
        if isinstance(data[0], dict):
            df = pd.DataFrame(data)
        elif isinstance(data[0], (list, tuple)):
            df = pd.DataFrame(data, columns=headers)
        else:
            raise ValueError("Format data tidak dikenali.")

        # Ubah kolom tanggal jadi string agar tidak jadi #####
        for col in df.columns:
            if "tanggal" in col.lower():
                df[col] = df[col].astype(str)

        df.to_excel(filename, index=False)

        # Auto-fit kolom
        wb = load_workbook(filename)
        ws = wb.active
        for col in ws.columns:
            max_length = 0
            column = col[0].column  # nomor kolom
            column_letter = get_column_letter(column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column_letter].width = max_length + 2
        wb.save(filename)

    def get_laporan_pengeluaran(self, bulan: str, tahun: str, kategori: str = "Semua"):
        cursor = self.conn
        query = """
            SELECT kd_pengeluaran, tanggal, kategori, deskripsi, jumlah, dibuat_oleh
            FROM pengeluaran
            WHERE MONTH(STR_TO_DATE(tanggal, '%%Y-%%m-%%d')) = %s AND YEAR(tanggal) = %s
        """
        params = [self._bulan_ke_angka(bulan), tahun]

        if kategori != "Semua":
            query += " AND kategori = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_laporan_bulanan(self, bulan: str, tahun: str, kategori: str = "Semua"):
        bulan_angka = self._bulan_ke_angka(bulan)

        if kategori == "Pengeluaran":
            return self.get_laporan_pengeluaran(bulan, tahun)

        elif kategori == "Pemasukan" or kategori == "Semua":
            cursor = self.conn
            query = """
                SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                       t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
                FROM transaksi t
                JOIN transaksi_bulanan tb ON t.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
                WHERE tb.nama_bulan = %s AND tb.tahun = %s
            """
            params = [bulan, tahun]

            cursor.execute(query, params)
            return cursor.fetchall()
        else:
            return []

    def _bulan_ke_angka(self, nama_bulan):
        daftar_bulan = {
            "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
            "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
            "September": 9, "Oktober": 10, "November": 11, "Desember": 12
        }
        return daftar_bulan.get(nama_bulan, 0)

    def get_laporan_tahunan(self, tahun: str, kategori: str = "Semua"):
        cursor = self.conn
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            JOIN transaksi_bulanan tb ON t.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
            WHERE tb.tahun = %s
        """
        params = [tahun]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_laporan_periode(self, dari_tanggal: str, sampai_tanggal: str, kategori: str = "Semua"):
        cursor = self.conn
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            WHERE t.tanggal_transaksi BETWEEN %s AND %s
        """
        params = [dari_tanggal, sampai_tanggal]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()
