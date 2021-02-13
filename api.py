from blizzardapi import BlizzardApi
import json
from datetime import date, datetime
import configparser

def low_val(arr):
  '''returns lowest cost fish object from the list of fish'''
  min_dict = arr[0]
  min = arr[0]["unit_price"]
  for a in range(0, len(arr)):
    if(arr[a]["unit_price"] < min):
      min = arr[a]["unit_price"]
      min_dict = arr[a]

  return min_dict

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

##eventually put in lambda with 1 hr repeated schedule

def main():
  ## reference config for secret key
  config = configparser.ConfigParser()
  config.read('config.ini')
  client_id = config.get('DEFAULT', 'Client_ID')

  secret_id = config.get('DEFAULT', 'Secret_ID')



  api_client = BlizzardApi(client_id, secret_id)
  # Unprotected API endpoint
  # actual endpoint to use once working
  # 5 is proudmoore's connected server ID
  auctions = api_client.wow.game_data.get_auctions("us", "en_US", "5")

  auctions = auctions["auctions"]

  ## pretend json read is the actual response for now


  ## load fish
  fish_list = []

  ## save fish IDs here to use later
  ## lost sole = 173032
  ## iridescent amberjack = 173033
  ## silvergill pike = 173034
  ## pocked bonefish = 173035
  ## spinefin pirahna = 173036
  ## elysian Thade = 173037

  lo_so = []
  ir_am = []
  si_pi = []
  po_bo = []
  sp_pi = []
  el_th = []

  now = datetime.utcnow()

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

  fish_list.append(low_val(lo_so))
  fish_list.append(low_val(ir_am))
  fish_list.append(low_val(si_pi))
  fish_list.append(low_val(po_bo))
  fish_list.append(low_val(sp_pi))
  fish_list.append(low_val(el_th))


  with open('fish.json', 'w') as outfile:
    json.dump(fish_list, outfile)

main()






#test -- write response to file to testing with
#with open('item.json', 'w') as outfile:
#  json.dump(item, outfile)