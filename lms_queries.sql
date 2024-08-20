create database library

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
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY IDENTITY(1,1),
    FirstName VARCHAR(100),
    LastName VARCHAR(100)
);
CREATE TABLE Users (
    U_ID INT PRIMARY KEY IDENTITY(1,1),
    U_FirstName VARCHAR(100),
    U_LastName VARCHAR(100),
    U_Email VARCHAR(255),
    U_Phone VARCHAR(20),
    U_address VARCHAR(255),
    UserAdmissionDate DATE
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
CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY IDENTITY(1,1),
    BookID INT,
    MemberID INT,
    ReservationDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);
insert into Categories values('Fiction'),
('Non-Fiction'),('Science Fiction'),('Fantasy'),('Mystery'),('Thriller'),('Romance'),
('Historical'),('Biography'),('Self-Help'),('Health'),('Travel'),('Children’s'),('Young Adult'),
('Poetry'),('Drama'),('Horror'),('Science'),('Technology'),('Business');
select * from Categories;
select * from Books;
select * from Librarians;
select * from Authors;
select * from Reservations;
select * from Members;

