# Import required modules
import csv
import sqlite3
 
# Connecting to the geeks database
connection = sqlite3.connect('Life_Expectancy.db')
 
# Creating a cursor object to execute SQL queries on a database table
cursor = connection.cursor()
 
# Table Definition
create_table = '''CREATE TABLE life_expectancy(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Country TEXT NOT NULL,
                Region TEXT NOT NULL,
                Year INTEGER NOT NULL,
                Infant_Deaths REAL NOT NULL,
                Under_Five_Deaths REAL NOT NULL,
                Adult_Deaths REAL NOT NULL,
                Alcohol_Consumption REAL NOT NULL,
                Hepatitis_B INTEGER NOT NULL,
                Measles INTEGER NOT NULL,
                BMI REAL NOT NULL,
                Polio INTEGER NOT NULL,
                Diphtheria INTEGER NOT NULL,
                Incidents_HIV REAL NOT NULL,
                GDP_Per_Capita INTEGER NOT NULL,
                Population_Millions REAL NOT NULL,
                Thinness_Ten_To_Nineteen_Years REAL NOT NULL,
                Thinness_Five_To_Nine_Years REAL NOT NULL,
                Schooling REAL NOT NULL,
                Economy_Status_Developed INTEGER NOT NULL,
                Economy_Status_Developing INTEGER NOT NULL,
                Life_Expectancy REAL NOT NULL
                );
                '''
 
# Creating the table into our database
cursor.execute(create_table)
 
# Opening the person-records.csv file
file = open('Life-Expectancy-Data-Updated.csv')
 
# Reading the contents of the person-records.csv file
contents = csv.reader(file)
 
# SQL query to insert data into the person table
insert_records = '''INSERT INTO life_expectancy (
    Country, Region, Year, Infant_Deaths, Under_Five_Deaths, Adult_Deaths, Alcohol_Consumption, Hepatitis_B, Measles, BMI, Polio, Diphtheria, Incidents_HIV, GDP_Per_Capita, Population_Millions,
    Thinness_Ten_To_Nineteen_Years, Thinness_Five_To_Nine_Years, Schooling, Economy_Status_Developed, Economy_Status_Developing, Life_Expectancy)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
 
# Importing the contents of the file into our person table
cursor.executemany(insert_records, contents)
 
# SQL query to retrieve all data from the person table To verify that the data of the csv file has been successfully inserted into the table
select_all = "SELECT * FROM life_expectancy"
rows = cursor.execute(select_all).fetchall()
 
# Output to the console screen
for r in rows:
    print(r)
 
# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()