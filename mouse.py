from AppKit import NSScreen

# Getting the main screen resolution using AppKit
screen_width = NSScreen.mainScreen().frame().size.width
screen_height = NSScreen.mainScreen().frame().size.height

def convert_to_pixel_coords(encoded_x, encoded_y, max_value=65535):
    x_ratio = screen_width / max_value
    y_ratio = screen_height / max_value

    pixel_x = int(encoded_x * x_ratio)
    pixel_y = int(encoded_y * y_ratio)

    return pixel_x, pixel_y