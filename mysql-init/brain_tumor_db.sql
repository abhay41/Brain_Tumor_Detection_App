-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 28, 2025 at 10:17 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `brain_tumor_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password_hash`, `created_at`) VALUES
(1, 'admin', 'pbkdf2:sha256:260000$Ji6mwPLufaqttsPD$470c9797a39942642b0a4cc7aa3097c6c27d960d2d40c4eaf8ff7287c34ea7d0', '2025-07-29 00:59:23');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `tumor_type` varchar(80) DEFAULT NULL,
  `diagnosis_date` date NOT NULL,
  `image_path` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `treatment`
--

CREATE TABLE `treatment` (
  `id` int(11) NOT NULL,
  `tumor_type` varchar(80) NOT NULL,
  `description` text NOT NULL,
  `recommended_medication` varchar(120) DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `side_effects` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `treatment`
--

INSERT INTO `treatment` (`id`, `tumor_type`, `description`, `recommended_medication`, `duration`, `side_effects`, `created_at`) VALUES
(1, 'Glioma', 'A malignant type of brain tumor that begins in glial cells. Common subtypes include astrocytomas, oligodendrogliomas, and ependymomas. \n                Treatment approach varies based on grade (I-IV), location, and genetic markers like IDH mutation and 1p/19q codeletion status. \n                Primary treatment often includes maximal safe surgical resection followed by concurrent chemoradiation.', 'First-line: Temozolomide (150-200mg/m² for 5 days every 28 days)\n                Second-line: Bevacizumab (10mg/kg every', 'Initial treatment: 6 weeks of concurrent chemoradi', 'Common: Fatigue, nausea, vomiting, decreased appetite, bone marrow suppression\n                Neurological: Seizures, headaches, cognitive changes\n                Radiation-related: Hair loss, skin irritation, brain swelling\n                Long-term: Memory issues, endocrine dysfunction\n                Bevacizumab-specific: Hypertension, wound healing problems, blood clots', '2025-06-10 22:27:28'),
(2, 'Meningioma', 'Typically benign tumors arising from the meninges. Classified by WHO grades I-III, with Grade I being most common (80%).\n                Location variants include parasagittal, convexity, sphenoid wing, and posterior fossa meningiomas.\n                Treatment strategy depends on size, location, growth rate, and symptoms.\n                Some cases may be managed with observation alone (watch and wait approach).', 'Primary treatment is usually surgical\n                Anticonvulsants: Levetiracetam (500-1000mg twice daily) or Phenyto', 'Surgery recovery: 4-8 weeks\n                Radiat', 'Surgical: Infection risk, bleeding, CSF leak, neurological deficits\n                Radiation-related: Fatigue, local hair loss, skin changes, cognitive effects\n                Location-specific: Visual problems, hearing loss, facial numbness\n                Long-term: Seizures, headaches, cognitive changes\n                Medication-related: Liver enzyme elevation, bone density changes', '2025-06-10 22:27:28'),
(3, 'No Tumor', 'Absence of neoplastic growth in brain tissue confirmed through imaging studies (MRI/CT).\n                May still require monitoring if patient has risk factors or concerning symptoms.\n                Focus on preventive care and addressing any underlying neurological symptoms.\n                Important to establish reason for initial imaging and ensure appropriate follow-up.', 'Symptomatic treatment as needed:\n                Headache management: NSAIDs or specific migraine medications\n          ', 'Initial follow-up: 6 months\n                Long-t', 'No treatment-specific side effects\n                Monitor for any new neurological symptoms\n                Regular assessment of risk factors\n                Psychological support may be needed for anxiety management', '2025-06-10 22:27:28'),
(4, 'Pituitary', 'Tumors arising from the pituitary gland, classified as functional (hormone-secreting) or non-functional.\n                Common variants include prolactinomas, growth hormone-secreting, ACTH-secreting, and non-functioning adenomas.\n                Treatment approach depends on tumor size (micro vs. macro), hormone status, and visual compromise.\n                May affect multiple endocrine systems requiring comprehensive hormonal evaluation.', 'Prolactinomas: Cabergoline (0.25-2mg twice weekly) or Bromocriptine (2.5-15mg daily)\n                Acromegaly: Octreot', 'Medical therapy: Ongoing, often lifelong\n         ', 'Medication-specific: Nausea, dizziness, fatigue, mood changes\n                Surgical: Diabetes insipidus, CSF leak, hormone deficiencies\n                Endocrine: Weight changes, sexual dysfunction, mood disorders\n                Visual: Vision changes, double vision\n                Long-term: Need for hormone replacement, metabolic changes', '2025-06-10 22:27:28');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `profile_image` varchar(200) DEFAULT NULL,
  `is_locked` tinyint(1) DEFAULT 0,
  `is_verified` tinyint(1) DEFAULT 0,
  `verification_code` varchar(6) DEFAULT NULL,
  `verification_timestamp` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `success` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `treatment`
--
ALTER TABLE `treatment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_login`
--
ALTER TABLE `user_login`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `treatment`
--
ALTER TABLE `treatment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_login`
--
ALTER TABLE `user_login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `patient`
--
ALTER TABLE `patient`
  ADD CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_login`
--
ALTER TABLE `user_login`
  ADD CONSTRAINT `user_login_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
