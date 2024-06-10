### Using GoPro Official SDK

import asyncio
from open_gopro import WirelessGoPro, Params

"""
NOTE(Connection): Connection to the camera via WiFi requires that the camera's WiFi Access Point be enabled.
This can be done by connecting to the camera via Bluetooth Low Energy and sending a 
command to enable AP Mode.

NOTE(SetCameraControl): In order to prevent undefined behavior between the camera and a connected app,
simultaneous use of the camera and a connected app is discouraged. 
A third party client should use the Set Camera Control Status command to tell the 
camera that the client wishes to claim control of the camera.
"""

async def main():
    async with WirelessGoPro() as gopro:
        ## Setting up connection over BLE via Bluetooth : Turn on Bluetooth
        ## Needed to establish other types of connection
        await gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
        await gopro.ble_setting.fps.set(Params.FPS.FPS_30)
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.ENABLE)
        await gopro.ble_command.set_shutter(shutter=Params.Toggle.DISABLE)
        ## Download the last captured file from the camera
        media = (await gopro.ble_command.get_last_captured_media()).data

        ## Connection: Must be enabled before user can connect via WIFI
        # await gopro.ble_command.enable_wifi_ap(enable=True)

        ## Authentication for WIFI connection
        SSID = gopro.ssid
        PASSWORD = gopro.password
        print(f'[+]Gopro Wifi Credentials:\n SSID: {SSID}\n PASSWORD: {PASSWORD}')
        # if gopro.connect_to_access_point(ssid=SSID, password=PASSWORD):
        #     print('[+]Wifi Authentication Successful')
        # else:
        #     print('[-]Wifi Authentication Failed')

        ## Setting up connection over HTTP via WIFI : Turn on wifi
        # await gopro.http_setting.resolution.set(Params.Resolution.RES_4K)
        # await gopro.http_setting.fps.set(Params.FPS.FPS_30)
        # await gopro.http_command.set_camera_control(mode=Params.CameraControl.EXTERNAL)
        # await gopro.http_command.set_shutter(shutter=Params.Toggle.ENABLE)
        # await gopro.http_command.set_shutter(shutter=Params.Toggle.DISABLE)
        # # Download the last captured file from the camera
        # media_list = (await gopro.http_command.get_last_captured_media()).data

        ## Setting up connection over HTTP via USB : Toggle connection 
        ## Only necessary for usb connections
        # await gopro.http_command.wired_usb_control(control=Params.Toggle.ENABLE)
        # await gopro.http_command.wired_usb_control(control=Params.Toggle.DISABLE)

        # Download the media captured
        await gopro.http_command.download_file(camera_file=media.filename)

asyncio.run(main())