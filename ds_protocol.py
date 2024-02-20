# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lex Ibanez
# laibanez@uci.edu
# 70063614

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys

response = namedtuple('response', ['type','message','token'], defaults= [None, None, None])

def extract_json(json_msg:str) -> response:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    message_dict = json.loads(json_msg)
    type = message_dict['response']['type']
    message = message_dict['response']['message']
    token = message_dict['response'].get('token')

  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return response(type, message, token)
