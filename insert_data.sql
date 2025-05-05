COPY address (street, house_number, postal_code, municipality, country)
FROM 'c:/_MaRn/syntra/projects/python_eindopdracht/proof_of_concept_folium/addressen_random.csv'
DELIMITER ','
CSV HEADER
QUOTE '"'
NULL ''
(
    FORMAT CSV,
    HEADER TRUE,
    FORCE_NULL (X, Y, OBJECTID, NAAM, ID)
);
