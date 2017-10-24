########################################################################
#
# Example code for basic demonstration of the LoPy module in OTAA mode.
# Used by Sensefarm in workshops
#
# Author: Daniel Lundell
# Email: daniel.lundell@sensefarm.com
# Copyright: MIT License
#
#########################################################################

import socket
import time
import binascii
import json
from network import LoRa

DATA_PACKET = {"acceleration":0,
               "roll": 0,
               "pitch": 0,
               "yaw": 0
              }

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# Setup authentication keys for OTAA
# DevEUI is fetched from the board and does not need to be supplied

# NOTE: This parameter must be changed to one obtained from the server
app_eui = binascii.unhexlify('12 34 00 00 00 00 00 00'.replace(' ',''))
# NOTE: This parameter must be changed to one obtained from the server
app_key = binascii.unhexlify('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ',''))

# Join a network using Over the Air Activation(OTAA)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Block and waits for the data to be sent and for the 2 receive windows to expire
s.setblocking(True)

#Data to be sent in LoRaWAN message - change to any value you like
acceleration = 1
roll = 2
pitch = 3
yaw = 4

while True:
    print('Sending with the following parameters')

    print('Acceleration:\t' + str(acceleration))
    DATA_PACKET['acceleration'] = str(acceleration)

    print('Roll:\t\t' + str(roll))
    DATA_PACKET['roll'] = str(roll)

    print('Pitch:\t\t' + str(pitch))
    DATA_PACKET['pitch'] = str(pitch)

    print('Yaw:\t\t' + str(yaw))
    DATA_PACKET['yaw'] = str(yaw)

    # send some data
    print('Sending LoRa message')
    s.send(json.dumps(DATA_PACKET))

    # make the socket non-blocking
    s.setblocking(False)

    # get any data received
    dw_data = s.recv(64)
    dw_data_length = len(dw_data)

    if dw_data_length > 0:
        print(dw_data)
    else:
        print('No downlink data')

    time.sleep(30)
