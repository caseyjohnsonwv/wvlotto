import re
import requests
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

parse_for_integer = '[^0-9]+'
parse_for_float = '[^0-9\.]+'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def get_games():
    url = "https://wvlottery.com/scratch-offs"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, features="html.parser")
    games = []
    for section in soup.findAll('a', attrs={'class':'game'}):
        link = section.get('href')
        games.append(link)
    return games


def get_prizes(game_url):
    r = requests.get(game_url, headers=headers)
    soup = BeautifulSoup(r.content, features="html.parser")
    output = {}
    # extract game price
    price = int(re.findall('<td>Ticket Price<\/td>\n\s+<td>\$(\d+)<\/td>',r.text)[0])
    output["price"] = price
    # extract total tickets in circulation
    tickets = re.findall('<td>Total tickets in game<\/td>\n\s+<td>([0-9,]+)<\/td>',r.text)[0]
    tickets = int(re.sub(parse_for_integer, '', tickets))
    output["circulation"] = tickets
    # extract game data
    prizes = {}
    table = soup.find('table', attrs={'class':'stat-table'})
    tbody = table.find('tbody')
    rows = tbody.findAll('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # process columns
        prize = int(re.sub(parse_for_integer,'',cols[0]))
        odds = re.match('1:([0-9,\.]+)',cols[1])
        odds = float(re.sub(parse_for_float,'',cols[1]))
        total_winners = int(re.sub(parse_for_integer,'',cols[2]))
        remaining_prizes = int(re.sub(parse_for_integer,'',cols[3]))
        remaining_dollars = int(re.sub(parse_for_integer,'',cols[4]))
        # map prize amount (keys) to its data (values)
        prizes[prize] = {"odds":odds, "total":total_winners, "remaining":remaining_prizes, "amount":remaining_dollars}
        output["prizes"] = prizes
    return output


def scrape_new_data(outputFile='raw.txt'):
    data = {}
    urls = get_games()
    i = 0
    for game_url in urls:
        print("Analyzing '{}'".format(game_url))
        try:
            game_data = get_prizes(game_url)
        except AttributeError:
            print("--> Information on '{}' not available".format(game_url))
            continue
        data[game_url] = game_data
    with open(outputFile,'w') as f:
        f.write(str(data))


scrape_new_data()
