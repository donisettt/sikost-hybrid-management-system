-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 08, 2025 at 04:58 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

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
-- Table structure for table `detail_transaksi`
--

CREATE TABLE `detail_transaksi` (
  `kd_detail_transaksi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_transaksi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal_bayar` date NOT NULL,
  `jumlah_bayar` int NOT NULL,
  `metode_pembayaran` enum('cash','transfer') COLLATE utf8mb4_general_ci NOT NULL,
  `bukti_pembayaran` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `catatan` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kamar`
--

CREATE TABLE `kamar` (
  `kd_kamar` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama_kamar` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tipe` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jumlah_kamar` int NOT NULL,
  `kuota` int NOT NULL,
  `harga` int NOT NULL,
  `fasilitas` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar`
--

INSERT INTO `kamar` (`kd_kamar`, `nama_kamar`, `tipe`, `jumlah_kamar`, `kuota`, `harga`, `fasilitas`) VALUES
('KVH-001', 'Kamar Mawar', 'Standar', 10, 2, 650000, 'Kipas Angin, Kasur, Lemari, Wifi'),
('KVH-002', 'Kamar Anggrek', 'Deluxe', 3, 2, 800000, 'AC, Kasur, Lemari, Wifi'),
('KVH-003', 'Kamar Tulip', 'Standar', 5, 2, 700000, 'Kipas Angin, Kasur, Lemari, Wifi'),
('KVH-004', 'Kamar Melati', 'Minimalis', 10, 4, 450000, 'Kasur, Lemari');

-- --------------------------------------------------------

--
-- Table structure for table `penyewa`
--

CREATE TABLE `penyewa` (
  `kd_penyewa` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jenis_kelamin` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `no_hp` char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `alamat` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `kd_unit` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penyewa`
--

INSERT INTO `penyewa` (`kd_penyewa`, `nama`, `jenis_kelamin`, `no_hp`, `alamat`, `kd_unit`) VALUES
('VH-001', 'Doni', 'Laki-laki', '087968678786', 'Bandung', 'MAWAR-002'),
('VH-002', 'Amelia', 'Perempuan', '08933232322372', 'Bekasi', 'ANGGREK-001'),
('VH-003', 'Andini Putri', 'Perempuan', '08977654356', 'Jakarta', 'MAWAR-001'),
('VH-004', 'Abdul Aziz', 'Laki-laki', '098675435675', 'Pangandaran', 'ANGGREK-002'),
('VH-005', 'Ilham Saputra', 'Laki-laki', '081313232221', 'Bekasi', 'ANGGREK-003'),
('VH-006', 'Febi Rindiya', 'Perempuan', '098765432', 'Cikarang', 'MELATI-001'),
('VH-007', 'Nadya Omara', 'Perempuan', '098789789789', 'Bekasi', 'TULIP-001'),
('VH-008', 'Gungun Gunawan', 'Laki-laki', '081334567212', 'Pangandaran', 'TULIP-002');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `kd_transaksi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_penyewa` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `kd_unit` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `tanggal_transaksi` date NOT NULL,
  `periode_awal` date NOT NULL,
  `nama_bulan` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `harga_perbulan` int NOT NULL,
  `total_biaya` int NOT NULL,
  `status_pembayaran` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `keterangan` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`kd_transaksi`, `kd_penyewa`, `kd_unit`, `tanggal_transaksi`, `periode_awal`, `nama_bulan`, `harga_perbulan`, `total_biaya`, `status_pembayaran`, `keterangan`) VALUES
('TR-VH-001', 'VH-001', 'MAWAR-001', '2025-06-27', '2025-06-27', '1', 650000, 650000, 'Lunas', 'OK');

-- --------------------------------------------------------

--
-- Table structure for table `unit_kamar`
--

CREATE TABLE `unit_kamar` (
  `kd_unit` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `kd_kamar` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('kosong','terisi') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `unit_kamar`
--

INSERT INTO `unit_kamar` (`kd_unit`, `kd_kamar`, `status`) VALUES
('ANGGREK-001', 'KVH-002', 'terisi'),
('ANGGREK-002', 'KVH-002', 'terisi'),
('ANGGREK-003', 'KVH-002', 'terisi'),
('MAWAR-001', 'KVH-001', 'terisi'),
('MAWAR-002', 'KVH-001', 'terisi'),
('MELATI-001', 'KVH-004', 'terisi'),
('TULIP-001', 'KVH-003', 'terisi'),
('TULIP-002', 'KVH-003', 'terisi');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `kode_user` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('admin','petugas') COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`kode_user`, `nama`, `username`, `password`, `role`) VALUES
('USR-VB-001', 'Doni Wahyono', 'donisw', '123456', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`kd_detail_transaksi`);

--
-- Indexes for table `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`kd_kamar`);

--
-- Indexes for table `penyewa`
--
ALTER TABLE `penyewa`
  ADD PRIMARY KEY (`kd_penyewa`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`kd_transaksi`);

--
-- Indexes for table `unit_kamar`
--
ALTER TABLE `unit_kamar`
  ADD PRIMARY KEY (`kd_unit`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`kode_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
