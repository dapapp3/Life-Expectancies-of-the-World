from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

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

@app.route("/")
def welcome():
    return (
        f"<p>Welcome to the Home page of the Life Expectancy visualizer API!</p>"
        f"<p>Usages of this API:</p>"
        f"/api/v1.0/country/year<br/>This route returns a JSON list of all stats for the chosen country during the chosen year.<br/><br/>"
    )

# API Routes
@app.route("/api/v1.0/<country>/<year>")
def country_stats_for_year(country,year):
    # Query DB for stats
    results = session.query(Life_Expectancy.Country, Life_Expectancy.Region, Life_Expectancy.Year, Life_Expectancy.Infant_Deaths, Life_Expectancy.Under_Five_Deaths, Life_Expectancy.Adult_Deaths, Life_Expectancy.Alcohol_Consumption, Life_Expectancy.Hepatitis_B, Life_Expectancy.Measles, Life_Expectancy.BMI, Life_Expectancy.Polio, Life_Expectancy.Diphtheria, Life_Expectancy.Incidents_HIV, Life_Expectancy.GDP_Per_Capita, Life_Expectancy.Population_Millions, Life_Expectancy.Thinness_Ten_To_Nineteen_Years, Life_Expectancy.Thinness_Five_To_Nine_Years, Life_Expectancy.Schooling, Life_Expectancy.Economy_Status_Developed, Life_Expectancy.Economy_Status_Developing, Life_Expectancy.Life_Expectancy).filter(Life_Expectancy.Country == country).filter(Life_Expectancy.Year == year).all()
    
    # Create list
    results_list = []
    for item in range(len(results)):
        results_list.append([results[item][0],results[item][1],results[item][2],results[item][3],results[item][4],results[item][5],results[item][6],results[item][7],results[item][8],results[item][9],results[item][10],results[item][11],results[item][12],results[item][13],results[item][14],results[item][15],results[item][16],results[item][17],results[item][18],results[item][19],results[item][20]])
    
    return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)