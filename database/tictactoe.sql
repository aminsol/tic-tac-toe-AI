-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 22, 2018 at 10:02 PM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tictactoe`
--

-- --------------------------------------------------------

--
-- Table structure for table `games_history`
--

CREATE TABLE `games_history` (
  `id` int(11) NOT NULL,
  `role` varchar(1) NOT NULL,
  `result` varchar(5) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `longterm`
--

CREATE TABLE `longterm` (
  `id` int(11) NOT NULL,
  `board_before` varchar(10) NOT NULL,
  `position` int(11) NOT NULL,
  `board_after` varchar(10) NOT NULL,
  `score` int(11) NOT NULL,
  `role` char(1) NOT NULL,
  `explored` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `moves_history`
--

CREATE TABLE `moves_history` (
  `id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `board_before` varchar(10) NOT NULL,
  `position` int(11) NOT NULL,
  `board_after` varchar(10) NOT NULL,
  `role` char(1) NOT NULL,
  `new` int(11) NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `shortterm`
--

CREATE TABLE `shortterm` (
  `id` int(11) NOT NULL,
  `board_before` varchar(10) NOT NULL,
  `position` int(11) NOT NULL,
  `board_after` varchar(10) NOT NULL,
  `role` char(1) NOT NULL,
  `new` int(11) NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `games_history`
--
ALTER TABLE `games_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `longterm`
--
ALTER TABLE `longterm`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `board_move` (`board_before`,`position`) USING BTREE;

--
-- Indexes for table `moves_history`
--
ALTER TABLE `moves_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shortterm`
--
ALTER TABLE `shortterm`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `board_move` (`board_before`,`position`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `games_history`
--
ALTER TABLE `games_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `longterm`
--
ALTER TABLE `longterm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `moves_history`
--
ALTER TABLE `moves_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shortterm`
--
ALTER TABLE `shortterm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
