from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os

# make output folder if doesn't exist
folder_path = './output'
file_path = './links.txt'

if Path(folder_path).is_dir():
    print(f'Folder path {folder_path} exists.')
else:
    os.mkdir('output')
    print('Folder "output" created.')

if Path(file_path).exists():
    print(f'File path {file_path} exists.')
else:
    with open('output/links.txt', 'w') as f:
        print(f'File {file_path} created.')
        pass

# vars
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
url = 'https://www.gasbuddy.com/gasprices/ohio/cleveland'
base_url = 'https://www.gasbuddy.com/'

price_class = 'text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL'

headers = {
    'User-Agent': user_agent
}

try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')

    links = []

    for link in soup.find_all('a'):
        a = link.get('href')
        links.append(a)
    
    # for loop doesn't work, write from link list straight
    with open('output/links.txt', 'w') as f: 
        if not links:
            print("Links is empty")
        else:
            # for some reason, need to conver link to str??? no idea
            for link in links:
                f.write(base_url + str(link) + '\n')

except requests.exceptions.RequestException as e:
    print(f'Error during request: {e}')
