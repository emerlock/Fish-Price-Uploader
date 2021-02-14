import configparser
import uuid
from datetime import datetime

import boto3
from blizzardapi import BlizzardApi


def low_val(arr):
  '''returns lowest cost fish object from the list of fish'''
  min_dict = arr[0]
  min = arr[0]["unit_price"]
  for a in range(0, len(arr)):
    if(arr[a]["unit_price"] < min):
      min = arr[a]["unit_price"]
      min_dict = arr[a]

  return min_dict


def load_table(fish_list):
  '''puts items into dynamodb from list format'''

  dynamodb = boto3.resource('dynamodb')

  table = dynamodb.Table('Fish-Price')
  for fish in fish_list:
    table.put_item(
      Item={
          'GUID': fish['GUID'],
          'id': fish['id'],
          'item': fish['item'],
          'quantity': fish['quantity'],
          'unit_price': fish['unit_price'],
          'time_left': fish['time_left'],
          'fish_name': fish['fish_name'],
          'date': fish['date'],
          'hour': fish['hour'],
      }
    )

## TODO: eventually put in lambda with 1 hr repeated schedule

def main():
  
  config = configparser.ConfigParser()
  config.read('config.ini')
  client_id = config.get('DEFAULT', 'Client_ID')

  secret_id = config.get('DEFAULT', 'Secret_ID')



  api_client = BlizzardApi(client_id, secret_id)
  
  # 5 is proudmoore's connected server ID
  # TODO: In future support more servers
  
  response = api_client.wow.game_data.get_auctions("us", "en_US", "5")
  auctions = response["auctions"]

  ## load fish
  fish_list = []

  ## save fish IDs here to use later
  ## lost sole = 173032
  ## iridescent amberjack = 173033
  ## silvergill pike = 173034
  ## pocked bonefish = 173035
  ## spinefin pirahna = 173036
  ## elysian Thade = 173037
  # TODO: find a better way? Each expansion different
  # items will want to be tracked

  # instantiate individual fish lists..
  # storing everything for each fish
  # then finding lowest value to just track that
  # reduce noise for first release
  # TODO: In future, include more to see if market can
  # be manipulated with buys
  lo_so = []
  ir_am = []
  si_pi = []
  po_bo = []
  sp_pi = []
  el_th = []

  # declare time here instead of in loop for two reasons:
  # one call better than unknown amount of calls
  # keep all fish to the same hour for edge cases
  now = datetime.utcnow()

  # extract out only fish auctions
  for auction in auctions:
    if auction['item']['id'] == 173032:
      auction['fish_name'] = 'Lost Sole'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      lo_so.append(auction)
    elif auction['item']['id'] == 173033:
      auction['fish_name'] = 'Iridescent Amberjack'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      ir_am.append(auction)
    elif auction['item']['id'] == 173034:
      auction['fish_name'] = 'Silvergill Pike'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      si_pi.append(auction)
    elif auction['item']['id'] == 173035:
      auction['fish_name'] = 'Pocked Bonefish'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      po_bo.append(auction)
    elif auction['item']['id'] == 173036:
      auction['fish_name'] = 'Spinefin Pirahna'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      sp_pi.append(auction)
    elif auction['item']['id'] == 173037:
      auction['fish_name'] = 'Elysian Thade'
      auction['date'] = now.strftime("%x")
      auction['hour'] = now.strftime("%H")
      el_th.append(auction)

  # set lowest value item to the list of items to store in dynamodb
  fish_list.append(low_val(lo_so))
  fish_list.append(low_val(ir_am))
  fish_list.append(low_val(si_pi))
  fish_list.append(low_val(po_bo))
  fish_list.append(low_val(sp_pi))
  fish_list.append(low_val(el_th))

  # UUID for partition key in dynamoDB
  for item in fish_list:
    item['GUID'] = str(uuid.uuid4())

  # TODO: change to dynamodb set items
  load_table(fish_list)
  
  # with open('fish.json', 'w') as outfile:
  #   json.dump(fish_list, outfile)

main()
