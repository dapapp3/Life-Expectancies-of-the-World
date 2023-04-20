from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from scipy.stats import percentileofscore

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Life_Expectancy.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the table
Life_Expectancy = Base.classes.LifeExp

# Create session from Python to the DB
session = Session(engine)

#################################################
# Set up Flask and landing page
#################################################
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
@cross_origin(supports_credentials=True)
def welcome():
    return (
        f"<p>Welcome to the Home page of the Life Expectancy visualizer API!</p>"
        f"<p>Usages of this API:</p>"
        f"/api/v1.0/base<br/>This route returns a JSON list of all stats for all countries in the data set.<br/><br/>"
        f"/api/v1.0/country<br/>This route returns a JSON list of dictionaries of all stats for the chosen country from 2000-2015.<br/><br/>"
        f"/api/v1.0/country/year<br/>This route returns a JSON dictionary of all stats for the chosen country during the chosen year.<br/><br/>"
        f"/api/v1.0/life-expectancy<br/>This route returns a JSON list of dictionaries of the chosen country's Name and average Life Expectancy between 2000-2015.<br/><br/>"
        f"/api/v1.0/avg_mortality<br/>This route returns a JSON list of dictionaries of the average mortality stats for different age groups, grouped by year from 2000-2015.<br/><br/>"
    )

# API Routes
@app.route("/api/v1.0/base")
@cross_origin(supports_credentials=True)
def all_country_stats():
    # Query DB for stats
    results = session.query(Life_Expectancy.Country, Life_Expectancy.Region, Life_Expectancy.Year, Life_Expectancy.Infant_Deaths, Life_Expectancy.Under_Five_Deaths, Life_Expectancy.Adult_Deaths, Life_Expectancy.Alcohol_Consumption, Life_Expectancy.Hepatitis_B, Life_Expectancy.Measles, Life_Expectancy.BMI, Life_Expectancy.Polio, Life_Expectancy.Diphtheria, Life_Expectancy.Incidents_HIV, Life_Expectancy.GDP_Per_Capita, Life_Expectancy.Population_Millions, Life_Expectancy.Thinness_Ten_To_Nineteen_Years, Life_Expectancy.Thinness_Five_To_Nine_Years, Life_Expectancy.Schooling, Life_Expectancy.Economy_Status_Developed, Life_Expectancy.Economy_Status_Developing, Life_Expectancy.Life_Expectancy).all()
    
    # Create list
    results_list = []
    for item in range(len(results)):
        results_list.append([results[item][0],results[item][1],results[item][2],results[item][3],results[item][4],results[item][5],results[item][6],results[item][7],results[item][8],results[item][9],results[item][10],results[item][11],results[item][12],results[item][13],results[item][14],results[item][15],results[item][16],results[item][17],results[item][18],results[item][19],results[item][20]])
    
    session.close()

    return jsonify(results_list)

@app.route("/api/v1.0/<country>")
@cross_origin(supports_credentials=True)
def country_stats_all_years(country):
    # Query DB for stats
    results = session.query(
        Life_Expectancy.Country,
        Life_Expectancy.Region,
        Life_Expectancy.Year,
        Life_Expectancy.Infant_Deaths,
        Life_Expectancy.Under_Five_Deaths,
        Life_Expectancy.Adult_Deaths,
        Life_Expectancy.Alcohol_Consumption,
        Life_Expectancy.Hepatitis_B,
        Life_Expectancy.Measles,
        Life_Expectancy.BMI,
        Life_Expectancy.Polio,
        Life_Expectancy.Diphtheria,
        Life_Expectancy.Incidents_HIV,
        Life_Expectancy.GDP_Per_Capita,
        Life_Expectancy.Population_Millions,
        Life_Expectancy.Thinness_Ten_To_Nineteen_Years,
        Life_Expectancy.Thinness_Five_To_Nine_Years,
        Life_Expectancy.Schooling,
        Life_Expectancy.Economy_Status_Developed,
        Life_Expectancy.Economy_Status_Developing,
        Life_Expectancy.Life_Expectancy
    ).filter(
        Life_Expectancy.Country == country
    ).all()

# Create a list of dictionaries for each year
    results_list = []
    for item in results:
        results_dict = {}
        results_dict['Country'] = item[0]
        results_dict['Region'] = item[1]
        results_dict['Year'] = item[2]
        results_dict['Infant_Deaths'] = item[3]
        results_dict['Under_Five_Deaths'] = item[4]
        results_dict['Adult_Deaths'] = item[5]
        results_dict['Alcohol_Consumption'] = item[6]
        results_dict['Hepatitis_B'] = item[7]
        results_dict['Measles'] = item[8]
        results_dict['BMI'] = item[9]
        results_dict['Polio'] = item[10]
        results_dict['Diphtheria'] = item[11]
        results_dict['Incidents_HIV'] = item[12]
        results_dict['GDP_Per_Capita'] = item[13]
        results_dict['Population_Millions'] = item[14]
        results_dict['Thinness_Ten_To_Nineteen_Years'] = item[15]
        results_dict['Thinness_Five_To_Nine_Years'] = item[16]
        results_dict['Schooling'] = item[17]
        results_dict['Economy_Status_Developed'] = item[18]
        results_dict['Economy_Status_Developing'] = item[19]
        results_dict['Life_Expectancy'] = item[20]
        results_list.append(results_dict)
    
    session.close()

    return jsonify(results_list)

@app.route("/api/v1.0/<country>/<year>")
@cross_origin(supports_credentials=True)
def country_stats_for_year(country, year):
    # Query DB for stats
    results = session.query(
        Life_Expectancy.Region,
        Life_Expectancy.Alcohol_Consumption,
        Life_Expectancy.BMI,
        Life_Expectancy.GDP_Per_Capita,
        Life_Expectancy.Population_Millions,
        Life_Expectancy.Life_Expectancy
    ).filter(
        Life_Expectancy.Country == country,
        Life_Expectancy.Year == year
    ).all()

    # Create dictionary
    results_dict = {}
    for item in results:
        results_dict['Region'] = item[0]
        results_dict['Alcohol_Consumption'] = item[1]
        results_dict['BMI'] = item[2]
        results_dict['GDP_Per_Capita'] = item[3]
        results_dict['Population_Millions'] = item[4]
        results_dict['Life_Expectancy'] = item[5]
    
    session.close()

    return jsonify(results_dict)

@app.route("/api/v1.0/life-expectancy")
@cross_origin(supports_credentials=True)
def compare_life_expectancy():
    # Query DB for stats
    results = session.query(Life_Expectancy.Country, func.avg(Life_Expectancy.Life_Expectancy)).group_by(Life_Expectancy.Country).all()

    # Sort results by Life Exp (Ascending)
    sorted_results = []
    for item in range(len(results)):
        sorted_results.append(results[item][1])
    sorted_results.sort()

    # Create list
    results_dict_list = []
    #all_life_exp_values = [result[1] for result in results]
    for item in range(len(results)):
        percentile = percentileofscore(sorted_results, results[item][1])
        results_dict_list.append({"Country": results[item][0], "Life Expectancy": round(results[item][1], 2), "Percentile": round(percentile, 0)})
    
    session.close()

    return jsonify(results_dict_list)

@app.route("/api/v1.0/avg_mortality")
@cross_origin(supports_credentials=True)
def avg_morality_stats():
    # Query DB for stats
    results = session.query(Life_Expectancy.Year, func.avg(Life_Expectancy.Infant_Deaths), func.avg(Life_Expectancy.Under_Five_Deaths), func.avg(Life_Expectancy.Adult_Deaths)).group_by(Life_Expectancy.Year).all()
    
    results_list = []
    for item in results:
        results_dict = {}
        results_dict['Year'] = item[0]
        results_dict['Infant_Deaths'] = item[1]
        results_dict['Under_Five_Deaths'] = item[2]
        results_dict['Adult_Deaths'] = item[3]
        results_list.append(results_dict)
        session.close()

    return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)