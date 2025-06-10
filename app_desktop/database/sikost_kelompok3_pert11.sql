-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Jun 2025 pada 02.04
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

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
  `kd_detail_transaksi` varchar(15) NOT NULL,
  `kd_transaksi` varchar(15) NOT NULL,
  `tanggal_bayar` date NOT NULL,
  `jumlah_bayar` int(11) NOT NULL,
  `metode_pembayaran` enum('cash','transfer') NOT NULL,
  `bukti_pembayaran` varchar(50) NOT NULL,
  `catatan` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `kamar`
--

CREATE TABLE `kamar` (
  `kd_kamar` varchar(11) NOT NULL,
  `nama_kamar` varchar(50) NOT NULL,
  `tipe` varchar(30) NOT NULL,
  `jumlah_kamar` int(11) NOT NULL,
  `kuota` int(11) NOT NULL,
  `harga` int(11) NOT NULL,
  `fasilitas` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kamar`
--

INSERT INTO `kamar` (`kd_kamar`, `nama_kamar`, `tipe`, `jumlah_kamar`, `kuota`, `harga`, `fasilitas`) VALUES
('KVH-001', 'Kamar Mawar', 'Standar', 3, 2, 1500000, 'AC, Kamar Mandi Dalam'),
('KVH-002', 'Kamar Melati', 'VIP', 2, 1, 2500000, 'AC, Water Heater, TV'),
('KVH-003', 'Kamar Sakura', 'Deluxe', 4, 3, 2000000, 'AC, Meja Belajar, Kamar Mandi Luar'),
('KVH-004', 'Kamar Dahlia', 'Standar', 1, 1, 1200000, 'Kipas Angin, Kamar Mandi Luar'),
('KVH-005', 'Kamar Lily', 'VIP', 2, 2, 2300000, 'AC, Kulkas, Water Heater');

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyewa`
--

CREATE TABLE `penyewa` (
  `kd_penyewa` char(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `jenis_kelamin` varchar(15) NOT NULL,
  `no_hp` char(15) NOT NULL,
  `alamat` varchar(50) NOT NULL,
  `kd_unit` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `penyewa`
--

INSERT INTO `penyewa` (`kd_penyewa`, `nama`, `jenis_kelamin`, `no_hp`, `alamat`, `kd_unit`) VALUES
('VH-001', 'Doni Wahyono', 'Laki-laki', '085217208593', 'Subang', 'Silahkan pilih ');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi`
--

CREATE TABLE `transaksi` (
  `kd_transaksi` varchar(15) NOT NULL,
  `kd_penyewa` varchar(15) NOT NULL,
  `kd_unit` varchar(15) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `tanggal_transaksi` date NOT NULL,
  `total_harga` int(11) NOT NULL,
  `status_transaksi` enum('aktif','selesai','batal') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `transaksi`
--

INSERT INTO `transaksi` (`kd_transaksi`, `kd_penyewa`, `kd_unit`, `tanggal_mulai`, `tanggal_selesai`, `tanggal_transaksi`, `total_harga`, `status_transaksi`) VALUES
('TRX-VH-001', 'VH-001', 'MAWAR-001', '2025-06-23', NULL, '2025-06-23', 650000, 'aktif');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_bulanan`
--

CREATE TABLE `transaksi_bulanan` (
  `kd_transaksi_bulanan` varchar(15) NOT NULL,
  `nama_bulan` varchar(20) NOT NULL,
  `tahun` varchar(15) NOT NULL
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
  `kd_unit` varchar(15) NOT NULL,
  `kd_kamar` varchar(15) NOT NULL,
  `status` enum('kosong','terisi') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `kode_user` varchar(15) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','petugas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`kode_user`, `nama`, `username`, `password`, `role`) VALUES
('USR-VH-001', 'Doni Wahyono', 'donisw', '123456', 'admin'),
('USR-VH-002', 'Lutfi Mahesa', 'lutfi', '123456', 'petugas');

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
