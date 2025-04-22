
SET client_min_messages TO WARNING;

-- ADDRESS
DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    address_id INT GENERATED ALWAYS AS IDENTITY,
    street VARCHAR(100) NOT NULL,
    house_number VARCHAR(10) NOT NULL,
    postal_code VARCHAR(4) NOT NULL, -- must be exactly 4 digits
    city VARCHAR(25) NOT NULL, -- bestaat er een controle voor gemeente in belgie
    longitude DECIMAL(10, 8), -- onetime api call to get the coordinates
    latitude DECIMAL(10, 8), -- onetime api call to get the coordinates
    -- region() calculated field ovl wvl bxl lim,...
    PRIMARY KEY (address_id)
)
;
INSERT INTO address (street, house_number, postal_code, city)
VALUES
    ('Hoofdstraat', '123', '1000', 'Brussel'),
    ('Kerkstraat', '456', '2000', 'Antwerpen'),
    ('Stationsstraat', '789', '3000', 'Leuven'),
    ('Dorpsstraat', '101', '8500', 'Kortrijk'),
    ('Marktplein', '314', '9000', 'Gent'),
    ('Boslaan', '171', '3500', 'Hasselt'),
    ('Zeedijk', '202', '8400', 'Oostende'),
    ('Mechelsesteenweg', '232', '2800', 'Mechelen'),
    ('Groenplaats', '262', '2300', 'Turnhout'),
    ('Koningin Astridlaan', '293', '1500', 'Halle'),
    ('Vrijheidslaan', '323', '8000', 'Brugge'),
    ('Leopoldlaan', '363', '3700', 'Tongeren'),
    ('Parklaan', '394', '4000', 'Luik'),
    ('Nieuwstraat', '424', '7000', 'Mons'),
    ('Rijksweg', '454', '7700', 'Moeskroen')
;
SELECT * FROM address;

-- PERSON
DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id INT GENERATED ALWAYS AS IDENTITY,
    name_first VARCHAR(50) NOT NULL,
    name_last VARCHAR(50) NOT NULL,
    name_title VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    PRIMARY KEY (person_id)
)
;
INSERT INTO person (name_first, name_last, name_title, phone_number, email) 
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
DROP TABLE IF EXISTS company CASCADE;
CREATE TABLE company (
    company_id INT GENERATED ALWAYS AS IDENTITY,
    address_id INT,
    company_name VARCHAR(100) NOT NULL,
    contactperson_id INT,
    tax_number VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY (company_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (contactperson_id) REFERENCES person(person_id)
);
insert into company (tax_number, address_id, company_name, contactperson_id)  
VALUES
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
    ('258147369', 11, 'Company K', 11),
    ('369258147', 12, 'Company L', 12),
    ('147258369', 13, 'Company M', 13),
    ('258963147', 14, 'Company N', 14),
    ('963258741', 15, 'Company O', 15)
;
SELECT * FROM company
;

-- CLIENT
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
DROP TABLE IF EXISTS article CASCADE;
CREATE TABLE article (
    article_id INT GENERATED ALWAYS AS IDENTITY,
    supplier_id INT,
    supplier_article_code VARCHAR(40),
    purchase_price DECIMAL(10, 2),
    description VARCHAR(100),
    PRIMARY KEY (article_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
);
INSERT INTO article (supplier_id, supplier_article_code, purchase_price, description)
    VALUES  
    (1, 'ART001', 10.00, 'Description for article 1'),
    (2, 'ART002', 15.50, 'Description for article 2'),
    (3, 'ART003', 20.00, 'Description for article 3'),
    (4, 'ART004', 25.75, 'Description for article 4'),
    (5, 'ART005', 30.00, 'Description for article 5')
    ;
SELECT * FROM article;

-- ASSIGNMENT
DROP TABLE IF EXISTS assignment CASCADE;
CREATE TABLE assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    client_id INT,
    calculator_id INT NOT NULL, -- there is always someone who makes the offer
    salesman_id INT, -- there are assignments without a salesman
    project_leader_id INT,
    scheduling VARCHAR(10), -- date or asap -- not necessary, just drop it
    date_acceptance DATE NOT NULL,
    date_start DATE,
    date_end DATE,
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
    ,(1, 5, 6, NULL, '2023-01-02', '2023-01-03', NULL)
    ,(8, 9, NULL, 11, '2023-01-03', NULL, NULL)
    ,(12, 13, 14, NULL, '2023-01-04', '2023-01-05', '2023-01-10')
    ,(16, 17, NULL, 19, '2023-01-05', '2023-01-06', '2023-01-08')
    ,(1, 2, 3, NULL, '2023-01-06', NULL, '2023-01-09')
    ,(5, 6, NULL, 8, '2023-01-07', '2023-01-08', NULL)
    ,(9, 10, 11, NULL, '2023-01-08', '2023-01-09', '2023-01-12')
    ,(13, 14, NULL, 16, '2023-01-09', NULL, NULL)
    ,(17, 18, 19, NULL, '2023-01-10', '2023-01-11', '2023-01-15')
;
SELECT * FROM assignment;


-- SUBASSIGNMENT
DROP TABLE IF EXISTS subassignment CASCADE;
CREATE TABLE sub_assignment (
    sub_assignment_id INT GENERATED ALWAYS AS IDENTITY,
    assignment_id INT,
    address_id INT,
    sub_name VARCHAR(10),
    sub_description VARCHAR(100),
    PRIMARY KEY (sub_assignment_id),
    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id)
);
SELECT * FROM sub_assignment;
INSERT INTO sub_assignment (
      assignment_id
    , address_id
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

/*
-- ASSIGNMENTLINE
DROP TABLE IF EXISTS assignmentline CASCADE;    
CREATE TABLE assignmentline (
    assignmentline_id INT GENERATED ALWAYS AS IDENTITY,
    sub_assignment_id INT,
    sales_price DECIMAL(10, 2),
    amount INT,
    article_id INT,
    PRIMARY KEY (assignmentline_id),
    FOREIGN KEY (subassignment_id) REFERENCES subassignment(subassignment_id)
)
INSERT INTO assignmentline (
      sub_assignment_id
    , sales_price
    , amount
    , article_id
)VALUES
    (1, 100.00, 10, 1),
    (1, 200.00, 5, 2),
    (2, 150.00, 8, 3),
    (2, 250.00, 12, 4),
    (3, 300.00, 15, 5),
    (4, 350.00, 20, 1),
    (4, 400.00, 25, 2),
    (5, 450.00, 30, 3)
 
;
SELECT * FROM assignmentline;

DROP TABLE IF EXISTS daily_assignment CASCADE;
CREATE TABLE daily_assignment (
    daily_assignment_id INT GENERATED ALWAYS AS IDENTITY,
    assignment_id INT,
    date DATE,
    assignment_description VARCHAR(100),
    PRIMARY KEY (daily_assignment_id),
    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id)
)




DROP TABLE IF EXISTS daily_assignment_line CASCADE;
CREATE TABLE daily_assignment_line (
    daily_assignment_line_id INT GENERATED ALWAYS AS IDENTITY,
    assignmentline_id INT,
    person_id INT,
    assignment_description VARCHAR(100),
    PRIMARY KEY (daily_assignment_line_id),
    FOREIGN KEY (assignmentline_id) REFERENCES assignmentline(assignmentline_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
)

*/
