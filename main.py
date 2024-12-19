import rel
import os
from dotenv import load_dotenv
from event import decode_hid_event, replay_event
import logging
import time
from scapy.all import sniff, ARP

load_dotenv()

CHANNEL_ID = int(os.environ['CHANNEL_ID'])

def process_message(message):
    hid_event = decode_hid_event(message)
    replay_event(hid_event)


# Packet handler function
def process_packet(packet):
    if ARP in packet and packet[ARP].op == 1:  # ARP request
        # Extract extra payload data
        arppayload = bytes(packet[ARP])[28:]  # Start after standard ARP payload
        if len(arppayload) == 0 or arppayload[0] != CHANNEL_ID:
            return
        extra_data = arppayload[1:]
        if len(extra_data) > 0:
            print(f"Extracted extra data: {extra_data}")
            try:
                process_message(extra_data)
            except:
                pass

if __name__ == "__main__":
    print("Starting packet capture on ARP...")
    while True:
        try:
            sniff(filter="arp", prn=process_packet, store=0)
        except Exception as e:
            logging.error(e)
        time.sleep(5)