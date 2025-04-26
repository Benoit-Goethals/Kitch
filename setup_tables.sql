
SET client_min_messages TO WARNING;
-- removes unnecessary messages from the console


-- Drop all tables in the correct order to avoid foreign key constraint issues
/*
DROP TABLE IF EXISTS day_assignment_line CASCADE;
DROP TABLE IF EXISTS day_assignment CASCADE;
DROP TABLE IF EXISTS assignment_line CASCADE;
DROP TABLE IF EXISTS sub_assignment CASCADE;
DROP TABLE IF EXISTS assignment CASCADE;
DROP TABLE IF EXISTS article CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS address CASCADE;
*/


-- ADDRESS
-- this table is used to store to store adresses in general
-- it is used for persons, clients and suppliers, which will refer to this table
DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    address_id      INT GENERATED ALWAYS AS IDENTITY,
    street          VARCHAR(100) NOT NULL,
    house_number    VARCHAR(10) NOT NULL,
    postal_code     VARCHAR(4) NOT NULL, 
        -- must be exactly 4 digits
    municipality            VARCHAR(25) NOT NULL, 
        -- is there an api to check municipality against postalcode??
    country         VARCHAR(50) DEFAULT 'BE',       
        -- default value for the country
    longitude       DECIMAL(10, 8) DEFAULT NULL, 
        -- onetime api call to get the coordinates
    latitude        DECIMAL(10, 8) DEFAULT NULL, 
        -- onetime api call to get the coordinates
    -- region() calculated field ovl wvl bxl lim,...
    PRIMARY KEY (address_id)
)
;
INSERT INTO address (
    street
    , house_number
    , postal_code
    , municipality
    , country
    )
VALUES
    ('Hoofdstraat', '123', '1000', 'Brussel', 'BE'),
    ('Kerkstraat', '456', '2000', 'Antwerpen', 'BE'),
    ('Stationsstraat', '789', '3000', 'Leuven', 'BE'),
    ('Dorpsstraat', '101', '8500', 'Kortrijk', 'BE'),
    ('Marktplein', '314', '9000', 'Gent', 'BE'),
    ('Boslaan', '171', '3500', 'Hasselt', 'BE'),
    ('Zeedijk', '202', '8400', 'Oostende', 'BE'),
    ('Mechelsesteenweg', '232', '2800', 'Mechelen', 'BE'),
    ('Groenplaats', '262', '2300', 'Turnhout', 'BE'),
    ('Koningin Astridlaan', '293', '1500', 'Halle', 'BE'),
    ('Vrijheidslaan', '323', '8000', 'Brugge', 'BE'),
    ('Leopoldlaan', '363', '3700', 'Tongeren', 'BE'),
    ('Parklaan', '394', '4000', 'Luik', 'BE'),
    ('Nieuwstraat', '424', '7000', 'Mons', 'BE'),
    ('Rijksweg', '454', '7700', 'Moeskroen', 'BE')
;
SELECT * FROM address;


-- PERSON
-- this table is used to store people in general
-- it is used for both internal people, client-persons and supplier-persons
-- people who are part of ... will be refered to by the person_id
DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id       INT GENERATED ALWAYS AS IDENTITY,
    address_id      INT,
    name_first      VARCHAR(50) NOT NULL,
    name_last       VARCHAR(50) NOT NULL,
    name_title      VARCHAR(50),
    job_description VARCHAR(50),
    date_of_birth   DATE, --date check
    phone_number    VARCHAR(20),
    email           VARCHAR(100),
    PRIMARY KEY (person_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id)
);
INSERT INTO person (
      name_first
    , name_last
    , name_title
    , phone_number
    , email) 
VALUES
    ('Marijn', 'Vandenholen', 'Dhr.', '0123456789', 'marijn.vandenholen@example.com'),
    ('Benoit', 'Goethals', 'Dhr.', '9876543210', 'benoit.peeters@example.com'),
    ('Jan', 'Jansen', 'Dhr.', '1234567890', 'jan.jansen@example.com'),
    ('Sofie', 'Vermeulen', 'Mevr.', '0987654321', 'sofie.vermeulen@example.com'),
    ('Annelies', 'De Smet', 'Dr.', '5551234567', 'annelies.desmet@example.com'),
    ('Bart', 'De Vries', 'Prof.', '5559876543', 'bart.devries@example.com'),
    ('Karel', 'Maes', 'Dhr.', '5555555555', 'karel.maes@example.com'),
    ('Diana', 'Van den Broeck', 'Mevr.', '5554444444', 'diana.vandenbroeck@example.com'),
    ('Ewout', 'De Clercq', 'Dhr.', '5553333333', 'ewout.declercq@example.com'),
    ('Fien', 'Van Damme', 'Mevr.', '5552222222', 'fien.vandamme@example.com'),
    ('Geert', 'De Jong', 'Dhr.', '5551111111', 'geert.dejong@example.com'),
    ('Hanne', 'De Bruyne', 'Mevr.', '5556667777', 'hanne.debruyne@example.com'),
    ('Tom', 'Van Acker', 'Dhr.', '5557778888', 'tom.vanacker@example.com'),
    ('Lies', 'Peeters', 'Mevr.', '5558889999', 'lies.peeters@example.com'),
    ('Koen', 'Claes', 'Dhr.', '5559990000', 'koen.claes@example.com'),
    ('Eva', 'Janssens', 'Mevr.', '5550001111', 'eva.janssens@example.com'),
    ('Pieter', 'De Vos', 'Dhr.', '5551112222', 'pieter.devos@example.com'),
    ('Sara', 'Van Dijk', 'Mevr.', '5552223333', 'sara.vandijk@example.com'),
    ('Lucas', 'Verhoeven', 'Dhr.', '5553334444', 'lucas.verhoeven@example.com'),
    ('Emma', 'De Wilde', 'Mevr.', '5554445555', 'emma.dewilde@example.com'),
    ('Jeroen', 'Van Dam', 'Dhr.', '5555556666', 'jeroen.vandam@example.com')
;
SELECT * FROM person
;

-- COMPANY
-- this table is used to store companies in general
-- it is used for both clients and suppliers
-- the the table client and supplier refer to this table, but share all attributes (except the id)
-- the table client and supplier are used to store the clients and suppliers in a more specific way
DROP TABLE IF EXISTS company CASCADE;
CREATE TABLE company (
    company_id          INT GENERATED ALWAYS AS IDENTITY,
    address_id          INT,
    contactperson_id    INT,
    company_name        VARCHAR(100) NOT NULL,
    tax_number          VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY (company_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (contactperson_id) REFERENCES person(person_id)
);
INSERT INTO company (
    tax_number
    , address_id
    , company_name
    , contactperson_id
    )  
VALUES
    -- used as clients in the example
    ('123456789', 1, 'Company A', 1),
    ('987654321', 2, 'Company B', 2),
    ('456789123', 3, 'Company C', 3),
    ('321654987', 4, 'Company D', 4),
    ('789123456', 5, 'Company E', 5),
    ('654321789', 6, 'Company F', 6),
    ('159753486', 7, 'Company G', 7),
    ('753159852', 8, 'Company H', 8),
    ('951753468', 9, 'Company I', 9),
    ('357951468', 10, 'Company J', 10),
    -- used as suppliers in the example
    ('258147369', 11, 'Company K', 11),
    ('369258147', 12, 'Company L', 12),
    ('147258369', 13, 'Company M', 13),
    ('258963147', 14, 'Company N', 14),
    ('963258741', 15, 'Company O', 15)
;
SELECT * FROM company
;
-- CLIENT
-- this table is used to store clients (and separate clients from suppliers)
-- a client will be created by adding a company by the company-id
-- The table client doesn't have specific attributes, but defines a company as a client by adding a company by the company-id
DROP TABLE IF EXISTS client CASCADE;
CREATE TABLE client (
    client_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (client_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
INSERT INTO client (company_id) 
    VALUES 
        (1), 
        (2), 
        (3), 
        (4), 
        (5), 
        (6), 
        (7), 
        (8), 
        (9), 
        (10)
        ;
SELECT * FROM client
;

-- SUPPLIER
-- This table is used to store supppliers (and separate suppliers from clients)
-- A supplier will be created by adding a company by the company-id
-- The table supplier doesn't have specific attributes, but defines a company as a supplier by adding a company by the company-id
DROP TABLE IF EXISTS supplier CASCADE;
CREATE TABLE supplier (
    supplier_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (supplier_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
INSERT INTO supplier (company_id) 
    VALUES 
        (11), 
        (12), 
        (13), 
        (14), 
        (15);
SELECT * FROM supplier;

-- ARTICLE
-- an article is a product that can be bought from a supplier
-- an article is linked to a supplier by the supplier_id and has a purchase price and a description
-- the supplier_arcticle_code is the code that the supplier uses to identify the article
-- the article_id is the unique identifier for the article in the system    
DROP TABLE IF EXISTS article CASCADE;
CREATE TABLE article (
    article_id              INT GENERATED ALWAYS AS IDENTITY,
    supplier_id             INT,
    supplier_article_code   VARCHAR(40),
    purchase_price          DECIMAL(10, 2),
    description             VARCHAR(100),
    PRIMARY KEY (article_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);
INSERT INTO article (
      supplier_id
    , supplier_article_code
    , purchase_price
    , description
    )
    VALUES  
      (1, 'ART001', 10.00, 'Description for article 1')
    , (1, 'ART002', 12.50, 'Description for article 2')
    , (1, 'ART003', 15.00, 'Description for article 3')
    , (2, 'ART004', 20.00, 'Description for article 4')
    , (2, 'ART005', 22.50, 'Description for article 5')
    , (2, 'ART006', 25.00, 'Description for article 6')
    , (3, 'ART007', 30.00, 'Description for article 7')
    , (3, 'ART008', 32.50, 'Description for article 8')
    , (3, 'ART009', 35.00, 'Description for article 9')
    , (4, 'ART010', 40.00, 'Description for article 10')
    , (4, 'ART011', 42.50, 'Description for article 11')
    , (4, 'ART012', 45.00, 'Description for article 12')
    , (5, 'ART013', 50.00, 'Description for article 13')
    , (5, 'ART014', 52.50, 'Description for article 14')
    , (5, 'ART015', 55.00, 'Description for article 15')
    ;
SELECT * FROM article;

-- ASSIGNMENT
-- TODO: renaming to project instead of assignment?
-- this table is used to store assignments
-- an assignment is a project that is assigned to the firm "Kitch" by a client
-- it is the overal grouping of all sub-assignments (and all assignment lines which are part of sub-assignements)

DROP TABLE IF EXISTS assignment CASCADE;
CREATE TABLE assignment (
    assignment_id       INT GENERATED ALWAYS AS IDENTITY,
    client_id           INT,
    calculator_id       INT NOT NULL, 
        -- there is always someone who makes the offer
    salesman_id         INT, 
        -- there are assignments without a salesman
    project_leader_id   INT,
    scheduling          VARCHAR(10), 
        -- date or asap -- not necessary, just drop it?
    date_acceptance     DATE NOT NULL,
    date_start          DATE, --NULL = ASAP
    date_end            DATE, --NULL = ASAP
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (client_id) REFERENCES person(person_id),
    FOREIGN KEY (calculator_id) REFERENCES person(person_id),
    FOREIGN KEY (salesman_id) REFERENCES person(person_id),
    FOREIGN KEY (project_leader_id) REFERENCES person(person_id)
);
INSERT INTO assignment (
      client_id
    , calculator_id
    , salesman_id
    , project_leader_id
    , date_acceptance
    , date_start
    , date_end
)
VALUES
      (1, 2, NULL, 4, '2023-01-01', '2023-01-02', '2023-01-05')
    , (1, 5, 6, NULL, '2023-01-02', '2023-01-03', NULL)
    , (8, 9, NULL, 11, '2023-01-03', NULL, NULL)
    , (12, 13, 14, NULL, '2023-01-04', '2023-01-05', '2023-01-10')
    , (16, 17, NULL, 19, '2023-01-05', '2023-01-06', '2023-01-08')
    , (1, 2, 3, NULL, '2023-01-06', NULL, '2023-01-09')
    , (5, 6, NULL, 8, '2023-01-07', '2023-01-08', NULL)
    , (9, 10, 11, NULL, '2023-01-08', '2023-01-09', '2023-01-12')
    , (13, 14, NULL, 16, '2023-01-09', NULL, NULL)
    , (17, 18, 19, NULL, '2023-01-10', '2023-01-11', '2023-01-15')
;
SELECT * FROM assignment;


-- SUBASSIGNMENT
-- this table is used to store sub-assignments
-- a sub-assignment is more like a phase of the assignment.
-- for isntance, a project can be divided into several phases, each with its own sub-assignment:
    -- 1. phase 1: delivery of items
    -- 2. phase 2: entering the items and putting into place
    -- 3. phase 3: connectiong the items to the electricity and water supply
    -- 4. phase 4: testing the items
-- a planner is free to decide how many sub-assignments he wants to create for a project, and what name he wants to give them (since it will be different for every project/assignment)

DROP TABLE IF EXISTS sub_assignment CASCADE;
CREATE TABLE sub_assignment (
    sub_assignment_id       INT GENERATED ALWAYS AS IDENTITY,
    assignment_id           INT,
    delivery_address_id     INT,
    sub_name                VARCHAR(10),
    sub_description         VARCHAR(100),
    PRIMARY KEY (sub_assignment_id),
    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id),
    FOREIGN KEY (delivery_address_id) REFERENCES address(address_id)
    -- get_status() --calculated field
    -- calculated fields based on the assignment lines
    -- date_ordered DATE, -- calculated field 
    -- date_received DATE, -- calculated field
    -- date_issued DATE, -- calculated field
    -- date_delivered DATE, -- calculated field
    -- date_installed DATE, -- calculated field
    -- date_invoiced DATE, -- calculated field
);
INSERT INTO sub_assignment (
      assignment_id
    , delivery_address_id
    , sub_name
    , sub_description
    )
VALUES
      (1, 1, 'Sub1', 'Description for Project1 Sub1')
    , (1, 2, 'Sub2', 'Description for Project1 Sub2')
    , (1, 3, 'Sub3', 'Description for Project1 Sub3')
    , (2, 1, 'Sub1', 'Description for Project2 Sub1')
    , (2, 2, 'Sub2', 'Description for Project2 Sub2')   
    , (3, 1, 'Sub1', 'Description for Project3 Sub1')
;
SELECT * FROM sub_assignment;

-- assignment_line
DROP TABLE IF EXISTS assignment_line CASCADE;    
CREATE TABLE assignment_line (
    assignment_line_id  INT GENERATED ALWAYS AS IDENTITY,
    sub_assignment_id   INT,
    sales_price         DECIMAL(10, 2),
    amount              INT,
    article_id          INT,
    date_acceptance     DATE, -- date will be copied from the assignment
    date_ordered        DATE,
    date_received       DATE,
    date_issued         DATE,
    date_delivered      DATE,
    date_installed      DATE,
    date_accepted       DATE,
    date_invoiced       DATE,
    date_paid           DATE,
    date_closed         DATE,
    PRIMARY KEY (assignment_line_id),
    FOREIGN KEY (sub_assignment_id) REFERENCES sub_assignment(sub_assignment_id)
);
INSERT INTO assignment_line (
      sub_assignment_id
    , sales_price
    , amount
    , article_id
)VALUES
      (1, 100.00, 10, 1)
    , (1, 200.00, 5, 2)
    , (2, 150.00, 8, 3)
    , (2, 250.00, 12, 4)
    , (3, 300.00, 15, 5)
    , (4, 350.00, 20, 1)
    , (4, 400.00, 25, 2)
    , (5, 450.00, 30, 3)
    ;
SELECT * FROM assignment_line;


-- DAYASSIGNMENT
-- this table is used to assign people to a project on a daily basis
DROP TABLE IF EXISTS day_assignment CASCADE;
CREATE TABLE day_assignment (
    day_assignment_id       INT GENERATED ALWAYS AS IDENTITY,
    sub_assignment_id       INT,
    person_id               INT,
    date                    DATE,
    assignment_description  VARCHAR(100),
    PRIMARY KEY (day_assignment_id),
    FOREIGN KEY (sub_assignment_id) REFERENCES sub_assignment(sub_assignment_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);
INSERT INTO day_assignment (
      sub_assignment_id
    , date
    , assignment_description
    )
    VALUES
          (1, '2023-01-01', 'Daily assignment for assignment1')
        , (2, '2023-01-02', 'Daily assignment for assignment2')
        , (3, '2023-01-03', 'Daily assignment for assignment3')
        , (4, '2023-01-04', 'Daily assignment for assignment4')
        , (5, '2023-01-05', 'Daily assignment for assignment5')
        ;
SELECT * FROM day_assignment;



/*



*/