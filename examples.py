examples = [
    {
        "input": "List all customers in France with a credit limit over 20,000.",
        "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
    },
    {
        "input": "Get the highest payment amount made by any customer.",
        "query": "SELECT MAX(amount) FROM payments;"
    },
    {
        "input": "Show product details for products in the 'Motorcycles' product line.",
        "query": "SELECT * FROM products WHERE productLine = 'Motorcycles';"
    },
    {
        "input": "Retrieve the names of employees who report to employee number 1002.",
        "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000.",
        "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
    },
    {
     'input':"what is price of `1968 Ford Mustang`",
     "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"
    },
    {
        "input": "Retrieve the names and salaries of employees who joined after January 1st, 2023.",
        "query": "SELECT firstName, lastName, salary FROM employees WHERE startDate > '2023-01-01';"
    },
    {
        "input": "List all departments with more than 10 employees.",
        "query": "SELECT departmentName FROM departments WHERE employeeCount > 10;"
    },
    {
        "input": "Show the average age of employees in each department.",
        "query": "SELECT departmentName, AVG(age) AS averageAge FROM employees GROUP BY departmentName;"
    },
    {
        "input": "Get the total number of employees hired in each year.",
        "query": "SELECT YEAR(startDate) AS hiringYear, COUNT(*) AS hires FROM employees GROUP BY hiringYear;"
    },
    {
        "input": "Retrieve the names of employees who have been promoted in the last 6 months.",
        "query": "SELECT firstName, lastName FROM employees WHERE promotionDate > DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH);"
    },
    {
        "input": "List all employees who have exceeded their annual leave quota.",
        "query": "SELECT firstName, lastName FROM employees WHERE remainingLeave < 0;"
    },
    {
        "input": "Show the highest and lowest salaries in the company.",
        "query": "SELECT MAX(salary) AS highestSalary, MIN(salary) AS lowestSalary FROM employees;"
    },
    {
        "input": "Get the average tenure of employees in each department.",
        "query": "SELECT departmentName, AVG(DATEDIFF(CURRENT_DATE(), startDate)) AS averageTenure FROM employees GROUP BY departmentName;"
    },
    {
        "input": "Retrieve the names of employees whose birthdays are in the next month.",
        "query": "SELECT firstName, lastName FROM employees WHERE MONTH(birthDate) = MONTH(DATE_ADD(CURRENT_DATE(), INTERVAL 1 MONTH));"
    },
    {
        "input": "List all employees who have attended training sessions in the past quarter.",
        "query": "SELECT DISTINCT firstName, lastName FROM employees INNER JOIN trainingSessions ON employees.employeeID = trainingSessions.employeeID WHERE trainingDate BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND CURRENT_DATE();"
    },
    {
        "input": "Show the total number of employees by job title.",
        "query": "SELECT jobTitle, COUNT(*) AS employeeCount FROM employees GROUP BY jobTitle;"
    },
    {
        "input": "Retrieve the names and ages of employees who have children.",
        "query": "SELECT firstName, lastName, age FROM employees WHERE numberOfChildren > 0;"
    },
    {
        "input": "List all employees who are eligible for retirement (age > 65).",
        "query": "SELECT firstName, lastName FROM employees WHERE age > 65;"
    },
    {
        "input": "Show the average number of sick days taken by employees in each department.",
        "query": "SELECT departmentName, AVG(sickDaysTaken) AS avgSickDays FROM employees GROUP BY departmentName;"
    },
    {
        "input": "Get the total number of male and female employees.",
        "query": "SELECT gender, COUNT(*) AS employeeCount FROM employees GROUP BY gender;"
    },
    {
        "input": "Retrieve the names of employees who have received awards in the past year.",
        "query": "SELECT firstName, lastName FROM employees WHERE awardDate BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND CURRENT_DATE();"
    },
    {
        "input": "List all employees who have completed their probation period.",
        "query": "SELECT firstName, lastName FROM employees WHERE startDate < DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH);"
    },
    {
        "input": "Show the department with the highest average employee satisfaction rating.",
        "query": "SELECT departmentName FROM employees GROUP BY departmentName ORDER BY AVG(satisfactionRating) DESC LIMIT 1;"
    },
    {
        "input": "Retrieve the names of employees who have taken unpaid leave in the last month.",
        "query": "SELECT firstName, lastName FROM employees WHERE unpaidLeaveStartDate BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND CURRENT_DATE();"
    },
    {
        "input": "List all employees who have completed mandatory compliance training.",
        "query": "SELECT firstName, lastName FROM employees WHERE complianceTrainingStatus = 'Completed';"
    }
] 
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector