from flask import Flask, render_template
from datetime import datetime
import pandas as pd

app = Flask(__name__)

df_var = pd.read_csv("weather_data/stations.txt", skiprows=17)


@app.route('/')
def home():
    return render_template("home.html", data=df_var.to_html())


# <station> is a special syntax flask uses to pass in params
@app.route('/api/v1/<station>/<date>')
def api_func(station, date):
    # Read in data from csv using API inputs.
    filename = f"weather_data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # Format our date into yyyy-mm-dd without time.
    formatted_date = datetime.strptime(date, "%Y%m%d").date()

    # Grab temperature from dataframe
    temperature = df.loc[df['    DATE'] == f'{formatted_date}']['   TG'].squeeze() / 10
    return {"station": station, "date": date, "temperature": temperature}


@app.route('/api/v1/<station>')
def all_data(station):
    filename = f"weather_data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route('/api/v1/yearly/<station>/<year>')
def year_data(station, year):
    filename = f"weather_data/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # Convert all datetimes to strings for rendering on home page.
    df["    DATE"] = df["    DATE"].astype(str)

    # Pull out all results that start with passed in year
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


app.run(debug=True, port=5000)
