import pandas as pd
import requests
import json
import csv


#get the all english database from scryfall
def Build_database():
  #fetch the 'Default Cards' dataset
  x = requests.get('https://data.scryfall.io/default-cards/default-cards-20230402210915.json')
  data = x.json()
  with open('data.json', 'w') as f:
    json.dump(data, f)

#make a csv to work with easyer later
def database_to_csv(database):
  with open(database, encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)
  df.to_csv(database.split('.',1)[0] + '.csv', encoding='utf-8', index=False)

#this function is to make runtime faster later if needed
#this can also be used to save on storage space if needed
def crop_database(database):
  #with open('all_cards.csv', encoding='utf-8') as inputfile:
  df = pd.read_csv(database,  low_memory=False)
  #all the catagorys we need put here
  df = df[['multiverse_ids', 'name', 'set', 'set_name', 'collector_number', 'cmc', 'colors', ]]
  df.to_csv('all_cards_edit.csv', encoding='utf-8', index=False)

#this gets the id needed for most of our serches
def find_card(code, num):
  with open('all_cards_edit.csv', 'r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        if line['set'] == code and line['collector_number'] == str(num):
          print(line['name'], line['collector_number'])
          return(line['multiverse_ids'])

#this one is specal as this changes with time so we dont trust the database here
#this is one where we ping scryfall to find it in real time
def get_price(id):
  #get the card.json with id
  #print('https://api.scryfall.com/cards/multiverse/' + id[1:-1])
  x = requests.get('https://api.scryfall.com/cards/multiverse/' + id[1:-1])
  card = x.json()
  print(card["prices"]["usd"])


#this gets any other traite we need
def get_attribute(id, attribute):
  with open('data.csv', 'r', encoding="utf8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        if line['multiverse_ids'] == id:
          return(line[attribute])



#this is for testing as when implemented this will never be called
def main():
  #Build_database()
  #database_to_csv('data.json')
  id = find_card('2x2', 168)
  get_price(id)
  attribute = get_attribute(id, 'colors')
  print(attribute)





if __name__ == "__main__":
  main()
