import requests
import json
import os
from datetime import datetime, timezone

# URL to get TLEs for active satellites
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"

# NORAD ID for the ISS
iss_norad_id = 25544
file_path = "iss_tle.json"


def fetch_iss_tle():
    # Send a GET request to the CelesTrak API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Loop through all satellites in the response
        for sat in data:
            if sat["NORAD_CAT_ID"] == iss_norad_id:
                # Extract the JSON data for the ISS
                tle_data = {
                    "OBJECT_NAME": sat["OBJECT_NAME"],
                    "OBJECT_ID": sat["OBJECT_ID"],
                    "EPOCH": sat["EPOCH"],
                    "MEAN_MOTION": sat["MEAN_MOTION"],
                    "ECCENTRICITY": sat["ECCENTRICITY"],
                    "INCLINATION": sat["INCLINATION"],
                    "RA_OF_ASC_NODE": sat["RA_OF_ASC_NODE"],
                    "ARG_OF_PERICENTER": sat["ARG_OF_PERICENTER"],
                    "MEAN_ANOMALY": sat["MEAN_ANOMALY"],
                    "EPHEMERIS_TYPE": sat["EPHEMERIS_TYPE"],
                    "CLASSIFICATION_TYPE": sat["CLASSIFICATION_TYPE"],
                    "NORAD_CAT_ID": sat["NORAD_CAT_ID"],
                    "ELEMENT_SET_NO": sat["ELEMENT_SET_NO"],
                    "REV_AT_EPOCH": sat["REV_AT_EPOCH"],
                    "BSTAR": sat["BSTAR"],
                    "MEAN_MOTION_DOT": sat["MEAN_MOTION_DOT"],
                    "MEAN_MOTION_DDOT": sat["MEAN_MOTION_DDOT"],
                    "date_fetched": datetime.now(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "")
                    + "Z",
                }
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
    tle = fetch_iss_tle()
    if tle:
        append_tle(tle)
        print(f"ISS TLE fetched and appended: {tle}")
    else:
        print("Could not fetch ISS TLE")
