import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

def fetch_listings(location, max_pages=5, limit=20):
    all_listings=[]
    for page in range(max_pages):
        offset = page * limit
        params = {
            "location": location,
            "home_type": "Houses",
            "status_type": "ForSale",
            "limit": limit,
            "offset": offset
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            listings = data.get("props", [])
            if not listings:
                break
            all_listings.extend(listings)
            print(f"Fetched page {page + 1} with {len(listings)} listings.")
        else:
            print(f"Request failed at page {page + 1}: {response.status_code}")
            break
    return all_listings

def save_to_csv(listings, filename="raw_data/listings.csv"):
    if not listings:
        print("No data to save.")
        return
    os.makedirs("raw_data", exist_ok=True)
    df = pd.json_normalize(listings)
    keep_cols = [
        "zpid", "price", "address", "bedrooms", "bathrooms", "livingArea",
        "zipcode", "city", "state", "latitude", "longitude", "statusText"
    ]
    df = df[[col for col in keep_cols if col in df.columns]]
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} listings to {filename}")

listings = fetch_listings(location="Johnson City, TN", max_pages=1, limit=20)
save_to_csv(listings)


