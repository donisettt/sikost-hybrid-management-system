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

    def export_excel(data, headers, filename="laporan.xlsx"):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)

        for row in data:
            ws.append(list(row))

        for cell in ws["1:1"]:
            cell.font = Font(bold=True)

        wb.save(filename)

    def export_pdf(data, headers, filename="laporan.pdf"):
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        x_offset = 30
        y_offset = height - 40
        line_height = 20

        c.setFont("Helvetica-Bold", 12)
        for i, header in enumerate(headers):
            c.drawString(x_offset + i * 80, y_offset, str(header))

        c.setFont("Helvetica", 10)
        for row in data:
            y_offset -= line_height
            for i, item in enumerate(row):
                c.drawString(x_offset + i * 80, y_offset, str(item))

        c.save()

    def get_laporan_bulanan(self, bulan: str, tahun: str, kategori: str = "Semua"):
        cursor = self.conn.cursor
        query = """
            SELECT t.kd_transaksi, t.kd_penyewa, t.kd_unit, t.tanggal_transaksi, t.total_harga,
                   t.diskon, t.biaya_tambahan, t.jumlah_bayar, t.uang_penyewa, t.kembalian, t.status_transaksi
            FROM transaksi t
            JOIN transaksi_bulanan tb ON t.kd_transaksi_bulanan = tb.kd_transaksi_bulanan
            WHERE tb.nama_bulan = %s AND tb.tahun = %s
        """
        params = [bulan, tahun]

        if kategori != "Semua":
            query += " AND t.status_transaksi = %s"
            params.append(kategori)

        cursor.execute(query, params)
        return cursor.fetchall()

    def get_laporan_tahunan(self, tahun: str, kategori: str = "Semua"):
        cursor = self.conn.cursor
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
        cursor = self.conn.cursor
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
