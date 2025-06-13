from app_desktop.database.connection import Database
from app_desktop.models.transaksi import Transaksi
from datetime import datetime

class TransaksiController:
    def __init__(self):
        self.db = Database()

    def fetch_kode_unit(self):
        query = """
            SELECT kd_unit FROM unit_kamar
        """
        self.db.execute(query)
        result = self.db.fetchall()
        kode_units = [row["kd_unit"] for row in result]
        return kode_units

    def fetch_kode_unit_kosong(self):
        query = """
            SELECT kd_unit FROM unit_kamar
            WHERE status = 'kosong'
        """
        self.db.execute(query)
        result = self.db.fetchall()
        return [row["kd_unit"] for row in result]

    def fetch_kode_penyewa(self):
        query = "SELECT kd_penyewa, nama FROM penyewa"
        self.db.execute(query)
        results = self.db.fetchall()
        return [{"kd_penyewa": r["kd_penyewa"], "nama": r["nama"]} for r in results]

    def get_harga_by_kode_unit(self, kd_unit):
        query = """
            SELECT k.harga 
            FROM kamar k
            JOIN unit_kamar uk ON uk.kd_kamar = k.kd_kamar
            WHERE uk.kd_unit = %s
        """
        self.db.execute(query, (kd_unit,))
        result = self.db.fetchone()
        return result['harga'] if result else 0

    def fetch_kd_unit_kosong(self, kd_penyewa):
        semua_kd_unit = self.fetch_kode_unit()
        kd_unit_aktif = self.fetch_kd_unit_terisi(kd_penyewa)

        kd_unit_kosong = [uk for uk in semua_kd_unit if uk["kd_unit"] not in kd_unit_aktif]
        return kd_unit_kosong

    def fetch_kd_unit_terisi(self, kd_penyewa):
        query = "SELECT kd_unit FROM transaksi"
        params = []
        if kd_penyewa:
            query += " WHERE kd_penyewa = %s"
            params.append(kd_penyewa)

        self.db.execute(query, params)
        return [row["kd_unit"] for row in self.db.fetchall()]

    def fetch_penyewa_belum_transaksi(self, kd_transaksi_bulanan):
        semua_penyewa = self.fetch_kode_penyewa()
        penyewa_aktif = self.fetch_penyewa_yang_sudah_transaksi(kd_transaksi_bulanan)

        penyewa_belum = [p for p in semua_penyewa if p["kd_penyewa"] not in penyewa_aktif]
        return penyewa_belum

    def fetch_penyewa_yang_sudah_transaksi(self, kd_transaksi_bulanan):
        query = "SELECT kd_penyewa FROM transaksi"
        params = []
        if kd_transaksi_bulanan:
            query += " WHERE kd_transaksi_bulanan = %s"
            params.append(kd_transaksi_bulanan)

        self.db.execute(query, params)
        return [row["kd_penyewa"] for row in self.db.fetchall()]

    def get_kd_penyewa_by_name(self, nama_penyewa):
        query = "SELECT kd_penyewa FROM penyewa WHERE nama = %s"
        self.db.execute(query, (nama_penyewa,))
        result = self.db.fetchone()
        return result['kd_penyewa'] if result else None

    def get_unit_dan_harga_by_penyewa(self, kd_penyewa):
        query = """
            SELECT uk.kd_unit, k.harga
            FROM penyewa p
            JOIN unit_kamar uk ON p.kd_unit = uk.kd_unit
            JOIN kamar k ON uk.kd_kamar = k.kd_kamar
            WHERE p.kd_penyewa = %s AND uk.status = 'terisi'
        """
        self.db.execute(query, (kd_penyewa,))
        result = self.db.fetchone()
        if result:
            return result["kd_unit"], result["harga"]
        return None, None

    def get_unit_info_by_kd_penyewa(self, kd_penyewa):
        query = """
            SELECT u.kd_unit, u.status 
            FROM penyewa p
            JOIN unit u ON p.kd_unit = u.kd_unit
            WHERE p.kd_penyewa = ?
        """
        self.db.execute(query, (kd_penyewa,))
        result = self.db.fetchone()

        if result:
            kd_unit, status = result
            return {"kd_unit": kd_unit, "status": status}
        return None

    def fetch_transaksi(self):
        query = """
            SELECT tr.kd_transaksi, tr.kd_transaksi_bulanan, p.nama AS kd_penyewa, uk.kd_unit,
            tr.tanggal_transaksi, tr.status_transaksi
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
                total_harga, status_transaksi, diskon, biaya_tambahan, jumlah_bayar, uang_penyewa,
                kembalian
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            transaksi.status_transaksi,
            transaksi.diskon,
            transaksi.biaya_tambahan,
            transaksi.jumlah_bayar,
            transaksi.uang_penyewa,
            transaksi.kembalian
        )
        self.db.execute(query, params)
        self.db.commit()

        query_update_status = """
            UPDATE unit_kamar SET status = 'terisi' WHERE kd_unit = %s
        """
        self.db.execute(query_update_status, (transaksi.kd_unit,))
        self.db.commit()

        query_update_penyewa_unit = """
            UPDATE penyewa SET kd_unit = %s WHERE kd_penyewa = %s
        """
        self.db.execute(query_update_penyewa_unit, (transaksi.kd_unit, transaksi.kd_penyewa))
        self.db.commit()

    def update_transaksi(self, transaksi: Transaksi):
        query = """
            UPDATE transaksi
            SET kd_transaksi_bulanan = %s, kd_penyewa = %s, kd_unit = %s,
                tanggal_mulai = %s, tanggal_selesai = %s, tanggal_transaksi = %s,
                total_harga = %s, status_transaksi = %s, diskon = %s, biaya_tambahan = %s,
                jumlah_bayar = %s, uang_penyewa = %s, kembalian = %s
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
            transaksi.diskon,
            transaksi.biaya_tambahan,
            transaksi.jumlah_bayar,
            transaksi.uang_penyewa,
            transaksi.kembalian,
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

    def generate_kode_transaksi(self, kd_transaksi_bulanan):
        nama_bulan, tahun = self.get_bulan_tahun_by_kd(kd_transaksi_bulanan)
        bulan_str = nama_bulan[:3].upper()
        tahun_str = str(tahun)[-2:]
        prefix = f"TRX-{bulan_str}{tahun_str}-"

        query = f"""
            SELECT kd_transaksi FROM transaksi
            WHERE kd_transaksi LIKE %s
            ORDER BY kd_transaksi DESC LIMIT 1
        """
        self.db.execute(query, (prefix + "%",))
        result = self.db.fetchone()

        if result:
            last_kode = result["kd_transaksi"]
            last_number = int(last_kode.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        new_kode = f"{prefix}{new_number:03d}"
        return new_kode

    def fetch_transaksi_bulanan(self, kd_transaksi_bulanan):
        query = """
            SELECT tr.kd_transaksi, tr.kd_transaksi_bulanan, p.nama AS kd_penyewa, uk.kd_unit,
               tr.tanggal_mulai, tr.tanggal_selesai, tr.tanggal_transaksi,
               tr.total_harga, tr.status_transaksi,
               tr.diskon, tr.biaya_tambahan, tr.jumlah_bayar,
               tr.uang_penyewa, tr.kembalian
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
                status_transaksi=row["status_transaksi"],
                diskon=row["diskon"],
                biaya_tambahan=row["biaya_tambahan"],
                jumlah_bayar=row["jumlah_bayar"],
                uang_penyewa=row["uang_penyewa"],
                kembalian=row["kembalian"]
            )
            transaksi_list.append(transaksi)
        return transaksi_list

    def get_all_transaksi_bulanan_summary(self):
        query = """
            SELECT tb.kd_transaksi_bulanan, tb.nama_bulan, tb.tahun, COUNT(tr.kd_transaksi) as jumlah
            FROM transaksi_bulanan tb
            LEFT JOIN transaksi tr ON tb.kd_transaksi_bulanan = tr.kd_transaksi_bulanan
            GROUP BY tb.kd_transaksi_bulanan, tb.nama_bulan, tb.tahun
            ORDER BY tb.tahun DESC, tb.nama_bulan DESC
        """
        self.db.execute(query)
        result = self.db.fetchall()

        return result

    def get_bulan_tahun_by_kd(self, kd_transaksi_bulanan):
        query = "SELECT nama_bulan, tahun FROM transaksi_bulanan WHERE kd_transaksi_bulanan = %s"
        self.db.execute(query, (kd_transaksi_bulanan,))
        result = self.db.fetchone()
        if result:
            return result["nama_bulan"], result["tahun"]
        return "Tidak Diketahui", ""

    def close_connection(self):
        self.db.close()