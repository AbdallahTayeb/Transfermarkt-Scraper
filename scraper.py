import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_flag(tag):
    flag_object = tag.find(class_='flaggenrahmen')
    return flag_object.get('title')

def get_name(tag):
    flag_object = tag.find(class_='hauptlink')
    return flag_object.get_text().strip()

def get_position(tag):
    flag_object = tag.find(class_='inline-table')
    position = flag_object.find_all('tr')[1]
    return position.get_text().strip()

def get_number(tag):
    flag_object = tag.find_all(class_='zentriert')[0]
    return flag_object.get_text().strip()

def get_age(tag):
    flag_object = tag.find_all(class_='zentriert')[1]
    return flag_object.get_text().strip()
    
def get_height(tag):
    flag_object = tag.find_all(class_='zentriert')[3]
    return flag_object.get_text().strip()

def get_foot(tag):
    flag_object = tag.find_all(class_='zentriert')[4]
    return flag_object.get_text().strip()

def get_join(tag):
    flag_object = tag.find_all(class_='zentriert')[5]
    return flag_object.get_text().strip()

def get_from(tag):
    flag_object = tag.find_all(class_='zentriert')[6].find('a')
    try:
        isfrom = flag_object.get('title')
    except:
        isfrom = np.nan
    return isfrom

def get_contract(tag):
    flag_object = tag.find_all(class_='zentriert')[7]
    return flag_object.get_text().strip()

def get_value(tag):
    flag_object = tag.find(class_='rechts hauptlink')
    return flag_object.get_text().strip()

def get_club_url(tag):
    flag_object = tag.find(class_='hauptlink no-border-links')
    return flag_object.find('a').get('href')

def find_urls(soup):
    table = soup.find('table', {'class': 'items'})
    clubs = table.find_all('tr',{'class':['odd','even']})
    return list(map(get_club_url,clubs))

def tf_format(urls):
    tf_urls = ["https://www.transfermarkt.com{}".format(url) for url in urls]
    return tf_urls

def convert_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    right_tab = soup.find_all('a',{'class':'tm-tab'})[1]
    new_url = right_tab.get('href')
    return new_url


url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"  # replace this with your URL

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

clubs_urls = find_urls(soup)
clubs_urls = tf_format(clubs_urls)

final_urls = list(map(convert_url,clubs_urls))
final_urls = tf_format(final_urls)

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


def scrap_players(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tags with class 'posrela'
    parent = soup.find(class_='grid-view')
    table = parent.find('table', {'class': 'items'})
    players = table.find_all('tr',{'class':['odd','even']})
    club_name = soup.find(class_="data-header__profile-container").find('img').get('title')

    # Extract the text from these tags

    countries = list(map(get_flag,players))
    names = list(map(get_name,players))
    positions = list(map(get_position,players))
    numbers = list(map(get_number,players))
    ages = list(map(get_age,players))
    heights = list(map(get_height,players))
    values = list(map(get_value,players))
    foots = list(map(get_foot,players))
    join_dates = list(map(get_join,players))
    contracts = list(map(get_contract,players))
    froms = list(map(get_from,players))
    clubs = [club_name]*len(players)

    df = pd.DataFrame({'club': clubs,
                        'number': numbers,
                        'name': names,
                        'position' : positions,
                        'age' : ages,
                        'height' : heights,
                        'foot' : foots,
                        'country' : countries,
                        'join_date' : join_dates,
                        'contract' :  contracts,
                        'former_club': froms,
                        'market_value':values})
 
    return df


db_players = pd.concat(list(map(scrap_players,final_urls)))
