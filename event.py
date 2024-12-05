from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from pynput.mouse import Controller as MouseController, Button
from AppKit import NSScreen
from utils import bytes_to_signed_int

# Getting the main screen resolution using AppKit
screen_width = NSScreen.mainScreen().frame().size.width
screen_height = NSScreen.mainScreen().frame().size.height

keyboard = KeyboardController()
mouse = MouseController()

def scale_coordinate(value, max_value):
    # Scale from the range -32768 to 32767 to 0 to max_value
    return (value + 32768) * max_value / 65535

def decode_hid_event(data):
    event = {}
    event_type_code = data[0]

    if event_type_code == 1:
        # Key event
        event['type'] = 'key'
        event['state'] = data[1] == 1
        event['key'] = chr(data[2])

    elif event_type_code == 2:
        # Mouse button event
        event['type'] = 'mouse_button'
        event['state'] = data[1] == 1
        event['button'] = chr(data[2])

    elif event_type_code == 3:
        # Mouse move event
        event['type'] = 'mouse_move'
        event['to'] = {
            'x': bytes_to_signed_int(data[1], data[2]),
            'y': bytes_to_signed_int(data[3], data[4]),
        }

    elif event_type_code == 4:
        # Mouse relative event
        event['type'] = 'mouse_relative'
        event['squash'] = data[1] == 1
        event['delta'] = []
        for i in range(2, len(data), 2):
            event['delta'].append({
                'x': data[i],
                'y': data[i + 1],
            })

    elif event_type_code == 5:
        # Mouse wheel event
        event['type'] = 'mouse_wheel'
        event['squash'] = data[1] == 1
        event['delta'] = {
            'x': data[2],
            'y': data[3],
        }

    else:
        raise ValueError(f"Unknown event type code: {event_type_code}")

    return event

def replay_event(event):
    if event['type'] == 'key':
        key = KeyCode.from_char(event['key'])
        if event['state']:
            keyboard.press(key)
        else:
            keyboard.release(key)

    elif event['type'] == 'mouse_button':
        button = Button.left if event['button'] == 'L' else Button.right  # Adjust as needed for button labels
        if event['state']:
            mouse.press(button)
        else:
            mouse.release(button)

    elif event['type'] == 'mouse_move':
        pixel_x = int(scale_coordinate(event['to']['x'], screen_width))
        pixel_y = int(scale_coordinate(event['to']['y'], screen_height))
        print(pixel_x, pixel_y)
        mouse.position = (pixel_x, pixel_y)

    elif event['type'] == 'mouse_relative':
        for delta in event['delta']:
            mouse.move(delta['x'], delta['y'])

    elif event['type'] == 'mouse_wheel':
        # The actual library method is `scroll`; this might differ slightly
        mouse.scroll(event['delta']['x'], event['delta']['y'])