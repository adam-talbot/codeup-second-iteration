####### MORE EXERCISES ######

### EMPLOYEES DATABASE ###

#1. How much do the current managers of each department get paid, relative to the average salary for the department? Is there any department where the department manager gets paid less than the average salary?

-- will need employees to get names, will need dept_emp to connect employees to department using emp_no, will need departments to get dept_name using dept_no, will need dep_manager to get managers

USE employees;

-- get current average salary for each department
SELECT dept_name, AVG(salary) AS avg_salary
FROM salaries AS s
JOIN dept_emp AS de ON de.emp_no = s.emp_no AND de.to_date > curdate() -- join to add department info to employees and only add for current employees
JOIN departments AS d USING(dept_no)
WHERE s.to_date > curdate() -- current salaries of all current employees
GROUP BY dept_name
ORDER BY dept_name;

-- get salaries for current department managers
SELECT dept_name, salary
FROM dept_manager AS dm
JOIN salaries AS s ON s.emp_no = dm.emp_no AND s.to_date > curdate()
JOIN departments AS d USING(dept_no)
WHERE dm.to_date > curdate()
ORDER BY dept_name;

DROP TABLE germain_1478.dept_ave_sal;

-- compare average salary for each department with manager salary for that department using temp tables
CREATE TEMPORARY TABLE germain_1478.dept_ave_sal AS
SELECT dept_name, AVG(salary) AS avg_salary
FROM salaries AS s
JOIN dept_emp AS de ON de.emp_no = s.emp_no AND de.to_date > curdate() -- join to add department info to employees and only add for current employees
JOIN departments AS d USING(dept_no)
WHERE s.to_date > curdate() -- current salaries of all current employees
GROUP BY dept_name
ORDER BY dept_name;

SELECT * FROM germain_1478.dept_ave_sal;

DESCRIBE germain_1478.dept_ave_sal;

DROP TABLE germain_1478.dept_ave_sal_vs_manager;

CREATE TEMPORARY TABLE germain_1478.dept_manager_sal AS
SELECT dept_name, salary
FROM dept_manager AS dm
JOIN salaries AS s ON s.emp_no = dm.emp_no AND s.to_date > curdate()
JOIN departments AS d USING(dept_no)
WHERE dm.to_date > curdate()
ORDER BY dept_name;

SELECT * FROM germain_1478.dept_manager_sal;
DESCRIBE germain_1478.dept_manager_sal;

-- join two tables on dept_name
SELECT dept_name, avg_salary AS dept_avg_sal, salary AS man_sal, (salary/avg_salary)*100 AS 'rel%'
FROM germain_1478.dept_ave_sal
JOIN germain_1478.dept_manager_sal USING(dept_name)
ORDER BY 4;

# yes, there are 2 departments where the manager makes less than the average salary for that department: Customer Service and Production


### WORLD DATABASE ###


#1. What languages are spoken in Santa Monica? (this actually shows breakdown of languages spoken across entire US, but matches desired results)

USE world;

SELECT LANGUAGE, percentage FROM countrylanguage WHERE CountryCode IN (SELECT CountryCode FROM city WHERE name = 'Santa Monica') ORDER BY percentage;

#2. How many different countries are in each region?

select region, count(region) as num_countries from country group by region order by num_countries;

#3. What is the population for each region?

select region, sum(population) as population from country group by region order by population desc;

#4. What is the population for each continent?

select Continent, sum(population) as population from country group by Continent order by population desc; 

#5. What is the average life expectancy globally?

select avg(LifeExpectancy) from country;

#6. What is the average life expectancy for each region, each continent? Sort the results from shortest to longest

select region, avg(LifeExpectancy) as life_expectancy from country group by region order by life_expectancy; -- for region

select Continent, avg(LifeExpectancy) as life_expectancy from country group by Continent order by life_expectancy; -- for continent

## BONUS ##

#1. Find all the countries whose local name is different from the official name

SELECT name, LocalName from country where name <> LocalName; -- 135 records returned

#2. How many countries have a life expectancy less than x? I will use 50
select name, LifeExpectancy from country where LifeExpectancy < 50; -- 28 records returned

#3. What state is city x located in? I will use Santa Monica
select name, district from city where name = 'Santa Monica'; -- Cali

#4. What region of the world is city x located in? I will use Bahamas
select name, region from country where name = 'Bahamas'; -- Caribbean
