from database.connection import Database
from models.transaksi import Transaksi
from datetime import datetime
import requests

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

    def ambil_no_hp_penyewa(self, kd_penyewa):
        query = "SELECT no_hp FROM penyewa WHERE kd_penyewa = %s"
        self.db.execute(query, (kd_penyewa,))
        hasil = self.db.fetchone()
        return hasil["no_hp"] if hasil else None

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

    def get_detail_transaksi(self, kd_transaksi):
        query = "SELECT * FROM transaksi WHERE kd_transaksi = %s"
        self.db.execute(query, (kd_transaksi,))
        result = self.db.fetchone()

        print("Result Type:", type(result))  # Debug: Tipe data hasil query
        print("Result Data:", result)  # Debug: Isi hasil query

        return result if result else {}

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
            SELECT
                tr.kd_transaksi,
                tr.kd_transaksi_bulanan,
                tr.kd_penyewa,
                p.nama AS nama_penyewa,
                tr.kd_unit,
                tr.tanggal_mulai,
                tr.tanggal_selesai,
                tr.tanggal_transaksi,
                tr.total_harga,
                tr.diskon,
                tr.biaya_tambahan,
                tr.jumlah_bayar,
                tr.uang_penyewa,
                tr.kembalian,
                tr.status_transaksi
            FROM transaksi tr
            JOIN penyewa p ON tr.kd_penyewa = p.kd_penyewa
            JOIN unit_kamar uk ON tr.kd_unit = uk.kd_unit
            ORDER BY tr.tanggal_transaksi DESC
        """
        self.db.execute(query)
        result = self.db.fetchall()

        transaksi_list = []
        for row in result:
            transaksi = Transaksi(
                kd_transaksi=row["kd_transaksi"],
                kd_transaksi_bulanan=row["kd_transaksi_bulanan"],
                kd_penyewa=row["kd_penyewa"],
                nama_penyewa=row["nama_penyewa"],  # kalau kamu butuh nama langsung
                kd_unit=row["kd_unit"],
                tanggal_mulai=row["tanggal_mulai"],
                tanggal_selesai=row["tanggal_selesai"],
                tanggal_transaksi=row["tanggal_transaksi"],
                total_harga=row["total_harga"],
                diskon=row["diskon"],
                biaya_tambahan=row["biaya_tambahan"],
                jumlah_bayar=row["jumlah_bayar"],
                uang_penyewa=row["uang_penyewa"],
                kembalian=row["kembalian"],
                status_transaksi=row["status_transaksi"]
            )
            transaksi_list.append(transaksi)

        return transaksi_list

    def ambil_no_hp_penyewa(self, kd_penyewa):
        query = "SELECT no_hp FROM penyewa WHERE kd_penyewa = %s"
        self.db.execute(query, (kd_penyewa,))
        hasil = self.db.fetchone()
        return hasil["no_hp"] if hasil else None

    def ambil_nama_penyewa(self, kd_penyewa):
        query = "SELECT nama FROM penyewa WHERE kd_penyewa = %s"
        self.db.execute(query, (kd_penyewa,))
        hasil = self.db.fetchone()
        return hasil["nama"] if hasil else None

    def kirim_wa_wablas(self, no_hp: str, pesan: str):
        token = "FxOEioHDnpQ3liM6zjIRcNlSGSVh1dF80jCY738OrubljoZovkRProM"
        url = "https://sby.wablas.com/api/send-message"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        payload = {
            "phone": no_hp,
            "message": pesan,
            "secret": False,
            "priority": True

        }

        print("📤 Payload yang dikirim:", payload)
        print("🔐 Headers:", headers)
        print("🌐 URL:", url)

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("✅ Notifikasi WA berhasil dikirim.")
            else:
                print("⚠️ Gagal kirim WA:", response.text)
        except Exception as e:
            print("❌ Error WA:", str(e))

    def format_tanggal_indonesia(self, tanggal: datetime.date):
        bulan_indo = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        return f"{tanggal.day} {bulan_indo[tanggal.month]} {tanggal.year}"

    def tambah_transaksi(self, transaksi: Transaksi):
        try:
            if transaksi.tanggal_mulai == transaksi.tanggal_selesai:
                from tkinter import messagebox
                messagebox.showwarning("Validasi Tanggal", "Tanggal mulai dan tanggal selesai tidak boleh sama.")
                return

            query_transaksi = """
                INSERT INTO transaksi (
                    kd_transaksi, kd_transaksi_bulanan, kd_penyewa, kd_unit,
                    tanggal_mulai, tanggal_selesai, tanggal_transaksi,
                    total_harga, status_transaksi, diskon, biaya_tambahan,
                    jumlah_bayar, uang_penyewa, kembalian
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params_transaksi = (
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
            self.db.execute(query_transaksi, params_transaksi)
            self.db.commit()

            # 🔁 Cek apakah penyewa sudah pernah punya unit sebelumnya
            self.db.execute("SELECT kd_unit FROM penyewa WHERE kd_penyewa = %s", (transaksi.kd_penyewa,))
            result = self.db.fetchone()
            unit_lama = result['kd_unit'] if result and result['kd_unit'] else None

            # Jika unit lama tidak sama dengan unit baru → set status unit lama jadi 'kosong'
            if unit_lama and unit_lama != transaksi.kd_unit:
                self.db.execute("UPDATE unit_kamar SET status = 'kosong' WHERE kd_unit = %s", (unit_lama,))
                self.db.commit()

            # Update unit baru jadi 'terisi'
            self.db.execute("UPDATE unit_kamar SET status = 'terisi' WHERE kd_unit = %s", (transaksi.kd_unit,))
            self.db.commit()

            # Update kolom kd_unit di penyewa
            self.db.execute("UPDATE penyewa SET kd_unit = %s WHERE kd_penyewa = %s",
                            (transaksi.kd_unit, transaksi.kd_penyewa))
            self.db.commit()

            # Simpan ke tabel detail_transaksi
            kd_detail_transaksi = self.generate_kd_detail_transaksi()
            query_detail = """
                INSERT INTO detail_transaksi (
                    kd_detail_transaksi, kd_transaksi, kd_penyewa, kd_unit, kd_transaksi_bulanan,
                    tanggal_transaksi, tanggal_mulai, tanggal_selesai,
                    total_harga, diskon, biaya_tambahan, jumlah_bayar,
                    uang_penyewa, kembalian, status_transaksi
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params_detail = (
                kd_detail_transaksi,
                transaksi.kd_transaksi,
                transaksi.kd_penyewa,
                transaksi.kd_unit,
                transaksi.kd_transaksi_bulanan,
                transaksi.tanggal_transaksi,
                transaksi.tanggal_mulai,
                transaksi.tanggal_selesai,
                transaksi.total_harga,
                transaksi.diskon,
                transaksi.biaya_tambahan,
                transaksi.jumlah_bayar,
                transaksi.uang_penyewa,
                transaksi.kembalian,
                transaksi.status_transaksi
            )
            self.db.execute(query_detail, params_detail)
            self.db.commit()

            tanggal_mulai_dt = datetime.strptime(transaksi.tanggal_mulai, "%Y-%m-%d").date()
            tanggal_selesai_dt = datetime.strptime(transaksi.tanggal_selesai, "%Y-%m-%d").date()
            tgl_mulai_str = self.format_tanggal_indonesia(tanggal_mulai_dt)
            tgl_selesai_str = self.format_tanggal_indonesia(tanggal_selesai_dt)

            no_hp = self.ambil_no_hp_penyewa(transaksi.kd_penyewa)
            nama = self.ambil_nama_penyewa(transaksi.kd_penyewa)

            pesan = (
                f"Hai, {nama}, terima kasih sudah memilih VibeHouse.\n"
                f"Berikut detail transaksi anda.\n\n"
                f"Kode Transaksi : {transaksi.kd_transaksi}\n"
                f"Kode Unit : {transaksi.kd_unit}\n"
                f"Periode : {tgl_mulai_str} s.d {tgl_selesai_str}\n"
                f"Diskon : Rp {transaksi.diskon}\n"
                f"Biaya Tambahan : Rp {transaksi.biaya_tambahan}\n"
                f"Total Bayar : Rp {transaksi.jumlah_bayar:,}\n"
                f"Status : {transaksi.status_transaksi.capitalize()}\n\n"
                f"Semoga betah di VibeHouse! ✨\n"
                f"- Management VibeHouse"
            )

            self.kirim_wa_wablas(no_hp, pesan)
            print("Transaksi dan detail berhasil ditambahkan.")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Gagal menambahkan transaksi:", str(e))

    def update_transaksi(self, transaksi: Transaksi):
        try:
            from tkinter import messagebox
            from datetime import datetime

            if transaksi.tanggal_mulai == transaksi.tanggal_selesai:
                messagebox.showwarning("Validasi Tanggal", "Tanggal mulai dan tanggal selesai tidak boleh sama.")
                return

            # Ambil unit lama
            self.db.execute("SELECT kd_unit FROM transaksi WHERE kd_transaksi = %s", (transaksi.kd_transaksi.strip(),))
            result = self.db.fetchone()
            unit_lama = result['kd_unit'] if result else None

            # === DEBUG: Tampilkan data update ===
            print("=== PARAMS UPDATE TRANSAKSI ===")
            params_update = (
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
                transaksi.kd_transaksi.strip()
            )
            for i, val in enumerate(params_update):
                print(f"{i + 1}: {val}")

            # Update tabel transaksi
            query_update = """
                UPDATE transaksi SET
                    kd_transaksi_bulanan = %s,
                    kd_penyewa = %s,
                    kd_unit = %s,
                    tanggal_mulai = %s,
                    tanggal_selesai = %s,
                    tanggal_transaksi = %s,
                    total_harga = %s,
                    status_transaksi = %s,
                    diskon = %s,
                    biaya_tambahan = %s,
                    jumlah_bayar = %s,
                    uang_penyewa = %s,
                    kembalian = %s
                WHERE kd_transaksi = %s
            """
            self.db.execute(query_update, params_update)
            print("Rows affected (transaksi):", self.db.cursor.rowcount)
            self.db.commit()

            # Update status unit jika unit berubah
            if unit_lama and unit_lama != transaksi.kd_unit:
                self.db.execute("UPDATE unit_kamar SET status = 'kosong' WHERE kd_unit = %s", (unit_lama,))
                self.db.commit()

            self.db.execute("UPDATE unit_kamar SET status = 'terisi' WHERE kd_unit = %s", (transaksi.kd_unit,))
            self.db.commit()

            self.db.execute("UPDATE penyewa SET kd_unit = %s WHERE kd_penyewa = %s",
                            (transaksi.kd_unit, transaksi.kd_penyewa))
            self.db.commit()

            # Update detail_transaksi
            query_update_detail = """
                UPDATE detail_transaksi SET
                    kd_penyewa = %s,
                    kd_unit = %s,
                    kd_transaksi_bulanan = %s,
                    tanggal_transaksi = %s,
                    tanggal_mulai = %s,
                    tanggal_selesai = %s,
                    total_harga = %s,
                    diskon = %s,
                    biaya_tambahan = %s,
                    jumlah_bayar = %s,
                    uang_penyewa = %s,
                    kembalian = %s,
                    status_transaksi = %s
                WHERE kd_transaksi = %s
            """
            params_detail_update = (
                transaksi.kd_penyewa,
                transaksi.kd_unit,
                transaksi.kd_transaksi_bulanan,
                transaksi.tanggal_transaksi,
                transaksi.tanggal_mulai,
                transaksi.tanggal_selesai,
                transaksi.total_harga,
                transaksi.diskon,
                transaksi.biaya_tambahan,
                transaksi.jumlah_bayar,
                transaksi.uang_penyewa,
                transaksi.kembalian,
                transaksi.status_transaksi,
                transaksi.kd_transaksi.strip()
            )
            self.db.execute(query_update_detail, params_detail_update)
            print("Rows affected (detail_transaksi):", self.db.cursor.rowcount)
            self.db.commit()

            # Kirim WA
            tanggal_mulai_dt = datetime.strptime(transaksi.tanggal_mulai, "%Y-%m-%d").date()
            tanggal_selesai_dt = datetime.strptime(transaksi.tanggal_selesai, "%Y-%m-%d").date()
            tgl_mulai_str = self.format_tanggal_indonesia(tanggal_mulai_dt)
            tgl_selesai_str = self.format_tanggal_indonesia(tanggal_selesai_dt)

            no_hp = self.ambil_no_hp_penyewa(transaksi.kd_penyewa)
            nama = self.ambil_nama_penyewa(transaksi.kd_penyewa)

            pesan = (
                f"Hai, {nama}, data transaksi Anda telah diperbarui.\n"
                f"Berikut update detailnya:\n\n"
                f"Kode Transaksi : {transaksi.kd_transaksi}\n"
                f"Kode Unit : {transaksi.kd_unit}\n"
                f"Periode : {tgl_mulai_str} s.d {tgl_selesai_str}\n"
                f"Diskon : Rp {transaksi.diskon}\n"
                f"Biaya Tambahan : Rp {transaksi.biaya_tambahan}\n"
                f"Total Bayar : Rp {transaksi.jumlah_bayar:,}\n"
                f"Status : {transaksi.status_transaksi.capitalize()}\n\n"
                f"Terima kasih atas kepercayaannya 🙏\n"
                f"- Management VibeHouse"
            )
            self.kirim_wa_wablas(no_hp, pesan)

            print("✅ Transaksi berhasil diperbarui.")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("❌ Gagal memperbarui transaksi:", str(e))

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
        prefix = f"TVH-{bulan_str}{tahun_str}-"

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

    def generate_kd_detail_transaksi(self):
        query = "SELECT kd_detail_transaksi FROM detail_transaksi ORDER BY kd_detail_transaksi DESC LIMIT 1"
        self.db.execute(query)
        result = self.db.fetchone()

        if result:
            last_code = result['kd_detail_transaksi'].split('-')[-1]
            new_number = int(last_code) + 1
        else:
            new_number = 1

        return f"DTVH-{new_number:03d}"

    def close_connection(self):
        self.db.close()