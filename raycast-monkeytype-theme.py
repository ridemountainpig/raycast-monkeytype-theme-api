import json


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')

    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])

    # Convert the hex string to RGB tuple
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb_color


def calculate_luminance(rgb_color):
    # Convert RGB to linear RGB
    linear_rgb = [channel / 255.0 for channel in rgb_color]

    # Apply sRGB gamma correction
    linear_rgb = [channel / 12.92 if channel <=
                  0.03928 else ((channel + 0.055) / 1.055) ** 2.4 for channel in linear_rgb]

    # Calculate luminance
    luminance = 0.2126 * linear_rgb[0] + 0.7152 * \
        linear_rgb[1] + 0.0722 * linear_rgb[2]
    return luminance


def is_light_or_dark(hex_color):
    rgb_color = hex_to_rgb(hex_color)
    luminance = calculate_luminance(rgb_color)

    # A luminance threshold of 0.5 is used to determine if the color is light or dark
    if luminance > 0.5:
        return "light"
    else:
        return "dark"


def get_monkeytype_theme():
    with open('monkeytype-theme.json') as f:
        theme = json.load(f)
    return theme


def generate_raycast_monkeytype_theme():
    themes = get_monkeytype_theme()
    raycast_monkeytype_theme = []
    for theme in themes:
        color_string = f"{theme['bgColor']},{theme['bgColor']},{theme['subColor']},{theme['mainColor']},{theme['subAltColor']},%23F50A0A,%23F5600A,%23E0A200,%2307BA65,%230A7FF5,%23470AF5,%23F50AA3"
        raycast_theme = {}
        raycast_theme['name'] = theme['name'].split('_')
        for i in range(len(raycast_theme['name'])):
            raycast_theme['name'][i] = raycast_theme['name'][i].capitalize()
        raycast_theme['name'] = ' '.join(raycast_theme['name'])
        raycast_theme['appearance'] = is_light_or_dark(theme['bgColor'])
        raycast_theme['colors'] = {
            'background': theme['bgColor'],
            'text': theme['subColor'],
            'selection': theme['mainColor'],
            'loader': theme['subAltColor'],
        }

        theme_url = f"https://themes.ray.so?version=1&name={raycast_theme['name'].replace(' ', '%20')}&author=Yen%20Cheng&authorUsername=ridemountainpig&colors={color_string.replace('#', '%23')}"
        raycast_theme['ray.so.light.url'] = f"{theme_url}&appearance=light"
        raycast_theme['ray.so.add.light.url'] = f"{raycast_theme['ray.so.light.url']}&addToRaycast"
        raycast_theme['ray.so.dark.url'] = f"{theme_url}&appearance=dark"
        raycast_theme['ray.so.add.dark.url'] = f"{raycast_theme['ray.so.dark.url']}&addToRaycast"
        raycast_monkeytype_theme.append(raycast_theme)

    with open('raycast-monkeytype-theme.json', 'w') as f:
        json.dump(raycast_monkeytype_theme, f, indent=4)


generate_raycast_monkeytype_theme()
