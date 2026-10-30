import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone

URL = "https://books.toscrape.com/"

response = requests.get(
    URL,
    timeout=30,
    headers={"User-Agent": "StudentWebScrapingProject/1.0"}
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select("article.product_pod"):
    title = book.h3.a.get("title", "").strip()
    price = book.select_one(".price_color").get_text(strip=True)
    availability = book.select_one(
        ".availability"
    ).get_text(" ", strip=True)

    rating_classes = book.select_one(
        ".star-rating"
    ).get("class", [])

    rating = next(
        (r for r in rating_classes if r != "star-rating"),
        "Unknown"
    )

    books.append({
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Rating": rating,
        "Scraped_At_UTC": datetime.now(
            timezone.utc
        ).isoformat()
    })

if not books:
    raise ValueError("No books found. Check the website structure.")

df = pd.DataFrame(books)

output_path = Path("data/products.xlsx")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_excel(output_path, index=False)

print(f"Total books scraped: {len(df)}")
print(f"Excel file saved to: {output_path.resolve()}")
print(df.head())