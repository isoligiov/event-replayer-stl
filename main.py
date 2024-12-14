import websocket
import rel
import os
from dotenv import load_dotenv
from event import decode_hid_event, replay_event

load_dotenv()

RELAY_SERVER_APP_NAME = os.environ['RELAY_SERVER_APP_NAME']

def on_message(ws, message):
    hid_event = decode_hid_event(message)
    replay_event(hid_event)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send_text(f'dest/{RELAY_SERVER_APP_NAME}')

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://streamlineanalytics.net:10010",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()