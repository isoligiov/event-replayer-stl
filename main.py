import sys
import os
from dotenv import load_dotenv
from event import decode_hid_event, replay_event
import logging
import time
from scapy.all import sniff, ARP

load_dotenv()

CHANNEL_ID = int(os.environ['CHANNEL_ID'])
double_sniff = False
packet_index = 0

def process_message(message):
    hid_event = decode_hid_event(message)
    replay_event(hid_event)


# Packet handler function
def process_packet(packet):
    global double_sniff, packet_index
    if ARP in packet and packet[ARP].op == 1:  # ARP request
        # Extract extra payload data
        arppayload = bytes(packet[ARP])[28:]  # Start after standard ARP payload
        if len(arppayload) == 0 or arppayload[0] != CHANNEL_ID:
            return
        extra_data = arppayload[1:]
        if len(extra_data) > 0:
            print(f"Extracted extra data: {extra_data}")
            try:
                if double_sniff is False or packet_index % 2 == 0:
                    process_message(extra_data)
            except:
                pass
            packet_index += 1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'dup':
        double_sniff = True
    print("Starting packet capture on ARP...")
    while True:
        try:
            sniff(filter="arp", prn=process_packet, store=0)
        except Exception as e:
            logging.error(e)
        time.sleep(5)