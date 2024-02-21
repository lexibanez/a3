# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lex Ibanez
# laibanez@uci.edu
# 70063614

# usr: lexibanez pwd: passwordlol
# token: b4337385-d222-4dfc-bc91-0450e40c0de3

from ds_protocol import extract_json
import socket
import json
import time

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  #TODO: return either True or False depending on results of required operation

  response_tuple = join_server(server, port, username, password)

  # if username or password is taken, return False
  if response_tuple.type == 'error':
    print(response_tuple.message)
    return False
  
  token = response_tuple.token
  post = {
    "token": token, 
    "post": {
       "entry": message, 
       "timestamp" : time.time()
     }
  }
  
  post_string = json.dumps(post)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((server, port))

    send = client.makefile('w')
    recv = client.makefile('r')

    send.write(post_string + '\r\n')
    send.flush()

    resp = recv.readline()
    response_tuple = extract_json(resp)


  if bio:
    bio = {
    "token": token, 
    "bio": {
       "entry": bio, 
       "timestamp" : time.time()
     }
  }
  

  bio_string = json.dumps(bio)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((server, port))

    send = client.makefile('w')
    recv = client.makefile('r')

    send.write(bio_string + '\r\n')
    send.flush()

    resp = recv.readline()
    response_tuple = extract_json(resp)

  return True



def join_server(server, port, username, password,):
  data = {
        "join": {
            "username": username,
            "password": password,
            "token": ''
        }
    }
  # create json string with data
  json_string = json.dumps(data)

  # start client and join DSP server
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((server, port))

    send = client.makefile('w')
    recv = client.makefile('r')

    send.write(json_string + '\r\n')
    send.flush()

    resp = recv.readline()
    # extract the server response into a named tuple
    response_tuple = extract_json(resp)

  return response_tuple

if __name__ == '__main__':
    send('168.235.86.101', 3021, 'lexibanez', 'passwordlol', ':0', 'testbio')