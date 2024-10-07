--Problem 1

use Demo_DB
use Covid_DB

SELECT 
    [Country Region] AS Country,
    (SUM(cast(Deaths as int)) * 100.0 / SUM(cast(Confirmed as int))) AS local_death_percentage
FROM covid_global
GROUP BY [Country Region] 
HAVING [Country Region]='India'


SELECT 
    (SUM(cast(Deaths as int)) * 100.0 / SUM(cast(Confirmed as int))) AS global_death_percentage
FROM covid_global



--Problem 2
SELECT * FROM worldometer_data
where Country_Region='India'

SELECT 
    Country_Region AS Country,
    (SUM(TotalCases) * 100.0 / SUM(Population)) AS Local_Infected_Population_Percentage
FROM worldometer_data
GROUP BY Country_Region 



SELECT 
	 SUM(TotalCases) AS Total_Case,
	 SUM(cast(Population AS BIGINT)) AS Total_Population,
    (SUM(TotalCases) * 100.0 / SUM(cast(Population AS BIGINT))) AS Gobal_Infected_Population_Percentage
FROM worldometer_data




--Problem 3
SELECT * FROM worldometer_data

SELECT 
    Country_Region AS Country,
    (SUM(TotalCases) * 100.0 / SUM(Population)) AS Highest_Infection_Rate
FROM worldometer_data
GROUP BY Country_Region 
ORDER BY Highest_Infection_Rate DESC;


--Problem 4

SELECT 
    Country_Region AS Country,
    TotalDeaths
FROM worldometer_data
ORDER BY TotalDeaths DESC;


SELECT
    Continent,
    SUM(TotalDeaths) AS Total_Continent_Deaths
FROM worldometer_data
GROUP BY  Continent
ORDER BY Total_Continent_Deaths DESC;



--Problem 5. Average number of deaths by day (Continents and Countries)
SELECT * FROM covid_19_clean

SELECT 
    Country_Region,Date,
	AVG(Deaths) AS DEATHS
FROM covid_19_clean
GROUP BY Country_Region,Date

SELECT 
    WHO_Region AS Continent,Date,
	AVG(Deaths) AS DEATHS
FROM covid_19_clean
GROUP BY WHO_Region,Date


--Problem 6. Average of cases divided by the number of population of each country (TOP 10)
SELECT * FROM worldometer_data


SELECT Top 10
    Country_Region,
	AVG(CAST(TotalCases AS float)/[Population]) AS DEATHS
FROM worldometer_data
GROUP BY Country_Region



--Problem 7. Considering the highest value of total cases, which countries have the highest rate of infection in relation to population?
SELECT * FROM worldometer_data


SELECT
    Country_Region,
    TotalCases,
    Population,
    (TotalCases * 1.0 / Population) AS InfectionRate
FROM worldometer_data
ORDER BY InfectionRate DESC



--Problem (Joins) 1. To find out the population vs the number of people vaccinated

SELECT * FROM covid_19_india
SELECT * FROM covid_vaccine_statewise
SELECT * FROM StatewiseTestingDetails

SELECT c.State,
SUM(c.Total_Individuals_Vaccinated) AS Total_Vaccine,
SUM(s.TotalSamples) AS Population
FROM
covid_vaccine_statewise AS c
INNER JOIN StatewiseTestingDetails AS s
ON s.state=c.state
GROUP BY c.State,s.State

--Problem (Joins) 2. To find out the percentage of different vaccine taken by people in a country

SELECT State,
ROUND(SUM(Covaxin_Doses_Administered)*100.0/SUM(Total_Doses_Administered),4) AS Covaxin,
ROUND(SUM(CoviShield_Doses_Administered)*100.0/SUM(Total_Doses_Administered),4) AS Covishield,
ROUND(SUM(Sputnik_V_Doses_Administered)*100.0/SUM(Total_Doses_Administered),4) AS Sputnik
FROM
covid_vaccine_statewise
GROUP BY State
ORDER BY State ASC


--Problem (Joins) 3. To find out percentage of people who took both the doses


SELECT 'percentage' AS ' ',
    ROUND(SUM(Second_Dose_Administered)*100.0/SUM(Total_Individuals_Vaccinated),4) AS Both_Doses
FROM 
    covid_vaccine_statewise;

SELECT MAX(Total_Individuals_Vaccinated )FROM covid_vaccine_statewiseWHERE State='India'--1381344997-- 250656880