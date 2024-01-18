-- SQL script to create a function SafeDiv

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
RETURN if(b = 0, 0, a / b);
