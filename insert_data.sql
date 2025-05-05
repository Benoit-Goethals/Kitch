-- PGSQL CODE TO UPLOAD DATA FROM ADDRESS.CSV TO ADDRESS TABLE
TRUNCATE TABLE address CASCADE;

COPY address (street, house_number, postal_code, municipality)
FROM 'C:/_MaRn/syntra/projects/python_eindopdracht/proof_of_concept_folium/addresses/addresses.csv'
DELIMITER ','
CSV HEADER
;

/*
SELECT * FROM address
LIMIT 10;
*/

SELECT * FROM address ;



