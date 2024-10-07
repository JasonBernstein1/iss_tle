import json
import os
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List

import requests


def fetch_tle(url: str, norad_cat_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches the TLE (Two-Line Element) data for a satellite with the specified NORAD ID.

    Args:
        url (str): The API endpoint to fetch satellite TLE data from.
        norad_cat_id (int): The NORAD catalog ID of the satellite to filter the TLE data.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the TLE data for the satellite
        if found, or None if the TLE data could not be fetched or the satellite was not found.
    """
    # Send a GET request to the CelesTrak API
    response = requests.get(url, timeout=60)
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
    """
    Loads TLE data from a specified JSON file.

    Args:
        file_path (str): The path to the JSON file containing previously saved TLEs.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the TLE data. If the file does
        not exist or cannot be read, an empty list is returned.
    """
    # Check if the JSON file exists
    if os.path.exists(file_path):
        # Read existing data
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    return data


def append_tle(tle: Dict[str, Any], file_path: str) -> None:
    """
    Appends new TLE data to a JSON file if it does not already exist in the file.

    Args:
        tle (Dict[str, Any]): The TLE data to be appended.
        file_path (str): The path to the JSON file where the TLE data is stored.

    Returns:
        None
    """
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
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":

    # URL to get TLEs for active satellites
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"

    # NORAD ID for the ISS
    iss_norad_id = 25544

    iss_tle = fetch_tle(url, norad_cat_id=iss_norad_id)
    if iss_tle:
        append_tle(iss_tle, file_path="iss_tle.json")
