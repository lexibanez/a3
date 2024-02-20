# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lex Ibanez
# laibanez@uci.edu
# 70063614

# usr: lexibanez pwd: passwordlol

from ds_protocol import extract_json
import socket
import json

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
  data = {
        "join": {
            "username": username,
            "password": password,
            "token": ''
        }
    }
  
  json_string = json.dumps(data)


  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((server, port))

    send = client.makefile('w')
    recv = client.makefile('r')

    send.write(json_string + '\r\n')
    send.flush()

    resp = recv.readline()
    response_tuple = extract_json(resp)

  return response_tuple


if __name__ == '__main__':
    send('168.235.86.101', 3021, 'newuser1233424', 'passwordlol', 'hello world')