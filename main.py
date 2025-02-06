import os
from dotenv import load_dotenv
from event import decode_hid_event, replay_event
import logging
import time
from scapy.all import sniff, ARP

load_dotenv()

CHANNEL_ID = int(os.environ['CHANNEL_ID'])
double_sniff = False
last_event_id = None

def process_message(message):
    hid_event = decode_hid_event(message)
    replay_event(hid_event)


# Packet handler function
def process_packet(packet):
    global double_sniff, last_event_id
    if ARP in packet and packet[ARP].op == 1:  # ARP request
        # Extract extra payload data
        arppayload = bytes(packet[ARP])[28:]  # Start after standard ARP payload
        if len(arppayload) < 2 or arppayload[0] != CHANNEL_ID:
            return
        event_id = arppayload[1]
        if last_event_id == event_id:
            return
        last_event_id = event_id
        extra_data = arppayload[2:]
        if len(extra_data) > 0:
            try:
                process_message(extra_data)
            except:
                pass

if __name__ == "__main__":
    print("Working ...")
    while True:
        try:
            sniff(filter="arp", prn=process_packet, store=0)
        except Exception as e:
            logging.error(e)
        time.sleep(5)