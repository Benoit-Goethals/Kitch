
/*
DROP TABLE IF EXISTS xxxxx CASCADE;
CREATE TABLE xxxxx (
    id INT GENERATED ALWAYS AS IDENTITY,

    PRIMARY KEY (id)
)
*/


DROP TABLE IF EXISTS salesorder CASCADE;
CREATE TABLE salesorder (
    salesorder_id INT GENERATED ALWAYS AS IDENTITY,
    salesman_id INT,
    customer_id INT,
    PRIMARY KEY (salesorder_id)
)

DROP TABLE IF EXISTS orderline CASCADE;
CREATE TABLE orderline (
    id INT GENERATED ALWAYS AS IDENTITY,
    salesorder_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (salesorder_id) REFERENCES salesorder(salesorder_id)
)

DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id INT GENERATED ALWAYS AS IDENTITY,

    PRIMARY KEY (person_id)
)

