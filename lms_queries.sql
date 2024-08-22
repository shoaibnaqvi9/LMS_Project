create database library;
use library;
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName VARCHAR(100)
);
CREATE TABLE Books (
    BookID INT PRIMARY KEY IDENTITY(1,1),
    Title VARCHAR(255) NOT NULL,
    ISBN VARCHAR(20) NOT NULL,
    Publisher VARCHAR(255),
    PublicationYear INT,
    CategoryID INT,
    Quantity INT,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);
CREATE TABLE Librarians (
    LibrarianID INT PRIMARY KEY IDENTITY(1,1),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20),
    Password VARCHAR(100),
    LibrariansAdmissionDate DATETIME
);
CREATE TABLE Students (
    S_ID INT PRIMARY KEY IDENTITY(1,1),
    S_FirstName VARCHAR(100),
    S_LastName VARCHAR(100),
    S_Email VARCHAR(255),
    S_Phone VARCHAR(20),
    S_address VARCHAR(255),
    S_AdmissionDate DATE
);
CREATE TABLE Reservations (
    R_ID INT PRIMARY KEY IDENTITY(1,1),
    BookID INT,
    S_ID INT,
    ReservationDate DATETIME,
    R_Status VARCHAR(20),
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (S_ID) REFERENCES Students(S_ID)
);
insert into Categories values('Fiction'),('Non-Fiction'),('Science Fiction'),('Fantasy'),('Mystery'),('Thriller'),('Romance'),
('Historical'),('Biography'),('Self-Help'),('Health'),('Travel'),('Children'),('Poetry'),('Drama'),('Horror'),('Science'),
('Technology'),('Business');

select * from Categories;
select * from Books;
select * from Librarians;
select * from Students;
select * from Reservations;
