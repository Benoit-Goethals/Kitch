
/*
DROP TABLE IF EXISTS xxxxx CASCADE;
CREATE TABLE xxxxx (
    id INT GENERATED ALWAYS AS IDENTITY,

    PRIMARY KEY (id)
)
*/

/*

een salesorder kan meerdere offertes bevatten
een offerte kan omgezet worden in een salesorder

een klant kan meerdere salesorders besteld hebben 
salesorder bestaat uit één klant

salesorder bestaat uit meerdere orderlines
orderline kan maar tot één salesorder behoren

salesorder bestaat uit meerdere workorders
workorder kan maar tot één salesorder behoren


sub
*/


/*

*/

/*
ORDERLINE:
+ elke orderline heeft zijn eigen id
+ kan voorkomen in een offerte
+ kan voorkomen in een salesorder
+ kan voorkomen in een workorder
+ bestaat uit
    + een product

*/

/*
OFFER:
+ een offer bestaat uit verschillende orderlijnen
*/

/*
SALESORDER:

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

