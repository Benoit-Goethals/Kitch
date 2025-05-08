
-- removes unnecessary messages from the console
SET client_min_messages TO WARNING;

-- Drop all tables in the correct order to avoid foreign key constraint issues
DROP TABLE IF EXISTS address CASCADE;
DROP TABLE IF EXISTS person CASCADE;

DROP TABLE IF EXISTS assignment CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS phase CASCADE;
DROP TABLE IF EXISTS orderline CASCADE;
DROP TABLE IF EXISTS article CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS company CASCADE;


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
OFFSET (SELECT COUNT(*) FROM address) - 10; -- last 10 lines


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
-- LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM person) - 10; -- last 10 lines
;


/* RUNQUERY END



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
INSERT INTO company (
    tax_number
    , address_id
    , company_name
    , contactperson_id
    )  
VALUES
    -- 80 clients
    ('123456789', 1, 'Client A', 1),
    ('987654321', 2, 'Client B', 2),
    ('456789123', 3, 'Client C', 3),
    ('321654987', 4, 'Client D', 4),
    ('789123456', 5, 'Client E', 5),
    ('654321789', 6, 'Client F', 6),
    ('159753486', 7, 'Client G', 7),
    ('753154852', 8, 'Client H', 8),
    ('951753468', 9, 'Client I', 9),
    ('357951468', 10, 'Client J', 10),
    ('123987456', 11, 'Client K', 11),
    ('987123654', 12, 'Client L', 12),
    ('456321789', 13, 'Client M', 13),
    ('321987654', 14, 'Client N', 14),
    ('789654123', 15, 'Client O', 15),
    ('654789321', 16, 'Client P', 16),
    ('159486753', 17, 'Client Q', 17),
    ('752852159', 18, 'Client R', 18),
    ('951468357', 19, 'Client S', 19),
    ('357468951', 20, 'Client T', 20),
    ('123654789', 21, 'Client U', 21),
    ('987456123', 22, 'Client V', 22),
    ('456987321', 23, 'Client W', 23),
    ('321123987', 24, 'Client X', 24),
    ('789321654', 25, 'Client Y', 25),
    ('654123987', 26, 'Client Z', 26),
    ('159753159', 27, 'Client AA', 27),
    ('753159753', 28, 'Client AB', 28),
    ('951753951', 29, 'Client AC', 29),
    ('357951357', 30, 'Client AD', 30),
    ('123321456', 31, 'Client AE', 31),
    ('987789123', 32, 'Client AF', 32),
    ('456654789', 33, 'Client AG', 33),
    ('321456987', 34, 'Client AH', 34),
    ('789987321', 35, 'Client AI', 35),
    ('654321123', 36, 'Client AJ', 36),
    ('159486159', 37, 'Client AK', 37),
    ('753852753', 38, 'Client AL', 38),
    ('951468952', 39, 'Client AM', 39),
    ('357468358', 40, 'Client AN', 40),
    ('123654123', 41, 'Client AO', 41),
    ('987456987', 42, 'Client AP', 42),
    ('456987654', 43, 'Client AQ', 43),
    ('321123321', 44, 'Client AR', 44),
    ('789321987', 45, 'Client AS', 45),
    ('654123654', 46, 'Client AT', 46),
    ('169753486', 47, 'Client AU', 47),
    ('753159852', 48, 'Client AV', 48),
    ('951750468', 49, 'Client AW', 49),
    ('357953468', 50, 'Client AX', 50),
    ('123987654', 51, 'Client AY', 51),
    ('987123456', 52, 'Client AZ', 52),
    ('456321987', 53, 'Client BA', 53),
    ('321987123', 54, 'Client BB', 54),
    ('789654321', 55, 'Client BC', 55),
    ('654789123', 56, 'Client BD', 56),
    ('159486853', 57, 'Client BE', 57),
    ('753852951', 58, 'Client BF', 58),
    ('951468753', 59, 'Client BG', 59),
    ('357468159', 60, 'Client BH', 60),
    ('123654951', 61, 'Client BI', 61),
    ('987456753', 62, 'Client BJ', 62),
    ('456987159', 63, 'Client BK', 63),
    ('321123753', 64, 'Client BL', 64),
    ('789321159', 65, 'Client BM', 65),
    ('654123951', 66, 'Client BN', 66),
    ('159753357', 67, 'Client BO', 67),
    ('753159456', 68, 'Client BP', 68),
    ('951753654', 69, 'Client BQ', 69),
    ('357951852', 70, 'Client BR', 70),
    ('123321753', 71, 'Client BS', 71),
    ('987789456', 72, 'Client BT', 72),
    ('456654951', 73, 'Client BU', 73),
    ('321456753', 74, 'Client BV', 74),
    ('789987159', 75, 'Client BW', 75),
    ('654321357', 76, 'Client BX', 76),
    ('159486654', 77, 'Client BY', 77),
    ('753852456', 78, 'Client BZ', 78),
    ('951468123', 79, 'Client CA', 79),
    ('357468987', 80, 'Client CB', 80),
    -- 20 suppliers
    ('258147369', 81, 'Supplier CC', 81),
    ('369258147', 82, 'Supplier CD', 82),
    ('147369258', 83, 'Supplier CE', 83),
    ('258369147', 84, 'Supplier CF', 84),
    ('369147258', 85, 'Supplier CG', 85),
    ('147258369', 86, 'Supplier CH', 86),
    ('258147368', 87, 'Supplier CI', 87),
    ('369258146', 88, 'Supplier CJ', 88),
    ('147369257', 89, 'Supplier CK', 89),
    ('258369148', 90, 'Supplier CL', 90),
    ('369147259', 91, 'Supplier CM', 91),
    ('147258370', 92, 'Supplier CN', 92),
    ('258147371', 93, 'Supplier CO', 93),
    ('369258372', 94, 'Supplier CP', 94),
    ('147369373', 95, 'Supplier CQ', 95),
    ('258369374', 96, 'Supplier CR', 96),
    ('369147375', 97, 'Supplier CS', 97),
    ('147258376', 98, 'Supplier CT', 98),
    ('258147377', 99, 'Supplier CU', 99),
    ('369258378', 100, 'Supplier CV', 100)


;
SELECT * FROM company
-- LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM company) - 10; -- last 10 lines
;
-- CLIENT
DROP TABLE IF EXISTS client CASCADE;
CREATE TABLE client (
    client_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (client_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
INSERT INTO client (
    company_id
)
VALUES
    (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20), (21), (22), (23), (24), (25), (26), (27), (28), (29), (30), (31), (32), (33), (34), (35), (36), (37), (38), (39), (40), (41), (42), (43), (44), (45), (46), (47), (48), (49), (50), (51), (52), (53), (54), (55), (56), (57), (58), (59), (60), (61), (62), (63), (64), (65), (66), (67), (68), (69), (70), (71), (72), (73), (74), (75), (76), (77), (78), (79), (80)
;

SELECT * FROM client
OFFSET (SELECT COUNT(*) FROM client) - 10; -- last 10 lines
;

-- SUPPLIER
DROP TABLE IF EXISTS supplier CASCADE;
CREATE TABLE supplier (
    supplier_id INT GENERATED ALWAYS AS IDENTITY,
    company_id INT,
    PRIMARY KEY (supplier_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);
INSERT INTO supplier (
    company_id
)values
(81), (82), (83), (84), (85), (86), (87), (88), (89), (90), (91), (92), (93), (94), (95), (96), (97), (98), (99), (100);
SELECT * FROM supplier
OFFSET (SELECT COUNT(*) FROM supplier) - 10 -- last 10 lines
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
INSERT INTO article (
      supplier_id
    , supplier_article_code
    , purchase_price
    , description
    )
    values
        -- 100 articles that can be sold to the client
    (1, 'ART001', 100.00, 'Description for article 1'),
    (1, 'ART002', 200.00, 'Description for article 2'),
    (1, 'ART003', 300.00, 'Description for article 3'),
    (2, 'ART004', 400.00, 'Description for article 4'),
    (2, 'ART005', 500.00, 'Description for article 5'),
    (2, 'ART006', 600.00, 'Description for article 6'),
    (3, 'ART007', 700.00, 'Description for article 7'),
    (3, 'ART008', 800.00, 'Description for article 8'),
    (3, 'ART009', 900.00, 'Description for article 9'),
    (4, 'ART010', 1000.00, 'Description for article 10'),
    (4, 'ART011', 1100.00, 'Description for article 11'),
    (4, 'ART012', 1200.00, 'Description for article 12'),
    (5, 'ART013', 1300.00, 'Description for article 13'),
    (5, 'ART014', 1400.00, 'Description for article 14'),
    (5, 'ART015', 1500.00, 'Description for article 15'),
    (6, 'ART016', 1600.00, 'Description for article 16'),
    (6, 'ART017', 1700.00, 'Description for article 17'),
    (6, 'ART018', 1800.00, 'Description for article 18'),
    (7, 'ART019', 1900.00, 'Description for article 19'),
    (7, 'ART020', 2000.00, 'Description for article 20'),
    (7, 'ART021', 2100.00, 'Description for article 21'),
    (8, 'ART022', 2200.00, 'Description for article 22'),
    (8, 'ART023', 2300.00, 'Description for article 23'),
    (8, 'ART024', 2400.00, 'Description for article 24'),
    (9, 'ART025', 2500.00, 'Description for article 25'),
    (9, 'ART026', 2600.00, 'Description for article 26'),
    (9, 'ART027', 2700.00, 'Description for article 27'),
    (10, 'ART028', 2800.00, 'Description for article 28'),
    (10, 'ART029', 2900.00, 'Description for article 29'),
    (10, 'ART030', 3000.00, 'Description for article 30'),
    (11, 'ART031', 3100.00, 'Description for article 31'),
    (11, 'ART032', 3200.00, 'Description for article 32'),
    (11, 'ART033', 3300.00, 'Description for article 33'),
    (12, 'ART034', 3400.00, 'Description for article 34'),
    (12, 'ART035', 3500.00, 'Description for article 35'),
    (12, 'ART036', 3600.00, 'Description for article 36'),
    (13, 'ART037', 3700.00, 'Description for article 37'),
    (13, 'ART038', 3800.00, 'Description for article 38'),
    (13, 'ART039', 3900.00, 'Description for article 39'),
    (14, 'ART040', 4000.00, 'Description for article 40'),
    (14, 'ART041', 4100.00, 'Description for article 41'),
    (14, 'ART042', 4200.00, 'Description for article 42'),
    (15, 'ART043', 4300.00, 'Description for article 43'),
    (15, 'ART044', 4400.00, 'Description for article 44'),
    (15, 'ART045', 4500.00, 'Description for article 45'),
    (16, 'ART046', 4600.00, 'Description for article 46'),
    (16, 'ART047', 4700.00, 'Description for article 47'),
    (16, 'ART048', 4800.00, 'Description for article 48'),
    (17, 'ART049', 4900.00, 'Description for article 49'),
    (17, 'ART050', 5000.00, 'Description for article 50'),
    (17, 'ART051', 5100.00, 'Description for article 51'),
    (18, 'ART052', 5200.00, 'Description for article 52'),
    (18, 'ART053', 5300.00, 'Description for article 53'),
    (18, 'ART054', 5400.00, 'Description for article 54'),
    (19, 'ART055', 5500.00, 'Description for article 55'),
    (19, 'ART056', 5600.00, 'Description for article 56'),
    (19, 'ART057', 5700.00, 'Description for article 57'),
    (20, 'ART058', 5800.00, 'Description for article 58'),
    (20, 'ART059', 5900.00, 'Description for article 59'),
    (20, 'ART060', 6000.00, 'Description for article 60'),
    (1, 'ART061', 6100.00, 'Description for article 61'),
    (1, 'ART062', 6200.00, 'Description for article 62'),
    (1, 'ART063', 6300.00, 'Description for article 63'),
    (2, 'ART064', 6400.00, 'Description for article 64'),
    (2, 'ART065', 6500.00, 'Description for article 65'),
    (2, 'ART066', 6600.00, 'Description for article 66'),
    (3, 'ART067', 6700.00, 'Description for article 67'),
    (3, 'ART068', 6800.00, 'Description for article 68'),
    (3, 'ART069', 6900.00, 'Description for article 69'),
    (4, 'ART070', 7000.00, 'Description for article 70'),
    (4, 'ART071', 7100.00, 'Description for article 71'),
    (4, 'ART072', 7200.00, 'Description for article 72'),
    (5, 'ART073', 7300.00, 'Description for article 73'),
    (5, 'ART074', 7400.00, 'Description for article 74'),
    (5, 'ART075', 7500.00, 'Description for article 75'),
    (6, 'ART076', 7600.00, 'Description for article 76'),
    (6, 'ART077', 7700.00, 'Description for article 77'),
    (6, 'ART078', 7800.00, 'Description for article 78'),
    (7, 'ART079', 7900.00, 'Description for article 79'),
    (7, 'ART080', 8000.00, 'Description for article 80'),
    (7, 'ART081', 8100.00, 'Description for article 81'),
    (8, 'ART082', 8200.00, 'Description for article 82'),
    (8, 'ART083', 8300.00, 'Description for article 83'),
    (8, 'ART084', 8400.00, 'Description for article 84'),
    (9, 'ART085', 8500.00, 'Description for article 85'),
    (9, 'ART086', 8600.00, 'Description for article 86'),
    (9, 'ART087', 8700.00, 'Description for article 87'),
    (10, 'ART088', 8800.00, 'Description for article 88'),
    (10, 'ART089', 8900.00, 'Description for article 89'),
    (10, 'ART090', 9000.00, 'Description for article 90'),
    (11, 'ART091', 9100.00, 'Description for article 91'),
    (11, 'ART092', 9200.00, 'Description for article 92'),
    (11, 'ART093', 9300.00, 'Description for article 93'),
    (12, 'ART094', 9400.00, 'Description for article 94'),
    (12, 'ART095', 9500.00, 'Description for article 95'),
    (12, 'ART096', 9600.00, 'Description for article 96'),
    (13, 'ART097', 9700.00, 'Description for article 97'),
    (13, 'ART098', 9800.00, 'Description for article 98'),
    (13, 'ART099', 9900.00, 'Description for article 99'),
    (14, 'ART100', 10000.00, 'Description for article 100')
    ;
SELECT * FROM article
OFFSET (SELECT COUNT(*) FROM article) - 10 -- last 10 lines
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
INSERT INTO project (
      client_id
    , calculator_id
    , salesman_id
    , project_leader_id
    , date_acceptance
    , date_start
    , date_end
)
VALUES
    (1, 101, 108, NULL, '2010-05-15', '2010-08-15', '2010-09-15'),
    (2, 102, 108, NULL, '2005-03-12', NULL, NULL),
    (3, 103, 109, NULL, '2018-07-22', '2018-10-22', '2018-11-22'),
    (4, 104, 110, 117, '2020-11-10', NULL, NULL),
    (5, 105, 111, NULL,NULL, NULL, NULL),
    (6, 106, 112, 118, '2008-09-14', '2008-12-14', '2009-01-14'),
    (7, 107, 113, NULL, '2015-06-20', NULL, NULL),
    (8, 101, 114, 119, '2019-03-08', '2019-06-08', '2019-07-08'),
    (9, 102, 115, NULL, '2003-12-19', '2004-03-19', '2004-04-19'),
    (10, 103, 116, 120, NULL, NULL, NULL),
    (11, 104, 108, NULL, '2016-08-11', '2016-11-11', NULL),
    (12, 105, 109, 117, '2007-02-12', '2007-05-12', NULL),
    (13, 106, 110, NULL, '2013-10-13', '2014-01-13', NULL),
    (14, 107, 111, 118, '2022-01-14', '2022-04-14', '2022-05-14'),
    (15, 101, 112, NULL, '2009-05-15', NULL, NULL),
    (16, 102, 113, 119, '2017-07-16', '2017-10-16', '2017-11-16'),
    (17, 103, 114, NULL, '2004-11-17', '2005-02-17', '2005-03-17'),
    (18, 104, 115, 120, NULL, NULL, NULL),
    (19, 105, 116, NULL, '2006-09-19', '2006-12-19', '2007-01-19'),
    (20, 106, 108, 117, '2023-02-20', '2023-05-20', NULL),
    (21, 107, 109, NULL, '2011-12-21', '2012-03-21', '2012-04-21'),
    (22, 101, 110, 118, NULL, NULL, NULL),
    (23, 102, 111, NULL, '2002-04-23', NULL, NULL),
    (24, 103, 112, 119, '2018-09-24', '2018-12-24', '2019-01-24'),
    (25, 104, 113, NULL, '2001-01-25', '2001-04-25', '2001-05-25'),
    (26, 105, 114, 120, NULL, '2019-08-26', '2019-09-26'),
    (27, 106, 115, NULL, '2000-07-27', '2000-10-27', '2000-11-27'),
    (28, 107, 116, 117, '2012-10-28', NULL, '2013-02-28'),
    (29, 101, 108, NULL, '2005-03-29', '2005-06-29', '2005-07-29'),
    (30, 102, 109, 118, '2021-08-30', '2021-11-30', '2021-12-30'),
    (31, 103, 110, NULL, NULL, NULL, NULL),
    (32, 104, 111, 119, '2016-04-01', '2016-07-01', '2016-08-01'),
    (33, 105, 112, NULL, '2003-06-02', '2003-09-02', '2003-10-02'),
    (34, 106, 113, 120, '2014-11-03', NULL, '2015-03-03'),
    (35, 107, 114, NULL, '2007-02-04', '2007-05-04', NULL),
    (36, 101, 115, 117, '2022-09-05', '2022-12-05', NULL),
    (37, 102, 116, NULL, '2008-01-06', '2008-04-06', '2008-05-06'),
    (38, 103, 108, 118, NULL, NULL, NULL),
    (39, 104, 109, NULL, '2006-10-08', '2007-01-08', NULL),
    (40, 105, 110, 119, NULL, '2013-06-09', '2013-07-09'),
    (41, 106, 111, NULL, '2002-07-10', '2002-10-10', '2002-11-10'),
    (42, 107, 112, 120, NULL, NULL, NULL),
    (43, 101, 113, NULL, '2001-04-12', '2001-07-12', NULL),
    (44, 102, 114, 117, '2019-08-13', '2019-11-13', '2019-12-13'),
    (45, 103, 115, NULL, '2004-11-14', '2005-02-14', '2005-03-14'),
    (46, 104, 116, 118, '2017-02-15', NULL, NULL),
    (47, 105, 108, NULL, '2009-06-16',NULL, NULL),
    (48, 106, 109, 119, '2023-01-17', '2023-04-17', '2023-05-17'),
    (49, 107, 110, NULL, NULL, '2011-12-18', '2012-01-18'),
    (50, 101, 111, 120, '2018-03-19', '2018-06-19', '2018-07-19')
;
SELECT * FROM project
-- last 10 lines
OFFSET (SELECT COUNT(*) FROM project) - 10
; 
-- PHASE
DROP TABLE IF EXISTS phase CASCADE;
CREATE TABLE phase (
    phase_id                INT GENERATED ALWAYS AS IDENTITY,
    project_id           INT,
    delivery_address_id     INT,
    sub_name                VARCHAR(10),
    sub_description         VARCHAR(100),
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
INSERT INTO phase (
      project_id
    , delivery_address_id
    , sub_name
    , sub_description
    )
VALUES
    (1, 1, 'Phase1', 'Description for Project1 Phase1'),
    (1, 1, 'Phase2', 'Description for Project1 Phase2'),
    (1, 1, 'Phase3', 'Description for Project1 Phase3'),
    (2, 2, 'Phase1', 'Description for Project2 Phase1'),
    (2, 2, 'Phase2', 'Description for Project2 Phase2'),
    (2, 2, 'Phase3', 'Description for Project2 Phase3'),
    (3, 3, 'Phase1', 'Description for Project3 Phase1'),
    (3, 3, 'Phase2', 'Description for Project3 Phase2'),
    (3, 3, 'Phase3', 'Description for Project3 Phase3'),
    (4, 4, 'Phase1', 'Description for Project4 Phase1'),
    (4, 4, 'Phase2', 'Description for Project4 Phase2'),
    (4, 4, 'Phase3', 'Description for Project4 Phase3'),
    (5, 5, 'Phase1', 'Description for Project5 Phase1'),
    (5, 5, 'Phase2', 'Description for Project5 Phase2'),
    (5, 5, 'Phase3', 'Description for Project5 Phase3'),
    (6, 6, 'Phase1', 'Description for Project6 Phase1'),
    (6, 6, 'Phase2', 'Description for Project6 Phase2'),
    (6, 6, 'Phase3', 'Description for Project6 Phase3'),
    (7, 7, 'Phase1', 'Description for Project7 Phase1'),
    (7, 7, 'Phase2', 'Description for Project7 Phase2'),
    (7, 7, 'Phase3', 'Description for Project7 Phase3'),
    (8, 8, 'Phase1', 'Description for Project8 Phase1'),
    (8, 8, 'Phase2', 'Description for Project8 Phase2'),
    (8, 8, 'Phase3', 'Description for Project8 Phase3'),
    (9, 9, 'Phase1', 'Description for Project9 Phase1'),
    (9, 9, 'Phase2', 'Description for Project9 Phase2'),
    (9, 9, 'Phase3', 'Description for Project9 Phase3'),
    (10, 10, 'Phase1', 'Description for Project10 Phase1'),
    (10, 10, 'Phase2', 'Description for Project10 Phase2'),
    (10, 10, 'Phase3', 'Description for Project10 Phase3'),
    (11, 11, 'Phase1', 'Description for Project11 Phase1'),
    (11, 11, 'Phase2', 'Description for Project11 Phase2'),
    (11, 11, 'Phase3', 'Description for Project11 Phase3'),
    (12, 12, 'Phase1', 'Description for Project12 Phase1'),
    (12, 12, 'Phase2', 'Description for Project12 Phase2'),
    (12, 12, 'Phase3', 'Description for Project12 Phase3'),
    (13, 13, 'Phase1', 'Description for Project13 Phase1'),
    (13, 13, 'Phase2', 'Description for Project13 Phase2'),
    (13, 13, 'Phase3', 'Description for Project13 Phase3'),
    (14, 14, 'Phase1', 'Description for Project14 Phase1'),
    (14, 14, 'Phase2', 'Description for Project14 Phase2'),
    (14, 14, 'Phase3', 'Description for Project14 Phase3'),
    (15, 15, 'Phase1', 'Description for Project15 Phase1'),
    (15, 15, 'Phase2', 'Description for Project15 Phase2'),
    (15, 15, 'Phase3', 'Description for Project15 Phase3'),
    (16, 16, 'Phase1', 'Description for Project16 Phase1'),
    (16, 16, 'Phase2', 'Description for Project16 Phase2'),
    (16, 16, 'Phase3', 'Description for Project16 Phase3'),
    (17, 17, 'Phase1', 'Description for Project17 Phase1'),
    (17, 17, 'Phase2', 'Description for Project17 Phase2'),
    (17, 17, 'Phase3', 'Description for Project17 Phase3'),
    (18, 18, 'Phase1', 'Description for Project18 Phase1'),
    (18, 18, 'Phase2', 'Description for Project18 Phase2'),
    (18, 18, 'Phase3', 'Description for Project18 Phase3'),
    (19, 19, 'Phase1', 'Description for Project19 Phase1'),
    (19, 19, 'Phase2', 'Description for Project19 Phase2'),
    (19, 19, 'Phase3', 'Description for Project19 Phase3'),
    (20, 20, 'Phase1', 'Description for Project20 Phase1'),
    (20, 20, 'Phase2', 'Description for Project20 Phase2'),
    (20, 20, 'Phase3', 'Description for Project20 Phase3'),
    (21, 21, 'Phase1', 'Description for Project21 Phase1'),
    (21, 21, 'Phase2', 'Description for Project21 Phase2'),
    (21, 21, 'Phase3', 'Description for Project21 Phase3'),
    (22, 22, 'Phase1', 'Description for Project22 Phase1'),
    (22, 22, 'Phase2', 'Description for Project22 Phase2'),
    (22, 22, 'Phase3', 'Description for Project22 Phase3'),
    (23, 23, 'Phase1', 'Description for Project23 Phase1'),
    (23, 23, 'Phase2', 'Description for Project23 Phase2'),
    (23, 23, 'Phase3', 'Description for Project23 Phase3'),
    (24, 24, 'Phase1', 'Description for Project24 Phase1'),
    (24, 24, 'Phase2', 'Description for Project24 Phase2'),
    (24, 24, 'Phase3', 'Description for Project24 Phase3'),
    (25, 25, 'Phase1', 'Description for Project25 Phase1'),
    (25, 25, 'Phase2', 'Description for Project25 Phase2'),
    (25, 25, 'Phase3', 'Description for Project25 Phase3'),
    (26, 26, 'Phase1', 'Description for Project26 Phase1'),
    (26, 26, 'Phase2', 'Description for Project26 Phase2'),
    (26, 26, 'Phase3', 'Description for Project26 Phase3'),
    (27, 27, 'Phase1', 'Description for Project27 Phase1'),
    (27, 27, 'Phase2', 'Description for Project27 Phase2'),
    (27, 27, 'Phase3', 'Description for Project27 Phase3'),
    (28, 28, 'Phase1', 'Description for Project28 Phase1'),
    (28, 28, 'Phase2', 'Description for Project28 Phase2'),
    (28, 28, 'Phase3', 'Description for Project28 Phase3'),
    (29, 29, 'Phase1', 'Description for Project29 Phase1'),
    (29, 29, 'Phase2', 'Description for Project29 Phase2'),
    (29, 29, 'Phase3', 'Description for Project29 Phase3'),
    (30, 30, 'Phase1', 'Description for Project30 Phase1'),
    (30, 30, 'Phase2', 'Description for Project30 Phase2'),
    (30, 30, 'Phase3', 'Description for Project30 Phase3'),
    (31, 31, 'Phase1', 'Description for Project31 Phase1'),
    (31, 31, 'Phase2', 'Description for Project31 Phase2'),
    (31, 31, 'Phase3', 'Description for Project31 Phase3'),
    (32, 32, 'Phase1', 'Description for Project32 Phase1'),
    (32, 32, 'Phase2', 'Description for Project32 Phase2'),
    (32, 32, 'Phase3', 'Description for Project32 Phase3'),
    (33, 33, 'Phase1', 'Description for Project33 Phase1'),
    (33, 33, 'Phase2', 'Description for Project33 Phase2'),
    (33, 33, 'Phase3', 'Description for Project33 Phase3'),
    (34, 34, 'Phase1', 'Description for Project34 Phase1'),
    (34, 34, 'Phase2', 'Description for Project34 Phase2'),
    (34, 34, 'Phase3', 'Description for Project34 Phase3'),
    (35, 35, 'Phase1', 'Description for Project35 Phase1'),
    (35, 35, 'Phase2', 'Description for Project35 Phase2'),
    (35, 35, 'Phase3', 'Description for Project35 Phase3'),
    (36, 36, 'Phase1', 'Description for Project36 Phase1'),
    (36, 36, 'Phase2', 'Description for Project36 Phase2'),
    (36, 36, 'Phase3', 'Description for Project36 Phase3'),
    (37, 37, 'Phase1', 'Description for Project37 Phase1'),
    (37, 37, 'Phase2', 'Description for Project37 Phase2'),
    (37, 37, 'Phase3', 'Description for Project37 Phase3'),
    (38, 38, 'Phase1', 'Description for Project38 Phase1'),
    (38, 38, 'Phase2', 'Description for Project38 Phase2'),
    (38, 38, 'Phase3', 'Description for Project38 Phase3'),
    (39, 39, 'Phase1', 'Description for Project39 Phase1'),
    (39, 39, 'Phase2', 'Description for Project39 Phase2'),
    (39, 39, 'Phase3', 'Description for Project39 Phase3'),
    (40, 40, 'Phase1', 'Description for Project40 Phase1'),
    (40, 40, 'Phase2', 'Description for Project40 Phase2'),
    (40, 40, 'Phase3', 'Description for Project40 Phase3'),
    (41, 41, 'Phase1', 'Description for Project41 Phase1'),
    (41, 41, 'Phase2', 'Description for Project41 Phase2'),
    (41, 41, 'Phase3', 'Description for Project41 Phase3'),
    (42, 42, 'Phase1', 'Description for Project42 Phase1'),
    (42, 42, 'Phase2', 'Description for Project42 Phase2'),
    (42, 42, 'Phase3', 'Description for Project42 Phase3'),
    (43, 43, 'Phase1', 'Description for Project43 Phase1'),
    (43, 43, 'Phase2', 'Description for Project43 Phase2'),
    (43, 43, 'Phase3', 'Description for Project43 Phase3'),
    (44, 44, 'Phase1', 'Description for Project44 Phase1'),
    (44, 44, 'Phase2', 'Description for Project44 Phase2'),
    (44, 44, 'Phase3', 'Description for Project44 Phase3'),
    (45, 45, 'Phase1', 'Description for Project45 Phase1'),
    (45, 45, 'Phase2', 'Description for Project45 Phase2'),
    (45, 45, 'Phase3', 'Description for Project45 Phase3'),
    (46, 46, 'Phase1', 'Description for Project46 Phase1'),
    (46, 46, 'Phase2', 'Description for Project46 Phase2'),
    (46, 46, 'Phase3', 'Description for Project46 Phase3'),
    (47, 47, 'Phase1', 'Description for Project47 Phase1'),
    (47, 47, 'Phase2', 'Description for Project47 Phase2'),
    (47, 47, 'Phase3', 'Description for Project47 Phase3'),
    (48, 48, 'Phase1', 'Description for Project48 Phase1'),
    (48, 48, 'Phase2', 'Description for Project48 Phase2'),
    (48, 48, 'Phase3', 'Description for Project48 Phase3'),
    (49, 49, 'Phase1', 'Description for Project49 Phase1'),
    (49, 49, 'Phase2', 'Description for Project49 Phase2'),
    (49, 49, 'Phase3', 'Description for Project49 Phase3'),
    (50, 50, 'Phase1', 'Description for Project50 Phase1'),
    (50, 50, 'Phase2', 'Description for Project50 Phase2'),
    (50, 50, 'Phase3', 'Description for Project50 Phase3');
    
SELECT * FROM phase
OFFSET (SELECT COUNT(*) FROM phase) - 10
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
INSERT INTO orderline (
      phase_id
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
SELECT * FROM orderline;


-- ASSIGNMENT
-- this table is used to assign people to a project on a daily basis
DROP TABLE IF EXISTS assignment CASCADE;
CREATE TABLE assignment (
    assignment_id       INT GENERATED ALWAYS AS IDENTITY,
    phase_id       INT,
    person_id               INT,
    date                    DATE,
    assignment_description  VARCHAR(100),
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (phase_id) REFERENCES phase(phase_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);
INSERT INTO assignment (
      phase_id
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
SELECT * FROM assignment;




RUNQUERY START */ 