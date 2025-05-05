-- PGSQL CODE TO UPLOAD DATA FROM ADDRESS.CSV TO ADDRESS TABLE
TRUNCATE TABLE address CASCADE;
ALTER SEQUENCE address_id_seq RESTART WITH 1;
COPY address (street, house_number, postal_code, municipality)
FROM 'C:/_MaRn/syntra/projects/python_eindopdracht/proof_of_concept_folium/addresses/addresses.csv'
DELIMITER ','
CSV HEADER
;

SELECT * FROM address
LIMIT 10 -- first 10
OFFSET (SELECT COUNT(*) FROM address) - 10; -- last 10 lines
/*
*/
;





