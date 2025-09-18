import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_openrent():
    base_url = "https://www.openrent.co.uk/properties-to-rent/oxford"
    listings = []

    for page in range(1, 3):  
        url = f"{base_url}?page={page}"
        print("Scraping:", url)
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        for item in soup.select(".propertyCard"):
            try:
                price = item.select_one(".propertyCard-price").text.strip().replace("£", "").replace("pcm", "")
                title = item.select_one(".propertyCard-address").text.strip()
                desc = item.select_one(".propertyCard-description").text.strip()

                listings.append({
                    "address": title,
                    "price": int(price.replace(',', '')),
                    "description": desc
                })
            except:
                continue

    df = pd.DataFrame(listings)
    df.to_csv("data/raw_openrent.csv", index=False)
    print("Saved to data/raw_openrent.csv")

if __name__ == "__main__":
    scrape_openrent()
