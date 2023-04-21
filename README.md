# Life-Expectancies-of-the-World

This repository contains code relating to a Flask API powered dashboard showcasing life expectancy data gathered from the World Health Organization (WHO) and a Kaggle CSV file for nearly 180 countries around the world between the years 2000 and 2015. The dashboard has interactive dropdown menu elements allowing the user to choose which country and year they want to see data visualized for.

In addition to 5 charts the dashboard contains (described later) a handy summary panel describing statistics for the chosen country during the chosen year. Some of the statistics included in the summary panel are:

1) Life expectancy (in years)
2) Income (GDP Per Capita)
3) Alcohol Consumption
4) BMI

The dashboard contains a line chart detailing the life expectancy for the selected country each year between 2000 and 2015, a bar chart detailing the population growth (or decline) over the same time frame, a gauge chart detailing the percentile that the selected country's average life expectancy during the time frame examined falls into relative to the rest of the countries in the data set, and two mortality multi-line charts detailing the selected country's mortality rates for infants, children age 5 and under, and adults compared to the mortality rates for those same sub-groups for all countries in the data set.

The original data set used to populate the database and power the visualizations can be found in the root directory of this repository in the form of a CSV file entitled "Life-Expectancy-Data-Updated.csv"

The code used to convert the original data set used to a SQLite database can be found in the root directory of this repository in the form of a python file entitled "CSV_To_SQLite.py"

The code used to build the Flask API can be found in the form of the "app.py" file located in the root folder of this repository.

The code used to create and update the dashboard visualizations can be found in the form of the "app.js" located in the static/js folder of this repository and "index.html" files located in the root folder of this repository.


Sources:

Kaggle, plotly, chart.js, module 14 challenge, TA's and class instructor. 
