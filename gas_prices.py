from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os
import argparse

# city and state input for url
state_input = input('Please enter state: ')
city_input = input('Please enter city: ')

# make output folder if doesn't exist
output_save = False
links_save = False

folder_path = './output'
file_path = './links.txt'

def folder_create():
    if Path(folder_path).is_dir():
        print(f'Folder path {folder_path} exists.')
    else:
        os.mkdir('output')
        print('Folder "output" created.')
    
def file_create():
    if Path(file_path).exists():
        print(f'File path {file_path} exists.')
    else:
        with open('output/links.txt', 'w') as f:
            print(f'File {file_path} created.')
            pass

# global vars
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

base_gas_prices_url = 'https://www.gasbuddy.com/gasprices/'
url = base_gas_prices_url + state_input + '/' + city_input
base_url = 'https://www.gasbuddy.com/'

# classes for information
price_box_main_class = 'GenericStationListItem-module__stationListItem___3Jmni'
price_box_class = 'Belt__childContainer___PJhvi'
price_box_station_name = 'a' # station name in a href tag 
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

# main function
def main():
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    
        soup = BeautifulSoup(r.content, 'html.parser')
    
        # handy reference for later usage
        links = []
    
        for link in soup.find_all('a'):
            a = link.get('href')
            links.append(a)
       
        # will only write to file if output folder and links file exists
        if links_save and output_save: 
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
        
        for item in soup.find_all(class_='GenericStationListItem-module__stationListItem___3Jmn4'):
            d = item.find(price_box_station_name)
            e = ''
            f = ''
            g = ''
            
            if d:
                price_box_station_name_list.append(d.text)
            else:
                price_box_station_name_list.append('N/A')
             
        for i in range(len(price_box_money_list) - 1):
            new_set = list((
                price_box_station_name_list[i],
                price_box_money_list[i], 
                price_box_time_list[i], 
                price_box_money_type_list[i]
                ))
            price_box_info.append(new_set) 
           
        # sorts list, low to high
        price_box_info.sort(key=lambda x: x[0])
            
        for item in price_box_info:
            print('Vendor: {:<12}\tPrice: {:^4}\tTime: {:<10}\tMoney Type: {:>10}'.format(item[0], item[1], item[2], item[3]))
    
    # catches failed response
    except requests.exceptions.RequestException as e:
        print(f'Error during request: {e}')

# cli arg parsing

parser = argparse.ArgumentParser()
parser.add_argument('-l', help='Likns file creation', action='store_true')
parser.add_argument('-o', help='Output folder creation', action='store_true')
parser.add_argument('-m', help='Main function', action='store_true')
args = parser.parse_args()

if args.o:
    output_save = True
    folder_create()

if args.l and output_save == True:
    links_save = True
    file_create()

if args.m:
    main()

