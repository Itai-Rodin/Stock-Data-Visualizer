from flask import Flask, render_template, request
from datetime import date
import api
import charts
import csv


app = Flask(__name__)

def load_symbols():
    symbols = []
    with open("stocks.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.append(row["Symbol"])
    return symbols


@app.route("/", methods=["GET", "POST"])
def index():
    chart = None
    error = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").strip().upper()
        chart_type = request.form.get("chart_type", "")
        time_series = request.form.get("time_series", "")
        start = request.form.get("start", "")
        end = request.form.get("end", "")

        functions = {
            "Intraday": "TIME_SERIES_INTRADAY",
            "Daily": "TIME_SERIES_DAILY",
            "Weekly": "TIME_SERIES_WEEKLY",
            "Monthly": "TIME_SERIES_MONTHLY"
        }

        if not symbol:
            error = "Please select a stock."
        elif chart_type not in ("Bar", "Line"):
            error = "Please select a valid chart type."
        elif time_series not in functions:
            error = "Please select a valid time series."
        elif not start or not end or start > end or end > date.today().isoformat():
            error = "Please select a valid date range."
        else:
            try:
                series = api.fetch_stock_data(symbol, functions[time_series])
                rows = api.filter_by_date(series, start, end)
                result = charts.build_chart(
                    rows, symbol, chart_type, time_series, start, end
                )
                chart = result.render(is_unicode=True)
            except (api.StockDataError, ValueError, KeyError) as exc:
                error = str(exc)

    return render_template(
    "index.html",
    chart=chart,
    error=error,
    symbols=load_symbols()
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)