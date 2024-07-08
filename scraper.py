import requests
from bs4 import BeautifulSoup

def scrape_hotel_details(hotel_name: str):
    # Format the search query
    search_query = hotel_name.replace(" ", "+")
    url = f"https://www.booking.com/searchresults.es.html?ss={search_query}"
    print(f"URL: {url}")
    
    # Define headers to emulate a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Save the parsed HTML content to a file for debugging
    with open("debug_response_parsed.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    # Find the first hotel result using updated selectors
    hotel_element = soup.find("a", {"data-testid": "property-card-desktop-single-image"})
    if not hotel_element:
        raise ValueError("Hotel not found")
    
    # Extract the hotel URL
    hotel_url = hotel_element['href']
    print(f"Hotel URL: {hotel_url}")

    # Make another GET request to the hotel URL
    hotel_response = requests.get(hotel_url, headers=headers)
    print(f"Hotel page response status code: {hotel_response.status_code}")
    hotel_response.raise_for_status()  # Raise an HTTPError for bad responses

    # Save the hotel page HTML content to a file
    hotel_content = hotel_response.text
    with open("hotel_page.html", "w", encoding="utf-8") as file:
        file.write(hotel_content)

    # Parse the hotel page HTML content with BeautifulSoup
    hotel_soup = BeautifulSoup(hotel_content, "html.parser")

    # Extract hotel details (modify these selectors as needed)
    name = hotel_soup.find("h2", {"class": "hp__hotel-name"}).text.strip() if hotel_soup.find("h2", {"class": "hp__hotel-name"}) else "No Name Found"
    location = hotel_soup.find("span", {"class": "hp_address_subtitle"}).text.strip() if hotel_soup.find("span", {"class": "hp_address_subtitle"}) else "No Location Found"
    description = hotel_soup.find("div", {"id": "property_description_content"}).text.strip() if hotel_soup.find("div", {"id": "property_description_content"}) else "No Description Found"
    number_of_comments = hotel_soup.find("span", {"class": "review_score_value"}).text.strip() if hotel_soup.find("span", {"class": "review_score_value"}) else "No Comments Found"
    
    return {
        "name": name,
        "location": location,
        "description": description,
        "number_of_comments": number_of_comments,
        "url": hotel_url
    }

# Example usage:
try:
    hotel_data = scrape_hotel_details("Catalonia Barcelona Plaza")
    print(hotel_data)
except ValueError as e:
    print(f"Error: {e}")
