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

/*
insert into Categories values('Fiction'),('Non-Fiction'),('Science Fiction'),('Fantasy'),('Mystery'),('Thriller'),('Romance'),
('Historical'),('Biography'),('Self-Help'),('Health'),('Travel'),('Children'),('Poetry'),('Drama'),('Horror'),('Science'),
('Technology'),('Business'),('Comic');
INSERT INTO Books (Title, ISBN, Publisher, PublicationYear, CategoryID, Quantity) 
VALUES
('The Midnight Library', '9780525559474', 'Chatto & Windus', 2020, 1, 12),
('Where the Crawdads Sing', '9780735219090', 'G.P. Putnams Sons', 2018, 7, 14),
('Normal People', '9781984822178', 'Hogarth', 2018, 1, 11),
('The Vanishing Half', '9780593135066', 'Riverhead Books', 2020, 1, 10),
('Educated', '9780399590504', 'Random House', 2018, 9, 15),
('The Silent Patient', '9781250301697', 'Celadon Books', 2019, 5, 9),
('Little Fires Everywhere', '9780735224292', 'Penguin Press', 2017, 1, 13),
('Circe', '9780316334754', 'Little, Brown and Company', 2018, 4, 12),
('The Night Circus', '9780307744432', 'Doubleday', 2011, 4, 11),
('The Girl on the Train', '9781594634024', 'Riverhead Books', 2015, 6, 10),
('Big Little Lies', '9780399167065', 'Penguin Books', 2014, 7, 14),
('The Goldfinch', '9780316055437', 'Little, Brown and Company', 2013, 1, 8),
('A Little Life', '9780804172707', 'Doubleday', 2015, 1, 9),
('The Underground Railroad', '9780425287138', 'Doubleday', 2016, 1, 11),
('The Water Dancer', '9780399590597', 'Riverhead Books', 2019, 1, 13),
('Such a Fun Age', '9780525541905', 'G.P. Putnams Sons', 2019, 1, 10),
('The Testaments', '9780385543773', 'Nan A. Talese', 2019, 1, 14),
('Becoming', '9781524763138', 'Crown Publishing Group', 2018, 9, 12),
('The Immortalists', '9780399590511', 'Riverrun', 2018, 1, 15),
('The 5th Wave', '9780399162411', 'G.P. Putnams Sons', 2013, 3, 10),
('Red, White & Royal Blue', '9781250316776', 'St. Martins Griffin', 2019, 7, 11),
('The Light We Lost', '9781501156507', 'Atria Books', 2017, 7, 9),
('An American Marriage', '9781616208768', 'Algonquin Books', 2018, 1, 12),
('The Paris Library', '9781984826213', 'Atria Books', 2021, 1, 8),
('Before We Were Strangers', '9781501100519', 'Atria Books', 2015, 7, 13),
('Homegoing', '9781101971062', 'Knopf', 2016, 1, 10),
('The Girl with the Louding Voice', '9780063086474', 'Dutton', 2020, 1, 15),
('The Henna Artist', '9780778308776', 'Park Row', 2020, 1, 12),
('Such a Fun Age', '9780525541905', 'G.P. Putnams Sons', 2019, 1, 11),
('The Chain', '9780316535855', 'Minotaur Books', 2019, 5, 14),
('The Huntress', '9780062560231', 'William Morrow', 2019, 5, 10),
('The Woman in the Window', '9784777880327', 'HarperCollins', 2018, 6, 9),
('Little Fires Everywhere', '9780735224285', 'Penguin Press', 2017, 1, 12),
('The Light We Lost', '9781501156507', 'Atria Books', 2017, 7, 11),
('The Tattooist of Auschwitz', '9781785038720', 'Zaffre', 2018, 1, 14),
('The Book Thief', '9780375842207', 'Alfred A. Knopf', 2005, 1, 10),
('The Dutch House', '9780062982681', 'HarperCollins', 2019, 1, 12),
('Watchmen', '9780930289232', 'DC Comics', 1986, 20, 12),
('Maus', '9780394747231', 'Pantheon Books', 1986, 20, 10),
('Sandman: Preludes & Nocturnes', '9781563890130', 'DC Comics', 1991, 20, 11),
('Batman: The Killing Joke', '9781401216672', 'DC Comics', 1988, 20, 8),
('V for Vendetta', '9781401206551', 'DC Comics', 1988, 20, 9),
('Saga Vol. 1', '9781607066019', 'Image Comics', 2012, 20, 15),
('The Walking Dead Vol. 1', '9781582402726', 'Image Comics', 2004, 20, 14),
('Persepolis', '9780375714573', 'Pantheon Books', 2003, 20, 13),
('The Avengers: Infinity Gauntlet', '9780785104030', 'Marvel Comics', 1991, 20, 11),
('Spider-Man: Blue', '9780785116416', 'Marvel Comics', 2002, 20, 10),
('X-Men: Days of Future Past', '9780785137380', 'Marvel Comics', 1981, 20, 12),
('Bone Vol. 1: Out from Boneville', '9781888963141', 'Cartoon Books', 1991, 20, 14),
('Akira Vol. 1', '9781934264070', 'Kodansha', 1984, 20, 9),
('One Piece Vol. 1', '9781421500094', 'Viz Media', 1999, 20, 16),
('Dragon Ball Vol. 1', '9781569319278', 'Viz Media', 1984, 20, 13),
('Naruto Vol. 1', '9781591161780', 'Viz Media', 2003, 20, 15),
('Death Note Vol. 1', '9781421501688', 'Viz Media', 2003, 20, 14),
('My Hero Academia Vol. 1', '9781612621770', 'Viz Media', 2014, 20, 13),
('Bleach Vol. 1', '9781591165580', 'Viz Media', 2002, 20, 12),
('Fullmetal Alchemist Vol. 1', '9781591169205', 'Viz Media', 2001, 20, 11),
('Attack on Titan Vol. 1', '9781612620247', 'Kodansha', 2009, 20, 16),
('JoJo’s Bizarre Adventure Vol. 1', '9781421530698', 'Viz Media', 1987, 20, 10),
('Inuyasha Vol. 1', '9781591161384', 'Viz Media', 1996, 20, 13),
('Dragon Ball Z Vol. 1', '9781569319001', 'Viz Media', 1996, 20, 14),
('Naruto Shippuden Vol. 1', '9781421513798', 'Viz Media', 2009, 20, 12),
('Attack on Titan: No Regrets Vol. 1', '9781612627611', 'Kodansha', 2014, 20, 11),
('Tokyo Ghoul Vol. 1', '9781421580254', 'Viz Media', 2014, 20, 15),
('Death Note: Another Note', '9781421506584', 'Viz Media', 2006, 20, 12),
('Hellsing Vol. 1', '9781593071782', 'Dark Horse Comics', 2001, 20, 10),
('Tokyo Revengers Vol. 1', '9781646511521', 'Kodansha', 2017, 20, 13);
*/
select * from Categories;
select * from Books;
select * from Librarians;
select * from Students;
select * from Reservations;
