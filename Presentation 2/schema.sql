CREATE DATABASE IF NOT EXISTS harshitha_sports_club CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE harshitha_sports_club;


-- 1. MEMBERSHIP_PLAN
CREATE TABLE MEMBERSHIP_PLAN (
    Plan_ID INT PRIMARY KEY,
    Plan_Name VARCHAR(50),
    Duration INT,
    Fee_Amount DECIMAL(10,2),
    Description VARCHAR(100)
);

INSERT INTO MEMBERSHIP_PLAN VALUES
(1,'Basic',3,1500,'Basic Plan'),
(2,'Standard',6,2800,'Standard Plan'),
(3,'Premium',12,5000,'Premium Plan'),
(4,'Student',6,2000,'Student Plan'),
(5,'Gold',12,7000,'Gold Plan'),
(6,'Silver',6,3500,'Silver Plan'),
(7,'Family',12,9000,'Family Plan'),
(8,'Monthly',1,600,'Monthly Plan'),
(9,'Quarterly',3,1600,'Quarterly Plan'),
(10,'Annual',12,5500,'Annual Plan');


-- 2. MEMBER
CREATE TABLE MEMBER (
    Member_ID INT PRIMARY KEY,
    Name VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(10),
    Phone VARCHAR(15),
    Email VARCHAR(50),
    Address VARCHAR(100),
    Join_Date DATE,
    Status VARCHAR(20),
    Plan_ID INT,
    FOREIGN KEY (Plan_ID) REFERENCES MEMBERSHIP_PLAN(Plan_ID)
);

INSERT INTO MEMBER VALUES
(1,'Rahul','2004-05-12','Male','9876543210','rahul@gmail.com','Hyderabad','2026-01-10','Active',1),
(2,'Priya','2005-02-18','Female','9876543211','priya@gmail.com','Secunderabad','2026-01-15','Active',2),
(3,'Arjun','2003-08-20','Male','9876543212','arjun@gmail.com','Kukatpally','2026-02-01','Active',3),
(4,'Sneha','2004-11-10','Female','9876543213','sneha@gmail.com','Madhapur','2026-02-05','Active',4),
(5,'Kiran','2002-03-25','Male','9876543214','kiran@gmail.com','Gachibowli','2026-02-10','Active',5),
(6,'Anu','2005-06-14','Female','9876543215','anu@gmail.com','Miyapur','2026-03-01','Active',6),
(7,'Vivek','2003-09-17','Male','9876543216','vivek@gmail.com','Ameerpet','2026-03-05','Active',7),
(8,'Divya','2004-12-22','Female','9876543217','divya@gmail.com','Begumpet','2026-03-10','Active',8),
(9,'Rohan','2002-07-08','Male','9876543218','rohan@gmail.com','Banjara Hills','2026-03-15','Inactive',9),
(10,'Meena','2005-01-30','Female','9876543219','meena@gmail.com','Kondapur','2026-03-20','Active',10);


-- 3. PAYMENT
CREATE TABLE PAYMENT (
    Payment_ID INT PRIMARY KEY,
    Payment_Date DATE,
    Amount DECIMAL(10,2),
    Remarks VARCHAR(100),
    Mode VARCHAR(20),
    Member_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES MEMBER(Member_ID)
);

INSERT INTO PAYMENT VALUES
(1,'2026-01-10',1500,'Membership Fee','Cash',1),
(2,'2026-01-15',2800,'Membership Fee','UPI',2),
(3,'2026-02-01',5000,'Membership Fee','Card',3),
(4,'2026-02-05',2000,'Membership Fee','UPI',4),
(5,'2026-02-10',7000,'Membership Fee','Card',5),
(6,'2026-03-01',3500,'Membership Fee','Cash',6),
(7,'2026-03-05',9000,'Membership Fee','UPI',7),
(8,'2026-03-10',600,'Monthly Fee','Cash',8),
(9,'2026-03-15',1600,'Membership Fee','UPI',9),
(10,'2026-03-20',5500,'Membership Fee','Card',10);


-- 4. SPORT
CREATE TABLE SPORT (
    Sport_ID INT PRIMARY KEY,
    Sport_Name VARCHAR(50),
    Description VARCHAR(100)
);

INSERT INTO SPORT VALUES
(1,'Cricket','Outdoor Sport'),
(2,'Football','Team Sport'),
(3,'Basketball','Indoor Sport'),
(4,'Tennis','Racket Sport'),
(5,'Badminton','Racket Sport'),
(6,'Volleyball','Team Sport'),
(7,'Swimming','Water Sport'),
(8,'Table Tennis','Indoor Sport'),
(9,'Athletics','Track Sport'),
(10,'Kabaddi','Team Sport');


-- 5. MEMBER_SPORT
CREATE TABLE MEMBER_SPORT (
    Member_ID INT,
    Sport_ID INT,
    PRIMARY KEY (Member_ID,Sport_ID),
    FOREIGN KEY (Member_ID) REFERENCES MEMBER(Member_ID),
    FOREIGN KEY (Sport_ID) REFERENCES SPORT(Sport_ID)
);

INSERT INTO MEMBER_SPORT VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(6,6),
(7,7),
(8,8),
(9,9),
(10,10);


-- 6. COACH
CREATE TABLE COACH (
    Coach_ID INT PRIMARY KEY,
    Coach_Name VARCHAR(50),
    Phone VARCHAR(15),
    Email VARCHAR(50),
    Experience INT
);

INSERT INTO COACH VALUES
(1,'Ramesh','9000000001','ramesh@gmail.com',8),
(2,'Suresh','9000000002','suresh@gmail.com',6),
(3,'Mahesh','9000000003','mahesh@gmail.com',10),
(4,'Raj','9000000004','raj@gmail.com',7),
(5,'Karthik','9000000005','karthik@gmail.com',5),
(6,'Anil','9000000006','anil@gmail.com',9),
(7,'Vijay','9000000007','vijay@gmail.com',12),
(8,'Ajay','9000000008','ajay@gmail.com',4),
(9,'Ravi','9000000009','ravi@gmail.com',11),
(10,'Mohan','9000000010','mohan@gmail.com',6);


-- 7. TEAM
CREATE TABLE TEAM (
    Team_ID INT PRIMARY KEY,
    Team_Name VARCHAR(50),
    Sport_ID INT,
    Coach_ID INT,
    FOREIGN KEY (Sport_ID) REFERENCES SPORT(Sport_ID),
    FOREIGN KEY (Coach_ID) REFERENCES COACH(Coach_ID)
);

INSERT INTO TEAM VALUES
(1,'Warriors',1,1),
(2,'FC Stars',2,2),
(3,'Hoopers',3,3),
(4,'Ace Team',4,4),
(5,'Smashers',5,5),
(6,'Volley Stars',6,6),
(7,'Aqua Team',7,7),
(8,'Table Kings',8,8),
(9,'Speed Runners',9,9),
(10,'Kabaddi Kings',10,10);


-- 8. FACILITY
CREATE TABLE FACILITY (
    Facility_ID INT PRIMARY KEY,
    Facility_Name VARCHAR(50),
    Location VARCHAR(50),
    Type VARCHAR(30),
    Availability VARCHAR(20)
);

INSERT INTO FACILITY VALUES
(1,'Cricket Ground','Block A','Ground','Available'),
(2,'Football Ground','Block B','Ground','Available'),
(3,'Basketball Court','Block C','Court','Available'),
(4,'Tennis Court','Block D','Court','Available'),
(5,'Badminton Court','Block E','Court','Available'),
(6,'Volleyball Court','Block F','Court','Available'),
(7,'Swimming Pool','Block G','Pool','Available'),
(8,'Table Tennis Hall','Block H','Hall','Available'),
(9,'Athletics Track','Block I','Track','Available'),
(10,'Kabaddi Ground','Block J','Ground','Available');


-- 9. TRAINING_SESSION
CREATE TABLE TRAINING_SESSION (
    Session_ID INT PRIMARY KEY,
    Session_Date DATE,
    Start_Time TIME,
    End_Time TIME,
    Team_ID INT,
    Facility_ID INT,
    FOREIGN KEY (Team_ID) REFERENCES TEAM(Team_ID),
    FOREIGN KEY (Facility_ID) REFERENCES FACILITY(Facility_ID)
);

INSERT INTO TRAINING_SESSION VALUES
(1,'2026-09-01','09:00:00','11:00:00',1,1),
(2,'2026-09-02','10:00:00','12:00:00',2,2),
(3,'2026-09-03','09:00:00','11:00:00',3,3),
(4,'2026-09-04','10:00:00','12:00:00',4,4),
(5,'2026-09-05','09:00:00','11:00:00',5,5),
(6,'2026-09-06','10:00:00','12:00:00',6,6),
(7,'2026-09-07','08:00:00','10:00:00',7,7),
(8,'2026-09-08','09:00:00','11:00:00',8,8),
(9,'2026-09-09','07:00:00','09:00:00',9,9),
(10,'2026-09-10','10:00:00','12:00:00',10,10);


-- 10. TOURNAMENT
CREATE TABLE TOURNAMENT (
    Tournament_ID INT PRIMARY KEY,
    Tournament_Name VARCHAR(50),
    Sport_ID INT,
    Start_Date DATE,
    End_Date DATE,
    Description VARCHAR(100),
    FOREIGN KEY (Sport_ID) REFERENCES SPORT(Sport_ID)
);

INSERT INTO TOURNAMENT VALUES
(1,'Cricket Cup',1,'2026-10-01','2026-10-05','Cricket Tournament'),
(2,'Football League',2,'2026-10-06','2026-10-10','Football Tournament'),
(3,'Basketball Cup',3,'2026-10-11','2026-10-15','Basketball Tournament'),
(4,'Tennis Open',4,'2026-10-16','2026-10-20','Tennis Tournament'),
(5,'Badminton Cup',5,'2026-10-21','2026-10-25','Badminton Tournament'),
(6,'Volleyball League',6,'2026-10-26','2026-10-30','Volleyball Tournament'),
(7,'Swimming Meet',7,'2026-11-01','2026-11-03','Swimming Tournament'),
(8,'Table Tennis Cup',8,'2026-11-04','2026-11-06','Table Tennis Tournament'),
(9,'Athletics Meet',9,'2026-11-07','2026-11-09','Athletics Tournament'),
(10,'Kabaddi Cup',10,'2026-11-10','2026-11-15','Kabaddi Tournament');


-- 11. PARTICIPANT
CREATE TABLE PARTICIPANT (
    Participant_ID INT PRIMARY KEY,
    Tournament_ID INT,
    Member_ID INT,
    Team_ID INT,
    Role VARCHAR(30),
    FOREIGN KEY (Tournament_ID) REFERENCES TOURNAMENT(Tournament_ID),
    FOREIGN KEY (Member_ID) REFERENCES MEMBER(Member_ID),
    FOREIGN KEY (Team_ID) REFERENCES TEAM(Team_ID)
);

INSERT INTO PARTICIPANT VALUES
(1,1,1,1,'Player'),
(2,2,2,2,'Player'),
(3,3,3,3,'Player'),
(4,4,4,4,'Player'),
(5,5,5,5,'Player'),
(6,6,6,6,'Player'),
(7,7,7,7,'Player'),
(8,8,8,8,'Player'),
(9,9,9,9,'Player'),
(10,10,10,10,'Player');


-- 12. FIXTURE
CREATE TABLE FIXTURE (
    Fixture_ID INT PRIMARY KEY,
    Fixture_Date DATE,
    Time TIME,
    Venue VARCHAR(50),
    Tournament_ID INT,
    FOREIGN KEY (Tournament_ID) REFERENCES TOURNAMENT(Tournament_ID)
);

INSERT INTO FIXTURE VALUES
(1,'2026-10-01','10:00:00','Ground 1',1),
(2,'2026-10-06','10:00:00','Ground 2',2),
(3,'2026-10-11','11:00:00','Court 1',3),
(4,'2026-10-16','11:00:00','Court 2',4),
(5,'2026-10-21','10:00:00','Court 3',5),
(6,'2026-10-26','10:00:00','Court 4',6),
(7,'2026-11-01','09:00:00','Pool 1',7),
(8,'2026-11-04','10:00:00','Hall 1',8),
(9,'2026-11-07','08:00:00','Track 1',9),
(10,'2026-11-10','10:00:00','Ground 3',10);


-- 13. RESULT
CREATE TABLE RESULT (
    Result_ID INT PRIMARY KEY,
    Home_Score INT,
    Away_Score INT,
    Winner VARCHAR(50),
    Remarks VARCHAR(100),
    Fixture_ID INT,
    FOREIGN KEY (Fixture_ID) REFERENCES FIXTURE(Fixture_ID)
);

INSERT INTO RESULT VALUES
(1,120,110,'Warriors','Good Match',1),
(2,2,1,'FC Stars','Close Match',2),
(3,80,75,'Hoopers','Good Match',3),
(4,6,4,'Ace Team','Good Match',4),
(5,21,18,'Smashers','Close Match',5),
(6,3,2,'Volley Stars','Close Match',6),
(7,5,3,'Aqua Team','Good Match',7),
(8,11,9,'Table Kings','Good Match',8),
(9,10,8,'Speed Runners','Good Match',9),
(10,25,20,'Kabaddi Kings','Close Match',10);


-- 14. EQUIPMENT
CREATE TABLE EQUIPMENT (
    Equipment_ID INT PRIMARY KEY,
    Equipment_Name VARCHAR(50),
    Category VARCHAR(50),
    Quantity INT
);

INSERT INTO EQUIPMENT VALUES
(1,'Cricket Bat','Cricket',20),
(2,'Football','Football',15),
(3,'Basketball','Basketball',15),
(4,'Tennis Racket','Tennis',20),
(5,'Badminton Racket','Badminton',25),
(6,'Volleyball','Volleyball',15),
(7,'Swimming Goggles','Swimming',20),
(8,'Table Tennis Bat','Table Tennis',20),
(9,'Running Shoes','Athletics',30),
(10,'Kabaddi Shoes','Kabaddi',20);


-- 15. EQUIPMENT_ISSUE
CREATE TABLE EQUIPMENT_ISSUE (
    Issue_ID INT PRIMARY KEY,
    Issue_Date DATE,
    Return_Date DATE,
    `Condition` VARCHAR(30),
    Member_ID INT,
    Equipment_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES MEMBER(Member_ID),
    FOREIGN KEY (Equipment_ID) REFERENCES EQUIPMENT(Equipment_ID)
);

INSERT INTO EQUIPMENT_ISSUE VALUES
(1,'2026-09-01','2026-09-02','Good',1,1),
(2,'2026-09-02','2026-09-03','Good',2,2),
(3,'2026-09-03','2026-09-04','Good',3,3),
(4,'2026-09-04','2026-09-05','Good',4,4),
(5,'2026-09-05','2026-09-06','Good',5,5),
(6,'2026-09-06','2026-09-07','Good',6,6),
(7,'2026-09-07','2026-09-08','Good',7,7),
(8,'2026-09-08','2026-09-09','Good',8,8),
(9,'2026-09-09','2026-09-10','Good',9,9),
(10,'2026-09-10','2026-09-11','Good',10,10);