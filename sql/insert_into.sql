--my_table
INSERT INTO my_table (col1, col2, col3)
VALUES
    ('a', 'b', 'c'),
    ('x', 'y', 'z')
;
SELECT *
FROM my_table
OFFSET (
        SELECT COUNT(*)
        FROM my_table
    ) - 10
;

--another_table
INSERT INTO another_table (foo, bar)
VALUES
    (1, 2),
    (3, 4)
;
SELECT *
FROM another_table
OFFSET (
        SELECT COUNT(*)
        FROM another_table
    ) - 10
;

