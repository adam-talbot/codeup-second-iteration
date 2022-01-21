### MYSQL REVIEW ###

USE employees;

SHOW tables;

DESCRIBE employees;

SELECT 
	CONCAT(first_name, ' ', last_name) as full_name,
	birth_date, 
	hire_date,
	(DATEDIFF(curdate(), hire_date)) as number_of_days_employed
FROM employees
WHERE hire_date LIKE '199%'
	AND birth_date LIKE '%-12-25'
ORDER BY number_of_days_employed DESC;

SELECT CONCAT(
		LOWER(SUBSTR(first_name, 1, 1)), # lower-case first letter of first name 
		LOWER(SUBSTR(last_name, 1, 4)), # lower-case first four letters of last name
		'_', # add underscore
		SUBSTR(birth_date, 6, 2), # month born
		SUBSTR(YEAR(birth_date), 3, 2) # last 2 digits of year born
		     ) as username, #create alias
		   first_name, last_name, birth_date
FROM employees;

SELECT CONCAT(
		LOWER(SUBSTR(first_name, 1, 1)), # lower-case first letter of first name 
		LOWER(SUBSTR(last_name, 1, 4)), # lower-case first four letters of last name
		'_', # add underscore
		SUBSTR(birth_date, 6, 2), # month born
		SUBSTR(birth_date, 3, 2) # last 2 digits of year born
		     ) as username, #create alias
		   first_name, last_name, birth_date
FROM employees;

SELECT first_name, last_name
FROM employees
WHERE last_name LIKE 'E%e'
GROUP BY first_name, last_name;

SELECT CONCAT(first_name, ' ', last_name) as full_name, COUNT(*) as n_same_name
FROM employees
WHERE last_name LIKE 'E%e'
GROUP BY full_name
HAVING n_same_name > 1;

SELECT d.dept_name AS 'Department Name', CONCAT(e.first_name, ' ', e.last_name) AS 'Department Manager' #select columns to be displayed and use aliases to rename
FROM employees AS e #select starting table that we will be joining to and rename to facilitate referencing columns
JOIN dept_manager AS dm #join with inner join to the employees the dept_manager table (associative table) renaming using an alias again
ON dm.emp_no = e.emp_no #we are using column in common emp_no to connect the two tables
JOIN departments AS d #join with inner join to the table the departments table renaming using alias again
ON d.dept_no = dm.dept_no #we are using column in common (dept_no) to connect the two tables
WHERE dm.to_date > curdate() AND e.gender = 'F' #Set condition to make sure we are only getting back current managers that are female
ORDER BY d.dept_name; #order results to match order shown in exercises - can reference column name using original name or aliases

# Find all the current employees with the same hire date as employee 101010 using a sub-query.

# Create subqueries first
SELECT hire_date
FROM employees
WHERE emp_no = '101010';

SELECT emp_no
FROM dept_emp
WHERE to_date > curdate();

# Now use subqueries as where clause in final query
SELECT *
FROM employees
WHERE hire_date = (
	SELECT hire_date
	FROM employees
	WHERE emp_no = '101010')
AND emp_no IN (
	SELECT emp_no
	FROM dept_emp
	WHERE to_date > CURDATE());
	
	
### Cognizant Tekstac Problems ###

-- CREATE TABLE IF NOT EXISTS department (
--     department_id INT,
--     department_name VARCHAR(30),
--     department_block_number INT,
--     PRIMARY KEY (department_id)
-- );
    

INSERT INTO department(department_id, department_name, department_block_number)
VALUES
    (1, 'CSE', 3),
    (2, 'IT', 3),
    (3, 'SE', 3);

SELECT department_name
FROM department
WHERE department_block_number = 3
ORDER BY department_name;