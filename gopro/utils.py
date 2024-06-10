### Using GoPro Official API package

import requests

def connect_wired_usb():
    url = "http://10.5.5.9:8080/gopro/camera/control/wired_usb"
    querystring = {"p":"1"} # 0:disabled, 1:enabled

    response = requests.request("GET", url, params=querystring)
    if response.status_code == 200:
        print('[+]Camera connected successfully')
        return True
    return False


def set_shutter():
    url = "http://10.5.5.9:8080/gopro/camera/control/wired_usb"
    response = requests.request("GET", url)
    if response.status_code == 200:
        print('[+]Camera connected successfully')
        return True
    return False

def turbo_transfer():
    pass

def keep_alive():
    """
    In order to maximize battery life, GoPro cameras automatically go to sleep after some time. This logic is handled by a combination of the Auto Power Down setting which most (but not all) cameras support and a Keep Alive message that the user can regularly send to the camera.

    The camera will automatically go to sleep if both timers reach zero.

    The Auto Power Down timer is reset when the user taps the LCD screen, presses a button on the camera, programmatically (un)sets the shutter, sets a setting, or loads a Preset.

    The Keep Alive timer is reset when the user sends a keep alive message.

    The best practice to prevent the camera from inadvertently going to sleep is to start sending Keep Alive messages every 3.0 seconds after a connection is established.
    """
    url = "http://10.5.5.9:8080/gopro/camera/keep_alive"
    response = requests.request("GET", url)
    if response.status_code == 200:
        return True
    return False


# if __name__ == '__main__':
#     connect_wired_usb()
