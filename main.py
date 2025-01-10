from flask import Flask, render_template
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

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

app.run(debug=True, port=5000)