import requests
import json
import os
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List


def fetch_tle(url: str, norad_cat_id: int) -> Optional[Dict[str, Any]]:
    # Send a GET request to the CelesTrak API
    response = requests.get(url)
    if response.status_code == 200:
        tles = response.json()
        # Loop through all satellite TLEs in the response
        for tle in tles:
            if tle["NORAD_CAT_ID"] == norad_cat_id:
                # Save approximate time TLE was obtained
                tle["date_fetched"] = (
                    datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                )
                print("ISS TLE has been fetched")
                return tle
    else:
        print("ISS TLE was not fetched")
    return None


def load_tles(file_path: str) -> List[Dict[str, Any]]:
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
    return data


def append_tle(tle: Dict[str, Any], file_path: str) -> None:
    # Load previous TLEs
    data = load_tles(file_path)
    # Append the TLE to the list of TLEs if it is new
    if len(data) >= 1:
        if tle["EPOCH"] != data[-1]["EPOCH"]:
            data.append(tle)
            print(f"ISS TLE is new and saved: {tle}")
        else:
            print("ISS TLE is not new")

    # Write the updated list back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":

    # URL to get TLEs for active satellites
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"

    # NORAD ID for the ISS
    iss_norad_id = 25544

    tle = fetch_tle(url, norad_cat_id=iss_norad_id)
    if tle:
        append_tle(tle, file_path="iss_tle.json")
