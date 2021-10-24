DROP DATABASE IF EXISTS AUTONOMOUS_DRIVING_ASSISTANCE;

CREATE SCHEMA AUTONOMOUS_DRIVING_ASSISTANCE;
USE AUTONOMOUS_DRIVING_ASSISTANCE;

CREATE TABLE CAMERAS (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    Latitude DOUBLE NOT NULL,
    Longitude DOUBLE NOT NULL,
    XRotation DOUBLE NOT NULL,
    YRotation DOUBLE NOT NULL
);

CREATE TABLE CARS (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    CameraID INT NOT NULL,
    Latitude DOUBLE NOT NULL,
    Longitude DOUBLE NOT NULL,
    
    FOREIGN KEY (CameraID) REFERENCES CAMERAS(ID)
);

CREATE TABLE OBSTACLES (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    CameraID INT NOT NULL,
    Latitude DOUBLE NOT NULL,
    Longitude DOUBLE NOT NULL,
    
    FOREIGN KEY (CameraID) REFERENCES CAMERAS(ID)
);