import re
import requests
from bs4 import BeautifulSoup
from database import BookDatabaseManager

# Star rating text to integer map
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# Scrape first 20 books and store in SQLite
def scrape_first_20_books(url: str = "http://books.toscrape.com/"):
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")

    db_manager = BookDatabaseManager()
    scraped_books = []

    # Limit to first 20 books
    for item in book_elements[:20]:
        # Extract title
        title_tag = item.h3.find("a")
        title = title_tag["title"] if title_tag and "title" in title_tag.attrs else title_tag.text

        # Extract price
        price_text = item.find("p", class_="price_color").text
        price_clean = re.sub(r"[^\d.]", "", price_text)
        price = float(price_clean)

        # Extract availability
        availability = item.find("p", class_="instock availability").text.strip()
        in_stock = "In stock" in availability

        # Extract star rating
        star_tag = item.find("p", class_=re.compile(r"star-rating"))
        rating = 0
        if star_tag:
            classes = star_tag.get("class", [])
            for c in classes:
                if c in RATING_MAP:
                    rating = RATING_MAP[c]
                    break

        # Save record to database.
        book = db_manager.create_book(
            title=title,
            price=price,
            in_stock=in_stock,
            rating=rating
        )
        scraped_books.append(book)

    print(f"Successfully scraped and stored {len(scraped_books)} books into books.db!")
    return scraped_books

if __name__ == "__main__":
    scrape_first_20_books()
