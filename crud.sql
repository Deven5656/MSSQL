CREATE TABLE Employee(
EmployeeID int PRIMARY KEY,
FirstName varchar(10),
LastName varchar(10),
Emp_Dept varchar(5),
Salary int
);

SELECT * FROM Employee
SELECT FirstName, LastName FROM Employee WHERE Emp_Dept = 'IT';

INSERT INTO Employee
(EmployeeID,FirstName,LastName ,Emp_Dept,Salary )
VALUES (1,'Deven', 'Gupta','IT',45000);


UPDATE Employee SET Salary=50000 WHERE EmployeeID=1

DELETE FROM Employee WHERE
EmployeeID = 5;

DROP TABLE Employee