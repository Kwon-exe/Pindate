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


-- ============================================================
-- USERS (40 total: 25 customers, 8 venue owners, 3 admins, 4 data analysts)
-- accountIds 1-25 = CUSTOMER, 26-33 = VENUE_OWNER, 34-36 = ADMIN, 37-40 = DATA_ANALYST
-- ============================================================
 
INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, city, role) VALUES
   ('maya.chen@email.com',     'password', 'Maya',     'Chen',      'mayac',     '617-555-0101', 'Boston',      'CUSTOMER'),
   ('james.park@email.com',    'password', 'James',    'Park',      'jpark99',   '617-555-0102', 'Cambridge',   'CUSTOMER'),
   ('sofia.reyes@email.com',   'password', 'Sofia',    'Reyes',     'sofiaar',   '617-555-0103', 'Somerville',  'CUSTOMER'),
   ('ethan.nguyen@email.com',  'password', 'Ethan',    'Nguyen',    'ethann',    '617-555-0104', 'Boston',      'CUSTOMER'),
   ('olivia.brooks@email.com', 'password', 'Olivia',   'Brooks',    'liv_b',     '617-555-0105', 'Brookline',   'CUSTOMER'),
   ('noah.patel@email.com',    'password', 'Noah',     'Patel',     'noahp',     '617-555-0106', 'Cambridge',   'CUSTOMER'),
   ('ava.martinez@email.com',  'password', 'Ava',      'Martinez',  'avam',      '617-555-0107', 'Allston',     'CUSTOMER'),
   ('liam.obrien@email.com',   'password', 'Liam',     'OBrien',    'liamob',    '617-555-0108', 'Boston',      'CUSTOMER'),
   ('isabella.kim@email.com',  'password', 'Isabella', 'Kim',       'bellak',    '617-555-0109', 'Cambridge',   'CUSTOMER'),
   ('mason.wright@email.com',  'password', 'Mason',    'Wright',    'masonw',    '617-555-0110', 'Somerville',  'CUSTOMER'),
   ('zoe.thompson@email.com',  'password', 'Zoe',      'Thompson',  'zoet',      '617-555-0111', 'Boston',      'CUSTOMER'),
   ('lucas.fisher@email.com',  'password', 'Lucas',    'Fisher',    'lucasf',    '617-555-0112', 'Brookline',   'CUSTOMER'),
   ('amelia.hughes@email.com', 'password', 'Amelia',   'Hughes',    'ameliah',   '617-555-0113', 'Cambridge',   'CUSTOMER'),
   ('daniel.ortiz@email.com',  'password', 'Daniel',   'Ortiz',     'danielo',   '617-555-0114', 'Boston',      'CUSTOMER'),
   ('harper.singh@email.com',  'password', 'Harper',   'Singh',     'harpers',   '617-555-0115', 'Somerville',  'CUSTOMER'),
   ('elijah.cohen@email.com',  'password', 'Elijah',   'Cohen',     'elijahc',   '617-555-0116', 'Allston',     'CUSTOMER'),
   ('mia.walker@email.com',    'password', 'Mia',      'Walker',    'miaw',      '617-555-0117', 'Boston',      'CUSTOMER'),
   ('henry.lopez@email.com',   'password', 'Henry',    'Lopez',     'henryl',    '617-555-0118', 'Cambridge',   'CUSTOMER'),
   ('charlotte.ali@email.com', 'password', 'Charlotte','Ali',       'charla',    '617-555-0119', 'Brookline',   'CUSTOMER'),
   ('benjamin.yu@email.com',   'password', 'Benjamin', 'Yu',        'benyu',     '617-555-0120', 'Boston',      'CUSTOMER'),
   ('ella.ramirez@email.com',  'password', 'Ella',     'Ramirez',   'ellar',     '617-555-0121', 'Somerville',  'CUSTOMER'),
   ('oliver.clark@email.com',  'password', 'Oliver',   'Clark',     'oliverc',   '617-555-0122', 'Boston',      'CUSTOMER'),
   ('lily.adams@email.com',    'password', 'Lily',     'Adams',     'lilya',     '617-555-0123', 'Cambridge',   'CUSTOMER'),
   ('jackson.ito@email.com',   'password', 'Jackson',  'Ito',       'jacksoni',  '617-555-0124', 'Allston',     'CUSTOMER'),
   ('grace.morris@email.com',  'password', 'Grace',    'Morris',    'gracem',    '617-555-0125', 'Boston',      'CUSTOMER');
 
 
-- Venue Owners (role = 'VENUE_OWNER')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, role) VALUES
   ('marcus.r@venues.com',     'password', 'Marcus',   'Rivera',   'marcusr_owner', '617-555-0201', 'VENUE_OWNER'),
   ('priya.sharma@venues.com', 'password', 'Priya',    'Sharma',   'priyas_owner',  '617-555-0202', 'VENUE_OWNER'),
   ('carlos.m@venues.com',     'password', 'Carlos',   'Mendez',   'carlosm_owner', '617-555-0203', 'VENUE_OWNER'),
   ('rachel.goldberg@venues.com','password','Rachel',  'Goldberg', 'rachelg_owner', '617-555-0204', 'VENUE_OWNER'),
   ('dimitri.volkov@venues.com','password','Dimitri',  'Volkov',   'dimitriv_owner','617-555-0205', 'VENUE_OWNER'),
   ('amara.okafor@venues.com', 'password', 'Amara',    'Okafor',   'amarao_owner',  '617-555-0206', 'VENUE_OWNER'),
   ('hiroshi.tanaka@venues.com','password','Hiroshi',  'Tanaka',   'hiroshit_owner','617-555-0207', 'VENUE_OWNER'),
   ('gabriela.silva@venues.com','password','Gabriela', 'Silva',    'gabrielas_owner','617-555-0208','VENUE_OWNER');
 
 
-- Admins (role = 'ADMIN')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, role) VALUES
   ('admin1@pindate.com', 'password', 'Josh',    'Doe',    'joshd_admin',    'ADMIN'),
   ('admin2@pindate.com', 'password', 'Tom',     'Nguyen', 'tomn_admin',     'ADMIN'),
   ('admin3@pindate.com', 'password', 'Rebecca', 'Stone',  'rebeccas_admin', 'ADMIN');
 
 
-- Data Analysts (role = 'DATA_ANALYST')
INSERT INTO Users (email, pwdHash, firstName, lastName, username, phoneNum, city, role) VALUES
   ('analyst1@pindate.com', 'password', 'Nadia',   'Patel',  'nadiap_data',  '617-555-0501', 'Boston',    'DATA_ANALYST'),
   ('analyst2@pindate.com', 'password', 'Marcus',  'Owens',  'marcuso_da',   '617-555-0502', 'Cambridge', 'DATA_ANALYST'),
   ('analyst3@pindate.com', 'password', 'Jasmine', 'Wu',     'jasminew_da',  '617-555-0503', 'Boston',    'DATA_ANALYST'),
   ('analyst4@pindate.com', 'password', 'Derek',   'Bishop', 'derekb_da',    '617-555-0504', 'Somerville','DATA_ANALYST');
 
 
-- ============================================================
-- VENUES (35 total) - realistic Boston/Cambridge/Somerville/Brookline/Allston spots
-- Owner IDs 26-33
-- ============================================================
 
INSERT INTO Venues (ownerId, name, description, address, city, phoneNum, rating, minPrice, maxPrice) VALUES
   (26, 'Rooftop Lantern',       'A rooftop bar with stunning Boston skyline views.',                '123 High St',        'Boston',     '617-555-0301', 4.50, 20.00, 80.00),
   (27, 'The Cozy Corner',       'A warm cafe perfect for intimate dates and great coffee.',         '456 Elm Ave',        'Cambridge',  '617-555-0302', 4.20,  5.00, 30.00),
   (28, 'Neon Arcade Lounge',    'Retro arcade games paired with craft cocktails.',                  '789 Main St',        'Somerville', '617-555-0303', 4.70, 10.00, 50.00),
   (26, 'Harbor House Rooftop',  'Waterfront dining with skyline views and date-night menus.',       '18 Seaport Blvd',    'Boston',     '617-555-0304', 4.80, 25.00, 90.00),
   (27, 'Velvet Hour',           'A moody lounge with craft drinks, live music, and plush seating.', '27 Brattle St',      'Cambridge',  '617-555-0305', 4.60, 15.00, 75.00),
   (28, 'Greenline Garden',      'A laid-back park cafe for coffee walks, picnics, and sunset hangs.','91 Somerville Ave', 'Somerville', '617-555-0306', 4.30,  8.00, 35.00),
   (29, 'The Beacon Tavern',     'A classic Beacon Hill pub with fireplaces and fireside tables.',   '45 Charles St',      'Boston',     '617-555-0307', 4.40, 18.00, 65.00),
   (30, 'Foundry Coffee Co.',    'Industrial-chic espresso bar with pour-overs and pastries.',       '212 Mass Ave',       'Cambridge',  '617-555-0308', 4.55,  6.00, 22.00),
   (31, 'Union Square Social',   'Craft cocktails and shared plates in the heart of Union Square.',  '50 Bow St',          'Somerville', '617-555-0309', 4.35, 12.00, 55.00),
   (32, 'The Alden Room',        'Speakeasy-style cocktail bar hidden behind a bookstore.',          '88 Boylston St',     'Boston',     '617-555-0310', 4.75, 20.00, 85.00),
   (33, 'Mirador Terrace',       'Latin-inspired rooftop with tapas, sangria, and live DJs.',        '14 Summer St',       'Boston',     '617-555-0311', 4.50, 22.00, 78.00),
   (29, 'Harvard Square Bistro', 'A French bistro tucked off Harvard Square with a candlelit patio.','7 Holyoke St',       'Cambridge',  '617-555-0312', 4.65, 20.00, 70.00),
   (30, 'The Glasshouse',        'Botanical-themed brunch cafe with glass atrium seating.',          '305 Beacon St',      'Brookline',  '617-555-0313', 4.45, 10.00, 40.00),
   (31, 'Davis Drafthouse',      'Neighborhood beer hall with 40 taps and trivia nights.',           '22 Elm St',          'Somerville', '617-555-0314', 4.25,  8.00, 38.00),
   (32, 'Paper Lantern Izakaya', 'Japanese izakaya with sake flights and yakitori.',                 '163 Newbury St',     'Boston',     '617-555-0315', 4.70, 18.00, 68.00),
   (33, 'Coolidge Corner Cafe',  'Family-run cafe with homemade pastries and latte art.',            '280 Harvard St',     'Brookline',  '617-555-0316', 4.40,  5.00, 25.00),
   (26, 'The Copley Room',       'Elegant dining room across from the Boston Public Library.',       '560 Boylston St',    'Boston',     '617-555-0317', 4.85, 35.00, 120.00),
   (27, 'Kendall Pour House',    'Kendall Square gastropub with seasonal New England menu.',         '4 Cambridge Center', 'Cambridge',  '617-555-0318', 4.30, 15.00, 55.00),
   (28, 'Porter Tea Garden',     'Quiet tea house serving matcha, oolong, and mochi desserts.',      '1815 Mass Ave',      'Cambridge',  '617-555-0319', 4.60,  7.00, 28.00),
   (29, 'Fenway Firepit',        'Outdoor firepit lounge steps from Fenway Park.',                   '88 Lansdowne St',    'Boston',     '617-555-0320', 4.15, 14.00, 50.00),
   (30, 'Inman Oyster Bar',      'Seafood-focused raw bar in Inman Square with natural wines.',      '1345 Cambridge St',  'Cambridge',  '617-555-0321', 4.65, 22.00, 85.00),
   (31, 'The Lamplighter',       'Craft brewery and taproom with rotating guest taps.',              '284 Broadway',       'Cambridge',  '617-555-0322', 4.45, 10.00, 40.00),
   (32, 'Back Bay Ballroom',     'Grand ballroom lounge with live jazz every weekend.',              '99 Clarendon St',    'Boston',     '617-555-0323', 4.55, 25.00, 95.00),
   (33, 'Allston Alley',         'Casual gaming bar with pinball machines and street food.',         '155 Brighton Ave',   'Allston',    '617-555-0324', 4.20,  9.00, 36.00),
   (26, 'The North End Nook',    'Tiny Italian wine bar with handmade pasta and espresso.',          '132 Hanover St',     'Boston',     '617-555-0325', 4.75, 18.00, 62.00),
   (27, 'Teele Square Tavern',   'Cozy neighborhood pub with fireside booths and burger nights.',    '1153 Broadway',      'Somerville', '617-555-0326', 4.35, 12.00, 42.00),
   (28, 'Boylston Bookshop Cafe','Independent bookstore with espresso bar and reading nooks.',       '745 Boylston St',    'Boston',     '617-555-0327', 4.50,  6.00, 24.00),
   (29, 'The Cambridge Common',  'Historic tavern in Cambridge with live Irish music.',              '1667 Mass Ave',      'Cambridge',  '617-555-0328', 4.25, 12.00, 45.00),
   (30, 'Seaport Sunset Club',   'Ultra-lounge with waterfront cabanas and bottle service.',         '55 Pier 4 Blvd',     'Boston',     '617-555-0329', 4.40, 30.00, 150.00),
   (31, 'The Painted Burro',     'Mexican cantina with mezcal flights and brunch margaritas.',       '219 Elm St',         'Somerville', '617-555-0330', 4.55, 14.00, 50.00),
   (32, 'Brookline Booksellers Cafe','Quiet cafe inside a beloved indie bookstore.',                 '279 Harvard St',     'Brookline',  '617-555-0331', 4.45,  5.00, 20.00),
   (33, 'Gardner Garden Lounge', 'Museum-adjacent garden bar with botanical cocktails.',             '25 Evans Way',       'Boston',     '617-555-0332', 4.60, 16.00, 60.00),
   (26, 'Pinball Prophet',       'Retro arcade and dive bar with tournaments every Friday.',         '311 Somerville Ave', 'Somerville', '617-555-0333', 4.30,  8.00, 35.00),
   (27, 'Harvard Film Archive',  'Independent art-house theater with curated film series.',          '24 Quincy St',       'Cambridge',  '617-555-0334', 4.80, 10.00, 20.00),
   (28, 'Esplanade Picnic Co.',  'Outdoor grab-and-go picnic company along the Charles River.',      '1 Embankment Rd',    'Boston',     '617-555-0335', 4.40, 12.00, 45.00);
 
 
-- ============================================================
-- VENUE CATEGORY (bridge table — 60+ rows)
-- Categories: 1=Restaurant, 2=Bar, 3=Cafe, 4=Lounge, 5=Club, 6=Park, 7=Museum, 8=Theater, 9=Arcade, 10=Rooftop
-- ============================================================
 
INSERT INTO VenueCategory (venueId, categoryId) VALUES
   (1, 2), (1, 10), (1, 4), (1, 1),
   (2, 3), (2, 1),
   (3, 9), (3, 4), (3, 2), (3, 1),
   (4, 1), (4, 10), (4, 2),
   (5, 2), (5, 4), (5, 1),
   (6, 3), (6, 6), (6, 1),
   (7, 2), (7, 1), (7, 4),
   (8, 3), (8, 1),
   (9, 2), (9, 4), (9, 1),
   (10, 2), (10, 4), (10, 1),
   (11, 10), (11, 2), (11, 5), (11, 1),
   (12, 1), (12, 4), (12, 2),
   (13, 3), (13, 1), (13, 6),
   (14, 2), (14, 1),
   (15, 1), (15, 2), (15, 4),
   (16, 3), (16, 1),
   (17, 1), (17, 4), (17, 2),
   (18, 1), (18, 2), (18, 4),
   (19, 3), (19, 1),
   (20, 4), (20, 2), (20, 10),
   (21, 1), (21, 2), (21, 4),
   (22, 2), (22, 1),
   (23, 4), (23, 5), (23, 2),
   (24, 2), (24, 9), (24, 1),
   (25, 1), (25, 2), (25, 4),
   (26, 2), (26, 1), (26, 4),
   (27, 3), (27, 1), (27, 7),
   (28, 2), (28, 1), (28, 4),
   (29, 4), (29, 5), (29, 10), (29, 2),
   (30, 1), (30, 2), (30, 4),
   (31, 3), (31, 1), (31, 7),
   (32, 2), (32, 4), (32, 6), (32, 1),
   (33, 9), (33, 2), (33, 1),
   (34, 8), (34, 7),
   (35, 6), (35, 1), (35, 3),
   (1, 5), (4, 4), (5, 5), (10, 1), (11, 4), (12, 10), (17, 10),
   (20, 1), (21, 4), (23, 1), (25, 10), (29, 1), (32, 2), (33, 4),
   (6, 2), (7, 10), (9, 2), (13, 4), (18, 10), (22, 1), (24, 2),
   (26, 2), (27, 3), (28, 9), (30, 3);
 
 
-- ============================================================
-- VENUE VIBE (bridge table — 65+ rows)
-- Vibes: 1=Romantic, 2=Casual, 3=Upscale, 4=Cozy, 5=Lively, 6=Chill, 7=Adventurous, 8=Artsy, 9=Trendy, 10=Intimate
-- ============================================================
 
INSERT INTO VenueVibe (venueId, vibeId) VALUES
   (1, 1), (1, 3), (1, 9), (1, 5),
   (2, 4), (2, 10), (2, 6), (2, 2),
   (3, 5), (3, 7), (3, 9), (3, 2),
   (4, 1), (4, 3), (4, 5),
   (5, 9), (5, 10), (5, 1), (5, 3),
   (6, 2), (6, 6), (6, 8),
   (7, 4), (7, 2), (7, 10), (7, 1),
   (8, 2), (8, 6), (8, 9), (8, 8),
   (9, 5), (9, 9), (9, 2),
   (10, 1), (10, 10), (10, 3), (10, 8),
   (11, 5), (11, 9), (11, 3), (11, 7),
   (12, 1), (12, 3), (12, 10), (12, 4),
   (13, 8), (13, 6), (13, 4), (13, 2),
   (14, 2), (14, 5), (14, 6),
   (15, 1), (15, 10), (15, 9), (15, 3),
   (16, 4), (16, 2), (16, 6),
   (17, 3), (17, 1), (17, 10),
   (18, 2), (18, 5), (18, 9),
   (19, 4), (19, 6), (19, 10), (19, 8),
   (20, 5), (20, 2), (20, 7),
   (21, 3), (21, 9), (21, 1), (21, 8),
   (22, 2), (22, 5), (22, 6),
   (23, 3), (23, 1), (23, 8), (23, 5),
   (24, 2), (24, 5), (24, 7),
   (25, 1), (25, 4), (25, 10), (25, 3),
   (26, 2), (26, 4), (26, 6),
   (27, 8), (27, 4), (27, 6), (27, 10),
   (28, 2), (28, 5), (28, 6),
   (29, 9), (29, 3), (29, 5), (29, 7),
   (30, 5), (30, 7), (30, 2),
   (31, 4), (31, 6), (31, 8), (31, 10),
   (32, 1), (32, 8), (32, 3), (32, 6),
   (33, 2), (33, 7), (33, 5),
   (34, 8), (34, 6), (34, 10),
   (35, 6), (35, 2), (35, 7),
   (1, 6), (10, 5), (17, 5), (25, 5), (12, 5);
 
 
-- ============================================================
-- REVIEWS (55 total — weak entity, 50-75 range)
-- Users 1-25 review across venues 1-35
-- ============================================================
 
INSERT INTO Reviews (userId, venueId, comment, rating, isFlagged) VALUES
   (1,  1,  'Absolutely stunning views, perfect for a date night!',                         4.80, FALSE),
   (2,  2,  'Such a cozy spot. The lattes are amazing.',                                    4.20, FALSE),
   (3,  3,  'So much fun, the retro games made the night unforgettable.',                   4.70, FALSE),
   (1,  4,  'The waterfront view and menu make this an easy yes for a special night out.',  4.60, FALSE),
   (2,  5,  'A polished lounge with great cocktails and just enough energy for a first date.',4.40, FALSE),
   (3,  6,  'Relaxed, walkable, and perfect for a coffee date that can turn into a picnic.',4.10, FALSE),
   (4,  7,  'Beacon Hill charm all the way. Fireplace tables are everything.',              4.50, FALSE),
   (5,  8,  'Best pour-over in Cambridge, hands down.',                                     4.70, FALSE),
   (6,  9,  'Loved the shared plates. Great vibe on a Friday.',                             4.30, FALSE),
   (7,  10, 'A hidden gem. The speakeasy entrance is such a cool touch.',                   4.90, FALSE),
   (8,  11, 'Rooftop sangria in the summer is unbeatable.',                                 4.50, FALSE),
   (9,  12, 'The candlelit patio made our anniversary so special.',                         4.80, FALSE),
   (10, 13, 'Brunch goals. The atrium is gorgeous.',                                        4.40, FALSE),
   (11, 14, 'Fun trivia night, solid beer selection.',                                      4.10, FALSE),
   (12, 15, 'Yakitori was incredible and the sake flight was a great deal.',                4.70, FALSE),
   (13, 16, 'My go-to neighborhood cafe. Always friendly.',                                 4.50, FALSE),
   (14, 17, 'Worth every penny for a special occasion.',                                    4.90, FALSE),
   (15, 18, 'Great seasonal menu, very Kendall.',                                           4.20, FALSE),
   (16, 19, 'Matcha was top-notch and the vibe was so peaceful.',                           4.60, FALSE),
   (17, 20, 'Fun before a Sox game but nothing too special.',                               3.90, FALSE),
   (18, 21, 'Oysters were fresh and the natural wine list is killer.',                      4.70, FALSE),
   (19, 22, 'Good beer, loud on weekends. Best midweek.',                                   4.20, FALSE),
   (20, 23, 'Jazz nights here are a whole experience.',                                     4.60, FALSE),
   (21, 24, 'Pinball plus tacos equals a perfect date.',                                    4.30, FALSE),
   (22, 25, 'Tiny but mighty. The cacio e pepe is unreal.',                                 4.80, FALSE),
   (23, 26, 'Very neighborhood feel, great burgers.',                                       4.20, FALSE),
   (24, 27, 'Love browsing books with an espresso in hand.',                                4.60, FALSE),
   (25, 28, 'Live Irish music brought the whole place together.',                           4.40, FALSE),
   (1,  29, 'Fancy but fun. Cabanas are worth the splurge.',                                4.50, FALSE),
   (2,  30, 'Brunch margs were strong and the guac is legit.',                              4.60, FALSE),
   (3,  31, 'Perfect rainy day cafe. So quiet and comfortable.',                            4.50, FALSE),
   (4,  32, 'Cocktails here are plated like art.',                                          4.70, FALSE),
   (5,  33, 'Old-school arcade energy. Loved the tournament night.',                        4.30, FALSE),
   (6,  34, 'Saw a foreign film I could never find elsewhere. Amazing.',                    4.90, FALSE),
   (7,  35, 'Grabbed picnic baskets for a Charles River afternoon. Perfect.',               4.50, FALSE),
   (8,  1,  'Cocktails were pricey but the view earns it.',                                 4.30, FALSE),
   (9,  4,  'Went for our anniversary, everything was perfect.',                            4.80, FALSE),
   (10, 10, 'The Alden Room is a Boston must-visit.',                                       4.90, FALSE),
   (11, 15, 'Great izakaya energy, staff was super attentive.',                             4.60, FALSE),
   (12, 21, 'Oyster happy hour is unbeatable.',                                             4.50, FALSE),
   (13, 25, 'Felt transported to Italy. Stunning wine list.',                               4.80, FALSE),
   (14, 3,  'Super fun date night idea, would go back.',                                    4.40, FALSE),
   (15, 8,  'Barista made me a latte with a heart on it. Made my day.',                     4.50, FALSE),
   (16, 12, 'Steak frites were perfect. So cozy.',                                          4.70, FALSE),
   (17, 17, 'Incredible service and atmosphere. A classic.',                                4.90, FALSE),
   (18, 23, 'Jazz plus a martini equals a great Friday.',                                   4.50, FALSE),
   (19, 6,  'Nice for a casual hang but can get crowded.',                                  4.00, FALSE),
   (20, 11, 'Rooftop sangria flight is a whole vibe.',                                      4.50, FALSE),
   (21, 16, 'Sweet family vibe, best chai I have had.',                                     4.50, FALSE),
   (22, 30, 'Guac, margs, and tacos. What more do you want.',                               4.50, FALSE),
   (23, 7,  'Perfect snowy night spot.',                                                    4.60, FALSE),
   (24, 13, 'Brunch line was long but so worth it.',                                        4.40, FALSE),
   (25, 19, 'Ceremonial matcha experience is a must.',                                      4.70, FALSE),
   (1,  33, 'Best pinball in the city.',                                                    4.30, FALSE),
   (2,  24, 'Loved the street food pop-up they had last weekend.',                          4.20, FALSE),
   (3,  20, 'Came before a game, fun energy.',                                              4.00, TRUE);
 
 
-- ============================================================
-- POSTS (40 total — weak entity)
-- Owners 26-33 post to their venues
-- ============================================================
 
INSERT INTO Posts (ownerId, venueId, content) VALUES
   (26, 1,  'Join us this Friday for live jazz under the stars. Reserve your table now.'),
   (27, 2,  'New seasonal menu is here. Try our maple oat latte while it lasts.'),
   (28, 3,  'Double tokens every Tuesday night. Bring your date for double the fun.'),
   (26, 4,  'Sunset seating is now open on the rooftop patio.'),
   (27, 5,  'Live acoustic sets every Thursday at Velvet Hour.'),
   (28, 6,  'Morning coffee and weekend picnic baskets are back.'),
   (29, 7,  'Fireside reservations open for the winter season.'),
   (30, 8,  'New single-origin Ethiopian roast just dropped.'),
   (31, 9,  'Happy hour extended to 7pm on weekdays.'),
   (32, 10, 'Reservations required. Message us for the password.'),
   (33, 11, 'Sangria Sundays are back. Live DJ from 4-10pm.'),
   (29, 12, 'Our tasting menu is being refreshed next week. Stay tuned.'),
   (30, 13, 'Saturday brunch reservations are filling fast. Book early.'),
   (31, 14, 'Trivia night every Wednesday. $1 wings after 9pm.'),
   (32, 15, 'New sake flight lineup arriving next Friday.'),
   (33, 16, 'Valentines Day pastry boxes are now open for pre-order.'),
   (26, 17, 'Our private dining room is available for anniversary bookings.'),
   (27, 18, 'New New England fall menu dropped today. Come try the short rib.'),
   (28, 19, 'Matcha workshop this Saturday. $25 per person.'),
   (29, 20, 'Game day specials every home game. Fire tables reserved walk-in.'),
   (30, 21, 'Half-shell happy hour is back. 4-6pm Tuesday through Thursday.'),
   (31, 22, 'Two new guest IPAs on tap this week.'),
   (32, 23, 'Weekend jazz lineup posted. Saturday sells out fast.'),
   (33, 24, 'Street food popup this Saturday from 6-10pm.'),
   (26, 25, 'Handmade pasta night every Monday. Small plates only.'),
   (27, 26, 'Burger night is every Thursday. Drafts $4.'),
   (28, 27, 'New local author reading next Thursday at 7pm.'),
   (29, 28, 'Live Irish music every Sunday afternoon.'),
   (30, 29, 'Cabana reservations for summer now open.'),
   (31, 30, 'Brunch margs are bottomless Saturday and Sunday.'),
   (32, 31, 'New fall reading list is up in the cafe.'),
   (33, 32, 'Botanical cocktail class this weekend. Limited spots.'),
   (26, 33, 'Tournament Tuesday. Entry $10, winner takes the pot.'),
   (27, 34, 'Foreign film series kicks off next week. See website for lineup.'),
   (28, 35, 'Esplanade picnic bookings open 2 weeks in advance.'),
   (26, 1,  'Happy Hour is now from 4-7pm every weekday.'),
   (27, 5,  'Private event bookings for Velvet Hour are open through December.'),
   (28, 3,  'New pinball machine just arrived. Come try it.'),
   (32, 15, 'Yakitori tasting menu launching next month.'),
   (33, 11, 'We are hiring a weekend DJ. DM us if interested.'),
   (29, 7,  'Prix fixe menu added for Valentines week. Book now.'),
   (30, 13, 'New breakfast sandwich drops next Monday.'),
   (31, 9,  'Private event space now available to book online.'),
   (32, 10, 'Dress code tightened for weekends. Smart casual only.'),
   (33, 16, 'Croissants now available in lavender and matcha.'),
   (26, 17, 'Chef is hosting a tasting dinner on the 15th. Six seats only.'),
   (27, 18, 'Oyster Sunday is officially a thing. See you this weekend.'),
   (28, 19, 'New tea flight menu launched. Comes with house-made mochi.'),
   (29, 20, 'Fire tables are heated through November.'),
   (30, 21, 'Natural wine tasting next Thursday, $45 per person.'),
   (31, 22, 'Brewery tour Saturdays at 3pm. Free flight with tour.');
 
 
-- ============================================================
-- LISTS (30 total — weak entity)
-- ============================================================
 
INSERT INTO Lists (userId, name) VALUES
   (1,  'Dream Date Spots'),
   (2,  'Boston Favorites'),
   (3,  'Weekend Plans'),
   (4,  'Anniversary Ideas'),
   (5,  'Brunch Bucket List'),
   (6,  'Cozy Cafe Stops'),
   (7,  'Rooftop Season'),
   (8,  'Birthday Plans'),
   (9,  'Out of Towner Tour'),
   (10, 'Cheap and Cheerful'),
   (11, 'Splurge Night Out'),
   (12, 'Book and Coffee'),
   (13, 'After-Work Drinks'),
   (14, 'Jazz Night'),
   (15, 'Summer Sunset Spots'),
   (16, 'First Date Safe Bets'),
   (17, 'Rainy Day Cafes'),
   (18, 'Girls Night'),
   (19, 'Boyfriend Surprise'),
   (20, 'Cambridge Crawl'),
   (21, 'Somerville Staples'),
   (22, 'Allston Adventures'),
   (23, 'Brookline Gems'),
   (24, 'North End Nights'),
   (25, 'Seaport Spots'),
   (1,  'Cocktail Connoisseur'),
   (3,  'Date Night In Progress'),
   (5,  'Vegan-Friendly Picks'),
   (7,  'Post-Work Wind Down'),
   (10, 'Museum and a Meal'),
   (2,  'Low-Key First Dates'),
   (4,  'Impress the Parents'),
   (6,  'Study Cafes'),
   (8,  'Late Night Eats'),
   (9,  'Group Hang Spots'),
   (11, 'Wine Bar Tour'),
   (12, 'Quiet Reading Spots'),
   (13, 'Happy Hour Rotation'),
   (14, 'Live Music Nights'),
   (15, 'Waterfront Views'),
   (16, 'Walk-In Friendly'),
   (17, 'Vibe Check'),
   (18, 'Bachelorette Prep'),
   (19, 'Date Night Reset'),
   (20, 'Kendall to Harvard'),
   (21, 'Davis Square Run'),
   (22, 'Brighton Ave Loop'),
   (23, 'Coolidge Corner Hits'),
   (24, 'Italian Food Tour'),
   (25, 'Pier Crawl'),
   (1,  'Birthday Month Plans'),
   (3,  'Sunday Funday'),
   (5,  'Matcha Mission');
 
 
-- ============================================================
-- LIST VENUE (bridge table — 130+ rows)
-- ============================================================
 
INSERT INTO ListVenue (listId, venueId) VALUES
   (1, 1), (1, 4), (1, 10), (1, 12), (1, 15), (1, 17), (1, 25),
   (2, 1), (2, 7), (2, 10), (2, 17), (2, 20), (2, 25), (2, 29),
   (3, 3), (3, 6), (3, 11), (3, 14), (3, 24), (3, 33),
   (4, 4), (4, 10), (4, 12), (4, 17), (4, 25), (4, 32),
   (5, 2), (5, 13), (5, 16), (5, 30), (5, 31),
   (6, 2), (6, 8), (6, 16), (6, 19), (6, 27), (6, 31),
   (7, 1), (7, 4), (7, 11), (7, 29), (7, 32),
   (8, 3), (8, 9), (8, 14), (8, 23), (8, 33),
   (9, 1), (9, 7), (9, 17), (9, 20), (9, 25), (9, 34),
   (10, 2), (10, 6), (10, 8), (10, 16), (10, 24), (10, 26),
   (11, 4), (11, 10), (11, 17), (11, 23), (11, 29),
   (12, 8), (12, 13), (12, 19), (12, 27), (12, 31), (12, 34),
   (13, 5), (13, 9), (13, 18), (13, 22), (13, 26),
   (14, 10), (14, 23), (14, 32),
   (15, 1), (15, 4), (15, 11), (15, 29), (15, 35),
   (16, 2), (16, 5), (16, 12), (16, 25), (16, 27),
   (17, 2), (17, 8), (17, 13), (17, 19), (17, 27), (17, 31),
   (18, 3), (18, 5), (18, 11), (18, 23), (18, 30),
   (19, 10), (19, 12), (19, 17), (19, 25), (19, 32),
   (20, 2), (20, 5), (20, 8), (20, 12), (20, 18), (20, 19), (20, 21), (20, 22), (20, 28), (20, 34),
   (21, 3), (21, 6), (21, 9), (21, 14), (21, 26), (21, 30), (21, 33),
   (22, 24),
   (23, 13), (23, 16), (23, 31),
   (24, 25),
   (25, 4), (25, 29), (25, 35),
   (26, 5), (26, 10), (26, 11), (26, 15), (26, 23), (26, 32),
   (27, 1), (27, 4), (27, 10), (27, 17), (27, 25),
   (28, 2), (28, 6), (28, 13), (28, 19), (28, 27), (28, 30), (28, 31),
   (29, 5), (29, 9), (29, 14), (29, 22), (29, 26),
   (30, 1), (30, 17), (30, 34),
   (31, 2), (31, 12), (31, 16), (31, 26), (31, 27),
   (32, 4), (32, 10), (32, 17), (32, 25), (32, 32),
   (33, 8), (33, 19), (33, 27), (33, 31),
   (34, 9), (34, 14), (34, 24), (34, 30), (34, 33),
   (35, 3), (35, 11), (35, 20), (35, 24),
   (36, 10), (36, 17), (36, 25), (36, 32),
   (37, 8), (37, 19), (37, 27), (37, 31),
   (38, 5), (38, 9), (38, 14), (38, 22), (38, 26), (38, 30),
   (39, 10), (39, 14), (39, 23), (39, 32),
   (40, 1), (40, 4), (40, 11), (40, 29), (40, 35),
   (41, 3), (41, 6), (41, 24), (41, 33),
   (42, 1), (42, 10), (42, 17), (42, 25), (42, 32),
   (43, 3), (43, 5), (43, 11), (43, 18), (43, 24), (43, 30),
   (44, 4), (44, 17), (44, 25),
   (45, 2), (45, 5), (45, 8), (45, 12), (45, 18), (45, 19), (45, 21), (45, 34),
   (46, 3), (46, 14), (46, 26), (46, 33),
   (47, 24),
   (48, 13), (48, 16), (48, 31),
   (49, 25),
   (50, 4), (50, 29), (50, 35),
   (51, 1), (51, 4), (51, 10), (51, 17),
   (52, 3), (52, 6), (52, 24), (52, 33),
   (53, 2), (53, 8), (53, 19);
 
 
-- ============================================================
-- SAVED VENUES (60+ rows — users save venues they like)
-- ============================================================
 
INSERT INTO SavedVenues (userId, venueId) VALUES
   (1, 3), (1, 4), (1, 10), (1, 17), (1, 25), (1, 32),
   (2, 1), (2, 5), (2, 8), (2, 13), (2, 21), (2, 30),
   (3, 2), (3, 6), (3, 14), (3, 24), (3, 30), (3, 33),
   (4, 7), (4, 12), (4, 17), (4, 25), (4, 32),
   (5, 2), (5, 13), (5, 16), (5, 31), (5, 8),
   (6, 8), (6, 19), (6, 27), (6, 31), (6, 34),
   (7, 1), (7, 4), (7, 11), (7, 29), (7, 35),
   (8, 3), (8, 10), (8, 14), (8, 23), (8, 33),
   (9, 4), (9, 12), (9, 17), (9, 25), (9, 32),
   (10, 2), (10, 8), (10, 16), (10, 26), (10, 34),
   (11, 4), (11, 10), (11, 23), (11, 29), (11, 11),
   (12, 8), (12, 13), (12, 19), (12, 31), (12, 27),
   (13, 5), (13, 9), (13, 22), (13, 26), (13, 14),
   (14, 10), (14, 15), (14, 23), (14, 32), (14, 3),
   (15, 1), (15, 11), (15, 29), (15, 35), (15, 4),
   (16, 2), (16, 12), (16, 25), (16, 27), (16, 19),
   (17, 8), (17, 13), (17, 19), (17, 31), (17, 6),
   (18, 3), (18, 5), (18, 23), (18, 9), (18, 33),
   (19, 10), (19, 17), (19, 25), (19, 12), (19, 4),
   (20, 2), (20, 12), (20, 18), (20, 21), (20, 28), (20, 34),
   (21, 9), (21, 14), (21, 26), (21, 30), (21, 33),
   (22, 24), (22, 33), (22, 3),
   (23, 13), (23, 16), (23, 31), (23, 27),
   (24, 25), (24, 28), (24, 23), (24, 12),
   (25, 4), (25, 29), (25, 34), (25, 35), (25, 1), (25, 17);
 
 
-- ============================================================
-- VENUE APPLICATIONS (12 total)
-- ============================================================
 
INSERT INTO VenueApplications (ownerId, name, description, address, phone, minPrice, maxPrice, status) VALUES
   (26, 'Sky Garden',           'An outdoor terrace dining experience.',                   '321 Cloud Blvd, Boston, MA',        '617-555-0401', 30.00, 100.00, 'PENDING'),
   (27, 'Brew & Books',          'A bookstore cafe hybrid with craft beers.',               '654 Page St, Cambridge, MA',        '617-555-0402',  8.00,  40.00, 'APPROVED'),
   (28, 'Pixel Palace',          'Next-gen VR arcade and bar.',                             '987 Circuit Ave, Somerville, MA',   '617-555-0403', 15.00,  60.00, 'REJECTED'),
   (29, 'Back Bay Bistro',       'French bistro with seasonal tasting menus.',              '45 Newbury St, Boston, MA',         '617-555-0404', 25.00,  85.00, 'APPROVED'),
   (30, 'The Riverside Tap',     'Charles River waterfront beer garden.',                   '99 Memorial Dr, Cambridge, MA',     '617-555-0405', 10.00,  45.00, 'PENDING'),
   (31, 'Lumen Lounge',          'Immersive cocktail bar with projected art installations.','200 Tremont St, Boston, MA',        '617-555-0406', 20.00,  80.00, 'PENDING'),
   (32, 'Cambridge Creamery',    'Artisanal ice cream parlor with dessert flights.',        '88 Mount Auburn St, Cambridge, MA', '617-555-0407',  5.00,  20.00, 'APPROVED'),
   (33, 'The Green Room',        'Plant-based restaurant with living wall interiors.',      '302 Beacon St, Brookline, MA',      '617-555-0408', 18.00,  65.00, 'APPROVED'),
   (26, 'Harborfront Taphouse',  'Seaside taphouse with 50 local drafts.',                  '77 Waterfront Dr, Boston, MA',      '617-555-0409', 12.00,  50.00, 'REJECTED'),
   (27, 'Cloud Nine Karaoke',    'Private room karaoke lounge with bottle service.',        '15 Boylston Pl, Boston, MA',        '617-555-0410', 20.00,  90.00, 'PENDING'),
   (28, 'The Firefly Cafe',      'Late-night dessert and coffee spot open until 2am.',      '411 Somerville Ave, Somerville, MA','617-555-0411',  6.00,  28.00, 'APPROVED'),
   (29, 'Oak and Ember',         'Wood-fired steakhouse with craft cocktail program.',      '56 Kneeland St, Boston, MA',        '617-555-0412', 35.00, 140.00, 'REJECTED'),
   (30, 'The Velvet Bean',       'Specialty coffee bar with single-origin pour-overs.',     '91 Beacon St, Brookline, MA',       '617-555-0413',  5.00,  18.00, 'APPROVED'),
   (31, 'Nomad Kitchen',         'Globally-inspired small plates and natural wines.',       '14 Prospect St, Cambridge, MA',     '617-555-0414', 18.00,  70.00, 'PENDING'),
   (32, 'Riverside Arcade',      'Family-friendly arcade with weekend tournaments.',        '220 Monsignor Obrien Hwy, Cambridge, MA','617-555-0415',  8.00,  35.00, 'PENDING'),
   (33, 'Moonlight Mezcaleria',  'Intimate mezcal bar with Oaxacan small plates.',          '68 South St, Boston, MA',           '617-555-0416', 16.00,  70.00, 'APPROVED'),
   (26, 'The Paper Crane',       'Modern Japanese tea house with omakase service.',         '175 Tremont St, Boston, MA',        '617-555-0417', 28.00, 100.00, 'PENDING'),
   (27, 'Charter Club',          'Members-only rooftop with skyline views.',                '1 International Pl, Boston, MA',    '617-555-0418', 40.00, 180.00, 'REJECTED'),
   (28, 'Porter Bowl',            'Poke and grain bowl counter with outdoor seating.',      '1900 Mass Ave, Cambridge, MA',      '617-555-0419', 10.00,  25.00, 'APPROVED'),
   (29, 'Ember Room',            'Fireplace-lit wine bar with cheese flights.',             '108 Charles St, Boston, MA',        '617-555-0420', 15.00,  55.00, 'PENDING'),
   (30, 'The Ivy Patio',         'Covered garden cafe hidden behind a townhouse.',          '55 Commonwealth Ave, Boston, MA',   '617-555-0421', 12.00,  45.00, 'APPROVED'),
   (31, 'Red Line Diner',        'All-day diner with late night breakfast menu.',           '301 Mass Ave, Cambridge, MA',       '617-555-0422',  8.00,  25.00, 'APPROVED'),
   (32, 'Inkwell',                'Literary-themed cocktail bar with rotating menus.',      '18 Arlington St, Boston, MA',       '617-555-0423', 18.00,  70.00, 'PENDING'),
   (33, 'Pier Forty',             'Seafood-forward seaport bistro with raw bar.',           '40 Pier 4 Blvd, Boston, MA',        '617-555-0424', 22.00,  88.00, 'APPROVED'),
   (26, 'The Observatory Bar',   'Astronomy-themed cocktail bar with telescope deck.',      '400 Stuart St, Boston, MA',         '617-555-0425', 20.00,  75.00, 'REJECTED'),
   (27, 'Union Bean Co.',        'Small batch roaster and cafe with house-baked pastries.', '12 Union Sq, Somerville, MA',       '617-555-0426',  5.00,  22.00, 'APPROVED'),
   (28, 'The Wilder',             'Farm-to-table restaurant with open kitchen seating.',    '59 Brattle St, Cambridge, MA',      '617-555-0427', 25.00,  95.00, 'PENDING'),
   (29, 'Golden Hour',            'Sunset-themed rooftop lounge with tapas menu.',          '225 Franklin St, Boston, MA',       '617-555-0428', 22.00,  82.00, 'APPROVED'),
   (30, 'Sparrow and Vine',       'Wine bar focused on natural and biodynamic bottles.',    '84 Massachusetts Ave, Cambridge, MA','617-555-0429',14.00,  58.00, 'APPROVED'),
   (31, 'Broadway Beer Hall',     'German-style beer hall with long communal tables.',      '275 Broadway, Somerville, MA',      '617-555-0430', 10.00,  40.00, 'REJECTED'),
   (32, 'The Polished Penny',    'Vintage-inspired cocktail parlor with live piano.',       '130 Dartmouth St, Boston, MA',      '617-555-0431', 18.00,  75.00, 'PENDING'),
   (33, 'Brickline Bakehouse',    'Artisan bakery cafe with lunch counter service.',        '420 Harvard St, Brookline, MA',     '617-555-0432',  6.00,  24.00, 'APPROVED'),
   (26, 'Neon Church',            'Multi-room nightclub with visual art installations.',    '85 Lansdowne St, Boston, MA',       '617-555-0433', 20.00, 120.00, 'PENDING'),
   (27, 'Highline Hops',          'Craft brewery taproom with rooftop patio.',              '180 Western Ave, Allston, MA',      '617-555-0434', 10.00,  45.00, 'APPROVED'),
   (28, 'Birch & Bramble',        'Nordic-inspired cafe with foraged seasonal menu.',       '95 Holland St, Somerville, MA',     '617-555-0435',  8.00,  30.00, 'PENDING'),
   (29, 'The Reading Room',       'Library-themed lounge with rare spirits and books.',     '240 Tremont St, Boston, MA',        '617-555-0436', 18.00,  85.00, 'APPROVED'),
   (30, 'Greenway Grill',         'Al fresco grill spot along the Rose Kennedy Greenway.',  '200 Atlantic Ave, Boston, MA',      '617-555-0437', 14.00,  55.00, 'PENDING'),
   (31, 'La Placita',             'Puerto Rican cantina with live salsa nights.',           '170 Brighton Ave, Allston, MA',     '617-555-0438', 14.00,  50.00, 'APPROVED'),
   (32, 'Studio 88 Cafe',         'Photography studio cafe with rotating art shows.',       '88 Pearl St, Cambridge, MA',        '617-555-0439',  6.00,  20.00, 'APPROVED'),
   (33, 'The Oxbow',              'Craft cocktail bar with agricultural themed menu.',      '45 Kneeland St, Boston, MA',        '617-555-0440', 16.00,  68.00, 'REJECTED'),
   (26, 'Skylab Rooftop',         'Experimental rooftop with weekly pop-up chefs.',         '500 Washington St, Boston, MA',     '617-555-0441', 25.00,  95.00, 'PENDING'),
   (27, 'Pressed and Poured',     'Juice bar and wellness cafe with cold-pressed menu.',    '77 Huntington Ave, Boston, MA',     '617-555-0442',  6.00,  22.00, 'APPROVED'),
   (28, 'The Understudy',         'Theater-district wine bar with pre-show menu.',          '210 Stuart St, Boston, MA',         '617-555-0443', 15.00,  60.00, 'PENDING'),
   (29, 'Millpond Tavern',        'Rustic tavern with live folk music weekly.',             '118 Elm St, Somerville, MA',        '617-555-0444', 10.00,  42.00, 'APPROVED'),
   (30, 'Wildflour Cafe',         'Gluten-free bakery and brunch spot.',                    '305 Harvard St, Brookline, MA',     '617-555-0445',  8.00,  30.00, 'APPROVED'),
   (31, 'Chroma Bar',              'LED-lit cocktail bar with signature neon menus.',       '45 Province St, Boston, MA',        '617-555-0446', 18.00,  72.00, 'PENDING'),
   (32, 'Harvest Moon Bistro',    'Seasonal New England menu in a converted barn.',         '29 Church St, Cambridge, MA',       '617-555-0447', 22.00,  80.00, 'APPROVED'),
   (33, 'The Gilded Lily',        'Art deco cocktail lounge with live jazz trio.',          '155 Seaport Blvd, Boston, MA',      '617-555-0448', 22.00,  90.00, 'PENDING'),
   (26, 'Little Donkey',          'Small plates with a global menu and natural wine.',      '505 Mass Ave, Cambridge, MA',       '617-555-0449', 16.00,  60.00, 'APPROVED'),
   (27, 'Silverline Sports Bar',  'Sports bar with craft beer and gourmet pub grub.',       '900 Dorchester Ave, Boston, MA',    '617-555-0450', 10.00,  40.00, 'REJECTED'),
   (28, 'The Moss Room',          'Plant-filled cafe with botanical small plates.',         '35 Prospect St, Cambridge, MA',     '617-555-0451',  9.00,  32.00, 'APPROVED'),
   (29, 'Parkside Patio',         'Casual outdoor dining steps from the Boston Common.',    '110 Tremont St, Boston, MA',        '617-555-0452', 14.00,  52.00, 'PENDING');
 
 
-- ============================================================
-- REPORT TICKETS (10 total)
-- ============================================================
 
INSERT INTO ReportTickets (reporterId, reviewId, description, reason, status) VALUES
   (2,  1,    'This review seems fake and overly promotional.',                    'Suspected fake review',   'PENDING'),
   (3,  2,    'Review contains inappropriate language.',                           'Inappropriate content',   'RESOLVED'),
   (1,  NULL, 'Venue owner sent unsolicited messages.',                            'Harassment',              'RESOLVED'),
   (5,  55,   'This rating seems retaliatory, user may have been refused service.','Suspected fake review',   'UNDER REVIEW'),
   (8,  20,   'Reviewer is a competitor of the venue.',                            'Conflict of interest',    'PENDING'),
   (11, 14,   'Comment contains profanity.',                                       'Inappropriate content',   'DISMISSED'),
   (4,  NULL, 'Venue listing contains misleading pricing.',                        'Misleading information',  'UNDER REVIEW'),
   (7,  9,    'Review is clearly written by the owner.',                           'Suspected fake review',   'RESOLVED'),
   (15, NULL, 'User account appears to be a bot.',                                 'Spam account',            'PENDING'),
   (19, 33,   'Review references a venue the user never visited.',                 'Suspected fake review',   'DISMISSED'),
   (6,  3,    'Suspicious five-star rating with no details.',                      'Suspected fake review',   'PENDING'),
   (9,  7,    'Review is defamatory toward staff member.',                         'Harassment',              'UNDER REVIEW'),
   (12, 15,   'Content appears to be copied from another site.',                   'Plagiarism',              'DISMISSED'),
   (14, 22,   'Reviewer never checked in according to staff.',                     'Suspected fake review',   'RESOLVED'),
   (17, NULL, 'Venue photos look AI-generated.',                                   'Misleading information',  'PENDING'),
   (20, 28,   'Review contains personal attack on owner.',                         'Harassment',              'RESOLVED'),
   (22, 11,   'Account created same day as review.',                               'Suspected fake review',   'UNDER REVIEW'),
   (3,  40,   'Unusually aggressive tone, seems personal.',                        'Inappropriate content',   'DISMISSED'),
   (5,  NULL, 'Owner spamming promotional messages to users.',                     'Spam account',            'RESOLVED'),
   (8,  31,   'Review mentions an event that never happened.',                     'Misleading information',  'PENDING'),
   (10, 18,   'User mass-posting same review on multiple venues.',                 'Spam account',            'UNDER REVIEW'),
   (13, 24,   'Review contains hate speech.',                                      'Inappropriate content',   'RESOLVED'),
   (16, 45,   'Review seems coordinated with other accounts.',                     'Suspected fake review',   'PENDING'),
   (18, NULL, 'Listing description does not match actual venue.',                  'Misleading information',  'UNDER REVIEW'),
   (21, 12,   'Reviewer clearly works for competitor.',                            'Conflict of interest',    'DISMISSED'),
   (23, 50,   'Rating changed suddenly after staff dispute.',                      'Suspected fake review',   'PENDING'),
   (25, 6,    'Review contains unsubstantiated health claims.',                    'Misleading information',  'RESOLVED'),
   (1,  19,   'Reviewer received free service in exchange for review.',            'Conflict of interest',    'UNDER REVIEW'),
   (4,  37,   'Review uses slurs toward patrons.',                                 'Inappropriate content',   'RESOLVED'),
   (7,  NULL, 'Venue owner verbally harassed customer.',                           'Harassment',              'PENDING'),
   (11, 53,   'Low rating appears to be based on wrong venue.',                    'Misleading information',  'DISMISSED'),
   (15, 29,   'Review posted from multiple accounts with same wording.',           'Spam account',            'RESOLVED'),
   (2,  48,   'Review text appears automated.',                                    'Spam account',            'PENDING'),
   (6,  NULL, 'Venue profile image is trademarked.',                               'Copyright issue',         'UNDER REVIEW'),
   (9,  26,   'Inflammatory review against ethnic staff.',                         'Inappropriate content',   'RESOLVED'),
   (12, 35,   'Review suggests illegal activity.',                                 'Inappropriate content',   'UNDER REVIEW'),
   (14, NULL, 'Venue impersonating a chain location.',                             'Misleading information',  'PENDING'),
   (17, 41,   'Reviewer has personal grudge against staff.',                       'Conflict of interest',    'DISMISSED'),
   (20, 10,   'Suspect paid positive review.',                                     'Suspected fake review',   'RESOLVED'),
   (22, NULL, 'Account is promoting external services in DMs.',                    'Spam account',            'PENDING'),
   (25, 8,    'Review text is suspiciously identical to another.',                 'Plagiarism',              'UNDER REVIEW'),
   (3,  16,   'Review appears written by a bot.',                                  'Spam account',            'DISMISSED'),
   (5,  44,   'Review content is hateful toward religion.',                        'Inappropriate content',   'RESOLVED'),
   (8,  52,   'Review references prices that do not exist at venue.',              'Misleading information',  'PENDING'),
   (10, NULL, 'Venue showing fake awards on listing.',                             'Misleading information',  'UNDER REVIEW'),
   (13, 25,   'Review content violates privacy of named individual.',              'Harassment',              'RESOLVED'),
   (16, 13,   'Review tries to extort discount.',                                  'Harassment',              'DISMISSED'),
   (18, 5,    'Review is written in bad faith after refused refund.',              'Conflict of interest',    'PENDING'),
   (21, 21,   'Content clearly paid for by venue.',                                'Suspected fake review',   'RESOLVED'),
   (23, 42,   'Reviewer threatened owner in comments.',                            'Harassment',              'UNDER REVIEW'),
   (1,  4,    'Suspect coordinated positive review campaign.',                     'Suspected fake review',   'PENDING');
 
 
-- ============================================================
-- ADMIN LOG (15 total)
-- Admin IDs: 34, 35, 36
-- ============================================================
 
INSERT INTO AdminLog (appId, reportId, adminId, action, targetTable, targetId, notes) VALUES
   (2,    NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 2,  'All documents verified, application looks legitimate.'),
   (3,    NULL, 35, 'REJECTED_APPLICATION', 'VenueApplications', 3,  'Location not within supported service area.'),
   (NULL, 1,    34, 'FLAGGED_REVIEW',       'Reviews',           1,  'Flagged for further investigation by moderation team.'),
   (4,    NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 4,  'Chef credentials verified, venue looks strong.'),
   (7,    NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 7,  'Health permits in order, approved for launch.'),
   (8,    NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 8,  'Strong concept, approved unanimously.'),
   (9,    NULL, 35, 'REJECTED_APPLICATION', 'VenueApplications', 9,  'Insufficient business documentation submitted.'),
   (11,   NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 11, 'Late-night license confirmed.'),
   (12,   NULL, 36, 'REJECTED_APPLICATION', 'VenueApplications', 12, 'Zoning issue at proposed location.'),
   (NULL, 2,    35, 'RESOLVED_REPORT',      'Reviews',           2,  'Review removed after language check.'),
   (NULL, 3,    36, 'RESOLVED_REPORT',      'Users',             NULL,'Warning issued to venue owner.'),
   (NULL, 6,    34, 'DISMISSED_REPORT',     'Reviews',           14, 'Language within community guidelines.'),
   (NULL, 8,    35, 'RESOLVED_REPORT',      'Reviews',           9,  'Review removed, owner account warned.'),
   (NULL, 10,   36, 'DISMISSED_REPORT',     'Reviews',           33, 'Could not verify the claim, review preserved.'),
   (NULL, 4,    34, 'FLAGGED_REVIEW',       'Reviews',           55, 'Under investigation for possible retaliation.'),
   (13,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 13, 'Roaster licensed and certified.'),
   (14,   NULL, 36, 'REQUESTED_INFO',       'VenueApplications', 14, 'Needed updated menu samples before approval.'),
   (15,   NULL, 34, 'REQUESTED_INFO',       'VenueApplications', 15, 'Requested proof of family-friendly licensing.'),
   (16,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 16, 'Beverage license confirmed.'),
   (17,   NULL, 36, 'REQUESTED_INFO',       'VenueApplications', 17, 'Asked for tea sourcing documentation.'),
   (18,   NULL, 34, 'REJECTED_APPLICATION', 'VenueApplications', 18, 'Members-only concept does not align with platform.'),
   (19,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 19, 'Permits and lease verified.'),
   (20,   NULL, 36, 'REQUESTED_INFO',       'VenueApplications', 20, 'Awaiting fireplace safety inspection.'),
   (21,   NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 21, 'Landscape and permits all confirmed.'),
   (22,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 22, 'Late-night license verified.'),
   (23,   NULL, 36, 'REQUESTED_INFO',       'VenueApplications', 23, 'Asked for liquor license documentation.'),
   (24,   NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 24, 'Seafood sourcing documentation complete.'),
   (25,   NULL, 35, 'REJECTED_APPLICATION', 'VenueApplications', 25, 'Concept too similar to existing listing.'),
   (26,   NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 26, 'Clean inspection, approved.'),
   (27,   NULL, 34, 'REQUESTED_INFO',       'VenueApplications', 27, 'Awaiting farm partner contracts.'),
   (28,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 28, 'Outdoor permit verified.'),
   (29,   NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 29, 'Wine program approved by review panel.'),
   (30,   NULL, 34, 'REJECTED_APPLICATION', 'VenueApplications', 30, 'Address corresponds to occupied tenant.'),
   (31,   NULL, 35, 'REQUESTED_INFO',       'VenueApplications', 31, 'Requested photos of interior.'),
   (32,   NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 32, 'Bakery certification up to date.'),
   (33,   NULL, 34, 'REQUESTED_INFO',       'VenueApplications', 33, 'Nightclub permit pending city review.'),
   (34,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 34, 'Brewery license and outdoor permits clear.'),
   (35,   NULL, 36, 'REQUESTED_INFO',       'VenueApplications', 35, 'Requested sample menus.'),
   (NULL, 11,   34, 'RESOLVED_REPORT',      'Reviews',           3,  'Review removed after verification.'),
   (NULL, 12,   35, 'FLAGGED_REVIEW',       'Reviews',           7,  'Flagged for defamation review.'),
   (NULL, 13,   36, 'DISMISSED_REPORT',     'Reviews',           15, 'Plagiarism claim not supported.'),
   (NULL, 14,   34, 'RESOLVED_REPORT',      'Reviews',           22, 'Fake review removed.'),
   (NULL, 16,   35, 'RESOLVED_REPORT',      'Reviews',           28, 'Harassment removed, warning issued.'),
   (NULL, 17,   36, 'FLAGGED_REVIEW',       'Reviews',           11, 'Suspicious account flagged.'),
   (NULL, 19,   34, 'RESOLVED_REPORT',      'Users',             NULL,'Owner account suspended for spam.'),
   (NULL, 22,   35, 'RESOLVED_REPORT',      'Reviews',           24, 'Hate speech removed and user banned.'),
   (NULL, 29,   36, 'RESOLVED_REPORT',      'Reviews',           37, 'Removed slurs, banned user.'),
   (NULL, 32,   34, 'DISMISSED_REPORT',     'Reviews',           48, 'Not enough evidence of automation.'),
   (NULL, 35,   35, 'RESOLVED_REPORT',      'Reviews',           26, 'Removed and escalated to HR policy.'),
   (NULL, 38,   36, 'RESOLVED_REPORT',      'Reviews',           10, 'Paid review removed, venue warned.'),
   (NULL, 45,   34, 'RESOLVED_REPORT',      'Reviews',           25, 'Privacy violation removed.'),
   (36,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 36, 'Library concept approved, licenses in order.'),
   (38,   NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 38, 'Permits clear, approved.'),
   (42,   NULL, 34, 'APPROVED_APPLICATION', 'VenueApplications', 42, 'Wellness cafe approved.'),
   (44,   NULL, 35, 'APPROVED_APPLICATION', 'VenueApplications', 44, 'Entertainment permit verified.'),
   (47,   NULL, 36, 'APPROVED_APPLICATION', 'VenueApplications', 47, 'Historic use permit confirmed.');
 