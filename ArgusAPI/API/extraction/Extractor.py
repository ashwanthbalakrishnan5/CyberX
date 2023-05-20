from . import AdbHandler, HotspotHandler, LogHandler
import time
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from ArgusAPI.settings import STORAGE_ROOT

def execute_script(x: str, adb_handler: AdbHandler.AdbHandler):
    """
    This function executes as if its a script. Ashwanth you can move this to a file and run it as a script
    in any way you like mp  
    """
    if (x == "Device Connected"):
        # start the hotspot
        hotspothandler = HotspotHandler.HotspotHandler()
        hotspothandler.create_network_interface()
        adb_handler.send_wifi_payload()
        adb_handler.disable_mobile_data()
        adb_handler.connect_to_wifi()
        time.sleep(1)
        # Keep on checking if a device is connected to the hotspot by pinging the server from teh device
        # and checking by using tcpdump if we received the ping
        hotspothandler.continue_if_connected()
        # send a go to home action to close the app on screen
        adb_handler.go_home()
        # sleep for just 5 seconds so that the home screen is cleared away
        time.sleep(5)
        # Get Basic Device Info so that UI can start running
        adb_handler.get_device_info()
        # switch over to wireless debugging
        adb_handler.switch_to_wifi_debugging(hotspothandler.device_ip)
        # Get data from the device
        adb_handler.get_contacts()
        adb_handler.get_calllogs()
        adb_handler.get_sms()
        # Move the sms and callogs dumps
        LogHandler.LogHandler().logMessage("All data synced")


def start_payload():
    # start the adb server
    adb_handler = AdbHandler.AdbHandler()
    adb_handler.stop_server()
    adb_handler.start_server()
    time.sleep(1)
    # adb_handler.get_files()
    # notify if a device is connected
    print("start payload")
    adb_handler.notify_if_device_connected(execute_script, adb_handler)
    print("end payload")
    # return {"key": "value"}
    return adb_handler


