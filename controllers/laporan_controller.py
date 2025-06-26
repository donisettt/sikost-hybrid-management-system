import openpyxl
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import requests
from database.connection import Database

class LaporanController:
    def __init__(self):
        self.conn = Database()

    def export_excel_pemasukan(self, data, headers, filename):
        import pandas as pd
        from openpyxl import load_workbook
        from openpyxl.utils import get_column_letter
        from openpyxl.styles import Alignment, Font, PatternFill

        if isinstance(data[0], dict):
            df = pd.DataFrame(data)
        elif isinstance(data[0], (list, tuple)):
            df = pd.DataFrame(data, columns=headers)
        else:
            raise ValueError("Format data tidak dikenali.")

        for col in df.columns:
            if "tanggal" in col.lower():
                df[col] = df[col].astype(str)

        df.to_excel(filename, index=False, startrow=5)

        wb = load_workbook(filename)
        ws = wb.active

        max_col = len(df.columns)
        last_col_letter = get_column_letter(max_col)

        ws.merge_cells(f"A1:{last_col_letter}1")
        ws["A1"] = "KOST VIBE HOUSE"
        ws["A1"].font = Font(size=14, bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

        ws.merge_cells(f"A2:{last_col_letter}2")
        ws["A2"] = "Jl. Raya Buah Batu, Kota Bandung"
        ws["A2"].alignment = Alignment(horizontal="center")

        ws.merge_cells(f"A3:{last_col_letter}3")
        ws["A3"] = "0823-2030-8986"
        ws["A3"].alignment = Alignment(horizontal="center")

        header_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
        for cell in ws[6]:
            cell.fill = header_fill
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max_length + 2

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

    def get_nomor_admin(self):
        cursor = self.conn
        query = "SELECT no_hp FROM users WHERE role = 'admin' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result['no_hp'] if result else None

    def kirim_wa_admin(self, message: str):
        cursor = self.conn
        cursor.execute("SELECT no_hp FROM users WHERE role = 'admin'")
        admin = cursor.fetchone()
        if admin and admin['no_hp']:
            no_hp = admin['no_hp']
            token = "FxOEioHDnpQ3liM6zjIRcNlSGSVh1dF80jCY738OrubljoZovkRProM"
            url = "https://sby.wablas.com/api/send-message"

            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            payload = {
                "phone": no_hp,
                "message": message
            }
            response = requests.post(url, headers=headers, json=payload)
            print("WA Admin Status:", response.status_code, response.text)