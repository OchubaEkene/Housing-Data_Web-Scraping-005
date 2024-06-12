import requests
from bs4 import BeautifulSoup
import sqlite3

# Establish connection to Sqlite database
conn = sqlite3.connect('houses.db')
c = conn.cursor()

# Create a table (if it doesn't exist)
# c.execute('''
#     CREATE TABLE houses(
#         spec REAL,
#         location TEXT,
#         price REAL,
#         company TEXT,
#         phone_no REAL,
#         bedrooms REAL,
#         bathrooms REAL,
#         toilet REAL,
#         parking_spaces REAL)''')


for i in range(1, 11):
    url = 'https://nigeriapropertycentre.com/for-sale/houses/showtype'+str(i)
    r = requests.get(url)
    # print(r)

    # Parsing
    soup = BeautifulSoup(r.text, "lxml")

    # Find the main container that holds all the products
    listings = soup.find("div", class_='col-md-8')

    for listing in listings:
        # Specifications
        spec = listings.find('h4', class_='content-title').text.strip()

        # Location
        location = listings.find('address', class_='voffset-bottom-10').text.strip()

        # Price
        price = listings.find('span', class_='pull-sm-left').text.strip()

        # Company Information
        company_info = listings.find('span', class_='marketed-by pull-right hidden-xs hidden-sm text-right').text.strip()
        company = company_info.split('\n')[0].strip()
        phone_no = company_info.split('n')[-1].strip()

#       # Bedrooms
        bedrooms = listings.find('i', class_='fal fa-bed')
        bedrooms = bedrooms.find_next('span').text.strip() if bedrooms else 0

        # Bathrooms
        bathrooms = listings.find('i', class_='fal fa-bath')
        bathrooms = bathrooms.find_next('span').text.strip() if bathrooms else 0

        # Toilet
        toilet = listings.find('i', class_='fal fa-toilet')
        toilet = toilet.find_next('span').text.strip() if toilet else 0

        # Parking spaces
        parking_spaces = listings.find('i', class_='fal fa-car')
        parking_spaces = parking_spaces.find_next('span').text.strip() if parking_spaces else 0

        # Insert data into the database
        c.execute('''INSERT INTO houses (spec, location, price, company, phone_no, bedrooms, bathrooms, toilet, parking_spaces) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (spec, location, price, company, phone_no, bedrooms, bathrooms, toilet, parking_spaces))

conn.commit()

conn.close()

print('Scraping Complete!')
