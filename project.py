# Import Libraries
from gettext import find
import requests
from bs4 import BeautifulSoup as bs
import json
import mysql.connector

# MySQL Database Connection
mydb = mysql.connector.connect(
    host="sql6.freesqldatabase.com",
    user="sql6520423",
    password="rujgDVI2I1",
    database="sql6520423"
)

# Database Queries
def saveDatabase(p_hotel_id, p_hotel_name, p_image_url, p_image_label):
    mycursor = mydb.cursor()
    sql = "INSERT INTO hotel_info (hotel_id, hotel_name, image_url,image_label) VALUES (%s, %s,%s, %s)"
    val = (p_hotel_id, p_hotel_name, p_image_url, p_image_label)
    mycursor.execute(sql, val)
    mydb.commit()


# Base URL
baseURL = 'https://www.kayak.co.in'

# Selected Location
findHotelName = "bali"

# Selected Hotel
hotelSlNo = 1

# ALL Locations Scrap by Base URL
soup = bs(requests.get(baseURL).text, features='html.parser')
allLocations = soup.find_all('div', {"class": "P_Ok-header"})

# Scrap Specific Location from all locations
for locationParent in allLocations:
    locationTag = locationParent.find('h3', {"class": "P_Ok-title"}).text

    # Scrap all Hotels by specific location
    if (locationTag.lower() == findHotelName):
        hotelLinkDiv = locationParent.find(
            'div', {"class": "P_Ok-header-links"})
        hotelsLink = baseURL+hotelLinkDiv.find_all('a')[2].get("href")
        hotelPage = bs(requests.get(hotelsLink).text, features='html.parser')
        hotels = hotelPage.find_all('div', {"class": "soom"})

        # Select one hotel from all hotels
        findHotel = hotels[hotelSlNo-1]
        hotelDetailLink = baseURL+findHotel.find('a').get("href")
        urlWords = hotelDetailLink.split(".")
        hotelId = urlWords[len(urlWords)-2]
        print(hotelId)

        # Select Hotel Page
        hotelDetailPage = bs(requests.get(hotelDetailLink).text,
                             features='html.parser')

        # Scrap json from scripts
        jsonData = hotelDetailPage.find_all(
            "script", {"type": "application/ld+json"})[2].text
        json_object = json.loads(jsonData)

        # Scrap Hotel Name
        hotelName = json_object["name"]
        print(hotelName)

        for photo in json_object["photo"]:

            # Generate photo's url
            photosUrl = photo["contentUrl"].split("?")[0]
            print(photosUrl)

            # Generate photo's label
            descWords = photo["description"].split("-")
            photosLabel = descWords[len(descWords)-1].strip()
            print(photosLabel)

            # Values save in Database
            saveDatabase(hotelId, hotelName, photosUrl, photosLabel)
