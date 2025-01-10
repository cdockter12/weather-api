from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

# <station> is a special syntax flask uses to pass in params
@app.route('/api/v1/<station>/<date>')
def api_func(station, date):
    df = pandas.read_csv("")
    temperature = df.station(date)
    return {"station": station, "date": date, "temperature": temperature}

app.run(debug=True)