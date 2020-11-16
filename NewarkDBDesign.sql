CREATE TABLE `flight` (
  `flight_id` int PRIMARY KEY AUTO_INCREMENT,
  `destination_id` varcharacter,
  `airline_id` int,
  `flight_number` varchar(255),
  `status` varchar(255)
);

CREATE TABLE `departure` (
  `flight_id` int PRIMARY KEY,
  `terminal` varchar(255),
  `gate` varchar(255),
  `estimated_hour` datetime,
  `real_hour` datetime
);

CREATE TABLE `arrival` (
  `flight_id` int PRIMARY KEY,
  `terminal` varchar(255),
  `gate` varchar(255),
  `estimated_hour` datetime,
  `real_hour` datetime
);

CREATE TABLE `airline` (
  `airline_id` int PRIMARY KEY AUTO_INCREMENT,
  `airline_name` varchar(255),
  `airline_shortname` varchar(255)
);

CREATE TABLE `destination` (
  `destination_id` int PRIMARY KEY AUTO_INCREMENT,
  `destination_name` varchar(255),
  `destination_short` varchar(255),
  `destination_site` varchar(255)
);

ALTER TABLE `departure` ADD FOREIGN KEY (`flight_id`) REFERENCES `flight` (`flight_id`);

ALTER TABLE `arrival` ADD FOREIGN KEY (`flight_id`) REFERENCES `flight` (`flight_id`);

ALTER TABLE `flight` ADD FOREIGN KEY (`airline_id`) REFERENCES `airline` (`airline_id`);

ALTER TABLE `flight` ADD FOREIGN KEY (`destination_id`) REFERENCES `destination` (`destination_id`);
