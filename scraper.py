import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO)

def scrape_hotel_details(hotel_name: str):
    logging.info(f"Scraping details for hotel: {hotel_name}")

    # Format the search query
    search_query = hotel_name.replace(" ", "+")
    url = f"https://www.booking.com/searchresults.es.html?ss={search_query}"
    logging.info(f"URL: {url}")
    
    # Define headers to emulate a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    logging.info(f"Response status code: {response.status_code}")
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    logging.info("Parsed HTML content")
   
   # Write the parsed HTML content to a file for inspection
    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    # Find the first hotel result using updated selectors
    hotel_element = soup.find("a", {"data-testid": "property-card-desktop-single-image"})
    if not hotel_element:
        logging.error("Hotel not found")
        raise ValueError("Hotel not found")
    
    # Extract the hotel URL
    hotel_url = hotel_element['href']
    logging.info(f"Hotel URL: {hotel_url}")

    # Make another GET request to the hotel URL
    hotel_response = requests.get(hotel_url, headers=headers)
    logging.info(f"Hotel page response status code: {hotel_response.status_code}")
    hotel_response.raise_for_status()  # Raise an HTTPError for bad responses

    # Parse the hotel page HTML content with BeautifulSoup
    hotel_soup = BeautifulSoup(hotel_response.text, "html.parser")
    logging.info("Parsed hotel page HTML content")

    # Extract hotel details (modify these selectors as needed)
    name = hotel_soup.find("h2", {"class": "pp-header__title"}).text.strip() if hotel_soup.find("h2", {"class": "pp-header__title"}) else "No Name Found"
    location = hotel_soup.find("span", {"class": "hp_address_subtitle"}).text.strip() if hotel_soup.find("span", {"class": "hp_address_subtitle"}) else "No Location Found"
    description = hotel_soup.find("div", {"id": "property_description_content"}).text.strip() if hotel_soup.find("div", {"id": "property_description_content"}) else "No Description Found"
    number_of_comments_text = hotel_soup.find("a", {"data-testid": "Property-Header-Nav-Tab-Trigger-reviews"}).text.strip() if hotel_soup.find("a", {"data-testid": "Property-Header-Nav-Tab-Trigger-reviews"}) else "No Comments Found"
    number_of_comments_match = re.search(r'\(([\d\.]+)\)', number_of_comments_text)
    number_of_comments = int(number_of_comments_match.group(1).replace('.', '')) if number_of_comments_match else 0
    rating_text = hotel_soup.find("div", {"class": "c617a39cca"}).text.strip() if hotel_soup.find("div", {"class": "c617a39cca"}) else "No Rating Found"
    rating_match = re.search(r'[\d\.]+', rating_text)
    rating = float(rating_match.group()) if rating_match else 0.0

    logging.info(f"Extracted details - Name: {name}, Location: {location}, Description: {description}, Comments: {number_of_comments}, Rating: {rating}")

    # Extract image URLs
    image_grid = hotel_soup.find('div', {"class": "clearfix bh-photo-grid bh-photo-grid--space-down fix-score-hover-opacity"})
    image_elements = image_grid.find_all('a', {"class": "bh-photo-grid-item"}) if image_grid else []
    image_urls = [img.get('data-thumb-url') for img in image_elements if img.get('data-thumb-url')]
    logging.info(f"Extracted images: {image_urls}")

    # Extract most popular facilities
    facilities = []
    facilities_section = hotel_soup.find('div', {'data-testid': 'property-most-popular-facilities-wrapper'})
    if facilities_section:
        facilities_list_items = facilities_section.find_all('li', {'class': 'd044972638'})
        for item in facilities_list_items:
            facility = item.find('span', {'class': 'ebd881c9a1'})
            if facility:
                facilities.append(facility.text.strip())
    logging.info(f"Extracted facilities: {facilities}")

    return {
        "name": name,
        "location": location,
        "description": description,
        "number_of_comments": number_of_comments,
        "rating": rating,
        "images": image_urls,
        "facilities": facilities,
        "url": hotel_url
    }
