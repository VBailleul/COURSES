######### CONTINENT ###########


DELIMITER $$
CREATE PROCEDURE continent(IN c CHAR(13))
BEGIN
  SELECT Name FROM country WHERE Continent = c;
END $$


##### PAYS #####

DELIMITER $$
CREATE PROCEDURE pays(IN p CHAR(52))
BEGIN
  SELECT Name
  FROM city
  WHERE CountryCode = (SELECT Code FROM country WHERE Name = p);
END$$
DELIMITER ;


#### VILLE ####

DELIMITER $$
CREATE PROCEDURE ville(IN v CHAR(35))
BEGIN
  SELECT * FROM city
  WHERE Name = v;
END $$
DELIMITER ;