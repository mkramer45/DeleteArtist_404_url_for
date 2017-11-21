import bs4
from urllib import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import sqlite3

my_url = 'https://www.beatport.com/genre/tech-house/11/top-100'

# opening up connecting, grabbing the page
uClient = uReq(my_url)
# this will offload our content into a variable
page_html = uClient.read()
# closes our client
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("li",{"class":"bucket-item ec-item track"})

conn = sqlite3.connect('Beatscrape.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS BeatPortTechHouse(Artist TEXT, Song TEXT, Label TEXT, Price DECIMAL)')

# might need to remove these


# MSK, artist name
for container in containers:

	artistName = container["data-ec-d1"] 

	song_Name = container["data-ec-name"]

	label_Name = container["data-ec-brand"] 

	price_Amount = container["data-ec-price"]

	cursor.execute("INSERT INTO BeatPortTechHouse VALUES (?, ?, ?, ?)", (artistName, song_Name, label_Name, price_Amount))


# conn = sqlite3.connect('Beatscrape.db')
# cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS ArtistMonitor(id INTEGER PRIMARY KEY AUTOINCREMENT, DJname TEXT)')


conn.commit()
cursor.close()
conn.close()

