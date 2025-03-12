from bs4 import BeautifulSoup
import requests

url = 'https://www.scrapethissite.com/pages/simple/'
response = requests.get(url)
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

with open("output.txt", 'w', encoding='utf-8') as file:
    file.write(soup.prettify())