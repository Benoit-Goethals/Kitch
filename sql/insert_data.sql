
/*
+ the queries in this are only used to verify the amount of data in the tables (last 10 items are picked to check the numbers of items exisiting)
*/


SET client_min_messages TO WARNING;
-- removes unnecessary messages from the console

-- ADDRESS
TRUNCATE TABLE address CASCADE;
ALTER SEQUENCE address_address_id_seq RESTART WITH 1;
COPY address (street, house_number, postal_code, municipality, longitude, latitude)
FROM 'C:/_MaRn/syntra/projects/python_eindopdracht/kitch/addresses/addresses.csv'
-- TODO: find a way to get the path from the config file
DELIMITER ','
CSV HEADER
;
SELECT * FROM address
-- LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM address) - 10; -- last 10 lines


-- PERSON
TRUNCATE TABLE person CASCADE;
ALTER SEQUENCE person_person_id_seq RESTART WITH 1;
INSERT INTO person (
      name_first
    , name_last
    , name_title
    , phone_number
    , email) 
VALUES
    -- 80 clients person 
    ('Marijn', 'Vandenholen', 'Dhr.', '0123456789', 'marijn.vandenholen@client.com'),
    ('Benoit', 'Goethals', 'Dhr.', '9876543210', 'benoit.goethals@client.com'),
    ('Jan', 'Jansen', 'Dhr.', '1234567890', 'jan.jansen@client.com'),
    ('Sofie', 'Vermeulen', 'Mevr.', '0987654321', 'sofie.vermeulen@client.com'),
    ('Annelies', 'De Smet', 'Dr.', '5551234567', 'annelies.desmet@client.com'),
    ('Bart', 'De Vries', 'Prof.', '5559876543', 'bart.devries@client.com'),
    ('Karel', 'Maes', 'Dhr.', '5555555555', 'karel.maes@client.com'),
    ('Diana', 'Van den Broeck', 'Mevr.', '5554444444', 'diana.vandenbroeck@client.com'),
    ('Ewout', 'De Clercq', 'Dhr.', '5553333333', 'ewout.declercq@client.com'),
    ('Fien', 'Van Damme', 'Mevr.', '5552222222', 'fien.vandamme@client.com'),
    ('Geert', 'De Jong', 'Dhr.', '5551111111', 'geert.dejong@client.com'),
    ('Hanne', 'De Bruyne', 'Mevr.', '5556667777', 'hanne.debruyne@client.com'),
    ('Tom', 'Van Acker', 'Dhr.', '5557778888', 'tom.vanacker@client.com'),
    ('Lies', 'Peeters', 'Mevr.', '5558889999', 'lies.peeters@client.com'),
    ('Koen', 'Claes', 'Dhr.', '5559990000', 'koen.claes@client.com'),
    ('Eva', 'Janssens', 'Mevr.', '5550001111', 'eva.janssens@client.com'),
    ('Pieter', 'De Vos', 'Dhr.', '5551112222', 'pieter.devos@client.com'),
    ('Sara', 'Van Dijk', 'Mevr.', '5552223333', 'sara.vandijk@client.com'),
    ('Lucas', 'Verhoeven', 'Dhr.', '5553334444', 'lucas.verhoeven@client.com'),
    ('Emma', 'De Wilde', 'Mevr.', '5554445555', 'emma.dewilde@client.com'),
    ('Jeroen', 'Van Dam', 'Dhr.', '5555556666', 'jeroen.vandam@client.com'),
    ('Lotte', 'De Graaf', 'Mevr.', '5556667777', 'lotte.degraaf@client.com'),
    ('Niels', 'Van der Meer', 'Dhr.', '5557778888', 'niels.vandermeer@client.com'),
    ('Sanne', 'De Koning', 'Mevr.', '5558889999', 'sanne.dekoning@client.com'),
    ('Wouter', 'Van Loon', 'Dhr.', '5559990000', 'wouter.vanloon@client.com'),
    ('Tessa', 'De Groot', 'Mevr.', '5550001111', 'tessa.degroot@client.com'),
    ('Ruben', 'Van der Veen', 'Dhr.', '5551112222', 'ruben.vanderveen@client.com'),
    ('Kim', 'De Lange', 'Mevr.', '5552223333', 'kim.delange@client.com'),
    ('Thomas', 'Van der Heijden', 'Dhr.', '5553334444', 'thomas.vanderheijden@client.com'),
    ('Laura', 'De Vos', 'Mevr.', '5554445555', 'laura.devos@client.com'),
    ('Bram', 'Van der Wal', 'Dhr.', '5555556666', 'bram.vanderwal@client.com'),
    ('Eline', 'De Boer', 'Mevr.', '5556667777', 'eline.deboer@client.com'),
    ('Jasper', 'Van der Berg', 'Dhr.', '5557778888', 'jasper.vanderberg@client.com'),
    ('Maaike', 'De Leeuw', 'Mevr.', '5558889999', 'maaike.deleeuw@client.com'),
    ('Stefan', 'Van der Linden', 'Dhr.', '5559990000', 'stefan.vanderlinden@client.com'),
    ('Inge', 'De Bruin', 'Mevr.', '5550001111', 'inge.debruin@client.com'),
    ('Arne', 'Van der Velden', 'Dhr.', '5551112222', 'arne.vandervelden@client.com'),
    ('Evy', 'De Wit', 'Mevr.', '5552223333', 'evy.dewit@client.com'),
    ('Koen', 'Van der Zanden', 'Dhr.', '5553334444', 'koen.vanderzanden@client.com'),
    ('Liesbeth', 'De Haan', 'Mevr.', '5554445555', 'liesbeth.dehaan@client.com'),
    ('Jelle', 'Van der Hoek', 'Dhr.', '5555556666', 'jelle.vanderhoek@client.com'),
    ('Anke', 'De Vries', 'Mevr.', '5556667777', 'anke.devries@client.com'),
    ('Bart', 'Van der Plas', 'Dhr.', '5557778888', 'bart.vanderplas@client.com'),
    ('Sofie', 'De Jong', 'Mevr.', '5558889999', 'sofie.dejong@client.com'),
    ('Tom', 'Van der Steen', 'Dhr.', '5559990000', 'tom.vandersteen@client.com'),
    ('Ellen', 'De Vos', 'Mevr.', '5550001111', 'ellen.devos@client.com'),
    ('Mark', 'Van der Heuvel', 'Dhr.', '5551112222', 'mark.vanderheuvel@client.com'),
    ('Ilse', 'De Groot', 'Mevr.', '5552223333', 'ilse.degroot@client.com'),
    ('Wim', 'Van der Meulen', 'Dhr.', '5553334444', 'wim.vandermeulen@client.com'),
    ('Nina', 'De Bruin', 'Mevr.', '5554445555', 'nina.debruin@client.com'),
    ('Frank', 'Van der Veen', 'Dhr.', '5555556666', 'frank.vanderveen@client.com'),
    ('Sanne', 'De Koning', 'Mevr.', '5556667777', 'sanne.dekoning@client.com'),
    ('Jeroen', 'Van der Wal', 'Dhr.', '5557778888', 'jeroen.vanderwal@client.com'),
    ('Lotte', 'De Graaf', 'Mevr.', '5558889999', 'lotte.degraaf@client.com'),
    ('Niels', 'Van der Meer', 'Dhr.', '5559990000', 'niels.vandermeer@client.com'),
    ('Tessa', 'De Groot', 'Mevr.', '5550001111', 'tessa.degroot@client.com'),
    ('Ruben', 'Van der Veen', 'Dhr.', '5551112222', 'ruben.vanderveen@client.com'),
    ('Kim', 'De Lange', 'Mevr.', '5552223333', 'kim.delange@client.com'),
    ('Thomas', 'Van der Heijden', 'Dhr.', '5553334444', 'thomas.vanderheijden@client.com'),
    ('Laura', 'De Vos', 'Mevr.', '5554445555', 'laura.devos@client.com'),
    ('Bram', 'Van der Wal', 'Dhr.', '5555556666', 'bram.vanderwal@client.com'),
    ('Eline', 'De Boer', 'Mevr.', '5556667777', 'eline.deboer@client.com'),
    ('Jasper', 'Van der Berg', 'Dhr.', '5557778888', 'jasper.vanderberg@client.com'),
    ('Maaike', 'De Leeuw', 'Mevr.', '5558889999', 'maaike.deleeuw@client.com'),
    ('Stefan', 'Van der Linden', 'Dhr.', '5559990000', 'stefan.vanderlinden@client.com'),
    ('Inge', 'De Bruin', 'Mevr.', '5550001111', 'inge.debruin@client.com'),
    ('Arne', 'Van der Velden', 'Dhr.', '5551112222', 'arne.vandervelden@client.com'),
    ('Evy', 'De Wit', 'Mevr.', '5552223333', 'evy.dewit@client.com'),
    ('Koen', 'Van der Zanden', 'Dhr.', '5553334444', 'koen.vanderzanden@client.com'),
    ('Liesbeth', 'De Haan', 'Mevr.', '5554445555', 'liesbeth.dehaan@client.com'),
    ('Jelle', 'Van der Hoek', 'Dhr.', '5555556666', 'jelle.vanderhoek@kitch.com'),
    ('Anke', 'De Vries', 'Mevr.', '5556667777', 'anke.devries@client.com'),
    ('Bart', 'Van der Plas', 'Dhr.', '5557778888', 'bart.vanderplas@client.com'),
    ('Sofie', 'De Jong', 'Mevr.', '5558889999', 'sofie.dejong@client.com'),
    ('Tom', 'Van der Steen', 'Dhr.', '5559990000', 'tom.vandersteen@client.com'),
    ('Ellen', 'De Vos', 'Mevr.', '5550001111', 'ellen.devos@client.com'),
    ('Mark', 'Van der Heuvel', 'Dhr.', '5551112222', 'mark.vanderheuvel@client.com'),
    --  20 suppliers person
    ('Ilse', 'De Groot', 'Mevr.', '5552223333', 'ilse.degroot@supplier.com'),
    ('Wim', 'Van der Meulen', 'Dhr.', '5553334444', 'wim.vandermeulen@supplier.com'),
    ('Nina', 'De Bruin', 'Mevr.', '5554445555', 'nina.debruin@supplier.com'),
    ('Frank', 'Van der Veen', 'Dhr.', '5555556666', 'frank.vanderveen@supplier.com'),
    ('Sanne', 'De Koning', 'Mevr.', '5556667777', 'sanne.dekoning@supplier.com'),
    ('Jeroen', 'Van der Wal', 'Dhr.', '5557778888', 'jeroen.vanderwal@supplier.com'),
    ('Lotte', 'De Graaf', 'Mevr.', '5558889999', 'lotte.degraaf@supplier.com'),
    ('Niels', 'Van der Meer', 'Dhr.', '5559990000', 'niels.vandermeer@supplier.com'),
    ('Lars', 'Van den Berg', 'Dhr.', '5551231234', 'lars.vandenberg@supplier.com'),
    ('Mila', 'De Winter', 'Mevr.', '5552342345', 'mila.dewinter@supplier.com'),
    ('Noah', 'Van der Zee', 'Dhr.', '5553453456', 'noah.vanderzee@supplier.com'),
    ('Emma', 'De Vos', 'Mevr.', '5554564567', 'emma.devos@supplier.com'),
    ('Finn', 'Van der Meer', 'Dhr.', '5555675678', 'finn.vandermeer@supplier.com'),
    ('Lars', 'Van den Berg', 'Dhr.', '5551231234', 'lars.vandenberg@supplier.com'),
    ('Mila', 'De Winter', 'Mevr.', '5552342345', 'mila.dewinter@supplier.com'),
    ('Noah', 'Van der Zee', 'Dhr.', '5553453456', 'noah.vanderzee@supplier.com'),
    ('Emma', 'De Vos', 'Mevr.', '5554564567', 'emma.devos@supplier.com'),
    ('Finn', 'Van der Meer', 'Dhr.', '5555675678', 'finn.vandermeer@supplier.com'),
    ('Lena', 'De Vries', 'Mevr.', '5556786789', 'lena.devries@supplier.com'),
    ('Oliver', 'Van den Bosch', 'Dhr.', '5557897890', 'oliver.vandenbosch@supplier.com'),
    ('Sophie', 'De Jong', 'Mevr.', '5558908901', 'sophie.dejong@supplier.com'),
    -- 20 kitch person
    ('Liam', 'Van den Broek', 'Dhr.', '5551111111', 'liam.vandenbroek@kitch.com'),
    ('Emma', 'De Vries', 'Mevr.', '5552222222', 'emma.devries@kitch.com'),
    ('Noah', 'Van der Linden', 'Dhr.', '5553333333', 'noah.vanderlinden@kitch.com'),
    ('Olivia', 'De Jong', 'Mevr.', '5554444444', 'olivia.dejong@kitch.com'),
    ('Lucas', 'Van der Meer', 'Dhr.', '5555555555', 'lucas.vandermeer@kitch.com'),
    ('Mila', 'De Bruin', 'Mevr.', '5556666666', 'mila.debruin@kitch.com'),
    ('Ethan', 'Van den Berg', 'Dhr.', '5557777777', 'ethan.vandenberg@kitch.com'),
    ('Sophie', 'De Groot', 'Mevr.', '5558888888', 'sophie.degroot@kitch.com'),
    ('James', 'Van der Heijden', 'Dhr.', '5559999999', 'james.vanderheijden@kitch.com'),
    ('Charlotte', 'De Vos', 'Mevr.', '5550000000', 'charlotte.devos@kitch.com'),
    ('Benjamin', 'Van der Wal', 'Dhr.', '5551234567', 'benjamin.vanderwal@kitch.com'),
    ('Ella', 'De Winter', 'Mevr.', '5552345678', 'ella.dewinter@kitch.com'),
    ('Alexander', 'Van der Zee', 'Dhr.', '5553456789', 'alexander.vanderzee@kitch.com'),
    ('Lily', 'De Haan', 'Mevr.', '5554567890', 'lily.dehaan@kitch.com'),
    ('Henry', 'Van der Plas', 'Dhr.', '5555678901', 'henry.vanderplas@kitch.com'),
    ('Isabella', 'De Leeuw', 'Mevr.', '5556789012', 'isabella.deleeuw@kitch.com'),
    ('William', 'Van der Velden', 'Dhr.', '5557890123', 'william.vandervelden@kitch.com'),
    ('Emily', 'De Wit', 'Mevr.', '5558901234', 'emily.dewit@kitch.com'),
    ('Michael', 'Van der Zanden', 'Dhr.', '5559012345', 'michael.vanderzanden@kitch.com'),
    ('Charlotte', 'De Vos', 'Mevr.', '5558901234', 'charlotte.devos@kitch.com'),
    ('Benjamin', 'Van der Wal', 'Dhr.', '5559012345', 'benjamin.vanderwal@kitch.com'),
    ('Ella', 'De Winter', 'Mevr.', '5550123456', 'ella.dewinter@kitch.com')

;
SELECT * FROM person
OFFSET (SELECT COUNT(*) FROM person) - 10;
;


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
INSERT INTO supplier (
    company_id
)values
    (81), (82), (83), (84), (85), (86), (87), (88), (89), (90), (91), (92), (93), (94), (95), (96), (97), (98), (99), (100);
SELECT * FROM supplier
OFFSET (SELECT COUNT(*) FROM supplier) - 10 -- last 10 lines
;

-- ARTICLE
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
INSERT INTO phase (
      project_id
    , delivery_address_id
    , name
    , description
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


INSERT INTO orderline (
      phase_id	
    , sales_price	
    , amount	
    , article_id	
    , date_acceptance	
    , date_ordered	
    , date_received	
    , date_issued	
    , date_delivered	
    , date_installed	
    , date_accepted	
    , date_invoiced	
    , date_paid	
    , date_closed
)VALUES
  (143,5141,2,65,null,null,null,null,null,null,null,null,null,null)
, (139,6347,2,24,'2023-08-21','2023-08-24','2024-08-23','2024-11-10','2024-12-12','2025-01-27','2025-02-18','2025-04-18',null,null)
, (30,11143,3,83,null,null,null,null,null,null,null,null,null,null)
, (23,16824,1,38,'2022-03-19','2022-12-12','2022-12-22','2023-05-19','2023-07-10','2023-07-13','2023-08-10','2023-08-30','2023-09-20','2023-11-18')
, (48,15683,2,17,null,null,null,null,null,null,null,null,null,null)
, (119,913,1,32,null,null,null,null,null,null,null,null,null,null)
, (110,7050,3,63,'2025-02-20',null,null,null,null,null,null,null,null,null)
, (150,2504,3,28,'2022-04-19','2022-06-08','2022-08-30','2022-11-06','2022-12-28','2023-03-24','2023-04-03','2023-04-26','2023-06-01','2023-07-06')
, (46,3166,2,28,'2022-01-24','2022-11-28','2023-05-11','2023-07-18','2023-09-07','2023-11-11','2023-11-18','2024-01-07','2024-01-22','2024-01-31')
, (137,9925,2,94,'2024-11-06','2025-03-10',null,null,null,null,null,null,null,null)
, (129,358,3,87,'2020-08-04','2021-02-16','2022-02-11','2022-02-22','2022-05-04','2022-06-15','2022-06-26','2022-06-29','2022-08-22','2022-09-01')
, (43,7943,2,78,'2023-06-20','2023-09-25','2024-07-15','2024-08-02','2024-09-26','2024-10-13','2024-10-20','2024-12-04','2025-01-29','2025-02-07')
, (58,8909,1,12,'2022-03-04','2023-01-24','2023-08-03','2024-03-25','2024-06-04','2024-08-27','2024-09-16','2024-10-30','2024-12-20','2025-02-13')
, (86,4346,2,65,'2021-12-16','2022-01-06','2022-04-09','2022-06-24','2022-09-07','2022-10-10','2022-10-20','2022-11-25','2023-01-19','2023-02-15')
, (59,13219,1,33,'2024-05-28','2024-11-22',null,null,null,null,null,null,null,null)
, (28,16423,3,40,null,null,null,null,null,null,null,null,null,null)
, (68,10423,1,51,'2025-03-01','2025-04-19',null,null,null,null,null,null,null,null)
, (147,7633,1,61,'2022-11-25','2023-08-21','2024-05-26','2025-01-15','2025-02-26',null,null,null,null,null)
, (43,10384,2,95,'2025-01-31','2025-03-28',null,null,null,null,null,null,null,null)
, (11,13284,2,7,'2021-03-09','2021-12-14','2022-05-09','2022-08-13','2022-11-05','2022-11-22','2022-11-27','2022-12-26','2023-01-04','2023-01-11')
, (66,11770,2,76,null,null,null,null,null,null,null,null,null,null)
, (76,8494,2,93,null,null,null,null,null,null,null,null,null,null)
, (83,3665,2,66,'2022-03-23','2022-11-04','2023-03-28','2023-07-11','2023-08-17','2023-09-14','2023-10-09','2023-12-05','2024-02-02','2024-03-05')
, (82,10145,2,76,'2023-11-25','2024-11-18','2025-03-25',null,null,null,null,null,null,null)
, (57,5010,1,65,'2021-10-09','2022-04-12','2022-08-01','2023-02-13','2023-03-23','2023-06-19','2023-06-30','2023-08-13','2023-10-09','2023-12-06')
, (62,68,2,1,'2020-11-18','2021-03-27','2021-10-13','2021-12-22','2021-12-30','2022-04-07','2022-05-03','2022-05-03','2022-05-12','2022-05-21')
, (42,10834,2,70,'2024-12-15',null,null,null,null,null,null,null,null,null)
, (12,13891,1,36,'2022-12-31','2023-10-10','2024-04-28','2024-11-03','2024-12-20','2024-12-21','2025-01-12','2025-02-20','2025-04-14','2025-04-19')
, (71,14746,3,7,'2021-01-07','2021-01-08','2021-04-13','2021-11-27','2022-01-21','2022-02-18','2022-03-12','2022-04-23','2022-04-24','2022-05-16')
, (15,4392,2,65,'2020-12-25','2021-03-01','2021-11-01','2021-12-15','2022-02-11','2022-03-08','2022-03-29','2022-04-25','2022-05-09','2022-06-06')
, (89,2609,2,28,null,null,null,null,null,null,null,null,null,null)
, (79,2386,3,68,'2021-03-29','2021-12-10','2022-11-15','2023-07-13','2023-07-18','2023-10-31','2023-11-23','2023-12-24','2024-02-20','2024-03-10')
, (135,3655,3,74,'2020-07-23','2020-10-31','2021-10-24','2022-09-16','2022-12-01','2023-02-15','2023-03-09','2023-03-18','2023-04-08','2023-04-08')
, (69,14482,3,43,'2025-04-02',null,null,null,null,null,null,null,null,null)
, (35,16356,3,40,'2021-10-14','2022-06-28','2022-07-07','2023-03-18','2023-04-17','2023-08-14','2023-09-12','2023-10-23','2023-11-14','2024-01-04')
, (59,14649,1,33,'2020-08-22','2021-02-12','2022-01-20','2022-06-30','2022-09-16','2023-01-11','2023-02-04','2023-02-25','2023-03-29','2023-04-24')
, (116,11760,3,25,null,null,null,null,null,null,null,null,null,null)
, (97,17199,1,38,'2024-05-31','2025-02-14',null,null,null,null,null,null,null,null)
, (28,5557,2,100,null,null,null,null,null,null,null,null,null,null)
, (71,14509,2,52,'2022-08-18','2023-04-07','2024-01-28','2024-06-18','2024-08-08','2024-10-08','2024-10-14','2024-10-18','2024-10-20','2024-10-20')
, (115,10353,1,83,'2022-09-30','2022-11-28','2023-08-06','2023-10-13','2023-11-29','2023-12-22','2023-12-22','2024-01-22','2024-03-04','2024-03-07')
, (15,4509,2,90,null,null,null,null,null,null,null,null,null,null)
, (40,9206,1,92,'2024-05-02','2024-10-11',null,null,null,null,null,null,null,null)
, (148,13847,2,46,'2020-10-06','2021-10-06','2022-08-28','2023-06-21','2023-08-27','2023-11-08','2023-11-21','2024-01-18','2024-02-12','2024-03-25')
, (60,5141,1,18,'2020-09-21','2021-02-28','2021-12-04','2021-12-14','2021-12-15','2022-01-04','2022-01-16','2022-03-07','2022-04-23','2022-05-27')
, (82,15015,2,33,null,null,null,null,null,null,null,null,null,null)
, (64,11571,2,13,'2020-10-28','2021-09-23','2022-03-02','2023-01-01','2023-03-14','2023-04-26','2023-05-06','2023-06-04','2023-07-14','2023-07-24')
, (83,8014,3,4,'2020-06-03','2021-04-23','2022-01-21','2022-11-14','2022-11-24','2022-12-08','2023-01-01','2023-01-31','2023-03-02','2023-03-18')
, (90,3153,2,60,null,null,null,null,null,null,null,null,null,null)
, (84,12927,2,72,'2024-03-23','2024-12-27','2025-03-09','2025-04-01','2025-04-28','2025-05-01',null,null,null,null)
, (49,10859,3,35,null,null,null,null,null,null,null,null,null,null)
, (4,321,3,87,'2022-03-24','2023-01-25','2023-11-26','2024-03-18','2024-06-06','2024-09-28','2024-10-19','2024-10-22','2024-10-27','2024-11-17')
, (138,12825,3,43,'2023-01-22','2023-02-17','2023-06-06','2024-04-08','2024-06-10','2024-06-27','2024-07-19','2024-09-07','2024-11-04','2024-12-05')
, (127,12859,1,73,null,null,null,null,null,null,null,null,null,null)
, (72,4833,1,65,'2021-07-06','2022-04-16','2022-12-23','2023-03-21','2023-04-09','2023-06-08','2023-06-19','2023-07-18','2023-08-06','2023-09-02')
, (34,8167,1,45,null,null,null,null,null,null,null,null,null,null)
, (90,12401,2,57,null,null,null,null,null,null,null,null,null,null)
, (111,9882,1,96,null,null,null,null,null,null,null,null,null,null)
, (50,7196,1,10,'2024-12-22','2025-01-21','2025-02-06',null,null,null,null,null,null,null)
, (26,11553,1,92,'2021-10-10','2021-11-04','2022-01-04','2022-07-29','2022-10-17','2022-12-16','2023-01-11','2023-03-03','2023-03-19','2023-04-10')
, (53,5768,3,18,'2020-11-07','2021-06-24','2022-06-04','2022-11-04','2022-12-10','2023-01-23','2023-02-01','2023-02-21','2023-03-24','2023-03-31')
, (8,7086,1,24,'2021-09-03','2021-12-17','2022-11-21','2023-08-31','2023-11-07','2023-11-29','2023-12-04','2023-12-26','2024-01-11','2024-01-16')
, (138,4276,3,74,'2022-06-19','2023-05-27','2023-06-04','2024-02-15','2024-04-29','2024-08-04','2024-08-26','2024-08-28','2024-09-05','2024-10-24')
, (20,18973,2,53,null,null,null,null,null,null,null,null,null,null)
, (72,2491,1,21,'2024-08-31','2024-12-27','2024-12-28','2025-01-06','2025-01-18','2025-02-24','2025-03-20','2025-04-14','2025-04-22',null)
, (7,3079,1,28,null,null,null,null,null,null,null,null,null,null)
, (17,14678,2,34,'2023-11-05','2024-05-21','2024-06-05','2025-02-03','2025-03-12',null,null,null,null,null)
, (57,8532,2,15,'2023-04-12','2023-10-13','2023-10-25','2024-02-04','2024-02-25','2024-06-20','2024-06-20','2024-06-30','2024-07-02','2024-08-06')
, (108,386,1,23,'2023-09-06','2023-09-28','2024-04-09','2025-04-02',null,null,null,null,null,null)
, (137,2452,1,28,null,null,null,null,null,null,null,null,null,null)
, (4,797,1,41,null,null,null,null,null,null,null,null,null,null)
, (142,655,3,80,'2024-04-20','2025-03-31',null,null,null,null,null,null,null,null)
, (111,8191,3,58,null,null,null,null,null,null,null,null,null,null)
, (140,15066,3,31,'2023-02-02','2024-02-01','2024-08-05','2024-09-29','2024-09-30','2024-12-18','2024-12-23','2025-02-16','2025-04-11','2025-04-22')
, (44,9378,3,88,'2022-02-16','2022-03-06','2022-11-21','2023-06-12','2023-07-08','2023-10-28','2023-11-19','2023-12-24','2024-01-12','2024-01-14')
, (11,3392,1,79,'2023-12-29','2024-07-04','2024-12-28',null,null,null,null,null,null,null)
, (51,8392,1,45,'2021-05-16','2021-12-03','2022-06-26','2023-02-11','2023-03-01','2023-06-08','2023-06-18','2023-07-03','2023-07-19','2023-09-16')
, (66,16781,2,40,'2024-09-04','2024-12-23',null,null,null,null,null,null,null,null)
, (4,5290,1,100,'2022-02-27','2023-01-20','2023-10-19','2024-04-21','2024-05-16','2024-07-12','2024-07-31','2024-08-31','2024-09-10','2024-10-18')
, (141,10281,3,76,'2022-05-09','2023-02-14','2023-11-06','2024-06-08','2024-07-03','2024-09-03','2024-09-23','2024-11-01','2024-12-04','2025-01-29')
, (2,11982,2,76,null,null,null,null,null,null,null,null,null,null)
, (143,4363,1,89,'2020-12-10','2021-05-08','2022-04-17','2022-10-08','2022-11-03','2023-02-25','2023-03-13','2023-04-25','2023-05-02','2023-05-13')
, (61,10739,2,59,'2024-12-14','2025-05-05',null,null,null,null,null,null,null,null)
, (62,896,2,41,null,null,null,null,null,null,null,null,null,null)
, (89,7272,1,4,'2024-12-02','2025-03-28',null,null,null,null,null,null,null,null)
, (2,3386,3,74,'2022-11-20','2023-10-19','2023-11-20','2024-07-28','2024-09-19','2024-12-12','2024-12-17','2025-02-07','2025-03-29','2025-04-02')
, (113,78,2,1,'2023-10-30','2024-09-24',null,null,null,null,null,null,null,null)
, (97,14144,2,52,null,null,null,null,null,null,null,null,null,null)
, (48,5209,1,69,'2024-03-11','2024-07-18',null,null,null,null,null,null,null,null)
, (75,10211,1,98,null,null,null,null,null,null,null,null,null,null)
, (29,12281,3,25,'2023-08-13','2024-04-04','2024-05-25','2024-12-16','2025-03-13','2025-03-14','2025-04-02',null,null,null)
, (105,14813,2,34,'2023-09-27','2024-06-06','2025-01-04',null,null,null,null,null,null,null)
, (145,1941,1,68,'2024-05-14','2024-09-08','2025-03-09','2025-03-20','2025-05-02',null,null,null,null,null)
, (91,706,2,41,'2022-04-16','2023-02-04','2023-05-15','2023-11-15','2024-01-05','2024-01-12','2024-01-12','2024-01-26','2024-02-01','2024-03-03')
, (101,13734,1,43,null,null,null,null,null,null,null,null,null,null)
, (6,7154,2,24,'2022-03-12','2022-04-03','2022-07-04','2022-10-22','2022-10-29','2023-01-21','2023-01-26','2023-03-10','2023-04-01','2023-05-16')
, (101,15813,2,38,'2022-04-04','2022-10-06','2022-11-29','2023-08-20','2023-10-27','2023-11-19','2023-12-19','2023-12-23','2024-01-24','2024-03-09')
, (122,16223,2,53,'2025-04-08',null,null,null,null,null,null,null,null,null)
, (70,12412,3,33,'2023-01-26','2023-09-17','2023-12-23','2024-09-22','2024-09-27','2024-12-18','2025-01-15','2025-01-16','2025-02-28','2025-04-09')
, (28,9000,2,39,'2023-09-03','2024-01-29','2024-10-24',null,null,null,null,null,null,null)
, (17,10230,1,92,null,null,null,null,null,null,null,null,null,null)
, (101,10421,3,96,'2021-11-23','2022-03-27','2022-09-17','2023-02-03','2023-03-14','2023-03-28','2023-04-02','2023-04-06','2023-05-16','2023-06-25')
, (145,3382,2,89,'2023-08-18','2023-11-05','2024-09-19','2025-05-04',null,null,null,null,null,null)
, (96,6569,2,4,null,null,null,null,null,null,null,null,null,null)
, (128,12452,1,30,'2025-01-27',null,null,null,null,null,null,null,null,null)
, (2,3779,1,79,'2025-05-01',null,null,null,null,null,null,null,null,null)
, (75,16196,3,67,null,null,null,null,null,null,null,null,null,null)
, (56,11810,2,33,'2021-10-04','2021-10-25','2022-09-20','2023-07-06','2023-07-10','2023-08-21','2023-08-31','2023-09-24','2023-10-29','2023-11-14')
, (4,5726,3,75,'2024-05-15','2025-05-07',null,null,null,null,null,null,null,null)
, (147,6904,1,10,'2021-10-18','2022-01-01','2022-07-30','2022-11-02','2022-12-30','2023-04-06','2023-04-13','2023-06-01','2023-07-02','2023-08-03')
, (6,11076,2,2,null,null,null,null,null,null,null,null,null,null)
, (88,7422,1,81,'2022-07-31','2023-03-26','2024-02-09','2024-11-28','2024-11-28','2025-01-19','2025-01-23','2025-03-16','2025-04-28',null)
, (142,10112,1,11,'2021-01-08','2021-03-11','2022-03-06','2022-05-10','2022-07-27','2022-08-25','2022-09-10','2022-10-18','2022-11-10','2022-12-23')
, (22,7360,1,64,null,null,null,null,null,null,null,null,null,null)
, (78,1406,2,6,null,null,null,null,null,null,null,null,null,null)
, (81,10902,2,11,'2024-07-24','2025-03-08',null,null,null,null,null,null,null,null)
, (121,4563,2,69,null,null,null,null,null,null,null,null,null,null)
, (61,7082,2,75,'2021-09-22','2022-07-16','2022-11-21','2023-05-25','2023-07-15','2023-09-07','2023-09-15','2023-09-26','2023-11-05','2023-11-10')
, (77,16958,1,99,'2020-07-26','2020-12-13','2021-09-29','2022-01-05','2022-02-22','2022-04-19','2022-05-09','2022-06-02','2022-07-22','2022-08-13')
, (120,14567,2,52,'2021-10-04','2022-02-25','2022-10-12','2023-10-12','2023-11-12','2023-11-18','2023-12-06','2023-12-19','2024-01-27','2024-02-18')
, (102,15361,1,8,'2020-11-22','2021-04-24','2021-06-22','2022-05-27','2022-06-07','2022-07-10','2022-07-24','2022-08-29','2022-10-23','2022-12-06')
, (125,12434,3,86,'2021-02-02','2022-02-02','2022-07-01','2022-10-02','2022-11-14','2023-02-26','2023-03-12','2023-05-05','2023-06-29','2023-08-08')
, (15,7960,3,15,'2023-02-27','2023-10-24','2024-01-10','2024-05-08','2024-05-23','2024-07-09','2024-07-13','2024-08-20','2024-08-20','2024-09-04')
, (141,9211,2,94,'2025-01-21',null,null,null,null,null,null,null,null,null)
, (90,12681,3,8,'2020-11-17','2021-02-03','2021-10-30','2022-08-11','2022-09-28','2022-10-02','2022-10-26','2022-11-29','2022-12-23','2022-12-27')
, (125,10822,2,92,null,null,null,null,null,null,null,null,null,null)
, (134,13694,1,55,'2024-03-20','2024-05-15','2024-07-09','2025-04-28',null,null,null,null,null,null)
, (107,5705,2,75,null,null,null,null,null,null,null,null,null,null)
, (98,3074,3,60,'2021-07-18','2021-09-17','2022-05-14','2022-10-22','2023-01-06','2023-02-03','2023-02-16','2023-02-27','2023-02-28','2023-03-26')
, (145,11877,3,35,null,null,null,null,null,null,null,null,null,null)
, (14,8540,2,47,'2022-01-02','2022-09-17','2023-02-10','2023-03-15','2023-04-26','2023-08-19','2023-08-28','2023-10-14','2023-12-09','2024-01-24')
, (116,18520,3,97,'2020-12-23','2021-02-02','2021-09-10','2022-07-18','2022-07-18','2022-10-11','2022-10-15','2022-11-03','2023-01-01','2023-01-12')
, (132,4042,2,20,null,null,null,null,null,null,null,null,null,null)
, (32,14513,3,52,'2024-04-16','2024-09-06',null,null,null,null,null,null,null,null)
, (53,11400,1,30,null,null,null,null,null,null,null,null,null,null)
, (97,5519,2,18,'2021-05-07','2021-12-03','2022-04-03','2023-01-06','2023-02-06','2023-02-08','2023-03-02','2023-03-17','2023-04-05','2023-04-06')
, (53,13928,3,25,'2025-01-22','2025-05-04',null,null,null,null,null,null,null,null)
, (87,11151,3,44,null,null,null,null,null,null,null,null,null,null)
, (57,11334,1,35,'2023-11-10','2024-04-18','2024-04-25','2024-09-04','2024-11-29','2025-03-02','2025-04-01','2025-04-11',null,null)
, (81,16773,3,38,'2020-09-15','2021-03-13','2021-12-28','2022-01-16','2022-03-19','2022-05-25','2022-05-29','2022-06-02','2022-06-10','2022-07-14')
, (22,10542,3,86,'2021-03-14','2021-10-27','2022-08-29','2022-09-03','2022-11-23','2022-12-01','2022-12-01','2023-01-14','2023-03-06','2023-03-25')
, (91,6415,2,18,'2021-10-28','2021-12-26','2022-01-24','2023-01-22','2023-02-18','2023-03-18','2023-03-30','2023-05-21','2023-05-26','2023-07-25')
, (1,16191,1,67,null,null,null,null,null,null,null,null,null,null)
, (131,9103,1,15,'2022-09-07','2023-07-29','2024-03-07','2024-08-24','2024-10-27','2025-02-11','2025-02-14','2025-04-13',null,null)
, (9,3447,1,66,'2022-04-01','2022-07-14','2023-02-18','2023-12-23','2023-12-30','2024-04-14','2024-04-14','2024-06-11','2024-06-26','2024-06-30')
, (12,11192,1,76,'2020-08-17','2021-03-21','2021-09-22','2022-02-01','2022-03-29','2022-04-08','2022-05-06','2022-05-30','2022-06-11','2022-07-15')
, (140,11566,1,7,null,null,null,null,null,null,null,null,null,null)
, (20,1733,2,85,'2020-09-14','2021-02-22','2021-12-07','2021-12-21','2021-12-27','2022-01-08','2022-01-15','2022-03-08','2022-03-16','2022-05-03')
, (38,14446,2,55,'2021-09-05','2022-06-18','2023-03-09','2023-06-19','2023-08-14','2023-09-01','2023-09-01','2023-09-24','2023-10-01','2023-11-12')
, (110,674,3,80,'2024-10-21','2024-12-26',null,null,null,null,null,null,null,null)
, (90,3718,3,74,'2023-09-03','2024-03-19','2024-05-15','2024-06-07','2024-07-24','2024-10-10','2024-10-25','2024-11-13','2025-01-09','2025-03-01')
, (66,4020,1,82,null,null,null,null,null,null,null,null,null,null)
, (75,705,1,80,'2023-10-08','2023-11-23','2024-01-06','2024-09-01','2024-11-15','2024-12-03','2024-12-12','2025-01-28','2025-02-09','2025-02-19')
, (86,8549,3,15,'2020-11-25','2021-03-03','2021-10-10','2022-04-05','2022-05-26','2022-09-01','2022-09-17','2022-10-07','2022-10-10','2022-10-15')
, (78,7752,1,12,'2021-02-16','2021-06-06','2021-09-22','2022-07-10','2022-10-01','2023-01-14','2023-01-31','2023-03-03','2023-04-19','2023-05-01')
, (87,352,3,50,'2022-09-10','2022-12-23','2023-02-02','2023-04-26','2023-04-26','2023-05-03','2023-06-01','2023-07-05','2023-08-26','2023-09-22')
, (141,381,1,50,'2024-02-14','2024-10-08',null,null,null,null,null,null,null,null)
, (107,15727,3,38,'2020-08-14','2021-03-10','2021-11-15','2022-03-09','2022-03-26','2022-04-09','2022-04-24','2022-06-09','2022-07-29','2022-09-27')
, (77,18792,3,53,null,null,null,null,null,null,null,null,null,null)
, (11,12541,3,43,null,null,null,null,null,null,null,null,null,null)
, (77,9071,2,71,'2023-09-18','2024-05-04','2024-12-07','2025-02-13','2025-05-01',null,null,null,null,null)
, (94,3851,2,79,'2024-12-08','2025-02-09',null,null,null,null,null,null,null,null)
, (112,883,3,41,'2023-03-05','2023-07-20','2024-02-10','2025-01-08','2025-02-01','2025-03-30','2025-04-01',null,null,null)
, (9,7720,3,78,null,null,null,null,null,null,null,null,null,null)
, (77,13111,2,35,'2022-11-27','2023-10-23','2024-01-22','2024-08-17','2024-11-12','2025-01-30','2025-02-10','2025-02-23','2025-04-11',null)
, (107,8629,2,78,'2021-03-03','2021-11-29','2022-06-02','2022-08-11','2022-09-18','2022-09-23','2022-10-21','2022-12-14','2023-02-12','2023-04-04')
, (137,8168,3,15,'2021-11-20','2022-05-04','2022-06-23','2022-10-23','2022-11-07','2022-12-10','2023-01-04','2023-02-27','2023-04-23','2023-06-14')
, (20,16932,2,40,'2025-04-19',null,null,null,null,null,null,null,null,null)
, (149,3324,3,60,null,null,null,null,null,null,null,null,null,null)
, (30,13752,1,17,'2021-06-17','2021-10-24','2022-09-04','2023-07-23','2023-08-12','2023-11-06','2023-11-27','2024-01-23','2024-03-02','2024-04-18')
, (4,680,3,80,null,null,null,null,null,null,null,null,null,null)
, (66,3910,2,20,'2020-09-07','2021-07-01','2022-01-20','2023-01-12','2023-03-02','2023-06-17','2023-06-24','2023-07-31','2023-08-12','2023-08-21')
, (38,4988,1,27,'2022-08-02','2023-02-15','2023-04-23','2023-07-07','2023-07-13','2023-07-20','2023-08-04','2023-08-16','2023-10-11','2023-11-06')
, (21,14939,3,99,'2024-06-27',null,null,null,null,null,null,null,null,null)
, (41,1722,1,19,null,null,null,null,null,null,null,null,null,null)
, (94,8722,1,95,'2021-07-29','2022-04-09','2022-05-02','2022-12-04','2023-01-01','2023-01-11','2023-01-23','2023-03-18','2023-05-07','2023-05-10')
, (133,12880,1,52,null,null,null,null,null,null,null,null,null,null)
, (147,2161,2,49,'2023-03-06','2024-02-20','2024-02-23','2024-07-16','2024-08-08','2024-10-24','2024-11-10','2024-11-18','2024-12-26','2025-01-29')
, (1,14067,3,34,null,null,null,null,null,null,null,null,null,null)
, (3,11742,3,57,'2020-11-10','2021-01-21','2021-12-09','2022-01-17','2022-03-12','2022-04-04','2022-05-02','2022-06-26','2022-07-28','2022-09-08')
, (55,7498,1,93,null,null,null,null,null,null,null,null,null,null)
, (7,855,3,5,'2024-06-26','2024-08-27','2025-03-20',null,null,null,null,null,null,null)
, (36,7674,3,81,'2021-05-07','2021-12-27','2022-10-11','2023-10-11','2024-01-03','2024-03-29','2024-04-17','2024-04-26','2024-05-01','2024-05-11')
, (99,3189,3,82,null,null,null,null,null,null,null,null,null,null)
, (132,3712,2,60,'2024-09-11','2024-12-27',null,null,null,null,null,null,null,null)
, (101,13059,2,98,'2021-12-26','2022-12-23','2023-02-15','2023-09-22','2023-10-06','2023-11-13','2023-12-04','2023-12-05','2023-12-30','2024-02-26')
, (8,14583,2,99,'2024-10-16',null,null,null,null,null,null,null,null,null)
, (61,14193,3,72,'2025-04-22',null,null,null,null,null,null,null,null,null)
, (139,9568,1,95,'2021-12-02','2022-06-25','2023-01-22','2023-10-15','2023-10-16','2023-10-28','2023-11-12','2023-12-04','2024-01-26','2024-02-07')
, (134,11255,1,46,'2021-12-28','2022-10-05','2023-06-16','2023-10-31','2023-12-16','2024-01-13','2024-02-07','2024-03-26','2024-03-26','2024-04-04')
, (31,12503,2,55,null,null,null,null,null,null,null,null,null,null)
, (43,8701,3,45,'2025-03-29',null,null,null,null,null,null,null,null,null)
, (104,740,3,80,'2025-01-27','2025-05-01',null,null,null,null,null,null,null,null)
, (140,433,1,50,null,null,null,null,null,null,null,null,null,null)
, (121,3949,1,82,'2023-02-05','2024-01-31','2024-04-16','2025-03-27','2025-03-28','2025-04-12','2025-04-25','2025-05-07',null,null)
, (9,12648,2,84,'2023-02-20','2024-01-02','2024-10-31',null,null,null,null,null,null,null)
, (125,6037,1,77,'2024-08-08','2025-01-21','2025-02-06',null,null,null,null,null,null,null)
, (43,14509,1,38,'2023-08-14','2023-11-25','2024-06-09',null,null,null,null,null,null,null)
, (2,7731,3,58,null,null,null,null,null,null,null,null,null,null)
, (97,10025,3,37,'2022-03-04','2022-05-14','2022-05-17','2023-03-17','2023-03-18','2023-05-15','2023-05-20','2023-07-01','2023-07-27','2023-09-04')
, (117,8304,3,63,'2023-03-03','2023-06-30','2024-01-21','2024-03-06','2024-05-01','2024-07-24','2024-07-26','2024-08-29','2024-10-05','2024-11-12')
, (94,9837,2,95,'2025-03-18',null,null,null,null,null,null,null,null,null)
, (110,4573,3,65,'2021-11-18','2021-12-14','2021-12-23','2022-07-16','2022-09-15','2022-11-13','2022-11-28','2022-12-13','2022-12-15','2022-12-27')
, (141,12235,2,33,'2021-08-31','2022-01-28','2022-04-03','2022-05-15','2022-07-29','2022-08-03','2022-08-21','2022-08-22','2022-08-22','2022-09-04')
, (116,11596,2,25,null,null,null,null,null,null,null,null,null,null)
, (44,14870,1,72,'2020-06-07','2020-11-17','2021-04-25','2022-01-14','2022-04-01','2022-05-08','2022-05-21','2022-06-16','2022-06-16','2022-07-31')
, (8,13378,3,43,'2023-04-22','2023-11-12','2024-11-01',null,null,null,null,null,null,null)
, (24,10640,3,84,'2025-03-28',null,null,null,null,null,null,null,null,null)
, (29,7434,1,22,null,null,null,null,null,null,null,null,null,null)
, (114,2059,3,68,'2021-08-18','2022-02-03','2022-05-05','2023-03-20','2023-03-29','2023-04-03','2023-05-02','2023-06-17','2023-07-22','2023-09-18')
, (108,4286,3,65,'2023-04-01','2023-06-17','2024-02-01','2024-10-22','2024-11-18','2025-01-08','2025-02-02','2025-03-26','2025-05-04',null)
, (71,4521,3,9,'2025-01-13',null,null,null,null,null,null,null,null,null)
, (75,2102,1,49,null,null,null,null,null,null,null,null,null,null)
, (105,11659,3,29,'2024-02-03','2024-11-27',null,null,null,null,null,null,null,null)
, (122,11328,3,26,'2021-04-09','2021-10-29','2022-03-12','2022-04-20','2022-05-16','2022-06-20','2022-07-11','2022-08-09','2022-09-07','2022-10-01')
, (4,7260,3,12,'2022-05-03','2023-03-16','2023-11-16','2023-11-20','2024-01-01','2024-03-22','2024-04-10','2024-05-01','2024-05-22','2024-07-18')
, (118,13340,2,35,'2021-06-07','2021-06-19','2021-07-22','2022-05-25','2022-06-28','2022-08-12','2022-09-09','2022-09-09','2022-09-12','2022-10-14')
, (60,2997,3,60,'2021-10-08','2022-02-20','2023-02-18','2024-02-16','2024-03-25','2024-05-06','2024-05-17','2024-06-07','2024-06-15','2024-06-27')
, (146,11165,1,30,'2022-06-14','2022-10-22','2023-05-21','2024-05-08','2024-06-27','2024-07-23','2024-07-23','2024-08-07','2024-08-10','2024-09-26')
, (83,15798,2,38,null,null,null,null,null,null,null,null,null,null)
, (109,9595,3,47,'2022-05-12','2023-04-28','2023-06-20','2023-10-30','2024-01-14','2024-03-09','2024-03-23','2024-05-13','2024-05-24','2024-06-16')
, (59,10812,1,51,'2023-06-12','2024-04-24','2025-03-06',null,null,null,null,null,null,null)
, (93,3595,3,60,'2023-02-10','2023-08-18','2023-08-26','2023-09-20','2023-10-26','2023-11-18','2023-12-16','2024-01-11','2024-03-08','2024-04-19')
, (110,12101,2,8,'2024-05-27',null,null,null,null,null,null,null,null,null)
, (24,11772,2,57,'2023-05-08','2024-02-29','2024-08-04',null,null,null,null,null,null,null)
, (57,1961,2,19,'2022-02-24','2022-11-07','2023-08-30','2024-08-03','2024-10-09','2024-10-15','2024-10-29','2024-12-05','2024-12-26','2025-01-05')
, (37,11862,1,83,'2021-02-13','2021-04-28','2022-04-27','2023-01-02','2023-02-14','2023-03-25','2023-04-04','2023-04-07','2023-06-04','2023-07-01')
, (129,4630,2,65,'2024-11-23','2025-01-24',null,null,null,null,null,null,null,null)
, (64,842,2,32,'2021-02-04','2021-05-15','2022-04-04','2023-02-02','2023-03-17','2023-06-16','2023-07-05','2023-08-20','2023-10-19','2023-10-28')
, (99,5560,3,18,'2024-07-13','2024-09-10',null,null,null,null,null,null,null,null)
, (44,12101,3,52,'2020-09-21','2021-08-14','2022-05-09','2023-03-20','2023-05-16','2023-06-19','2023-07-18','2023-08-05','2023-10-04','2023-10-10')
, (132,5862,3,100,null,null,null,null,null,null,null,null,null,null)
, (75,12233,1,7,'2021-06-18','2021-07-25','2021-12-31','2022-06-03','2022-07-28','2022-09-01','2022-09-13','2022-10-29','2022-11-19','2022-12-26')
, (150,12185,2,83,'2021-06-08','2022-03-08','2022-07-31','2022-12-28','2023-02-24','2023-03-18','2023-04-06','2023-05-25','2023-05-30','2023-06-04')
, (95,7303,2,10,null,null,null,null,null,null,null,null,null,null)
, (34,3099,1,60,'2024-03-25','2024-11-11','2025-02-15',null,null,null,null,null,null,null)
, (32,19681,3,31,'2021-11-22','2022-11-07','2023-02-09','2023-04-29','2023-07-28','2023-08-22','2023-08-31','2023-09-26','2023-11-12','2023-12-27')
, (62,4695,1,65,'2020-06-12','2020-09-09','2021-08-22','2022-03-10','2022-03-13','2022-06-08','2022-06-20','2022-07-28','2022-08-15','2022-10-04')
, (17,858,2,5,null,null,null,null,null,null,null,null,null,null)
, (89,13578,2,2,'2021-02-18','2022-01-28','2022-10-22','2022-11-28','2022-12-16','2023-03-21','2023-03-28','2023-05-04','2023-05-18','2023-07-06')
, (44,13626,1,35,null,null,null,null,null,null,null,null,null,null)
, (21,9149,3,47,null,null,null,null,null,null,null,null,null,null)
, (132,4243,2,90,null,null,null,null,null,null,null,null,null,null)
, (93,12798,3,30,'2021-06-30','2021-07-01','2021-12-20','2022-09-27','2022-11-12','2023-01-22','2023-02-03','2023-03-03','2023-03-05','2023-04-02')
, (86,6778,2,78,'2021-04-11','2021-11-13','2022-11-10','2022-12-20','2023-01-13','2023-02-20','2023-03-16','2023-04-12','2023-05-26','2023-06-11')
, (118,10639,3,92,'2024-05-12','2024-11-18',null,null,null,null,null,null,null,null)
, (111,2324,3,21,'2020-07-21','2021-06-03','2021-10-26','2021-11-25','2021-12-25','2022-03-17','2022-03-26','2022-04-11','2022-05-19','2022-07-06')
, (22,6366,2,4,'2023-04-12','2023-06-11','2024-02-28','2025-02-21','2025-03-08',null,null,null,null,null)
, (143,3219,2,62,'2022-06-14','2022-08-09','2022-11-24','2023-02-14','2023-04-10','2023-05-04','2023-05-28','2023-07-20','2023-08-22','2023-08-23')
, (129,13277,2,52,'2022-12-05','2023-05-10','2023-11-28','2024-01-21','2024-04-19','2024-05-03','2024-05-16','2024-06-05','2024-07-28','2024-08-08')
, (50,7612,2,61,'2022-05-19','2022-07-16','2022-08-19','2022-12-27','2023-02-28','2023-06-01','2023-06-05','2023-06-22','2023-06-22','2023-07-27')
, (23,2492,1,49,'2022-09-27','2023-07-05','2023-08-31','2024-06-21','2024-07-13','2024-09-03','2024-10-02','2024-11-10','2024-12-09','2025-01-24')
, (3,8014,2,15,null,null,null,null,null,null,null,null,null,null)
, (93,5059,1,65,'2024-07-07','2025-05-03',null,null,null,null,null,null,null,null)
, (59,10510,2,35,null,null,null,null,null,null,null,null,null,null)
, (150,13351,1,13,null,null,null,null,null,null,null,null,null,null)
, (42,7799,3,24,null,null,null,null,null,null,null,null,null,null)
, (138,631,3,80,'2020-06-02','2020-10-25','2021-05-05','2021-09-06','2021-11-11','2022-03-02','2022-03-25','2022-04-19','2022-04-28','2022-06-03')
, (48,8250,2,93,null,null,null,null,null,null,null,null,null,null)
, (109,7822,1,61,'2022-02-13','2023-01-28','2023-06-25','2024-03-05','2024-05-21','2024-06-29','2024-07-04','2024-07-07','2024-08-31','2024-10-23')
, (103,2860,1,60,'2025-05-08',null,null,null,null,null,null,null,null,null)
, (3,18814,1,97,'2023-08-12','2024-08-10','2024-11-15','2025-03-20',null,null,null,null,null,null)
, (48,15031,2,13,null,null,null,null,null,null,null,null,null,null)
, (26,4054,3,74,null,null,null,null,null,null,null,null,null,null)
, (91,114,1,16,'2024-03-12','2024-12-12','2025-03-04',null,null,null,null,null,null,null)
, (29,16766,1,53,'2021-08-08','2021-08-21','2022-07-06','2023-06-14','2023-08-01','2023-08-12','2023-09-05','2023-09-28','2023-10-20','2023-12-18')
, (90,2504,3,49,null,null,null,null,null,null,null,null,null,null)
, (73,7560,2,63,'2024-06-26','2024-08-01','2024-12-25','2025-04-02',null,null,null,null,null,null)
, (35,7059,1,77,'2022-05-05','2022-06-22','2022-09-22','2023-05-19','2023-06-13','2023-09-07','2023-09-29','2023-11-04','2023-11-23','2023-12-22')
, (141,9352,3,22,'2023-04-30','2023-11-20','2024-04-20','2024-06-18','2024-08-06','2024-08-16','2024-08-21','2024-09-27','2024-11-07','2025-01-03')
, (36,6230,3,100,'2022-02-22','2022-08-19','2023-05-22','2023-05-28','2023-08-11','2023-10-01','2023-10-10','2023-11-14','2024-01-04','2024-01-24')
, (74,374,1,23,'2025-04-07',null,null,null,null,null,null,null,null,null)
, (2,8706,3,88,null,null,null,null,null,null,null,null,null,null)
, (46,15690,1,53,null,null,null,null,null,null,null,null,null,null)
, (31,7520,2,24,'2023-05-16','2023-06-17','2024-03-27','2025-02-06','2025-03-02',null,null,null,null,null)
, (123,15802,1,99,null,null,null,null,null,null,null,null,null,null)
, (52,15537,3,67,null,null,null,null,null,null,null,null,null,null)
, (66,3567,2,66,'2020-10-28','2021-04-11','2022-01-08','2022-07-09','2022-09-11','2022-12-20','2023-01-04','2023-02-21','2023-03-17','2023-03-25')
, (6,19242,3,31,null,null,null,null,null,null,null,null,null,null)
, (20,8318,1,71,'2021-04-28','2021-06-27','2022-02-11','2022-02-15','2022-03-24','2022-07-02','2022-07-07','2022-08-04','2022-08-05','2022-08-24')
, (78,3577,1,3,'2023-01-01','2023-09-23','2024-04-20','2024-09-26','2024-12-25','2025-02-11','2025-02-16','2025-04-12','2025-05-03',null)
, (26,6407,3,10,'2021-09-01','2021-09-04','2021-11-02','2022-05-02','2022-07-10','2022-08-19','2022-09-02','2022-10-29','2022-12-05','2022-12-19')
, (33,6359,2,4,'2024-09-08','2024-09-19',null,null,null,null,null,null,null,null)
, (96,8233,3,64,'2021-07-23','2021-10-04','2021-11-08','2022-04-04','2022-04-29','2022-07-31','2022-08-18','2022-09-19','2022-10-23','2022-12-22')
, (148,1910,1,19,'2024-07-28',null,null,null,null,null,null,null,null,null)
, (49,10919,3,51,'2024-09-02','2024-11-01',null,null,null,null,null,null,null,null)
, (97,1085,3,6,'2024-03-16','2024-03-24','2024-06-08','2024-11-30','2024-12-11','2025-02-21','2025-03-21','2025-04-24',null,null)
, (117,7923,1,39,'2020-12-31','2021-08-06','2021-11-08','2022-05-05','2022-07-05','2022-10-18','2022-11-01','2022-11-08','2022-12-02','2023-01-30')
, (89,7410,2,12,'2023-04-28','2023-07-17','2023-08-22','2023-11-29','2023-12-11','2024-02-14','2024-03-07','2024-04-22','2024-06-06','2024-06-06')
, (118,7916,1,71,null,null,null,null,null,null,null,null,null,null)
, (138,831,2,32,null,null,null,null,null,null,null,null,null,null)
, (99,816,2,32,null,null,null,null,null,null,null,null,null,null)
, (112,11291,2,70,'2021-01-03','2021-02-14','2021-04-10','2021-05-24','2021-08-02','2021-08-11','2021-08-30','2021-08-30','2021-09-21','2021-10-12')
, (36,5526,2,91,null,null,null,null,null,null,null,null,null,null)
, (51,12257,3,33,null,null,null,null,null,null,null,null,null,null)
, (90,5086,3,65,'2020-08-18','2021-03-31','2021-04-02','2021-05-30','2021-06-17','2021-10-11','2021-10-19','2021-12-08','2022-01-19','2022-02-22')
, (119,4831,1,100,'2020-06-27','2021-03-13','2021-09-07','2022-08-28','2022-11-12','2023-01-24','2023-01-24','2023-02-24','2023-04-08','2023-05-07')
, (75,114,3,16,'2021-06-24','2022-01-20','2022-09-26','2023-06-26','2023-08-31','2023-12-18','2023-12-30','2024-02-01','2024-03-18','2024-03-19')
, (17,9132,2,88,'2021-11-06','2021-12-07','2022-02-05','2022-04-24','2022-06-07','2022-08-16','2022-08-19','2022-08-27','2022-08-27','2022-10-01')
, (41,11879,3,33,'2022-09-28','2023-07-06','2024-06-11','2025-01-18','2025-04-13',null,null,null,null,null)
, (91,4239,1,42,'2022-05-10','2022-08-05','2023-07-29','2024-06-06','2024-08-11','2024-08-19','2024-08-29','2024-10-26','2024-11-08','2024-12-17')
, (60,12391,2,34,'2024-07-01','2025-01-11','2025-05-06',null,null,null,null,null,null,null)
, (36,2114,1,49,null,null,null,null,null,null,null,null,null,null)
, (122,13992,1,55,'2020-08-08','2020-10-22','2021-10-19','2021-11-26','2021-12-25','2022-02-23','2022-02-28','2022-04-25','2022-06-06','2022-08-03')
, (105,859,2,32,null,null,null,null,null,null,null,null,null,null)
, (80,11585,3,26,'2025-04-21',null,null,null,null,null,null,null,null,null)
, (14,4113,1,79,null,null,null,null,null,null,null,null,null,null)
, (50,18389,2,54,null,null,null,null,null,null,null,null,null,null)
, (95,10299,1,51,'2022-05-04','2022-11-18','2023-04-24','2024-04-13','2024-06-17','2024-09-24','2024-10-01','2024-10-31','2024-11-12','2024-12-28')
, (72,7442,2,81,'2022-10-16','2023-01-06','2023-09-16','2024-05-15','2024-07-16','2024-10-27','2024-11-01','2024-12-18','2025-01-14','2025-03-08')
, (107,5905,2,18,'2024-08-07','2025-01-03',null,null,null,null,null,null,null,null)
, (149,4111,3,82,'2021-08-24','2021-10-10','2022-02-19','2023-02-17','2023-03-13','2023-04-14','2023-04-24','2023-06-02','2023-07-15','2023-08-31')
, (79,11670,1,70,'2025-02-04',null,null,null,null,null,null,null,null,null)
, (104,4197,1,89,null,null,null,null,null,null,null,null,null,null)
, (15,4117,2,89,null,null,null,null,null,null,null,null,null,null)
, (101,8144,3,63,'2023-07-03','2023-12-05','2024-03-13','2025-02-14','2025-05-02',null,null,null,null,null)
, (28,6065,2,81,'2024-09-07','2024-12-01','2024-12-08',null,null,null,null,null,null,null)
, (104,19092,3,97,'2021-05-28','2022-03-28','2022-07-12','2022-09-14','2022-10-23','2023-02-17','2023-03-01','2023-03-04','2023-04-07','2023-05-09')
, (34,8454,3,71,'2021-02-01','2021-05-05','2021-08-23','2022-01-23','2022-02-10','2022-02-15','2022-03-12','2022-05-03','2022-05-26','2022-07-08')
, (18,10865,3,59,'2024-04-04','2024-06-21','2025-03-23',null,null,null,null,null,null,null)
, (34,13911,3,46,'2025-02-27',null,null,null,null,null,null,null,null,null)
, (32,4793,1,65,null,null,null,null,null,null,null,null,null,null)
, (31,12863,2,84,null,null,null,null,null,null,null,null,null,null)
, (55,12549,3,76,'2020-10-02','2020-12-17','2021-01-24','2021-09-10','2021-11-02','2021-12-22','2022-01-15','2022-02-22','2022-04-20','2022-05-11')
, (101,584,1,56,'2023-11-27','2024-05-16','2025-01-02','2025-02-04','2025-04-30',null,null,null,null,null)
, (72,15351,3,97,'2024-12-11',null,null,null,null,null,null,null,null,null)
, (53,5169,2,9,'2022-11-09','2023-06-11','2024-05-19','2024-08-28','2024-08-29','2024-12-17','2024-12-25','2025-02-21','2025-03-02','2025-03-16')
, (146,4880,1,27,'2021-11-13','2022-02-17','2023-01-02','2023-12-05','2023-12-09','2023-12-21','2023-12-31','2024-01-21','2024-03-19','2024-04-28')
, (11,12036,3,30,'2024-01-15','2024-04-28','2025-02-28',null,null,null,null,null,null,null)
, (136,9533,3,96,'2024-11-28',null,null,null,null,null,null,null,null,null)
, (135,12130,1,13,'2025-01-18',null,null,null,null,null,null,null,null,null)
, (23,13717,3,57,'2023-10-03','2023-10-28','2024-03-14','2024-12-06','2025-02-10','2025-04-12','2025-04-18','2025-05-01',null,null)
, (56,7118,1,61,null,null,null,null,null,null,null,null,null,null)
, (141,3417,1,89,'2024-12-08','2025-04-09',null,null,null,null,null,null,null,null)
, (129,7463,1,64,null,null,null,null,null,null,null,null,null,null)
, (149,17248,1,53,'2024-04-09','2024-06-21','2025-03-15','2025-04-05',null,null,null,null,null,null)
, (141,8243,2,22,'2025-05-08',null,null,null,null,null,null,null,null,null)
, (68,12653,3,2,'2023-04-13','2024-01-14','2024-11-27',null,null,null,null,null,null,null)
, (59,13671,2,52,'2021-07-25','2021-08-04','2022-03-02','2022-03-11','2022-05-16','2022-08-30','2022-09-25','2022-11-06','2022-12-29','2023-02-09')
, (141,8090,2,12,'2022-10-25','2023-10-11','2024-02-17','2024-11-06','2024-12-30','2025-03-18','2025-04-13','2025-04-28',null,null)
, (112,3725,1,82,'2024-03-30','2025-02-04',null,null,null,null,null,null,null,null)
, (120,14627,1,36,'2021-12-09','2022-02-24','2022-10-19','2023-08-15','2023-08-17','2023-08-24','2023-09-12','2023-10-04','2023-12-01','2024-01-07')
, (9,65,3,1,'2024-11-08',null,null,null,null,null,null,null,null,null)
, (150,18430,1,67,'2023-07-08','2023-10-07','2023-10-19','2024-01-13','2024-02-03','2024-05-13','2024-05-21','2024-06-25','2024-06-27','2024-06-30')
, (143,11389,1,44,'2020-08-02','2021-03-21','2021-12-04','2022-01-30','2022-01-31','2022-05-22','2022-06-11','2022-07-28','2022-07-31','2022-09-16')
, (42,15617,2,43,'2023-10-11','2024-08-07','2024-12-06','2024-12-11','2025-02-06',null,null,null,null,null)
, (81,3383,3,89,'2022-03-25','2022-08-30','2023-01-19','2023-10-06','2024-01-04','2024-03-08','2024-04-06','2024-04-19','2024-04-25','2024-05-03')
, (22,7075,2,4,null,null,null,null,null,null,null,null,null,null)
, (86,18824,1,99,'2022-04-04','2022-11-22','2022-12-13','2023-11-03','2023-11-22','2024-01-20','2024-02-16','2024-03-09','2024-04-01','2024-05-24')
, (58,975,1,32,null,null,null,null,null,null,null,null,null,null)
, (36,14470,3,25,'2022-11-27','2023-11-20','2024-05-11','2024-06-17','2024-09-13','2024-12-09','2024-12-17','2025-01-11','2025-01-14','2025-01-25')
, (108,8347,3,37,'2021-11-17','2021-12-03','2022-06-06','2022-10-28','2022-11-01','2023-02-06','2023-02-20','2023-02-26','2023-04-02','2023-05-14')
, (4,353,2,87,null,null,null,null,null,null,null,null,null,null)
, (106,9967,2,76,'2022-11-26','2023-08-11','2024-07-14','2025-01-19','2025-04-05',null,null,null,null,null)
, (36,12972,3,52,'2022-06-27','2022-11-19','2023-10-30','2024-06-27','2024-08-11','2024-08-11','2024-09-06','2024-09-14','2024-11-01','2024-11-22')
, (148,11093,3,35,'2024-02-17','2024-04-01','2024-10-07',null,null,null,null,null,null,null)
, (33,7951,1,45,'2024-05-17','2025-01-20',null,null,null,null,null,null,null,null)
, (94,17320,1,97,'2023-12-11','2024-12-09',null,null,null,null,null,null,null,null)
, (9,9521,2,45,'2023-07-12','2023-11-01','2023-11-27','2024-09-11','2024-10-02','2024-12-18','2025-01-08','2025-02-08','2025-03-28','2025-04-29')
, (140,4911,1,100,'2024-04-12','2024-11-01',null,null,null,null,null,null,null,null)
, (87,1766,2,14,'2024-03-01','2024-08-31',null,null,null,null,null,null,null,null)
, (133,12103,3,13,'2023-11-09','2024-03-01','2024-12-04',null,null,null,null,null,null,null)
, (17,13059,1,44,'2020-09-11','2021-07-11','2021-11-18','2022-01-26','2022-04-12','2022-06-01','2022-06-18','2022-07-18','2022-09-16','2022-10-06')
, (109,13768,2,36,'2021-10-15','2022-10-09','2023-06-15','2024-02-26','2024-03-15','2024-06-01','2024-06-04','2024-07-29','2024-08-03','2024-08-24')
, (51,13032,3,52,null,null,null,null,null,null,null,null,null,null)
, (88,10507,3,84,'2023-07-25','2024-02-11','2025-01-17',null,null,null,null,null,null,null)
, (101,1884,2,19,null,null,null,null,null,null,null,null,null,null)
, (18,11689,3,8,'2020-06-09','2021-05-17','2021-06-03','2022-04-24','2022-06-17','2022-08-31','2022-09-19','2022-10-22','2022-11-13','2022-12-20')
, (73,7994,2,64,null,null,null,null,null,null,null,null,null,null)
, (13,8980,3,58,null,null,null,null,null,null,null,null,null,null)
, (78,2023,3,19,'2021-04-20','2021-07-03','2021-11-19','2022-05-12','2022-05-13','2022-05-14','2022-05-17','2022-06-17','2022-07-31','2022-08-15')
, (4,15153,1,8,'2025-04-20',null,null,null,null,null,null,null,null,null)
, (27,8801,3,63,'2024-04-05','2025-01-03','2025-03-13',null,null,null,null,null,null,null)
, (78,10493,3,88,'2020-08-07','2021-01-17','2021-06-01','2022-04-18','2022-04-24','2022-06-04','2022-06-10','2022-06-24','2022-08-18','2022-09-04')
, (26,6492,3,81,null,null,null,null,null,null,null,null,null,null)
, (38,11132,2,30,'2024-02-17','2024-06-18','2024-11-11','2025-02-24',null,null,null,null,null,null)
, (48,5468,2,27,'2021-12-08','2022-02-09','2022-06-27','2022-08-14','2022-10-05','2022-12-10','2022-12-27','2023-01-21','2023-02-25','2023-03-30')
, (133,16776,3,31,null,null,null,null,null,null,null,null,null,null)
, (129,17341,2,54,'2020-12-05','2021-06-29','2022-03-03','2022-04-20','2022-05-10','2022-08-13','2022-08-25','2022-10-03','2022-11-23','2022-12-15')
, (20,6950,3,61,null,null,null,null,null,null,null,null,null,null)
, (131,10596,2,92,'2025-03-30',null,null,null,null,null,null,null,null,null)
, (18,2442,3,49,'2023-05-18','2023-11-10','2023-11-27','2024-01-07','2024-04-06','2024-08-03','2024-08-26','2024-10-04','2024-10-06','2024-11-27')
, (38,16737,3,40,'2022-11-15','2023-04-08','2023-04-19','2024-04-05','2024-06-15','2024-07-15','2024-07-30','2024-08-09','2024-08-29','2024-10-23')
, (149,8091,2,93,'2024-05-27','2024-09-10','2024-12-26',null,null,null,null,null,null,null)
, (28,489,2,23,'2021-05-17','2022-04-04','2023-02-20','2023-12-12','2024-01-17','2024-05-05','2024-05-12','2024-05-23','2024-07-18','2024-09-06')
, (17,14739,1,46,null,null,null,null,null,null,null,null,null,null)
, (50,11823,2,35,null,null,null,null,null,null,null,null,null,null)
, (113,4892,3,9,'2024-05-16','2024-10-26','2025-04-07',null,null,null,null,null,null,null)
, (100,7224,1,10,'2025-02-04',null,null,null,null,null,null,null,null,null)
, (137,7698,1,24,'2024-06-01',null,null,null,null,null,null,null,null,null)
, (128,11649,3,30,null,null,null,null,null,null,null,null,null,null)
, (143,8221,1,93,'2025-04-20',null,null,null,null,null,null,null,null,null)
, (118,11801,3,30,'2024-12-09',null,null,null,null,null,null,null,null,null)
, (33,9333,2,92,'2023-01-08','2023-01-16','2023-10-02','2023-12-19','2023-12-23','2024-04-01','2024-04-21','2024-05-24','2024-07-13','2024-08-16')
, (110,12831,1,35,'2024-10-06','2025-02-22',null,null,null,null,null,null,null,null)
, (42,15991,3,99,'2024-03-17','2024-05-09','2024-10-27',null,null,null,null,null,null,null)
, (111,4782,2,9,'2023-06-03','2024-03-11','2024-04-15','2024-07-14','2024-07-17','2024-10-29','2024-11-24','2024-11-29','2025-01-16','2025-01-23')
, (118,9282,1,48,'2020-09-01','2021-06-09','2022-03-02','2022-12-12','2022-12-14','2023-02-13','2023-03-01','2023-03-03','2023-04-01','2023-05-06')
, (67,11967,1,33,null,null,null,null,null,null,null,null,null,null)
, (111,10388,3,76,'2024-07-15','2025-03-06',null,null,null,null,null,null,null,null)
, (112,7807,2,58,null,null,null,null,null,null,null,null,null,null)
, (92,90,1,16,'2022-08-09','2023-03-09','2023-07-12','2024-07-05','2024-07-29','2024-08-22','2024-08-30','2024-09-18','2024-10-16','2024-11-12')
, (141,4402,1,27,'2024-10-15',null,null,null,null,null,null,null,null,null)
, (62,6358,3,77,'2023-04-22','2023-10-14','2024-05-04','2024-12-26','2025-03-14',null,null,null,null,null)
, (82,3733,2,20,'2024-11-02','2025-01-28',null,null,null,null,null,null,null,null)
, (107,734,2,56,'2025-03-15',null,null,null,null,null,null,null,null,null)
, (60,8018,3,61,null,null,null,null,null,null,null,null,null,null)
, (80,3332,1,79,null,null,null,null,null,null,null,null,null,null)
, (56,6299,3,18,'2022-04-28','2022-07-30','2023-07-11','2023-08-16','2023-09-05','2023-11-01','2023-11-10','2023-12-12','2023-12-28','2024-02-06')
, (107,5782,2,100,'2021-04-05','2021-10-26','2021-12-06','2022-07-26','2022-09-21','2022-12-10','2022-12-18','2023-01-30','2023-02-18','2023-04-19')
, (5,7072,2,12,null,null,null,null,null,null,null,null,null,null)
, (128,357,2,50,'2023-07-18','2023-09-17','2024-04-07','2025-03-25','2025-04-18',null,null,null,null,null)
, (116,7431,2,4,'2022-12-25','2023-09-30','2024-03-19','2024-04-30','2024-05-08','2024-07-14','2024-07-30','2024-08-09','2024-10-05','2024-10-26')
, (105,14253,1,8,'2020-07-24','2021-01-18','2021-07-30','2021-10-05','2021-12-06','2022-04-01','2022-05-01','2022-05-02','2022-05-19','2022-07-16')
, (18,13097,2,7,'2024-03-21','2024-05-29','2025-04-26',null,null,null,null,null,null,null)
, (67,4975,2,91,'2022-10-11','2023-09-03','2024-03-04','2024-05-31','2024-07-22','2024-09-26','2024-09-30','2024-11-21','2025-01-20','2025-03-02')
, (49,17488,3,31,'2021-11-19','2022-05-07','2022-11-06','2023-07-11','2023-09-16','2023-12-16','2024-01-10','2024-02-01','2024-03-07','2024-04-17')
, (89,117,2,16,'2024-05-06','2025-02-23',null,null,null,null,null,null,null,null)
, (36,12846,3,7,null,null,null,null,null,null,null,null,null,null)
, (137,10527,1,76,'2024-06-07','2024-10-08','2024-10-17','2024-12-01','2025-01-06','2025-03-24','2025-04-16','2025-04-16',null,null)
, (95,8486,1,78,'2022-07-26','2022-11-24','2023-08-18','2024-03-05','2024-05-12','2024-05-25','2024-06-21','2024-06-21','2024-07-25','2024-08-05')
, (92,18818,3,31,null,null,null,null,null,null,null,null,null,null)
, (9,10315,3,83,'2023-02-09','2023-09-13','2024-07-01','2024-09-06','2024-09-27','2024-11-25','2024-12-04','2024-12-12','2025-01-21','2025-02-21')
, (99,1876,3,14,'2021-12-17','2022-10-18','2023-02-11','2023-08-24','2023-09-07','2023-12-18','2024-01-01','2024-02-02','2024-03-16','2024-05-07')
, (31,9023,1,15,null,null,null,null,null,null,null,null,null,null)
, (52,9412,1,37,'2024-09-27',null,null,null,null,null,null,null,null,null)
, (55,338,3,87,'2023-07-06','2024-02-29','2024-03-23','2024-07-05','2024-09-12','2024-10-29','2024-11-18','2025-01-05','2025-02-22','2025-03-04')
, (86,12970,1,35,'2025-05-03',null,null,null,null,null,null,null,null,null)
, (44,1780,1,85,'2022-10-13','2022-11-20','2023-03-21','2023-06-14','2023-07-04','2023-07-11','2023-08-08','2023-09-20','2023-11-16','2023-12-06')
, (31,5061,2,65,'2023-11-22','2024-02-12','2024-08-14','2024-11-19','2025-01-25','2025-02-12','2025-02-13','2025-02-19','2025-03-20','2025-03-22')
, (70,7056,2,10,'2022-03-16','2023-01-26','2023-03-14','2023-06-18','2023-08-12','2023-08-22','2023-08-31','2023-10-05','2023-10-11','2023-12-01')
, (19,866,3,5,'2023-01-08','2023-08-06','2024-04-12','2024-04-28','2024-06-20','2024-09-12','2024-09-27','2024-10-02','2024-11-12','2025-01-10')
, (121,14129,2,8,'2024-06-15','2025-03-24',null,null,null,null,null,null,null,null)
, (31,17307,1,31,null,null,null,null,null,null,null,null,null,null)
, (40,6174,2,18,'2021-08-20','2021-12-01','2022-10-22','2023-03-18','2023-05-30','2023-07-27','2023-08-12','2023-08-19','2023-09-21','2023-09-29')
, (73,18577,1,97,'2021-09-21','2021-10-31','2021-11-10','2022-07-26','2022-09-23','2022-12-27','2023-01-05','2023-01-31','2023-03-19','2023-05-16')
, (105,12872,3,72,'2021-04-01','2022-03-24','2022-10-25','2023-02-13','2023-04-05','2023-04-22','2023-04-22','2023-06-04','2023-07-09','2023-08-11')
, (126,98,3,16,null,null,null,null,null,null,null,null,null,null)
, (7,907,1,5,'2020-11-15','2021-05-25','2021-12-08','2022-08-27','2022-10-26','2022-12-11','2023-01-04','2023-01-08','2023-02-25','2023-03-30')
, (107,5351,2,100,'2020-10-20','2021-07-17','2022-01-24','2022-03-21','2022-04-14','2022-04-17','2022-05-03','2022-06-26','2022-08-12','2022-10-10')
, (80,5031,2,100,null,null,null,null,null,null,null,null,null,null)
, (148,7050,3,64,null,null,null,null,null,null,null,null,null,null)
, (100,13555,3,52,null,null,null,null,null,null,null,null,null,null)
, (72,15432,2,31,null,null,null,null,null,null,null,null,null,null)
, (82,13651,1,46,'2022-07-15','2023-06-10','2023-10-15','2024-02-18','2024-05-14','2024-08-30','2024-09-22','2024-11-14','2024-12-08','2025-02-05')
, (73,8275,3,58,'2020-09-25','2021-05-20','2022-03-18','2022-12-21','2023-01-05','2023-04-02','2023-05-01','2023-05-14','2023-07-12','2023-07-28')
, (141,12864,3,98,'2021-09-06','2022-07-05','2022-09-18','2023-03-12','2023-05-22','2023-07-31','2023-08-21','2023-09-02','2023-09-25','2023-11-03')
, (45,11574,2,76,'2022-05-04','2022-10-13','2023-08-01','2023-11-28','2024-01-03','2024-05-02','2024-05-04','2024-05-23','2024-05-27','2024-07-07')
, (90,13530,1,7,null,null,null,null,null,null,null,null,null,null)
, (124,1761,2,85,'2021-10-26','2022-05-31','2022-11-15','2023-01-20','2023-02-10','2023-06-04','2023-06-04','2023-07-19','2023-08-08','2023-08-26')
, (130,10924,3,86,null,null,null,null,null,null,null,null,null,null)
, (36,16591,1,99,'2022-11-08','2023-06-23','2024-02-08','2024-09-22','2024-11-09','2024-12-12','2024-12-15','2025-02-11','2025-03-22','2025-05-08')
, (115,13613,3,8,'2023-12-14','2024-07-29',null,null,null,null,null,null,null,null)
, (129,1487,3,14,null,null,null,null,null,null,null,null,null,null)
, (35,4294,2,42,null,null,null,null,null,null,null,null,null,null)
, (131,7258,2,81,null,null,null,null,null,null,null,null,null,null)
, (66,14489,3,99,null,null,null,null,null,null,null,null,null,null)
, (25,602,2,80,null,null,null,null,null,null,null,null,null,null)
, (108,15478,2,99,'2020-08-30','2020-09-04','2021-04-02','2021-06-20','2021-07-06','2021-09-25','2021-10-14','2021-11-05','2021-11-13','2021-12-27')
, (5,6355,1,77,'2024-12-15',null,null,null,null,null,null,null,null,null)
, (130,12071,3,36,'2021-06-07','2022-03-08','2022-12-14','2023-03-21','2023-03-23','2023-04-30','2023-05-16','2023-05-26','2023-06-18','2023-07-05')
, (113,3143,2,60,null,null,null,null,null,null,null,null,null,null)
, (55,439,2,23,'2023-02-28','2023-09-05','2023-12-17','2024-05-21','2024-08-17','2024-09-03','2024-09-14','2024-09-25','2024-10-11','2024-10-24')
, (33,6200,3,18,'2024-09-23','2024-10-14','2025-05-04',null,null,null,null,null,null,null)
, (106,1889,2,85,'2022-07-05','2023-04-01','2023-07-02','2024-01-22','2024-03-23','2024-04-03','2024-04-08','2024-04-26','2024-06-06','2024-06-18')
, (7,2180,1,21,null,null,null,null,null,null,null,null,null,null)
, (149,1507,3,14,null,null,null,null,null,null,null,null,null,null)
, (143,7289,2,39,'2020-06-26','2020-07-17','2020-07-23','2021-03-09','2021-04-22','2021-04-30','2021-05-27','2021-06-13','2021-07-23','2021-08-02')
, (45,13805,3,36,'2022-08-10','2023-03-13','2023-08-10','2023-08-11','2023-10-15','2023-11-06','2023-11-23','2023-12-25','2024-01-17','2024-02-11')
, (24,1105,3,6,'2023-08-06','2024-02-16','2024-07-27',null,null,null,null,null,null,null)
, (139,1598,2,19,null,null,null,null,null,null,null,null,null,null)
, (104,4620,3,9,'2023-12-17','2024-05-05','2025-04-06',null,null,null,null,null,null,null)
, (121,3622,2,66,'2021-03-19','2021-07-20','2022-04-02','2023-01-09','2023-02-10','2023-02-17','2023-02-25','2023-02-26','2023-03-04','2023-03-14')
, (124,10331,2,11,'2022-10-10','2022-12-22','2023-11-12','2023-12-13','2024-01-23','2024-02-27','2024-03-18','2024-04-09','2024-06-01','2024-06-16')
, (19,12100,2,59,null,null,null,null,null,null,null,null,null,null)
, (130,8378,1,64,'2020-09-24','2020-10-24','2020-11-07','2021-05-31','2021-08-29','2021-09-17','2021-10-11','2021-11-06','2021-12-05','2022-01-21')
, (4,4855,3,65,'2022-11-06','2023-07-31','2023-09-20','2023-10-11','2023-11-12','2024-01-07','2024-02-05','2024-03-16','2024-04-09','2024-04-23')
, (71,14703,1,57,'2022-09-10','2023-05-14','2023-08-31','2023-11-03','2023-11-22','2024-02-23','2024-03-03','2024-04-03','2024-05-04','2024-06-30')
, (83,7381,3,22,'2024-04-13','2024-12-26','2025-01-23',null,null,null,null,null,null,null)
, (141,743,3,56,null,null,null,null,null,null,null,null,null,null)
, (46,8924,2,39,'2022-07-16','2023-05-20','2024-02-17','2024-12-17','2025-03-15',null,null,null,null,null)
, (25,12148,3,13,'2022-04-08','2022-12-25','2023-02-19','2023-09-19','2023-10-28','2024-01-29','2024-02-16','2024-02-28','2024-04-25','2024-06-17')
, (131,10621,2,70,null,null,null,null,null,null,null,null,null,null)
, (80,13470,2,25,'2020-10-28','2021-07-05','2022-05-22','2022-12-16','2023-01-15','2023-03-29','2023-04-18','2023-06-04','2023-07-13','2023-07-17')
, (74,3613,3,60,'2020-09-20','2021-06-14','2021-12-23','2022-10-21','2022-10-23','2022-11-16','2022-12-13','2022-12-18','2022-12-25','2022-12-25')
, (56,601,2,56,'2023-08-24','2024-02-15','2024-08-12',null,null,null,null,null,null,null)
, (98,12893,2,46,null,null,null,null,null,null,null,null,null,null)
, (123,16835,2,54,'2022-05-21','2023-03-31','2023-06-29','2023-07-30','2023-08-04','2023-08-26','2023-09-12','2023-11-11','2023-12-25','2024-01-24')
, (11,4562,1,27,'2024-05-26','2025-04-05','2025-04-20',null,null,null,null,null,null,null)
, (136,12386,1,55,'2024-11-12',null,null,null,null,null,null,null,null,null)
, (138,5223,1,9,'2020-06-26','2020-07-31','2020-09-06','2021-07-23','2021-08-13','2021-11-01','2021-11-08','2021-11-19','2021-12-20','2022-02-06')
, (57,14945,3,36,'2023-03-07','2024-01-30','2025-01-06',null,null,null,null,null,null,null)
, (54,5389,1,91,'2024-03-31','2024-08-15',null,null,null,null,null,null,null,null)
, (102,4300,2,42,null,null,null,null,null,null,null,null,null,null)
, (58,7446,3,10,'2022-06-19','2022-10-09','2023-05-13','2024-04-28','2024-06-02','2024-06-17','2024-07-04','2024-07-30','2024-09-13','2024-10-05')
, (40,13379,1,17,'2021-12-22','2021-12-24','2022-01-23','2022-08-07','2022-10-18','2022-11-05','2022-11-21','2023-01-06','2023-02-28','2023-03-18')
, (58,4118,3,74,'2020-06-06','2020-10-03','2021-03-27','2021-10-16','2021-12-22','2021-12-30','2022-01-16','2022-03-07','2022-04-18','2022-05-16')
, (24,12190,2,59,'2022-08-06','2022-10-13','2022-12-18','2023-09-06','2023-12-01','2024-03-07','2024-03-28','2024-04-25','2024-05-24','2024-07-02')
, (18,9110,1,48,'2021-03-17','2021-06-23','2021-12-22','2022-05-03','2022-07-10','2022-10-18','2022-11-02','2022-11-24','2022-12-29','2023-01-30')
, (32,16255,1,99,null,null,null,null,null,null,null,null,null,null)
;

SELECT * FROM orderline
OFFSET (SELECT COUNT(*) FROM orderline) - 10
;

-- ASSIGNMENT
INSERT INTO assignment (
      phase_id
    , date
    , description
    )
    VALUES
          (1, '2023-01-01', 'Daily assignment for assignment1')
        , (2, '2023-01-02', 'Daily assignment for assignment2')
        , (3, '2023-01-03', 'Daily assignment for assignment3')
        , (4, '2023-01-04', 'Daily assignment for assignment4')
        , (5, '2023-01-05', 'Daily assignment for assignment5')
        ;
SELECT * FROM assignment;