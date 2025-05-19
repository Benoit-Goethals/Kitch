/*
+ queries in this file only show the first 10 rows 
+ since every table is dropped at the start of the setup and no data will be inserted with this query, only the headers will be shown
+ data needs to be loaded with insert_data.sql
*/


-- removes unnecessary messages from the console
SET client_min_messages TO WARNING;

-- Drop all tables in the correct order to avoid foreign key constraint issues

DROP TABLE IF EXISTS assignment CASCADE;
DROP TABLE IF EXISTS orderline CASCADE;
DROP TABLE IF EXISTS phase CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS article CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS address CASCADE;


-- ADDRESS
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
SELECT * FROM address
LIMIT 10
;


-- PERSON
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
SELECT * FROM person
LIMIT 10
;

-- COMPANY
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
SELECT * FROM company
LIMIT 10
;


-- CLIENT
DROP TABLE IF EXISTS client CASCADE;
CREATE TABLE client (
    client_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (client_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
SELECT * FROM client
LIMIT 10
;

-- SUPPLIER
DROP TABLE IF EXISTS supplier CASCADE;
CREATE TABLE supplier (
    supplier_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (supplier_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
SELECT * FROM supplier
LIMIT 10
;

-- ARTICLE
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
SELECT * FROM article
LIMIT 10
;

-- PROJECT
DROP TABLE IF EXISTS project CASCADE;
CREATE TABLE project (
    project_id       INT GENERATED ALWAYS AS IDENTITY,
    client_id           INT,
    calculator_id       INT NOT NULL, 
        -- there is always someone who makes the offer
    salesman_id         INT, 
        -- there are projects without a salesman
    project_leader_id   INT,
    scheduling          VARCHAR(10), 
        -- date or asap -- not necessary, just drop it?
    date_acceptance     DATE,
    date_start          DATE, --NULL = ASAP
    date_end            DATE, --NULL = ASAP
    PRIMARY KEY (project_id),
    FOREIGN KEY (client_id) REFERENCES person(person_id),
    FOREIGN KEY (calculator_id) REFERENCES person(person_id),
    FOREIGN KEY (salesman_id) REFERENCES person(person_id),
    FOREIGN KEY (project_leader_id) REFERENCES person(person_id)
)
;
SELECT * FROM project
LIMIT 10
;

-- PHASE
DROP TABLE IF EXISTS phase CASCADE;
CREATE TABLE phase (
    phase_id                INT GENERATED ALWAYS AS IDENTITY,
    project_id           INT,
    delivery_address_id     INT,
    name                VARCHAR(10),    
    description         VARCHAR(100),
    date_start_client   DATE,
    date_end_client     DATE,
    date_start_planned  DATE,
    date_end_planned    DATE,
    manworkdays         INT,
    PRIMARY KEY (phase_id),
    FOREIGN KEY (project_id) REFERENCES project(project_id),
    FOREIGN KEY (delivery_address_id) REFERENCES address(address_id)
    -- get_status() --calculated field
    -- calculated fields based on the orderlines
    -- date_ordered DATE, -- calculated field 
    -- date_received DATE, -- calculated field
    -- date_issued DATE, -- calculated field
    -- date_delivered DATE, -- calculated field
    -- date_installed DATE, -- calculated field
    -- date_invoiced DATE, -- calculated field
);
SELECT * FROM phase
LIMIT 10
;


-- ORDERLINE
DROP TABLE IF EXISTS orderline CASCADE;    
CREATE TABLE orderline (
    orderline_id  INT GENERATED ALWAYS AS IDENTITY,
    phase_id   INT,
    sales_price         DECIMAL(10, 2),
    amount              INT,
    article_id          INT,
    date_acceptance     DATE, -- date will be copied from the project
    date_ordered        DATE,
    -- date_confirmed      DATE, -- item ontbreekt en moet nog toegevoegd worden
    date_received       DATE,
    date_issued         DATE,
    date_delivered      DATE,
    date_installed      DATE,
    date_accepted       DATE,
    date_invoiced       DATE,
    date_paid           DATE,
    date_closed         DATE,
    PRIMARY KEY (orderline_id),
    FOREIGN KEY (phase_id) REFERENCES phase(phase_id)
);
SELECT * FROM orderline
LIMIT 10
;


-- ASSIGNMENT
-- this table is used to assign people to a project on a daily basis
DROP TABLE IF EXISTS assignment CASCADE;
CREATE TABLE assignment (
    assignment_id       INT GENERATED ALWAYS AS IDENTITY,
    phase_id       INT,
    person_id               INT,
    date                    DATE,
    description  VARCHAR(100),
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (phase_id) REFERENCES phase(phase_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);





/* RUNQUERY END
RUNQUERY START */ 