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
CREATE TABLE BookAuthors (
    BookID INT,
    AuthorID INT,
    PRIMARY KEY (BookID, AuthorID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
);
CREATE TABLE Members (
    MemberID INT PRIMARY KEY IDENTITY(1,1),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20),
    Address VARCHAR(255),
    MembershipDate DATE
);
CREATE TABLE Librarians (
    LibrarianID INT PRIMARY KEY IDENTITY(1,1),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20)
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
CREATE TABLE Fines (
    FineID INT PRIMARY KEY IDENTITY(1,1),
    ReservationID INT,
    Amount DECIMAL(10, 2),
    PaymentDate DATE,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID)
);
insert into Categories values('Fiction'),
('Non-Fiction'),('Science Fiction'),('Fantasy'),('Mystery'),('Thriller'),('Romance'),
('Historical'),('Biography'),('Self-Help'),('Health'),('Travel'),('Children’s'),('Young Adult'),
('Poetry'),('Drama'),('Horror'),('Science'),('Technology'),('Business');
select * from Categories;
select * from Books;
select * from Authors;
select * from BookAuthors;
select * from Fines;
select * from Members;
select * from Reservations;
select * from Members;

