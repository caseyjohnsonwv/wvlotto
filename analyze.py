import re

class Game:
    def __init__(self, name, price, expected_value=0):
        self.name = name
        self.price = price
        self.expected_value = expected_value
        self.pay_ratio = self.expected_value/self.price
    def __repr__(self):
        return "{name} (${price}): ${value}".format(name=self.name, price=self.price, value=round(self.expected_value,2))

dataFile = 'raw.txt'
with open(dataFile, 'r') as f:
    string = f.read()

games = []

data = eval(string)
for game_url in data:
    name = re.findall('\/[A-Za-z0-9\-]+\/$',game_url)[0]
    price = data[game_url]["price"]
    expected_value = 0
    prizes = data[game_url]["prizes"]
    circulation = data[game_url]["circulation"]
    for prize in prizes:
        winners_remaining = prizes[prize]['remaining']
        probability = winners_remaining/circulation
        expected_value += prize * probability
    games.append(Game(name, price, expected_value))

games.sort(key=lambda g:g.pay_ratio, reverse=True)
for g in games:
    print(g)
