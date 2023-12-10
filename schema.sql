CREATE TABLE department_information (
  Department_ID varchar(255) NOT NULL,
  Department_Name varchar(255) NOT NULL,
  Date_of_Est date,
  PRIMARY KEY (Department_ID));

CREATE TABLE student_information (
  Student_ID varchar(255) NOT NULL,
  Department_Admission varchar(255) ,
  Date_of_Birth date DEFAULT NULL,
  Date_of_Admission date DEFAULT NULL,
  PRIMARY KEY (Student_ID),
  FOREIGN KEY (Department_Admission) REFERENCES department_information(Department_ID));

CREATE TABLE student_performance_data (
  Student_Id varchar(255) DEFAULT NULL,
  Semster_Name text,
  Paper_ID text,
  Paper_Name text,
  Marks int(11) DEFAULT NULL,
  FOREIGN KEY (Student_Id) REFERENCES student_information (Student_ID));

CREATE TABLE users (
  user_name varchar(255) NOT NULL,
  user_password varchar(255) NOT NULL,
  admin boolean DEFAULT 0);

