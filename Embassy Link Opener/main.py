import xml.etree.ElementTree as ET

import requests
from nsdotpy.session import NSSession


def login(session, nation: str, password: str) -> bool:
    return session.login(nation, password)


session = NSSession(
    "Destiny's Embassy Collecting Script",
    "0.9",
    "The Chinese Soviet",
    "The Chinese Soviet",
    'enter',
    link_to_src='tbd',
    logger=None
)

authenticated = login(session, "name", "password")

if authenticated:
    print("Authentication successful!")
else:
    print("Authentication failed.")


def get_all_regions():
    url = "https://www.nationstates.net/cgi-bin/api.cgi?q=regions"
    headers = {"User-Agent": "Useragent"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        regions = root.find("REGIONS").text.split(",")
        return regions
    else:
        print("Failed to fetch regions. API response status:", response.status_code)
        return []


def load_processed_regions(file_name):
    try:
        with open(file_name, "r") as f:
            content = f.read().strip()
            return set(region for region in content.split(",") if region)
    except FileNotFoundError:
        return set()


def save_processed_region(file_name, region):
    with open(file_name, "a") as f:
        f.write(region + ",")


def send_embassy_requests(regions, session, processed_regions_file):
    for i, region in enumerate(regions):
        if not session.request_embassy(region):
            print(f"Failed to send embassy request to {region}.")
        else:
            print(f"Successfully sent embassy request to {region}.")
            save_processed_region(processed_regions_file, region)
        print(f"Processed region {i + 1} of {len(regions)}. Press space to continue with the next region.")
        input()


if __name__ == "__main__":
    regions = get_all_regions()
    processed_regions_file = "processed_regions.txt"

    processed_regions = load_processed_regions(processed_regions_file)
    remaining_regions = [region for region in regions if region not in processed_regions]

    if remaining_regions:
        remaining_regions_reversed = remaining_regions[::-1]
        send_embassy_requests(remaining_regions_reversed, session, processed_regions_file)
    else:
        print("All regions have been processed.")
