
SET client_min_messages TO WARNING;
-- removes unnecessary messages from the console


/*
-- Drop all tables in the correct order to avoid foreign key constraint issues
DROP TABLE IF EXISTS assignment CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS phase CASCADE;
DROP TABLE IF EXISTS orderline CASCADE;
DROP TABLE IF EXISTS article CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS address CASCADE;
*/

-- this command removes unnecessary messages from the console

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

-- PGSQL CODE TO UPLOAD DATA FROM ADDRESS.CSV TO ADDRESS TABLE
-- TRUNCATE TABLE address CASCADE;
-- ALTER SEQUENCE address_address_id_seq RESTART WITH 1;
COPY address (street, house_number, postal_code, municipality, longitude, latitude)
FROM 'C:/_MaRn/syntra/projects/python_eindopdracht/proof_of_concept_folium/addresses/addresses.csv'
-- TODO: find a way to get the path from the config file
DELIMITER ','
CSV HEADER
;

SELECT * FROM address
LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM address) - 10; -- last 10 lines
/*
*/
;

/*
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
    ('Rijksweg', '454', '7700', 'Moeskroen', 'BE'),
    ('Lindenlaan', '505', '8000', 'Brugge', 'BE'),
    ('Eikenstraat', '606', '9000', 'Gent', 'BE'),
    ('Beukenlaan', '707', '1000', 'Brussel', 'BE'),
    ('Wilgenstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Dennendreef', '909', '3000', 'Leuven', 'BE'),
    ('Berkenlaan', '101', '4000', 'Luik', 'BE'),
    ('Acacialaan', '202', '5000', 'Namen', 'BE'),
    ('Kastanjelaan', '303', '6000', 'Charleroi', 'BE'),
    ('Populierenstraat', '404', '7000', 'Mons', 'BE'),
    ('Esdoornlaan', '505', '8000', 'Brugge', 'BE'),
    ('Hazelaarstraat', '606', '9000', 'Gent', 'BE'),
    ('Olmenlaan', '707', '1000', 'Brussel', 'BE'),
    ('Cederstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Lorkendreef', '909', '3000', 'Leuven', 'BE'),
    ('Plataanlaan', '101', '4000', 'Luik', 'BE'),
    ('Magnolialaan', '202', '5000', 'Namen', 'BE'),
    ('Tulpstraat', '303', '6000', 'Charleroi', 'BE'),
    ('Rozenlaan', '404', '7000', 'Mons', 'BE'),
    ('Viooltjesstraat', '505', '8000', 'Brugge', 'BE'),
    ('Narcissenlaan', '606', '9000', 'Gent', 'BE'),
    ('Dahlialaan', '707', '1000', 'Brussel', 'BE'),
    ('Irisstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Fresialaan', '909', '3000', 'Leuven', 'BE'),
    ('Anemonenlaan', '101', '4000', 'Luik', 'BE'),
    ('Krokusstraat', '202', '5000', 'Namen', 'BE'),
    ('Zonnebloemlaan', '303', '6000', 'Charleroi', 'BE'),
    ('Lavendelstraat', '404', '7000', 'Mons', 'BE'),
    ('Kamperfoelielaan', '505', '8000', 'Brugge', 'BE'),
    ('Jasmijnstraat', '606', '9000', 'Gent', 'BE'),
    ('Hortensialaan', '707', '1000', 'Brussel', 'BE'),
    ('Geraniumstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Chrysantenlaan', '909', '3000', 'Leuven', 'BE'),
    ('Asterstraat', '101', '4000', 'Luik', 'BE'),
    ('Gladiolenlaan', '202', '5000', 'Namen', 'BE'),
    ('Hyacintenstraat', '303', '6000', 'Charleroi', 'BE'),
    ('Lelielaan', '404', '7000', 'Mons', 'BE'),
    ('Orchideestraat', '505', '8000', 'Brugge', 'BE'),
    ('Pioenrozenlaan', '606', '9000', 'Gent', 'BE'),
    ('Rhododendronstraat', '707', '1000', 'Brussel', 'BE'),
    ('Seringenlaan', '808', '2000', 'Antwerpen', 'BE'),
    ('Varenstraat', '909', '3000', 'Leuven', 'BE'),
    ('Wisterialaan', '101', '4000', 'Luik', 'BE'),
    ('Zinnialaan', '202', '5000', 'Namen', 'BE'),
    ('Begonialaan', '303', '6000', 'Charleroi', 'BE'),
    ('Cyclamenstraat', '404', '7000', 'Mons', 'BE'),
    ('Druivenlaan', '505', '8000', 'Brugge', 'BE'),
    ('Frambozenstraat', '606', '9000', 'Gent', 'BE'),
    ('Aardbeilaan', '707', '1000', 'Brussel', 'BE'),
    ('Bessenstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Kersenlaan', '909', '3000', 'Leuven', 'BE'),
    ('Perzikstraat', '101', '4000', 'Luik', 'BE'),
    ('Appelstraat', '202', '5000', 'Namen', 'BE'),
    ('Pruimenlaan', '303', '6000', 'Charleroi', 'BE'),
    ('Abrikozenstraat', '404', '7000', 'Mons', 'BE'),
    ('Mangoelaan', '505', '8000', 'Brugge', 'BE'),
    ('Papayalaan', '606', '9000', 'Gent', 'BE'),
    ('Bananenstraat', '707', '1000', 'Brussel', 'BE'),
    ('Citroenlaan', '808', '2000', 'Antwerpen', 'BE'),
    ('Limoenstraat', '909', '3000', 'Leuven', 'BE'),
    ('Sinaasappellaan', '101', '4000', 'Luik', 'BE'),
    ('Mandarijnstraat', '202', '5000', 'Namen', 'BE'),
    ('Kiwiweg', '303', '6000', 'Charleroi', 'BE'),
    ('Ananasstraat', '404', '7000', 'Mons', 'BE'),
    ('Kokoslaan', '505', '8000', 'Brugge', 'BE'),
    ('Avocadostraat', '606', '9000', 'Gent', 'BE'),
    ('Tomatenlaan', '707', '1000', 'Brussel', 'BE'),
    ('Komkommerstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Paprikalaan', '909', '3000', 'Leuven', 'BE'),
    ('Courgettestraat', '101', '4000', 'Luik', 'BE'),
    ('Auberginestraat', '202', '5000', 'Namen', 'BE'),
    ('Wortellaan', '303', '6000', 'Charleroi', 'BE'),
    ('Radijsstraat', '404', '7000', 'Mons', 'BE'),
    ('Spinazielaan', '505', '8000', 'Brugge', 'BE'),
    ('Broccolistraat', '606', '9000', 'Gent', 'BE'),
    ('Bloemkoollaan', '707', '1000', 'Brussel', 'BE'),
    ('Spruitjesstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Erwtenlaan', '909', '3000', 'Leuven', 'BE'),
    ('Bonenstraat', '101', '4000', 'Luik', 'BE'),
    ('Linzenlaan', '202', '5000', 'Namen', 'BE'),
    ('Kikkererwtenstraat', '303', '6000', 'Charleroi', 'BE'),
    ('Sojabonenlaan', '404', '7000', 'Mons', 'BE'),
    ('Quinoastraat', '505', '8000', 'Brugge', 'BE'),
    ('Rijstlaan', '606', '9000', 'Gent', 'BE'),
    ('Pastastraat', '707', '1000', 'Brussel', 'BE'),
    ('Broodlaan', '808', '2000', 'Antwerpen', 'BE'),
    ('Croissantstraat', '909', '3000', 'Leuven', 'BE'),
    ('Pannenkoekenlaan', '101', '4000', 'Luik', 'BE'),
    ('Wafelstraat', '202', '5000', 'Namen', 'BE'),
    ('Chocoladelaan', '303', '6000', 'Charleroi', 'BE'),
    ('Koekjesstraat', '404', '7000', 'Mons', 'BE'),
    ('Ijsjeslaan', '505', '8000', 'Brugge', 'BE'),
    ('Taartstraat', '606', '9000', 'Gent', 'BE'),
    ('Puddinglaan', '707', '1000', 'Brussel', 'BE'),
    ('Yoghurtstraat', '808', '2000', 'Antwerpen', 'BE'),
    ('Melklaan', '909', '3000', 'Leuven', 'BE'),
    ('Kaasstraat', '101', '4000', 'Luik', 'BE'),
    ('Boterlaan', '202', '5000', 'Namen', 'BE'),
    ('Eistraat', '303', '6000', 'Charleroi', 'BE'),
    ('Roomlaan', '404', '7000', 'Mons', 'BE')

;
SELECT * FROM address;
*/

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
    ('Nina', 'De Bruin', 'Mevr.', '5554445555', 'nina.debruin@client.com')
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
    ('Finn', 'Van der Meer', 'Dhr.', '5555675678', 'finn.vandermeer@supplier.com')
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
    ('Michael', 'Van der Zanden', 'Dhr.', '5559012345', 'michael.vanderzanden@kitch.com')

;
SELECT * FROM person
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
    ('753159852', 8, 'Client H', 8),
    ('951753468', 9, 'Client I', 9),
    ('357951468', 10, 'Client J', 10),
    ('123987456', 11, 'Client K', 11),
    ('987123654', 12, 'Client L', 12),
    ('456321789', 13, 'Client M', 13),
    ('321987654', 14, 'Client N', 14),
    ('789654123', 15, 'Client O', 15),
    ('654789321', 16, 'Client P', 16),
    ('159486753', 17, 'Client Q', 17),
    ('753852159', 18, 'Client R', 18),
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
    ('951468951', 39, 'Client AM', 39),
    ('357468357', 40, 'Client AN', 40),
    ('123654123', 41, 'Client AO', 41),
    ('987456987', 42, 'Client AP', 42),
    ('456987654', 43, 'Client AQ', 43),
    ('321123321', 44, 'Client AR', 44),
    ('789321987', 45, 'Client AS', 45),
    ('654123654', 46, 'Client AT', 46),
    ('159753486', 47, 'Client AU', 47),
    ('753159852', 48, 'Client AV', 48),
    ('951753468', 49, 'Client AW', 49),
    ('357951468', 50, 'Client AX', 50),
    ('123987654', 51, 'Client AY', 51),
    ('987123456', 52, 'Client AZ', 52),
    ('456321987', 53, 'Client BA', 53),
    ('321987123', 54, 'Client BB', 54),
    ('789654321', 55, 'Client BC', 55),
    ('654789123', 56, 'Client BD', 56),
    ('159486753', 57, 'Client BE', 57),
    ('753852159', 58, 'Client BF', 58),
    ('951468357', 59, 'Client BG', 59),
    ('357468951', 60, 'Client BH', 60),
    ('123654789', 61, 'Client BI', 61),
    ('987456123', 62, 'Client BJ', 62),
    ('456987321', 63, 'Client BK', 63),
    ('321123987', 64, 'Client BL', 64),
    ('789321654', 65, 'Client BM', 65),
    ('654123987', 66, 'Client BN', 66),
    ('159753159', 67, 'Client BO', 67),
    ('753159753', 68, 'Client BP', 68),
    ('951753951', 69, 'Client BQ', 69),
    ('357951357', 70, 'Client BR', 70),
    ('123321456', 71, 'Client BS', 71),
    ('987789123', 72, 'Client BT', 72),
    ('456654789', 73, 'Client BU', 73),
    ('321456987', 74, 'Client BV', 74),
    ('789987321', 75, 'Client BW', 75),
    ('654321123', 76, 'Client BX', 76),
    ('159486159', 77, 'Client BY', 77),
    ('753852753', 78, 'Client BZ', 78),
    ('951468951', 79, 'Client CA', 79),
    ('357468357', 80, 'Client CB', 80),
    -- 20 suppliers
    ('258147369', 81, 'Supplier CC', 81),
    ('369258147', 82, 'Supplier CD', 82),
    ('147369258', 83, 'Supplier CE', 83),
    ('258369147', 84, 'Supplier CF', 84),
    ('369147258', 85, 'Supplier CG', 85),
    ('147258369', 86, 'Supplier CH', 86),
    ('258147369', 87, 'Supplier CI', 87),
    ('369258147', 88, 'Supplier CJ', 88),
    ('147369258', 89, 'Supplier CK', 89),
    ('258369147', 90, 'Supplier CL', 90),
    ('369147258', 91, 'Supplier CM', 91),
    ('147258369', 92, 'Supplier CN', 92),
    ('258147369', 93, 'Supplier CO', 93),
    ('369258147', 94, 'Supplier CP', 94),
    ('147369258', 95, 'Supplier CQ', 95),
    ('258369147', 96, 'Supplier CR', 96),
    ('369147258', 97, 'Supplier CS', 97),
    ('147258369', 98, 'Supplier CT', 98),
    ('258147369', 99, 'Supplier CU', 99),
    ('369258147', 100, 'Supplier CV', 100)

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
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20), (21), (22), (23), (24), (25), (26), (27), (28), (29), (30), (31), (32), (33), (34), (35), (36), (37), (38), (39), (40), (41), (42), (43), (44), (45), (46), (47), (48), (49), (50), (51), (52), (53), (54), (55), (56), (57), (58), (59), (60), (61), (62), (63), (64), (65), (66), (67), (68), (69), (70), (71), (72), (73), (74), (75), (76), (77), (78), (79), (80)
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
(81), (82), (83), (84), (85), (86), (87), (88), (89), (90), (91), (92), (93), (94), (95), (96), (97), (98), (99), (100);
SELECT * FROM supplier;

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
    (21, 'ART061', 6100.00, 'Description for article 61'),
    (21, 'ART062', 6200.00, 'Description for article 62'),
    (21, 'ART063', 6300.00, 'Description for article 63'),
    (22, 'ART064', 6400.00, 'Description for article 64'),
    (22, 'ART065', 6500.00, 'Description for article 65'),
    (22, 'ART066', 6600.00, 'Description for article 66'),
    (23, 'ART067', 6700.00, 'Description for article 67'),
    (23, 'ART068', 6800.00, 'Description for article 68'),
    (23, 'ART069', 6900.00, 'Description for article 69'),
    (24, 'ART070', 7000.00, 'Description for article 70'),
    (24, 'ART071', 7100.00, 'Description for article 71'),
    (24, 'ART072', 7200.00, 'Description for article 72'),
    (25, 'ART073', 7300.00, 'Description for article 73'),
    (25, 'ART074', 7400.00, 'Description for article 74'),
    (25, 'ART075', 7500.00, 'Description for article 75'),
    (26, 'ART076', 7600.00, 'Description for article 76'),
    (26, 'ART077', 7700.00, 'Description for article 77'),
    (26, 'ART078', 7800.00, 'Description for article 78'),
    (27, 'ART079', 7900.00, 'Description for article 79'),
    (27, 'ART080', 8000.00, 'Description for article 80'),
    (27, 'ART081', 8100.00, 'Description for article 81'),
    (28, 'ART082', 8200.00, 'Description for article 82'),
    (28, 'ART083', 8300.00, 'Description for article 83'),
    (28, 'ART084', 8400.00, 'Description for article 84'),
    (29, 'ART085', 8500.00, 'Description for article 85'),
    (29, 'ART086', 8600.00, 'Description for article 86'),
    (29, 'ART087', 8700.00, 'Description for article 87'),
    (30, 'ART088', 8800.00, 'Description for article 88'),
    (30, 'ART089', 8900.00, 'Description for article 89'),
    (30, 'ART090', 9000.00, 'Description for article 90'),
    (31, 'ART091', 9100.00, 'Description for article 91'),
    (31, 'ART092', 9200.00, 'Description for article 92'),
    (31, 'ART093', 9300.00, 'Description for article 93'),
    (32, 'ART094', 9400.00, 'Description for article 94'),
    (32, 'ART095', 9500.00, 'Description for article 95'),
    (32, 'ART096', 9600.00, 'Description for article 96'),
    (33, 'ART097', 9700.00, 'Description for article 97'),
    (33, 'ART098', 9800.00, 'Description for article 98'),
    (33, 'ART099', 9900.00, 'Description for article 99'),
    (34, 'ART100', 10000.00, 'Description for article 100')
    ;
SELECT * FROM article;

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
    date_acceptance     DATE NOT NULL,
    date_start          DATE, --NULL = ASAP
    date_end            DATE, --NULL = ASAP
    PRIMARY KEY (project_id),
    FOREIGN KEY (client_id) REFERENCES person(person_id),
    FOREIGN KEY (calculator_id) REFERENCES person(person_id),
    FOREIGN KEY (salesman_id) REFERENCES person(person_id),
    FOREIGN KEY (project_leader_id) REFERENCES person(person_id)
);
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
    (1, 101, NULL, 116, '2023-01-01', '2023-01-02', '2023-01-05'),
    (2, 102, 108, NULL, '2023-01-02', '2023-01-03', NULL),
    (3, 103, 109, NULL, '2023-01-03', NULL, NULL),
    (4, 104, 110, 117, '2023-01-04', '2023-01-05', '2023-01-10'),
    (5, 105, 111, NULL, '2023-01-05', '2023-01-06', '2023-01-08'),
    (6, 106, 112, 118, '2023-01-06', NULL, '2023-01-09'),
    (7, 107, 113, NULL, '2023-01-07', '2023-01-08', NULL),
    (8, 101, 114, 119, '2023-01-08', '2023-01-09', '2023-01-12'),
    (9, 102, 115, NULL, '2023-01-09', NULL, NULL),
    (10, 103, 116, 120, '2023-01-10', '2023-01-11', '2023-01-15'),
    (11, 104, 108, NULL, '2023-01-11', '2023-01-12', '2023-01-16'),
    (12, 105, 109, 117, '2023-01-12', '2023-01-13', '2023-01-17'),
    (13, 106, 110, NULL, '2023-01-13', '2023-01-14', '2023-01-18'),
    (14, 107, 111, 118, '2023-01-14', '2023-01-15', '2023-01-19'),
    (15, 101, 112, NULL, '2023-01-15', '2023-01-16', '2023-01-20'),
    (16, 102, 113, 119, '2023-01-16', '2023-01-17', '2023-01-21'),
    (17, 103, 114, NULL, '2023-01-17', '2023-01-18', '2023-01-22'),
    (18, 104, 115, 120, '2023-01-18', '2023-01-19', '2023-01-23'),
    (19, 105, 116, NULL, '2023-01-19', '2023-01-20', '2023-01-24'),
    (20, 106, 108, 117, '2023-01-20', '2023-01-21', '2023-01-25'),
    (21, 107, 109, NULL, '2023-01-21', '2023-01-22', '2023-01-26'),
    (22, 101, 110, 118, '2023-01-22', '2023-01-23', '2023-01-27'),
    (23, 102, 111, NULL, '2023-01-23', '2023-01-24', '2023-01-28'),
    (24, 103, 112, 119, '2023-01-24', '2023-01-25', '2023-01-29'),
    (25, 104, 113, NULL, '2023-01-25', '2023-01-26', '2023-01-30'),
    (26, 105, 114, 120, '2023-01-26', '2023-01-27', '2023-01-31'),
    (27, 106, 115, NULL, '2023-01-27', '2023-01-28', '2023-02-01'),
    (28, 107, 116, 117, '2023-01-28', '2023-01-29', '2023-02-02'),
    (29, 101, 108, NULL, '2023-01-29', '2023-01-30', '2023-02-03'),
    (30, 102, 109, 118, '2023-01-30', '2023-01-31', '2023-02-04'),
    (31, 103, 110, NULL, '2023-01-31', '2023-02-01', '2023-02-05'),
    (32, 104, 111, 119, '2023-02-01', '2023-02-02', '2023-02-06'),
    (33, 105, 112, NULL, '2023-02-02', '2023-02-03', '2023-02-07'),
    (34, 106, 113, 120, '2023-02-03', '2023-02-04', '2023-02-08'),
    (35, 107, 114, NULL, '2023-02-04', '2023-02-05', '2023-02-09'),
    (36, 101, 115, 117, '2023-02-05', '2023-02-06', '2023-02-10'),
    (37, 102, 116, NULL, '2023-02-06', '2023-02-07', '2023-02-11'),
    (38, 103, 108, 118, '2023-02-07', '2023-02-08', '2023-02-12'),
    (39, 104, 109, NULL, '2023-02-08', '2023-02-09', '2023-02-13'),
    (40, 105, 110, 119, '2023-02-09', '2023-02-10', '2023-02-14'),
    (41, 106, 111, NULL, '2023-02-10', '2023-02-11', '2023-02-15'),
    (42, 107, 112, 120, '2023-02-11', '2023-02-12', '2023-02-16'),
    (43, 101, 113, NULL, '2023-02-12', '2023-02-13', '2023-02-17'),
    (44, 102, 114, 117, '2023-02-13', '2023-02-14', '2023-02-18'),
    (45, 103, 115, NULL, '2023-02-14', '2023-02-15', '2023-02-19'),
    (46, 104, 116, 118, '2023-02-15', '2023-02-16', '2023-02-20'),
    (47, 105, 108, NULL, '2023-02-16', '2023-02-17', '2023-02-21'),
    (48, 106, 109, 119, '2023-02-17', '2023-02-18', '2023-02-22'),
    (49, 107, 110, NULL, '2023-02-18', '2023-02-19', '2023-02-23'),
    (50, 101, 111, 120, '2023-02-19', '2023-02-20', '2023-02-24'),
    (51, 102, 113, NULL, '2023-02-20', '2023-02-21', '2023-02-25'),
    (52, 103, 114, 117, '2023-02-21', '2023-02-22', '2023-02-26'),
    (53, 104, 115, NULL, '2023-02-22', '2023-02-23', '2023-02-27'),
    (54, 105, 116, 118, '2023-02-23', '2023-02-24', '2023-02-28'),
    (55, 106, 108, NULL, '2023-02-24', '2023-02-25', '2023-03-01'),
    (56, 107, 109, 119, '2023-02-25', '2023-02-26', '2023-03-02'),
    (57, 101, 110, NULL, '2023-02-26', '2023-02-27', '2023-03-03'),
    (58, 102, 111, 120, '2023-02-27', '2023-02-28', '2023-03-04'),
    (59, 103, 112, NULL, '2023-02-28', '2023-03-01', '2023-03-05'),
    (60, 104, 113, 117, '2023-03-01', '2023-03-02', '2023-03-06'),
    (61, 105, 114, NULL, '2023-03-02', '2023-03-03', '2023-03-07'),
    (62, 106, 115, 118, '2023-03-03', '2023-03-04', '2023-03-08'),
    (63, 107, 116, NULL, '2023-03-04', '2023-03-05', '2023-03-09'),
    (64, 101, 108, 119, '2023-03-05', '2023-03-06', '2023-03-10'),
    (65, 102, 109, NULL, '2023-03-06', '2023-03-07', '2023-03-11'),
    (66, 103, 110, 120, '2023-03-07', '2023-03-08', '2023-03-12'),
    (67, 104, 111, NULL, '2023-03-08', '2023-03-09', '2023-03-13'),
    (68, 105, 112, 117, '2023-03-09', '2023-03-10', '2023-03-14'),
    (69, 106, 113, NULL, '2023-03-10', '2023-03-11', '2023-03-15'),
    (70, 107, 114, 118, '2023-03-11', '2023-03-12', '2023-03-16'),
    (71, 101, 115, NULL, '2023-03-12', '2023-03-13', '2023-03-17'),
    (72, 102, 116, 119, '2023-03-13', '2023-03-14', '2023-03-18'),
    (73, 103, 108, NULL, '2023-03-14', '2023-03-15', '2023-03-19'),
    (74, 104, 109, 120, '2023-03-15', '2023-03-16', '2023-03-20'),
    (75, 105, 110, NULL, '2023-03-16', '2023-03-17', '2023-03-21'),
    (76, 106, 111, 117, '2023-03-17', '2023-03-18', '2023-03-22'),
    (77, 107, 112, NULL, '2023-03-18', '2023-03-19', '2023-03-23'),
    (78, 101, 113, 118, '2023-03-19', '2023-03-20', '2023-03-24'),
    (79, 102, 114, NULL, '2023-03-20', '2023-03-21', '2023-03-25'),
    (80, 103, 115, 119, '2023-03-21', '2023-03-22', '2023-03-26')
;
SELECT * FROM project;

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
      (1, 1, 'Sub1', 'Description for Project1 Sub1')
    , (1, 2, 'Sub2', 'Description for Project1 Sub2')
    , (1, 3, 'Sub3', 'Description for Project1 Sub3')
    , (2, 1, 'Sub1', 'Description for Project2 Sub1')
    , (2, 2, 'Sub2', 'Description for Project2 Sub2')   
    , (3, 1, 'Sub1', 'Description for Project3 Sub1')
;
SELECT * FROM phase;

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


-- DAYASSIGNMENT
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



/*



*/