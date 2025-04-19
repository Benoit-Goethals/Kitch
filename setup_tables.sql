

-- This script creates the tables for the database. It is assumed that the database is already created and connected.

DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id INT GENERATED ALWAYS AS IDENTITY,

    PRIMARY KEY (person_id)
)


DROP TABLE IF EXISTS company CASCADE;
CREATE TABLE company (
    company_id INT GENERATED ALWAYS AS IDENTITY,
    address_id INT,
    contactperson_id INT,
    tax_number VARCHAR(20),
    PRIMARY KEY (company_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (contactperson_id) REFERENCES person(person_id)
)


DROP TABLE IF EXISTS client CASCADE;
CREATE TABLE client (
    client_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (client_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
)


DROP TABLE IF EXISTS address CASCADE;
CREATE TABLE address (
    address_id INT GENERATED ALWAYS AS IDENTITY,
    street VARCHAR(100),
    house_number VARCHAR(10),
    postal_code VARCHAR(4),
    city VARCHAR(25),
    PRIMARY KEY (address_id)
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


DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id INT GENERATED ALWAYS AS IDENTITY,
    address_id INT,
    name VARCHAR(50),
    first_name VARCHAR(50),
    birth_date DATE,
    function_description VARCHAR(100),
    company_id INT,
    PRIMARY KEY (person_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
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