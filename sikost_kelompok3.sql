-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 01 Jul 2025 pada 19.39
-- Versi server: 8.4.3
-- Versi PHP: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sikost_kelompok3`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_transaksi`
--

CREATE TABLE `detail_transaksi` (
  `kd_detail_transaksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `kd_transaksi` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kd_penyewa` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kd_unit` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kd_transaksi_bulanan` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tanggal_transaksi` date DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `total_harga` int DEFAULT NULL,
  `diskon` int DEFAULT NULL,
  `biaya_tambahan` int DEFAULT NULL,
  `jumlah_bayar` int DEFAULT NULL,
  `uang_penyewa` int DEFAULT NULL,
  `kembalian` int DEFAULT NULL,
  `status_transaksi` enum('lunas','belum_lunas') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `detail_transaksi`
--

INSERT INTO `detail_transaksi` (`kd_detail_transaksi`, `kd_transaksi`, `kd_penyewa`, `kd_unit`, `kd_transaksi_bulanan`, `tanggal_transaksi`, `tanggal_mulai`, `tanggal_selesai`, `total_harga`, `diskon`, `biaya_tambahan`, `jumlah_bayar`, `uang_penyewa`, `kembalian`, `status_transaksi`) VALUES
('DTVH-001', 'TVH-JAN25-001', 'VH-001', 'ANGGREK-001', 'TB001', '2025-01-27', '2025-01-27', '2025-02-27', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-002', 'TVH-JAN25-002', 'VH-002', 'MELATI-001', 'TB001', '2025-01-27', '2025-01-27', '2025-02-27', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-003', 'TVH-JAN25-003', 'VH-003', 'MELATI-005', 'TB001', '2025-01-17', '2025-01-27', '2025-02-27', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-004', 'TVH-JAN25-004', 'VH-004', 'MAWAR-002', 'TB001', '2025-01-13', '2025-01-27', '2025-02-27', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-005', 'TVH-JAN25-005', 'VH-005', 'MAWAR-003', 'TB001', '2025-01-24', '2025-01-27', '2025-02-27', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-006', 'TVH-JAN25-006', 'VH-006', 'MAWAR-001', 'TB001', '2025-01-10', '2025-01-27', '2025-02-27', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-007', 'TVH-JAN25-007', 'VH-007', 'ANGGREK-002', 'TB001', '2025-01-22', '2025-01-27', '2025-02-27', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-008', 'TVH-JAN25-008', 'VH-008', 'MAWAR-004', 'TB001', '2025-01-23', '2025-01-27', '2025-02-27', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-009', 'TVH-JAN25-009', 'VH-009', 'ANGGREK-003', 'TB001', '2025-01-26', '2025-01-27', '2025-02-27', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-011', 'TVH-FEB25-001', 'VH-001', 'ANGGREK-001', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-012', 'TVH-FEB25-002', 'VH-002', 'MELATI-001', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-013', 'TVH-FEB25-003', 'VH-003', 'MELATI-005', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-014', 'TVH-FEB25-004', 'VH-004', 'MAWAR-002', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-015', 'TVH-FEB25-005', 'VH-005', 'MAWAR-003', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-016', 'TVH-FEB25-006', 'VH-006', 'MAWAR-001', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-017', 'TVH-FEB25-007', 'VH-007', 'ANGGREK-002', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-018', 'TVH-FEB25-008', 'VH-008', 'MAWAR-004', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-019', 'TVH-FEB25-009', 'VH-009', 'ANGGREK-003', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-020', 'TVH-FEB25-010', 'VH-010', 'MELATI-002', 'TB002', '2025-02-28', '2025-02-28', '2025-03-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-021', 'TVH-FEB25-011', 'VH-011', 'MAWAR-005', 'TB002', '2025-02-26', '2025-02-28', '2025-03-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-022', 'TVH-MAR25-001', 'VH-001', 'ANGGREK-001', 'TB003', '2025-03-26', '2025-03-28', '2025-04-28', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-023', 'TVH-MAR25-002', 'VH-002', 'MELATI-001', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-024', 'TVH-MAR25-003', 'VH-003', 'MELATI-005', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-025', 'TVH-MAR25-004', 'VH-012', 'MELATI-003', 'TB003', '2025-03-26', '2025-03-28', '2025-04-28', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-026', 'TVH-MAR25-005', 'VH-004', 'MAWAR-002', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-027', 'TVH-MAR25-006', 'VH-005', 'MAWAR-003', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-028', 'TVH-MAR25-007', 'VH-006', 'MAWAR-001', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-029', 'TVH-MAR25-008', 'VH-007', 'ANGGREK-002', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-030', 'TVH-MAR25-009', 'VH-008', 'MAWAR-004', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-031', 'TVH-MAR25-010', 'VH-009', 'ANGGREK-003', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-032', 'TVH-MAR25-011', 'VH-010', 'MELATI-002', 'TB003', '2025-03-28', '2025-03-28', '2025-04-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-033', 'TVH-APR25-001', 'VH-001', 'ANGGREK-001', 'TB004', '2025-04-28', '2025-04-28', '2025-05-28', 950000, 0, 0, 950000, 1000000, 50000, 'lunas'),
('DTVH-034', 'TVH-APR25-002', 'VH-002', 'MELATI-001', 'TB004', '2025-04-28', '2025-04-28', '2025-05-28', 750000, 0, 0, 750000, 750000, 0, 'lunas'),
('DTVH-035', 'TVH-MEI25-001', 'VH-010', 'MELATI-002', 'TB005', '2025-05-28', '2025-05-28', '2025-06-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-036', 'TVH-MEI25-002', 'VH-009', 'ANGGREK-003', 'TB005', '2025-05-28', '2025-05-28', '2025-06-28', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-037', 'TVH-MEI25-003', 'VH-001', 'ANGGREK-001', 'TB005', '2025-05-28', '2025-05-28', '2025-06-28', 950000, 0, 0, 950000, 950000, 0, 'lunas'),
('DTVH-038', 'TVH-MEI25-004', 'VH-002', 'MELATI-001', 'TB005', '2025-05-28', '2025-05-28', '2025-06-28', 750000, 0, 0, 750000, 800000, 50000, 'lunas'),
('DTVH-039', 'TVH-APR25-003', 'VH-004', 'MAWAR-002', 'TB004', '2025-04-28', '2025-04-28', '2025-05-28', 500000, 0, 0, 500000, 500000, 0, 'lunas'),
('DTVH-040', 'TVH-MEI25-005', 'VH-004', 'MAWAR-002', 'TB005', '2025-05-28', '2025-05-28', '2025-06-28', 500000, 0, 0, 500000, 500000, 0, 'lunas');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kamar`
--

CREATE TABLE `kamar` (
  `kd_kamar` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `nama_kamar` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `tipe` enum('ekonomi','standar','eksklusif') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jumlah_kamar` int NOT NULL,
  `kuota` int NOT NULL,
  `harga` int NOT NULL,
  `fasilitas` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kamar`
--

INSERT INTO `kamar` (`kd_kamar`, `nama_kamar`, `tipe`, `jumlah_kamar`, `kuota`, `harga`, `fasilitas`) VALUES
('KVH-001', 'Kamar Mawar', 'ekonomi', 10, 2, 500000, 'Kasur, Kipas Angin, Lemari'),
('KVH-002', 'Kamar Melati', 'standar', 5, 2, 750000, 'Kasur, Lemari, AC, Wifi'),
('KVH-003', 'Kamar Anggrek', 'eksklusif', 3, 2, 950000, 'Kasur, AC, Lemari, Wifi, Kompor, Free Laundry 1x Seminggu');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pengeluaran`
--

CREATE TABLE `pengeluaran` (
  `kd_pengeluaran` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal` date NOT NULL,
  `kategori` enum('peralatan','kebersihan','keamanan','internet','gaji','darurat') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `deskripsi` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jumlah_harga` int NOT NULL,
  `dibuat_oleh` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `bukti` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pengeluaran`
--

INSERT INTO `pengeluaran` (`kd_pengeluaran`, `tanggal`, `kategori`, `deskripsi`, `jumlah_harga`, `dibuat_oleh`, `bukti`) VALUES
('PGN-001', '2025-06-29', 'kebersihan', 'Sapu lidi 4', 20000, 'Doni Wahyono', 'image\\uploads\\2025-06-29\\ccebc9c7c8d3489b9d9dfd972270b2e7.png'),
('PGN-002', '2025-07-01', 'internet', 'Bayar tagihan internet bulanan', 545000, 'Doni Wahyono', 'image\\uploads\\2025-07-01\\25c288fd71d2409fadf5b55fb9bbf1eb.png');

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyewa`
--

CREATE TABLE `penyewa` (
  `kd_penyewa` char(11) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `jenis_kelamin` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` char(15) COLLATE utf8mb4_general_ci NOT NULL,
  `alamat` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('Aktif','Non-Aktif') COLLATE utf8mb4_general_ci NOT NULL,
  `kd_unit` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `penyewa`
--

INSERT INTO `penyewa` (`kd_penyewa`, `nama`, `jenis_kelamin`, `no_hp`, `alamat`, `status`, `kd_unit`) VALUES
('VH-001', 'Doni Wahyono', 'Laki-laki', '6282320308986', 'Subang', 'Aktif', 'ANGGREK-001'),
('VH-002', 'Siti Thoyibah', 'Perempuan', '62856775423322', 'Bandung', 'Aktif', 'MELATI-001'),
('VH-003', 'Putri Cantika', 'Perempuan', '6281223552144', 'Bekasi', 'Non-Aktif', 'Silahkan pilih kode unit'),
('VH-004', 'Aisah Gandari Rahmah', 'Perempuan', '6283866092997', 'Subang', 'Aktif', 'MAWAR-002'),
('VH-005', 'Ariyan Kusharthanto', 'Laki-laki', '6282116875164', 'Subang', 'Aktif', 'MAWAR-003'),
('VH-006', 'Lutfi Mahesa', 'Laki-laki', '6285703229695', 'Subang', 'Aktif', 'MAWAR-001'),
('VH-007', 'Indri Rohmawati', 'Perempuan', '6282129358093', 'Subang', 'Aktif', 'ANGGREK-002'),
('VH-008', 'Iin Solihin', 'Laki-laki', '62897765434567', 'Majalengka', 'Aktif', 'MAWAR-004'),
('VH-009', 'Gracia Satria Widodo', 'Perempuan', '6282153658988', 'Bekasi', 'Aktif', 'ANGGREK-003'),
('VH-010', 'Isvina Purnama', 'Perempuan', '6285353761055', 'Ciamis', 'Aktif', 'MELATI-002'),
('VH-011', 'Gilang Sutiyo', 'Laki-laki', '6281315665245', 'Bekasi', 'Non-Aktif', 'Silahkan pilih kode unit'),
('VH-012', 'Anggita Sulistiyo', 'Perempuan', '6282323551839', 'Subang', 'Non-Aktif', 'Silahkan pilih kode unit'),
('VH-013', 'Sohibin', 'Laki-laki', '62897897867867', 'Subang', 'Aktif', 'MELATI-003');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi`
--

CREATE TABLE `transaksi` (
  `kd_transaksi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_transaksi_bulanan` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `kd_penyewa` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_unit` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `tanggal_transaksi` date NOT NULL,
  `total_harga` int NOT NULL,
  `status_transaksi` enum('lunas','belum_lunas') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `diskon` int DEFAULT NULL,
  `biaya_tambahan` int DEFAULT NULL,
  `jumlah_bayar` int NOT NULL,
  `uang_penyewa` int DEFAULT NULL,
  `kembalian` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi`
--

INSERT INTO `transaksi` (`kd_transaksi`, `kd_transaksi_bulanan`, `kd_penyewa`, `kd_unit`, `tanggal_mulai`, `tanggal_selesai`, `tanggal_transaksi`, `total_harga`, `status_transaksi`, `diskon`, `biaya_tambahan`, `jumlah_bayar`, `uang_penyewa`, `kembalian`) VALUES
('TVH-APR25-001', 'TB004', 'VH-001', 'ANGGREK-001', '2025-04-28', '2025-05-28', '2025-04-28', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-APR25-002', 'TB004', 'VH-002', 'MELATI-001', '2025-04-28', '2025-05-28', '2025-04-28', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-APR25-003', 'TB004', 'VH-004', 'MAWAR-002', '2025-04-28', '2025-05-28', '2025-04-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-FEB25-001', 'TB002', 'VH-001', 'ANGGREK-001', '2025-02-28', '2025-03-28', '2025-02-28', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-FEB25-002', 'TB002', 'VH-002', 'MELATI-001', '2025-02-28', '2025-03-28', '2025-02-28', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-FEB25-003', 'TB002', 'VH-003', 'MELATI-005', '2025-02-28', '2025-03-28', '2025-02-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-FEB25-004', 'TB002', 'VH-004', 'MAWAR-002', '2025-02-28', '2025-03-28', '2025-02-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-FEB25-005', 'TB002', 'VH-005', 'MAWAR-003', '2025-02-28', '2025-03-28', '2025-02-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-FEB25-006', 'TB002', 'VH-006', 'MAWAR-001', '2025-02-28', '2025-03-28', '2025-02-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-FEB25-007', 'TB002', 'VH-007', 'ANGGREK-002', '2025-02-28', '2025-03-28', '2025-02-28', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-FEB25-008', 'TB002', 'VH-008', 'MAWAR-004', '2025-02-28', '2025-03-28', '2025-02-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-FEB25-009', 'TB002', 'VH-009', 'ANGGREK-003', '2025-02-28', '2025-03-28', '2025-02-28', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-FEB25-010', 'TB002', 'VH-010', 'MELATI-002', '2025-02-28', '2025-03-28', '2025-02-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-FEB25-011', 'TB002', 'VH-011', 'MAWAR-005', '2025-02-28', '2025-03-28', '2025-02-26', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-JAN25-001', 'TB001', 'VH-001', 'ANGGREK-001', '2025-01-27', '2025-02-27', '2025-01-27', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-JAN25-002', 'TB001', 'VH-002', 'MELATI-001', '2025-01-27', '2025-02-27', '2025-01-27', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-JAN25-003', 'TB001', 'VH-003', 'MELATI-005', '2025-01-27', '2025-02-27', '2025-01-17', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-JAN25-004', 'TB001', 'VH-004', 'MAWAR-002', '2025-01-27', '2025-02-27', '2025-01-13', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-JAN25-005', 'TB001', 'VH-005', 'MAWAR-003', '2025-01-27', '2025-02-27', '2025-01-24', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-JAN25-006', 'TB001', 'VH-006', 'MAWAR-001', '2025-01-27', '2025-02-27', '2025-01-10', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-JAN25-007', 'TB001', 'VH-007', 'ANGGREK-002', '2025-01-27', '2025-02-27', '2025-01-22', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-JAN25-008', 'TB001', 'VH-008', 'MAWAR-004', '2025-01-27', '2025-02-27', '2025-01-23', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-JAN25-009', 'TB001', 'VH-009', 'ANGGREK-003', '2025-01-27', '2025-02-27', '2025-01-26', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-MAR25-001', 'TB003', 'VH-001', 'ANGGREK-001', '2025-03-28', '2025-04-28', '2025-03-26', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-MAR25-002', 'TB003', 'VH-002', 'MELATI-001', '2025-03-28', '2025-04-28', '2025-03-28', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-MAR25-003', 'TB003', 'VH-003', 'MELATI-005', '2025-03-28', '2025-04-28', '2025-03-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-MAR25-004', 'TB003', 'VH-012', 'MELATI-003', '2025-03-28', '2025-04-28', '2025-03-26', 750000, 'lunas', 0, 0, 750000, 750000, 0),
('TVH-MAR25-005', 'TB003', 'VH-004', 'MAWAR-002', '2025-03-28', '2025-04-28', '2025-03-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-MAR25-006', 'TB003', 'VH-005', 'MAWAR-003', '2025-03-28', '2025-04-28', '2025-03-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-MAR25-007', 'TB003', 'VH-006', 'MAWAR-001', '2025-03-28', '2025-04-28', '2025-03-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-MAR25-008', 'TB003', 'VH-007', 'ANGGREK-002', '2025-03-28', '2025-04-28', '2025-03-28', 950000, 'lunas', 0, 0, 950000, 1000000, 50000),
('TVH-MAR25-009', 'TB003', 'VH-008', 'MAWAR-004', '2025-03-28', '2025-04-28', '2025-03-28', 500000, 'lunas', 0, 0, 500000, 500000, 0),
('TVH-MAR25-010', 'TB003', 'VH-009', 'ANGGREK-003', '2025-03-28', '2025-04-28', '2025-03-28', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-MAR25-011', 'TB003', 'VH-010', 'MELATI-002', '2025-03-28', '2025-04-28', '2025-03-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-MEI25-001', 'TB005', 'VH-010', 'MELATI-002', '2025-05-28', '2025-06-28', '2025-05-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-MEI25-002', 'TB005', 'VH-009', 'ANGGREK-003', '2025-05-28', '2025-06-28', '2025-05-28', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-MEI25-003', 'TB005', 'VH-001', 'ANGGREK-001', '2025-05-28', '2025-06-28', '2025-05-28', 950000, 'lunas', 0, 0, 950000, 950000, 0),
('TVH-MEI25-004', 'TB005', 'VH-002', 'MELATI-001', '2025-05-28', '2025-06-28', '2025-05-28', 750000, 'lunas', 0, 0, 750000, 800000, 50000),
('TVH-MEI25-005', 'TB005', 'VH-004', 'MAWAR-002', '2025-05-28', '2025-06-28', '2025-05-28', 500000, 'lunas', 0, 0, 500000, 500000, 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_bulanan`
--

CREATE TABLE `transaksi_bulanan` (
  `kd_transaksi_bulanan` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `nama_bulan` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `tahun` varchar(15) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi_bulanan`
--

INSERT INTO `transaksi_bulanan` (`kd_transaksi_bulanan`, `nama_bulan`, `tahun`) VALUES
('TB001', 'Januari', '2025'),
('TB002', 'Februari', '2025'),
('TB003', 'Maret', '2025'),
('TB004', 'April', '2025'),
('TB005', 'Mei', '2025');

-- --------------------------------------------------------

--
-- Struktur dari tabel `unit_kamar`
--

CREATE TABLE `unit_kamar` (
  `kd_unit` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_kamar` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('kosong','terisi') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `unit_kamar`
--

INSERT INTO `unit_kamar` (`kd_unit`, `kd_kamar`, `status`) VALUES
('ANGGREK-001', 'KVH-003', 'terisi'),
('ANGGREK-002', 'KVH-003', 'terisi'),
('ANGGREK-003', 'KVH-003', 'terisi'),
('BUNGA-001', 'KVH-004', 'kosong'),
('BUNGA-002', 'KVH-004', 'kosong'),
('BUNGA-003', 'KVH-004', 'kosong'),
('BUNGA-004', 'KVH-004', 'kosong'),
('BUNGA-005', 'KVH-004', 'kosong'),
('BUNGA-006', 'KVH-004', 'kosong'),
('BUNGA-007', 'KVH-004', 'kosong'),
('MAWAR-001', 'KVH-001', 'terisi'),
('MAWAR-002', 'KVH-001', 'terisi'),
('MAWAR-003', 'KVH-001', 'terisi'),
('MAWAR-004', 'KVH-001', 'terisi'),
('MAWAR-005', 'KVH-001', 'kosong'),
('MELATI-001', 'KVH-002', 'terisi'),
('MELATI-002', 'KVH-002', 'terisi'),
('MELATI-003', 'KVH-002', 'terisi'),
('MELATI-004', 'KVH-002', 'kosong'),
('MELATI-005', 'KVH-002', 'kosong');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `kode_user` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('admin','petugas') COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`kode_user`, `nama`, `username`, `password`, `no_hp`, `role`) VALUES
('USR-VH-001', 'Doni Wahyono', 'doniwk', '123456', '6282320308986', 'admin'),
('USR-VH-002', 'Lutfi', 'lutfi', '123456', '6285703229695', 'petugas'),
('USR-VH-003', 'Indri', 'indri', '123456', '6282129358093', 'petugas'),
('USR-VH-004', 'Aisah Gandari', 'aisah', '●●●●●●●', '6285765682932', 'petugas');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`kd_detail_transaksi`);

--
-- Indeks untuk tabel `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`kd_kamar`);

--
-- Indeks untuk tabel `pengeluaran`
--
ALTER TABLE `pengeluaran`
  ADD PRIMARY KEY (`kd_pengeluaran`);

--
-- Indeks untuk tabel `penyewa`
--
ALTER TABLE `penyewa`
  ADD PRIMARY KEY (`kd_penyewa`);

--
-- Indeks untuk tabel `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`kd_transaksi`);

--
-- Indeks untuk tabel `transaksi_bulanan`
--
ALTER TABLE `transaksi_bulanan`
  ADD PRIMARY KEY (`kd_transaksi_bulanan`);

--
-- Indeks untuk tabel `unit_kamar`
--
ALTER TABLE `unit_kamar`
  ADD PRIMARY KEY (`kd_unit`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`kode_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
