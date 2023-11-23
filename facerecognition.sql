CREATE DATABASE IF NOT EXISTS facerecognition;
USE facerecognition;

-- Table structure for table `Student`
DROP TABLE IF EXISTS `Student`;
CREATE TABLE `Student` (
  `student_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into the `Student` table
INSERT INTO `Student` VALUES (1, 'JACK', NOW(), '2021-01-20');

-- Create other tables as needed
-- Replace the placeholders below with actual table definitions

-- Table structure for table `Course`
-- Table structure for table `Course`
DROP TABLE IF EXISTS `Course`;
CREATE TABLE `Course` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `course_name` VARCHAR(100) NOT NULL,
  -- Add other columns as needed
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Table structure for table `Classroom`
-- Table structure for table `Classroom`
DROP TABLE IF EXISTS `Classroom`;
CREATE TABLE `Classroom` (
  `classroom_id` INT NOT NULL AUTO_INCREMENT,
  `room_number` VARCHAR(10) NOT NULL,
  -- Add other columns as needed
  PRIMARY KEY (`classroom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
