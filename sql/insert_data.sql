

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
-- LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM person) - 10; -- last 10 lines
;