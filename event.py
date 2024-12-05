from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from pynput.mouse import Controller as MouseController, Button
from AppKit import NSScreen
from utils import two_bytes_to_signed_int, byte_to_signed_int

# Getting the main screen resolution using AppKit
screen_width = NSScreen.mainScreen().frame().size.width
screen_height = NSScreen.mainScreen().frame().size.height

keyboard = KeyboardController()
mouse = MouseController()

def scale_coordinate(value, max_value):
    # Scale from the range -32768 to 32767 to 0 to max_value
    return (value + 32768) * max_value / 65535

def get_pynput_key(key_code):
    # Dictionary for extensive key mappings
    key_mapping = {
        "KeyA": KeyCode.from_char('a'),
        "KeyB": KeyCode.from_char('b'),
        "KeyC": KeyCode.from_char('c'),
        "KeyD": KeyCode.from_char('d'),
        "KeyE": KeyCode.from_char('e'),
        "KeyF": KeyCode.from_char('f'),
        "KeyG": KeyCode.from_char('g'),
        "KeyH": KeyCode.from_char('h'),
        "KeyI": KeyCode.from_char('i'),
        "KeyJ": KeyCode.from_char('j'),
        "KeyK": KeyCode.from_char('k'),
        "KeyL": KeyCode.from_char('l'),
        "KeyM": KeyCode.from_char('m'),
        "KeyN": KeyCode.from_char('n'),
        "KeyO": KeyCode.from_char('o'),
        "KeyP": KeyCode.from_char('p'),
        "KeyQ": KeyCode.from_char('q'),
        "KeyR": KeyCode.from_char('r'),
        "KeyS": KeyCode.from_char('s'),
        "KeyT": KeyCode.from_char('t'),
        "KeyU": KeyCode.from_char('u'),
        "KeyV": KeyCode.from_char('v'),
        "KeyW": KeyCode.from_char('w'),
        "KeyX": KeyCode.from_char('x'),
        "KeyY": KeyCode.from_char('y'),
        "KeyZ": KeyCode.from_char('z'),
        "Digit0": KeyCode.from_char('0'),
        "Digit1": KeyCode.from_char('1'),
        "Digit2": KeyCode.from_char('2'),
        "Digit3": KeyCode.from_char('3'),
        "Digit4": KeyCode.from_char('4'),
        "Digit5": KeyCode.from_char('5'),
        "Digit6": KeyCode.from_char('6'),
        "Digit7": KeyCode.from_char('7'),
        "Digit8": KeyCode.from_char('8'),
        "Digit9": KeyCode.from_char('9'),
        "Enter": Key.enter,
        "Escape": Key.esc,
        "Backspace": Key.backspace,
        "Tab": Key.tab,
        "Space": Key.space,
        "Minus": KeyCode.from_char('-'),
        "Equal": KeyCode.from_char('='),
        "BracketLeft": KeyCode.from_char('['),
        "BracketRight": KeyCode.from_char(']'),
        "Backslash": KeyCode.from_char('\\'),
        "Semicolon": KeyCode.from_char(';'),
        "Quote": KeyCode.from_char('\''),
        "Backquote": KeyCode.from_char('`'),
        "Comma": KeyCode.from_char(','),
        "Period": KeyCode.from_char('.'),
        "Slash": KeyCode.from_char('/'),
        "CapsLock": Key.caps_lock,
        "F1": Key.f1,
        "F2": Key.f2,
        "F3": Key.f3,
        "F4": Key.f4,
        "F5": Key.f5,
        "F6": Key.f6,
        "F7": Key.f7,
        "F8": Key.f8,
        "F9": Key.f9,
        "F10": Key.f10,
        "F11": Key.f11,
        "F12": Key.f12,
        # "PrintScreen": Key.print_screen,
        "ScrollLock": Key.scroll_lock,
        "Pause": Key.pause,
        "Insert": Key.insert,
        "Home": Key.home,
        "PageUp": Key.page_up,
        "Delete": Key.delete,
        "End": Key.end,
        "PageDown": Key.page_down,
        "ArrowRight": Key.right,
        "ArrowLeft": Key.left,
        "ArrowDown": Key.down,
        "ArrowUp": Key.up,
        "NumLock": Key.num_lock,
        "NumpadDivide": KeyCode.from_char('/'),
        "NumpadMultiply": KeyCode.from_char('*'),
        "NumpadSubtract": KeyCode.from_char('-'),
        "NumpadAdd": KeyCode.from_char('+'),
        "NumpadEnter": Key.enter,
        "Numpad1": KeyCode.from_char('1'),
        "Numpad2": KeyCode.from_char('2'),
        "Numpad3": KeyCode.from_char('3'),
        "Numpad4": KeyCode.from_char('4'),
        "Numpad5": KeyCode.from_char('5'),
        "Numpad6": KeyCode.from_char('6'),
        "Numpad7": KeyCode.from_char('7'),
        "Numpad8": KeyCode.from_char('8'),
        "Numpad9": KeyCode.from_char('9'),
        "Numpad0": KeyCode.from_char('0'),
        "NumpadDecimal": KeyCode.from_char('.'),
        "ShiftLeft": Key.shift,
        "ShiftRight": Key.shift_r,
        "ControlLeft": Key.ctrl,
        "ControlRight": Key.ctrl_r,
        "AltLeft": Key.alt,
        "AltRight": Key.alt_r,
        "MetaLeft": Key.cmd,
        "MetaRight": Key.cmd_r,
        # Add more if needed, depending on your specific requirements
    }

    return key_mapping.get(key_code, None)

def decode_hid_event(data):
    event = {}
    event_type_code = data[0]

    if event_type_code == 1:
        # Key event
        key = data[2:].decode('utf-8')
        if key is None:
            return
        print(key)
        event['type'] = 'key'
        event['state'] = data[1] == 1
        event['key'] = key

    elif event_type_code == 2:
        # Mouse button event
        event['type'] = 'mouse_button'
        event['state'] = data[1] == 1
        event['button'] = chr(data[2])

    elif event_type_code == 3:
        # Mouse move event
        event['type'] = 'mouse_move'
        event['to'] = {
            'x': two_bytes_to_signed_int(data[1], data[2]),
            'y': two_bytes_to_signed_int(data[3], data[4]),
        }

    # elif event_type_code == 4:
    #     # Mouse relative event
    #     event['type'] = 'mouse_relative'
    #     event['squash'] = data[1] == 1
    #     event['delta'] = []
    #     for i in range(2, len(data), 2):
    #         event['delta'].append({
    #             'x': byte_to_signed_int(data[i]),
    #             'y': byte_to_signed_int(data[i + 1]),
    #         })

    elif event_type_code == 5:
        # Mouse wheel event
        event['type'] = 'mouse_wheel'
        event['squash'] = data[1] == 1
        event['delta'] = {
            'x': byte_to_signed_int(data[2]),
            'y': byte_to_signed_int(data[3]),
        }

    else:
        raise ValueError(f"Unknown event type code: {event_type_code}")

    return event

def replay_event(event):
    if event['type'] == 'key':
        key = get_pynput_key(event['key'])
        if event['state']:
            keyboard.press(key)
        else:
            keyboard.release(key)

    elif event['type'] == 'mouse_button':
        button = Button.left if event['button'] == 'l' else Button.right  # Adjust as needed for button labels
        if event['state']:
            mouse.press(button)
        else:
            mouse.release(button)

    elif event['type'] == 'mouse_move':
        pixel_x = int(scale_coordinate(event['to']['x'], screen_width))
        pixel_y = int(scale_coordinate(event['to']['y'], screen_height))
        mouse.position = (pixel_x, pixel_y)

    # elif event['type'] == 'mouse_relative':
    #     for delta in event['delta']:
    #         mouse.move(delta['x'], delta['y'])

    elif event['type'] == 'mouse_wheel':
        # The actual library method is `scroll`; this might differ slightly
        mouse.scroll(event['delta']['x'], event['delta']['y'])