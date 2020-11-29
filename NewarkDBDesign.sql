CREATE TABLE `all_flights` (
  `flight_id` INT PRIMARY KEY AUTO_INCREMENT,
  `City` VARCHAR(255),
  `Flight_number` VARCHAR(255),
  `Airline` VARCHAR(255),
  `Estimated_hour` VARCHAR(255),
  `Departure_Hour` VARCHAR(255),
  `Departure_Terminal` VARCHAR(255),
  `Departure_Gate` VARCHAR(255),
  `Arrival_Hour` VARCHAR(255),
  `Arrival_Terminal` VARCHAR(255),
  `Arrival_Gate` VARCHAR(255),
  `Status` VARCHAR(255),
  `Arrival_Departure` VARCHAR(255),
  `date` VARCHAR(255)
);

CREATE TABLE `flights` (
  `orig_ind` INT PRIMARY KEY,
  `flight_ind` INT,
  `flight_num` VARCHAR
);

CREATE TABLE `city` (
  `destination_id` INT PRIMARY KEY AUTO_INCREMENT,
  `city_name` VARCHAR(255),
  `city_short_name` VARCHAR(255)
);

ALTER TABLE `flights` ADD FOREIGN KEY (`flight_ind`) REFERENCES `all_flights` (`flight_id`);

ALTER TABLE `city` ADD FOREIGN KEY (`city_name`) REFERENCES `all_flights` (`City`);
