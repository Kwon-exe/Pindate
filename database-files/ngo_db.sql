DROP DATABASE IF EXISTS pindate;
CREATE DATABASE IF NOT EXISTS pindate;
USE pindate;


CREATE TABLE Users (
   accountId   INT             NOT NULL AUTO_INCREMENT,
   email       VARCHAR(255)    NOT NULL UNIQUE,
   pwdHash     VARCHAR(255)    NOT NULL,
   firstName   VARCHAR(100)    NOT NULL,
   lastName    VARCHAR(100)    NOT NULL,
   username    VARCHAR(100)    NOT NULL UNIQUE,
   phoneNum    VARCHAR(20),
   city        VARCHAR(100),
   role        VARCHAR(50)     NOT NULL DEFAULT 'CUSTOMER',
   createdAt   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (accountId),
   CONSTRAINT chk_account_role CHECK (role IN ('CUSTOMER', 'VENUE_OWNER', 'ADMIN', 'DATA_ANALYST'))
);




CREATE TABLE Category (
   categoryId  INT             NOT NULL AUTO_INCREMENT,
   name        VARCHAR(100)    NOT NULL UNIQUE,
   PRIMARY KEY (categoryId)
);


INSERT INTO Category (name) VALUES
   ('Restaurant'), ('Bar'), ('Cafe'), ('Lounge'), ('Club'),
   ('Park'), ('Museum'), ('Theater'), ('Arcade'), ('Rooftop');




CREATE TABLE Vibe (
   vibeId      INT             NOT NULL AUTO_INCREMENT,
   name        VARCHAR(100)    NOT NULL UNIQUE,
   PRIMARY KEY (vibeId)
);


INSERT INTO Vibe (name) VALUES
   ('Romantic'), ('Casual'), ('Upscale'), ('Cozy'), ('Lively'),
   ('Chill'), ('Adventurous'), ('Artsy'), ('Trendy'), ('Intimate');




CREATE TABLE Venues (
   venueId     INT             NOT NULL AUTO_INCREMENT,
   ownerId     INT,
   name        VARCHAR(255)    NOT NULL,
   description TEXT,
   address     VARCHAR(255)    NOT NULL,
   city        VARCHAR(100)    NOT NULL,
   phoneNum    VARCHAR(20),
   rating      NUMERIC(3, 2),
   minPrice    NUMERIC(10, 2),
   maxPrice    NUMERIC(10, 2),
   PRIMARY KEY (venueId),
   CONSTRAINT chk_venue_rating CHECK (rating >= 0 AND rating <= 5),
   CONSTRAINT chk_venue_price  CHECK (minPrice <= maxPrice),
   CONSTRAINT fk_venue_owner   FOREIGN KEY (ownerId) REFERENCES Users(accountId)
);




CREATE TABLE VenueCategory (
   venueId     INT             NOT NULL,
   categoryId  INT             NOT NULL,
   PRIMARY KEY (venueId, categoryId),
   CONSTRAINT fk_venuecategory_venue     FOREIGN KEY (venueId)    REFERENCES Venues(venueId),
   CONSTRAINT fk_venuecategory_category  FOREIGN KEY (categoryId) REFERENCES Category(categoryId)
);




CREATE TABLE VenueVibe (
   venueId     INT             NOT NULL,
   vibeId      INT             NOT NULL,
   PRIMARY KEY (venueId, vibeId),
   CONSTRAINT fk_venuevibe_venue FOREIGN KEY (venueId) REFERENCES Venues(venueId),
   CONSTRAINT fk_venuevibe_vibe  FOREIGN KEY (vibeId)  REFERENCES Vibe(vibeId)
);




CREATE TABLE Reviews (
   reviewId    INT             NOT NULL AUTO_INCREMENT,
   userId      INT             NOT NULL,
   venueId     INT             NOT NULL,
   comment     TEXT,
   rating      NUMERIC(3, 2)   NOT NULL,
   isFlagged   BOOLEAN         NOT NULL DEFAULT FALSE,
   createdAt   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (reviewId),
   CONSTRAINT chk_review_rating CHECK (rating >= 0 AND rating <= 5),
   CONSTRAINT fk_review_user    FOREIGN KEY (userId)  REFERENCES Users(accountId),
   CONSTRAINT fk_review_venue   FOREIGN KEY (venueId) REFERENCES Venues(venueId)
);




CREATE TABLE Posts (
   postId      INT             NOT NULL AUTO_INCREMENT,
   ownerId     INT             NOT NULL,
   venueId     INT             NOT NULL,
   content     TEXT            NOT NULL,
   postDate    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (postId),
   CONSTRAINT fk_post_owner FOREIGN KEY (ownerId) REFERENCES Users(accountId),
   CONSTRAINT fk_post_venue FOREIGN KEY (venueId) REFERENCES Venues(venueId)
);




CREATE TABLE Lists (
   listId      INT             NOT NULL AUTO_INCREMENT,
   userId      INT             NOT NULL,
   name        VARCHAR(255)    NOT NULL,
   PRIMARY KEY (listId),
   CONSTRAINT fk_list_user FOREIGN KEY (userId) REFERENCES Users(accountId)
);




CREATE TABLE ListVenue (
   listId      INT             NOT NULL,
   venueId     INT             NOT NULL,
   PRIMARY KEY (listId, venueId),
   CONSTRAINT fk_listvenue_list  FOREIGN KEY (listId)  REFERENCES Lists(listId),
   CONSTRAINT fk_listvenue_venue FOREIGN KEY (venueId) REFERENCES Venues(venueId)
);




CREATE TABLE SavedVenues (
   userId      INT             NOT NULL,
   venueId     INT             NOT NULL,
   savedAt     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (userId, venueId),
   CONSTRAINT fk_savedvenues_user  FOREIGN KEY (userId)  REFERENCES Users(accountId),
   CONSTRAINT fk_savedvenues_venue FOREIGN KEY (venueId) REFERENCES Venues(venueId)
);




CREATE TABLE VenueApplications (
   applicationId   INT             NOT NULL AUTO_INCREMENT,
   ownerId         INT,
   name            VARCHAR(255)    NOT NULL,
   description     TEXT,
   address         VARCHAR(255)    NOT NULL,
   phone           VARCHAR(20),
   minPrice        NUMERIC(10, 2),
   maxPrice        NUMERIC(10, 2),
   createdAt       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   status          VARCHAR(50)     NOT NULL DEFAULT 'PENDING',
   PRIMARY KEY (applicationId),
   CONSTRAINT chk_app_status CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
   CONSTRAINT chk_app_price  CHECK (minPrice <= maxPrice),
   CONSTRAINT fk_app_owner   FOREIGN KEY (ownerId) REFERENCES Users(accountId)
);




CREATE TABLE ReportTickets (
   reportId    INT             NOT NULL AUTO_INCREMENT,
   reporterId  INT,
   reviewId    INT,
   description TEXT,
   reason      VARCHAR(255)    NOT NULL,
   createdAt   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   status      VARCHAR(50)     NOT NULL DEFAULT 'PENDING',
   PRIMARY KEY (reportId),
   CONSTRAINT chk_ticket_status  CHECK (status IN ('PENDING', 'UNDER REVIEW', 'RESOLVED', 'DISMISSED')),
   CONSTRAINT fk_report_reporter FOREIGN KEY (reporterId) REFERENCES Users(accountId),
   CONSTRAINT fk_report_review   FOREIGN KEY (reviewId)   REFERENCES Reviews(reviewId)
);




CREATE TABLE AdminLog (
   logId       INT             NOT NULL AUTO_INCREMENT,
   appId       INT,
   reportId    INT,
   adminId     INT             NOT NULL,
   action      VARCHAR(255)    NOT NULL,
   targetTable VARCHAR(100),
   targetId    INT,
   performedAt TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
   notes       TEXT,
   PRIMARY KEY (logId),
   CONSTRAINT fk_adminlog_app    FOREIGN KEY (appId)    REFERENCES VenueApplications(applicationId),
   CONSTRAINT fk_adminlog_report FOREIGN KEY (reportId) REFERENCES ReportTickets(reportId),
   CONSTRAINT fk_adminlog_admin  FOREIGN KEY (adminId)  REFERENCES Users(accountId)
);


INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, city, role) VALUES
   ('maya.chen@email.com',   '$2b$12$abc123', 'Maya',  'Chen',  'mayac',   '617-555-0101', 'Boston',    'CUSTOMER'),
   ('james.park@email.com',  '$2b$12$def456', 'James', 'Park',  'jpark99', '617-555-0102', 'Cambridge', 'CUSTOMER'),
   ('sofia.reyes@email.com', '$2b$12$ghi789', 'Sofia', 'Reyes', 'sofiaar', '617-555-0103', 'Somerville','CUSTOMER');


-- Venue Owners (role = 'VENUE_OWNER')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, role) VALUES
   ('marcus.r@venues.com',    '$2b$12$own111', 'Marcus', 'Rivera', 'marcusr_owner', '617-555-0201', 'VENUE_OWNER'),
   ('priya.sharma@venues.com','$2b$12$own222', 'Priya',  'Sharma', 'priyas_owner',  '617-555-0202', 'VENUE_OWNER'),
   ('carlos.m@venues.com',    '$2b$12$own333', 'Carlos', 'Mendez', 'carlosm_owner', '617-555-0203', 'VENUE_OWNER');


-- Admins (role = 'ADMIN')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, role) VALUES
   ('admin1@pindate.com', '$2b$12$adm111', 'Josh', 'Doe',    'joshd_admin', 'ADMIN'),
   ('admin2@pindate.com', '$2b$12$adm222', 'Tom',  'Nguyen', 'tomn_admin',  'ADMIN');


-- Data Analysts (role = 'DATA_ANALYST')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, city, role) VALUES
   ('analyst1@pindate.com', '$2b$12$da111', 'Nadia',  'Patel', 'nadiap_data', '617-555-0501', 'Boston',    'DATA_ANALYST'),
   ('analyst2@pindate.com', '$2b$12$da222', 'Marcus', 'Owens', 'marcuso_da',  '617-555-0502', 'Cambridge', 'DATA_ANALYST');




INSERT INTO Venues (ownerId, name, description, address, city, phoneNum, rating, minPrice, maxPrice) VALUES
   (4, 'Rooftop Lantern',    'A rooftop bar with stunning Boston skyline views.',        '123 High St', 'Boston',    '617-555-0301', 4.50, 20.00, 80.00),
   (5, 'The Cozy Corner',    'A warm cafe perfect for intimate dates and great coffee.', '456 Elm Ave',  'Cambridge', '617-555-0302', 4.20,  5.00, 30.00),
   (6, 'Neon Arcade Lounge', 'Retro arcade games paired with craft cocktails.',          '789 Main St', 'Somerville','617-555-0303', 4.70, 10.00, 50.00);


INSERT INTO VenueCategory (venueId, categoryId) VALUES
   (1, 2), (1, 10), (2, 3), (3, 9), (3, 4);


INSERT INTO VenueVibe (venueId, vibeId) VALUES
   (1, 1), (1, 3), (2, 4), (2, 10), (3, 5), (3, 7);


INSERT INTO Reviews (userId, venueId, comment, rating, isFlagged) VALUES
   (1, 1, 'Absolutely stunning views, perfect for a date night!',        4.80, FALSE),
   (2, 2, 'Such a cozy spot. The lattes are amazing.',                   4.20, FALSE),
   (3, 3, 'So much fun — the retro games made the night unforgettable.', 4.70, FALSE);


INSERT INTO Posts (ownerId, venueId, content) VALUES
   (4, 1, 'Join us this Friday for live jazz under the stars! Reserve your table now.'),
   (5, 2, 'New seasonal menu is here — try our maple oat latte while it lasts!'),
   (6, 3, 'Double tokens every Tuesday night. Bring your date for double the fun!');


INSERT INTO Lists (userId, name) VALUES
   (1, 'Dream Date Spots'),
   (2, 'Boston Favorites'),
   (3, 'Weekend Plans');


INSERT INTO ListVenue (listId, venueId) VALUES
   (1, 1), (1, 2), (2, 3), (3, 1);


INSERT INTO SavedVenues (userId, venueId) VALUES
   (1, 3), (2, 1), (3, 2);


INSERT INTO VenueApplications (ownerId, name, description, address, phone, minPrice, maxPrice, status) VALUES
   (4, 'Sky Garden',   'An outdoor terrace dining experience.',     '321 Cloud Blvd, Boston, MA',     '617-555-0401', 30.00, 100.00, 'PENDING'),
   (5, 'Brew & Books', 'A bookstore cafe hybrid with craft beers.', '654 Page St, Cambridge, MA',     '617-555-0402',  8.00,  40.00, 'APPROVED'),
   (6, 'Pixel Palace', 'Next-gen VR arcade and bar.',               '987 Circuit Ave, Somerville, MA','617-555-0403', 15.00,  60.00, 'REJECTED');


INSERT INTO ReportTickets (reporterId, reviewId, description, reason, status) VALUES
   (2, 1,    'This review seems fake and overly promotional.', 'Suspected fake review', 'PENDING'),
   (3, 2,    'Review contains inappropriate language.',        'Inappropriate content', 'RESOLVED'),
   (1, NULL, 'Venue owner sent unsolicited messages.',         'Harassment',            'RESOLVED');


INSERT INTO AdminLog (appId, reportId, adminId, action, targetTable, targetId, notes) VALUES
   (2,    NULL, 7, 'APPROVED_APPLICATION', 'VenueApplications', 2, 'All documents verified, application looks legitimate.'),
   (3,    NULL, 8, 'REJECTED_APPLICATION', 'VenueApplications', 3, 'Location not within supported service area.'),
   (NULL, 1,    7, 'FLAGGED_REVIEW',       'Reviews',           1, 'Flagged for further investigation by moderation team.');
