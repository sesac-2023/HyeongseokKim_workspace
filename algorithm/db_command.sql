CREATE DATABASE study CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER hskim@localhost IDENTIFIED BY "153104";
SELECT GRANTEE, PRIVILEGE_TYPE, IS_GRANTABLE FROM INFORMATION_SCHEMA.USER_PRIVILEGES;
GRANT ALL PRIVILEGES ON study.* TO hskim@localhost;
CREATE TABLE Person(
    PersonID INT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255)
);

CREATE TABLE Person(
    PersonID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    PRIMARY KEY(PersonID)
);

INSERT INTO Person(FirstName, LastName, Address, City, ) 
VALUES ("HYEONGSEOK", "KIM", "KOREA", "SEOUL");
ALTER TABLE Person ADD Email Varchar(255);
INSERT INTO Person(Email) 
VALUES ("hyungsuk0815@gmail.com");
INSERT INTO Person(FirstName, LastName, Address, City, Email) 
VALUES ("HYEONGSEOK", "KIM", "KOREA", "SEOUL", "hyungsuk0815@gmail.com");

CREATE TABLE Students(
    StudentID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(255),
    Age TINYINT,
    Address VARCHAR(255),
    PRIMARY KEY(StudentID)
);

CREATE TABLE Grades(
    StudentID INT,
    Math TINYINT,
    English TINYINT,
    Science TINYINT,
    PRIMARY KEY(StudentID)
);

--Students
INSERT INTO Students(Name, Age, Address) VALUES ("홍길동", "30", "인천");

INSERT INTO Students(Name, Age, Address) VALUES ("이연걸", "60", "서울");

INSERT INTO Students(Name, Age, Address) VALUES ("이몽룡", "42", "대전");

INSERT INTO Students(Name, Age, Address) VALUES ("성춘향", "27", "경기");

INSERT INTO Students(Name, Age, Address) VALUES ("김형석", "32", "서울");

--Grades
INSERT INTO Grades(StudentID, Math, English, Science) VALUES ("1", "90", "80", "50");

INSERT INTO Grades(StudentID, Math, English, Science) VALUES ("2", "69", "76", "65");

INSERT INTO Grades(StudentID, Math, English, Science) VALUES ("3", "98", "87", "97");

INSERT INTO Grades(StudentID, Math, English, Science) VALUES ("4", "87", "67", "79");

INSERT INTO Grades(StudentID, Math, English, Science) VALUES ("5", "100", "80", "92");

--SELECT문
SELECT CustomerName, Country FROM Customers; #고객이름, 국가목록 조회

SELECT * FROM Customers; #고객정보전체조회

SELECT DISTINCT Country FROM Customers; #고객국가목록 중복없이 조회

SELECT * FROM Customers WHERE Country="France"; #국가가 프랑스인 고객 조회

SELECT * FROM Customers WHERE ContactName LIKE "Mar%"; #Mar로 시작하는 ContactName을 가진 직원 조회

SELECT * FROM Customers WHERE ContactName LIKE "%et"; #et로 끝나는 ContactName을 가진 직원 조회

SELECT * FROM Customers WHERE Country="France" AND ContactName LIKE "La%";
#국가가 프랑스이고 직원이름이 La로 시작하는 고객 조회

SELECT * FROM Customers WHERE Country="France" OR ContactName LIKE "La%";
#국가가 프랑스이거나 직원이름이 La로 시작하는 고객 조회

SELECT * FROM Customers WHERE NOT Country="France";
#국가가 프랑스가 아닌 고객조회

SELECT * FROM Customers WHERE Country IN ("France", "Spain");
#국가가 프랑스이거나 스페인인 고객조회

SELECT * FROM Products WHERE Price BETWEEN 15 AND 20;
#가격이 15에서 20사이인 제품 조회

SELECT * FROM Customers WHERE PostalCode IS NULL;
#우편번호가 NULL인 고객 조회
SELECT * FROM Customers WHERE PostalCode="";
#NULL이 조회가 안되면 공백을 의심
UPDATE Customers SET Postalcode=NULL WHERE PostalCode="";
#공백을 NULL로 변경

SELECT * FROM Customers WHERE PostalCode IS NOT NULL;
#우편번호가 NULL이 아닌 고객 조회

SELECT * From Customers ORDER BY CustomerName ASC;
#고객이름 오름차순 조회

SELECT * From Customers ORDER BY CustomerName DESC;
#고객이름 내림차순 조회

SELECT * From Customers LIMIT 10;
#고객 10명만 조회
SELECT * From Customers LIMIT 10 OFFSET 10;
#고객 10명 뒤에서 부터 10명 조회

SELECT * ,
CASE 
	WHEN Price<30 THEN "저"
    WHEN Price BETWEEN 30 AND 50 THEN "중"
	WHEN Price>50 THEN "고"
END AS "Level"
FROM Products;
혹은
SELECT * ,
CASE 
	WHEN Price<30 THEN "저"
	WHEN Price>50 THEN "고"
    ELSE "중"
END AS "Level"
FROM Products;
#조건에 따라 정해진 값 반환하고 AS로 칼럼이름 설정

SELECT COUNT(*)
FROM Customers
WHERE Country="France";
#국가가 프랑스인 고객의 수 세기

SELECT AVG(Price)
FROM Products;
#전체 상품 가격의 평균 구하기

SELECT SUM(Quantity)
FROM OrderDetails;
#전체 주문상품 합계 구하기

SELECT MIN(Price)
FROM Products;
#전체 상품 가격의 최솟값 구하기

SELECT MAX(Price)
FROM Products;
#전체 상품 가격의 최댓값 구하기

SELECT Country, COUNT(*) AS CustomerNbr
FROM Customers
GROUP BY Country
ORDER BY CustomerNbr ASC;
#국가별로 그룹화하여 고객수별로 내림차순 정렬

SELECT Country, City, COUNT(*) AS CustomerNbr
FROM Customers
GROUP BY Country, City
ORDER BY CustomerNbr DESC;
#국가별, 도시별로 그룹화하여 고객수별로 오름차순 정렬

SELECT CustomerName, Address 
FROM (
	SELECT * 
	FROM Customers
	WHERE Country="UK"
)
WHERE City="London";
#영국에 사는 고객 중, City가 London인 고객들만 출력

--실습
SELECT FirstName, BirthDate, Notes
FROM Employees
WHERE LastName="King";
#직원(Employees)중 이름(LastName)이 ‘King’인 직원의 이름과 생일(BirthDate)과 노트(Notes)를 조회해주세요.

SELECT ProductName, Price
FROM Products
WHERE ProductName LIKE "C%" AND Price > 20
ORDER BY Price DESC;
#상품(Products)중 상품명(ProductName)이 ‘C’로 시작하고 가격(Price)이 20보다 큰 상품의 상품명과 가격을 가격이 비싼순으로 
조회해주세요.

SELECT CategoryID, SUM(Price) AS Sum, MAX(Price) AS Max, MIN(Price) As Min
FROM Products
GROUP BY CategoryID;
#상품(Products)의 카테고리아이디(CategoryID) 별로 상품가격의 합, 가장 비싼 상품 가격, 가장 저렴한 상품 가격을 구하세요.
(칼럼명 재설정과 CategoryID 표시까지 함)

SELECT *,
CASE
      WHEN ProductNum > 10 THEN "많음"
      ELSE "적음"
END AS "Many/Little"
FROM(
    SELECT CategoryID, COUNT(*) AS ProductNum 
    FROM Products
    GROUP BY CategoryID
)
ORDER BY ProductNum DESC;
#상품(Products)의 카테고리아이디(CategoryID) 별로 상품개수와 상품개수가 10개가 넘을경우 많음 아니면 적음이 표시되 
어있는 칼럼을 하나 추가하고 상품수가 많은 순서대로 조회해주세요

SELECT Country, CountryNum, TotalCustomer, CountryNum*100/TotalCustomer AS Percentile
FROM(
    SELECT Country, COUNT(*) AS CountryNum, (SELECT COUNT(*) FROM Customers) AS TotalCustomer
    FROM Customers
    GROUP BY Country
)
ORDER BY Percentile ASC;
#고객(Customers)의 국가(Country)별 고객수와 백분위 (국가별고객수 / 전체고객수 * 100)을 구하세요.(백분위로 오름차순 정렬까지)
