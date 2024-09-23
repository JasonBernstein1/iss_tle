import requests
import json
import os
from datetime import datetime, timezone
from typing import Optional, Any, Dict


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
                return tle
    return None


def append_tle(tle: Dict[str, Any], file_path: str) -> None:
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

    # Append the new TLE to the list
    data.append(tle)

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
        print(f"ISS TLE fetched and appended: {tle}")
    else:
        print("Could not fetch ISS TLE")
