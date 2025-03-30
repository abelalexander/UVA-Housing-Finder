import requests
import time
import math
import api_key

API_KEY = api_key.API_KEY

def convert_to_minutes(text):
    try:
        text = text.lower()
        hours = 0
        mins = 0

        if "hour" in text:
            if "hours" in text:
                parts = text.split("hours")
            else:
                parts = text.split("hour")

            hours = int(parts[0].strip())

            if "min" in parts[1]:
                mins_part = parts[1].replace("mins", "").replace("min", "").strip()
                if mins_part:
                    mins = int(mins_part)
        elif "min" in text:
            mins = int(text.replace("mins", "").replace("min", "").strip())

        return hours * 60 + mins
    except Exception as e:
        print(f"⚠️ Failed to convert time '{text}': {e}")
        return 999

# === New: Batch fetch distances for up to 25 addresses at once ===
def get_walking_info_batch(origins, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    origin_string = "|".join(origins)

    params = {
        "origins": origin_string,
        "destinations": destination,
        "mode": "walking",
        "units": "imperial",
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        elements = data["rows"]

        results = []
        for i, row in enumerate(elements):
            el = row["elements"][0]
            if el["status"] == "OK":
                results.append((el["duration"]["text"], el["distance"]["text"]))
            else:
                results.append((f"❌ API Error: {el['status']}", ""))
        return results

    except Exception as e:
        print(f"⚠️ Batch request failed: {e}")
        return [("⚠️ Exception", "")] * len(origins)

# === Add walk time + distance columns to the DataFrame ===
def add_walking_data(df, destination):
    print("⏱ Starting batched distance pull...")

    batch_size = 25
    all_results = []

    addresses = df["address"].tolist()
    for i in range(0, len(addresses), batch_size):
        batch = addresses[i:i + batch_size]
        print(f"📦 Processing batch {i // batch_size + 1} of {math.ceil(len(addresses) / batch_size)}")
        results = get_walking_info_batch(batch, destination)
        all_results.extend(results)
        time.sleep(0.5)  # be polite to the API

    walking_times, walking_distances = zip(*all_results)
    df["walking_time"] = walking_times
    df["walking_distance"] = walking_distances
    df["walk_time_min"] = df["walking_time"].apply(convert_to_minutes)

    print("✅ Batched distance info applied to DataFrame")
    return df