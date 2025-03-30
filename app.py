from flask import Flask, render_template, request, jsonify
import pandas as pd
from scraper import get_apartments
from distancePuller import add_walking_data

app = Flask(__name__)  # Flask will look for templates/ directory by default

# ===== School Name to Address Mapping =====
school_destinations = {
    "engineering": "Thornton Hall, Charlottesville, VA",
    "data_science": "Data Science Institute, Charlottesville, VA",
    "mcintire": "McIntire School of Commerce, Charlottesville, VA",
    "arts_sciences": "College of Arts and Sciences, Charlottesville, VA"
}

# ===== Home Page Route =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== Handle Form Submission & Show Filtered Results =====
@app.route("/information", methods=["POST"])
def results():
    # === Get user input ===
    try:
        max_price = int(request.form.get("price", 9999))
    except ValueError:
        max_price = 9999

    try:
        beds = int(request.form.get("beds", 0))
    except ValueError:
        beds = 0

    try:
        max_time = int(request.form.get("distance", 999))
    except ValueError:
        max_time = 999

    school = request.form.get("school", "engineering")
    destination = school_destinations.get(school, "Thornton Hall, Charlottesville, VA")

    # === Scrape and calculate walk times ===
    df = get_apartments()
    df = add_walking_data(df, destination)

    # ✅ Parse price
    def parse_price(price_str):
        try:
            return int(price_str.replace("$", "").split("-")[0].replace(",", ""))
        except:
            return 99999

    df["min_price"] = df["price"].apply(parse_price)

    # ✅ Parse beds
    df["num_beds"] = df["beds"].str.extract(r"(\d+)").iloc[:, 0].astype(float).fillna(0)

    # ✅ Apply filters
    filtered = df[
        (df["min_price"] <= max_price) &
        (df["walk_time_min"] <= max_time) &
        (df["num_beds"] >= beds)
    ]

    # ✅ Convert to list of dicts for template
    filtered = filtered.sort_values(by="walk_time_min")
    listings = filtered.drop(columns=["min_price", "walk_time_min"]).to_dict(orient="records")

    return render_template("information.html", listings=listings)


# ===== API (optional, not used by frontend right now) =====
@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    max_price = int(data.get("price", 9999))
    beds = str(data.get("beds", ""))
    max_time = int(data.get("distance", 999))
    school = data.get("school", "engineering")
    destination = school_destinations.get(school, "Thornton Hall, Charlottesville, VA")

    df = get_apartments()
    df = add_walking_data(df, destination)

    def parse_price(price_str):
        try:
            return int(price_str.replace("$", "").split("-")[0].replace(",", ""))
        except:
            return 99999

    def parse_time(time_str):
        try:
            return int(time_str.split()[0])
        except:
            return 999

    df["min_price"] = df["price"].apply(parse_price)
    df["walk_time_min"] = df["walking_time"].apply(parse_time)

    filtered = df[
        (df["min_price"] <= max_price) &
        (df["walk_time_min"] <= max_time) &
        (df["beds"].str.contains(beds))
    ]

    return jsonify(filtered.drop(columns=["min_price", "walk_time_min"]).to_dict(orient="records"))

# ===== Run App =====
if __name__ == "__main__":
    app.run(debug=True)