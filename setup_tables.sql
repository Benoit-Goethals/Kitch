

-- This script creates the tables for the database. It is assumed that the database is already created and connected.




DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    address_id INT GENERATED ALWAYS AS IDENTITY,
    street VARCHAR(100),
    house_number VARCHAR(10),
    postal_code VARCHAR(4),
    city VARCHAR(25),
    PRIMARY KEY (address_id)
)

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

INSERT INTO person (name_first, name_last, name_title, phone_number, email) 
VALUES
    ('Marijn', 'Vandenholen', 'Mr.', '0123456789', 'marijn.vandenholen@example.com'),
    ('Benoit', 'achternaam', 'Mr.', '9876543210', 'benoit.achternaam@example.com'),
    ('John', 'Doe', 'Mr.', '1234567890', 'john.doe@example.com'),
    ('Jane', 'Smith', 'Ms.', '0987654321', 'jane.smith@example.com'),
    ('Alice', 'Johnson', 'Dr.', '5551234567', 'alice.johnson@example.com'),
    ('Bob', 'Brown', 'Prof.', '5559876543', 'bob.brown@example.com'),
    ('Charlie', 'Davis', 'Mr.', '5555555555', 'charlie.davis@example.com')
;


DROP TABLE IF EXISTS company CASCADE;
CREATE TABLE company (
    company_id INT GENERATED ALWAYS AS IDENTITY,
    address_id INT,
    company_name VARCHAR(100) NOT NULL,
    contactperson_id INT,
    tax_number VARCHAR(20),
    PRIMARY KEY (company_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (contactperson_id) REFERENCES person(person_id)
)

insert into company (address_id, contactperson_id, tax_number)  
VALUES
    (1, 1, '123456789'),
    (2, 2, '987654321'),
    (3, 3, '456789123'),
    (4, 4, '321654987'),
    (5, 5, '789123456'),
    (6, 6, '654321789'),
    (7, 7, '159753486'),
    (8, 8, '753159852'),
    (9, 9, '951753468'),
    (10, 10, '357951468'),
    (11, 11, '258147369'),
    (12, 12, '369258147'),
    (13, 13, '147258369'),
    (14, 14, '258963147'),
    (15, 15, '963258741')


DROP TABLE IF EXISTS client CASCADE;
CREATE TABLE client (
    client_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (client_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
)





DROP TABLE IF EXISTS assignment CASCADE;
CREATE TABLE assignment (
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    client_id INT,
    calculator_id INT,
    salesman_id INT,
    project_leader_id INT,
    scheduling VARCHAR(10),
    acceptance_date DATE,
    date_start DATE,
    date_end DATE,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (client_id) REFERENCES person(person_id),
    FOREIGN KEY (calculator_id) REFERENCES person(person_id),
    FOREIGN KEY (salesman_id) REFERENCES person(person_id),
    FOREIGN KEY (project_leader_id) REFERENCES person(person_id)
)


DROP TABLE IF EXISTS subassignment CASCADE;
CREATE TABLE subassignment (
    subassignment_id INT GENERATED ALWAYS AS IDENTITY,
    assignment_id INT,
    address_id INT,
    sub_name VARCHAR(100),
    PRIMARY KEY (subassignment_id),
    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id)
)


DROP TABLE IF EXISTS assignmentline CASCADE;    
CREATE TABLE assignmentline (
    assignmentline_id INT GENERATED ALWAYS AS IDENTITY,
    subassignment_id INT,
    sales_price DECIMAL(10, 2),
    PRIMARY KEY (assignmentline_id),
    FOREIGN KEY (subassignment_id) REFERENCES subassignment(subassignment_id)
)


DROP TABLE IF EXISTS article CASCADE;
CREATE TABLE article (
    article_id INT GENERATED ALWAYS AS IDENTITY,
    supplier_id INT,
    supplier_code VARCHAR(20),
    purchase_price DECIMAL(10, 2),
    PRIMARY KEY (article_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
)







DROP TABLE IF EXISTS daily_assignment CASCADE;
CREATE TABLE daily_assignment (
    daily_assignment_id INT GENERATED ALWAYS AS IDENTITY,
    assignment_id INT,
    date DATE,
    assignment_description VARCHAR(100),
    PRIMARY KEY (daily_assignment_id),
    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id)
)


DROP TABLE IF EXISTS supplier CASCADE;
CREATE TABLE supplier (
    supplier_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (supplier_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
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

