import requests
import json
import os
from datetime import datetime, timezone

# URL to get TLEs for active satellites
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"

# NORAD ID for the ISS
iss_norad_id = 25544
file_path = "iss_tle.json"


def fetch_tle(url: str, norad_cat_id: int):
    # Send a GET request to the CelesTrak API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Loop through all satellites in the response
        for sat in data:
            if sat["NORAD_CAT_ID"] == norad_cat_id:
                # Extract the JSON data for the given ID
                tle_data = sat
                tle_data["date_fetched"] = (
                    datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                )
                return tle_data
    return None


def append_tle(tle_data):
    # Check if the JSON file exists
    if os.path.exists(file_path):
        # Read existing data
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new TLE data to the list
    data.append(tle_data)

    # Write the updated list back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    tle = fetch_tle(url, iss_norad_id)
    if tle:
        append_tle(tle)
        print(f"ISS TLE fetched and appended: {tle}")
    else:
        print("Could not fetch ISS TLE")
