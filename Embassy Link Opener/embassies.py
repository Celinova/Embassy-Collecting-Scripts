import webbrowser
import time
import requests
import xml.etree.ElementTree as ET

def get_all_regions(headers):
    url = "https://www.nationstates.net/cgi-bin/api.cgi?q=regions"

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

def open_region_links(regions, batch_size, processed_regions_file):
    base_url = "https://www.nationstates.net/region="

    for i in range(0, len(regions), batch_size):
        for region in regions[i:i + batch_size]:
            if region not in processed_regions:
                url = base_url + region
                webbrowser.open(url)
                save_processed_region(processed_regions_file, region)
        print(f"Opened regions {i + 1} to {min(i + batch_size, len(regions))}. Press enter to continue with the next batch.")
        input()

if __name__ == "__main__":
    app_name = input("Enter your app name: ")
    contact_email = input("Enter your contact email: ")
    headers = {"User-Agent": f"{app_name}/{contact_email}"}

    regions = get_all_regions(headers)
    batch_size = int(input("Enter the number of regions to process at a time: "))
    processed_regions_file = "processed_regions.txt"

    processed_regions = load_processed_regions(processed_regions_file)
    remaining_regions = [region for region in regions if region not in processed_regions]

    if remaining_regions:
        open_region_links(remaining_regions, batch_size, processed_regions_file)
    else:
        print("All regions have been processed.")
