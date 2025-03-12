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

# classes for information
price_box_main_class = 'GenericStationListItem-module__stationListItem___3Jmni'
price_box_class = 'Belt__childContainer___PJhvi'
price_box_rating = ''
price_box_address = ''
price_box_city_state = ''
price_box_money = 'text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL'
price_box_time = 'ReportedBy-module__postedTime___J5H9Z'
price_box_money_type = 'text__left___1iOw3 StationDisplayPrice-module__cashTag___14vFI'

# how to seem like a real boy
headers = {
    'User-Agent': user_agent
}

try:
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')

    # handy reference for later usage
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

    # price box component lists            
    price_box_station_name_list = []
    price_box_rating_list = []
    price_box_address_list = []
    price_box_city_state_list = []    
    price_box_money_list = []
    price_box_time_list = []
    price_box_money_type_list = []
    price_box_info = []
    
    # price box information, top class container
    # needs other elements
    for item in soup.find_all(class_='StationDisplayPrice-module__borderContainer___FfIQJ StationDisplayPrice-module__bordered___ExChJ'):
        a = item.find(class_=price_box_money)
        b = item.find(class_=price_box_time)
        c = item.find(class_=price_box_money_type)
        d = item.find('a')
        e = ''
        f = ''
        g = ''
         
        if a:
            price_box_money_list.append(a.text)
        else:
            price_box_money_list.append('N/A')
        if b:
            price_box_time_list.append(b.text)
        else:
            price_box_time_list.append('N/A')
        if c:
            price_box_money_type_list.append(c.text)
        else:
            price_box_money_type_list.append('N/A')
        
    for i in range(len(price_box_money_list) - 1):
        new_set = list((price_box_money_list[i], price_box_time_list[i], price_box_money_type_list[i]))
        price_box_info.append(new_set) 
       
    # sorts list, low to high
    price_box_info.sort(key=lambda x: x[0])    
    for item in price_box_info:
        print('Price: {:>4} Time: {:>15} Money Type: {:>6}'.format(item[0], item[1], item[2]))

# catches failed response
except requests.exceptions.RequestException as e:
    print(f'Error during request: {e}')
