-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2025 at 07:17 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smort`
--

-- --------------------------------------------------------

--
-- Table structure for table `region`
--

CREATE TABLE `region` (
  `ID` int(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `region` varchar(50) NOT NULL,
  `latitude` decimal(8,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `region`
--

INSERT INTO `region` (`ID`, `name`, `region`, `latitude`, `longitude`) VALUES
(1, 'seri iskandar', 'perak tengah', '4.599766', '101.088338'),
(2, 'pekan ipoh', 'kinta', '4.718927', '101.121763'),
(3, 'batu gajah', 'kinta tengah', '4.471511', '101.044970');

-- --------------------------------------------------------


-- --------------------------------------------------------

--
-- Table structure for table `sensor`
--

CREATE TABLE `sensor` (
  `ID` int(100) NOT NULL,
  `latitude` decimal(8,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor`
--

INSERT INTO `sensor` (`ID`, `latitude`, `longitude`, `name`) VALUES
(1, '4.382715', '100.974509', 'V6'),
(2, '4.386550', '100.974736', 'Sport Complex'),
(3, '4.386821', '100.970825', 'V1'),
(4, '4.388135', '100.967944', 'V2 '),
(5, '4.376466', '100.969537', 'UTP Plant'),
(6, '4.598820', '101.077110', 'Ipoh Parade'),
(7, '4.424457', '101.045338', 'Big Portion'),
(8, '4.459991', '101.049471', 'KTM Batu gajah'),
(9, '4.475300', '101.087400', 'Kellie Castle');

-- --------------------------------------------------------
--
-- Table structure for table `region_sensor`
--

CREATE TABLE `region_sensor` (
  `region_ID` int(11) NOT NULL,
  `sensor_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `region_sensor`
--

INSERT INTO `region_sensor` (`region_ID`, `sensor_ID`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 6),
(3, 7),
(3, 8),
(3, 9);

--
-- Table structure for table `sensor_record`
--

CREATE TABLE `sensor_record` (
  `smort_ID` int(100) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `trash_level` float(5,2) NOT NULL,
  `image` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor_record`
--

INSERT INTO `sensor_record` (`smort_ID`, `time_stamp`, `trash_level`, `image`) VALUES
(1, '2023-09-30 16:00:00', 10.00, ''),
(1, '2023-09-30 16:30:00', 20.00, ''),
(1, '2023-09-30 17:00:00', 30.00, ''),
(1, '2023-09-30 17:30:00', 40.00, ''),
(1, '2023-09-30 18:00:00', 50.00, ''),
(1, '2023-09-30 18:30:00', 60.00, ''),
(1, '2023-09-30 19:00:00', 70.00, ''),
(1, '2023-09-30 19:30:00', 80.00, ''),
(1, '2023-09-30 20:00:00', 90.00, ''),
(1, '2023-09-30 20:30:00', 100.00, ''),
(1, '2023-09-30 21:00:00', 0.00, ''),
(2, '2023-09-30 16:00:00', 15.00, ''),
(2, '2023-09-30 16:30:00', 25.00, ''),
(2, '2023-09-30 17:00:00', 35.00, ''),
(2, '2023-09-30 17:30:00', 45.00, ''),
(2, '2023-09-30 18:00:00', 55.00, ''),
(2, '2023-09-30 18:30:00', 65.00, ''),
(2, '2023-09-30 19:00:00', 75.00, ''),
(2, '2023-09-30 19:30:00', 85.00, ''),
(2, '2023-09-30 20:00:00', 95.00, ''),
(2, '2023-09-30 20:30:00', 5.00, ''),
(2, '2023-09-30 21:00:00', 15.00, ''),
(3, '2023-09-30 16:00:00', 15.00, ''),
(3, '2023-09-30 16:30:00', 25.00, ''),
(3, '2023-09-30 17:00:00', 35.00, ''),
(3, '2023-09-30 17:30:00', 45.00, ''),
(3, '2023-09-30 18:00:00', 55.00, ''),
(3, '2023-09-30 18:30:00', 65.00, ''),
(3, '2023-09-30 19:00:00', 75.00, ''),
(3, '2023-09-30 19:30:00', 85.00, ''),
(3, '2023-09-30 20:00:00', 95.00, ''),
(3, '2023-09-30 20:30:00', 5.00, ''),
(3, '2023-09-30 21:00:00', 15.00, ''),
(4, '2023-09-30 16:00:00', 15.00, ''),
(4, '2023-09-30 16:30:00', 25.00, ''),
(4, '2023-09-30 17:00:00', 35.00, ''),
(4, '2023-09-30 17:30:00', 45.00, ''),
(4, '2023-09-30 18:00:00', 55.00, ''),
(4, '2023-09-30 18:30:00', 65.00, ''),
(4, '2023-09-30 19:00:00', 75.00, ''),
(4, '2023-09-30 19:30:00', 85.00, ''),
(4, '2023-09-30 20:00:00', 95.00, ''),
(4, '2023-09-30 20:30:00', 5.00, ''),
(4, '2023-09-30 21:00:00', 15.00, ''),
(5, '2023-09-30 16:00:00', 15.00, ''),
(5, '2023-09-30 16:30:00', 25.00, ''),
(5, '2023-09-30 17:00:00', 35.00, ''),
(5, '2023-09-30 17:30:00', 45.00, ''),
(5, '2023-09-30 18:00:00', 55.00, ''),
(5, '2023-09-30 18:30:00', 65.00, ''),
(5, '2023-09-30 19:00:00', 75.00, ''),
(5, '2023-09-30 19:30:00', 85.00, ''),
(5, '2023-09-30 20:00:00', 95.00, ''),
(5, '2023-09-30 20:30:00', 5.00, ''),
(5, '2023-09-30 21:00:00', 15.00, ''),
(6, '2023-09-30 16:00:00', 15.00, ''),
(6, '2023-09-30 16:30:00', 25.00, ''),
(6, '2023-09-30 17:00:00', 35.00, ''),
(6, '2023-09-30 17:30:00', 45.00, ''),
(6, '2023-09-30 18:00:00', 55.00, ''),
(6, '2023-09-30 18:30:00', 65.00, ''),
(6, '2023-09-30 19:00:00', 75.00, ''),
(6, '2023-09-30 19:30:00', 85.00, ''),
(6, '2023-09-30 20:00:00', 95.00, ''),
(6, '2023-09-30 20:30:00', 5.00, ''),
(6, '2023-09-30 21:00:00', 15.00, ''),
(7, '2023-09-30 16:00:00', 15.00, ''),
(7, '2023-09-30 16:30:00', 25.00, ''),
(7, '2023-09-30 17:00:00', 35.00, ''),
(7, '2023-09-30 17:30:00', 45.00, ''),
(7, '2023-09-30 18:00:00', 55.00, ''),
(7, '2023-09-30 18:30:00', 65.00, ''),
(7, '2023-09-30 19:00:00', 75.00, ''),
(7, '2023-09-30 19:30:00', 85.00, ''),
(7, '2023-09-30 20:00:00', 95.00, ''),
(7, '2023-09-30 20:30:00', 5.00, ''),
(7, '2023-09-30 21:00:00', 15.00, ''),
(8, '2023-09-30 16:00:00', 15.00, ''),
(8, '2023-09-30 16:30:00', 25.00, ''),
(8, '2023-09-30 17:00:00', 35.00, ''),
(8, '2023-09-30 17:30:00', 45.00, ''),
(8, '2023-09-30 18:00:00', 55.00, ''),
(8, '2023-09-30 18:30:00', 65.00, ''),
(8, '2023-09-30 19:00:00', 75.00, ''),
(8, '2023-09-30 19:30:00', 85.00, ''),
(8, '2023-09-30 20:00:00', 95.00, ''),
(8, '2023-09-30 20:30:00', 5.00, ''),
(8, '2023-09-30 21:00:00', 15.00, ''),
(9, '2023-09-30 16:00:00', 5.00, ''),
(9, '2023-09-30 16:30:00', 15.00, ''),
(9, '2023-09-30 17:00:00', 25.00, ''),
(9, '2023-09-30 17:30:00', 35.00, ''),
(9, '2023-09-30 18:00:00', 45.00, ''),
(9, '2023-09-30 18:30:00', 55.00, ''),
(9, '2023-09-30 19:00:00', 65.00, ''),
(9, '2023-09-30 19:30:00', 75.00, ''),
(9, '2023-09-30 20:00:00', 85.00, ''),
(9, '2023-09-30 20:30:00', 95.00, ''),
(9, '2023-09-30 21:00:00', 5.00, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `region_sensor`
--
ALTER TABLE `region_sensor`
  ADD PRIMARY KEY (`region_ID`,`sensor_ID`),
  ADD KEY `sensor` (`sensor_ID`);

--
-- Indexes for table `sensor`
--
ALTER TABLE `sensor`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `sensor_record`
--
ALTER TABLE `sensor_record`
  ADD PRIMARY KEY (`smort_ID`,`time_stamp`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `region`
--
ALTER TABLE `region`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `sensor`
--
ALTER TABLE `sensor`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `region_sensor`
--
ALTER TABLE `region_sensor`
  ADD CONSTRAINT `region` FOREIGN KEY (`region_ID`) REFERENCES `region` (`ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `sensor` FOREIGN KEY (`sensor_ID`) REFERENCES `sensor` (`ID`) ON DELETE CASCADE;

--
-- Constraints for table `sensor_record`
--
ALTER TABLE `sensor_record`
  ADD CONSTRAINT `record` FOREIGN KEY (`smort_ID`) REFERENCES `sensor` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
