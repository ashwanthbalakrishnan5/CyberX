# Use type hinting in all suggestions

from typing import List, Dict
from . import DEPENDENCY_PATH, CommandHandler, LogHandler, ARTIFACTS_PATH, FILE_PATH
import time
import os
import shutil
import django
import sys
import nmap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ArgusAPI.settings')
django.setup()

from API.models import ADBStatus,Device
from ArgusAPI.settings import STORAGE_ROOT
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
        adb = ADBStatus.objects.create()
        adb.save()
        adbstatus = ADBStatus.objects.get(pk=1)
        # Keep listing out the devices that are connected till we detect one using 
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
                        adbstatus.connec_status = "Device Connected No Permission"
                        adbstatus.save()
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
                adbstatus.connec_status = "No Devices Connected"
                adbstatus.save()
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

    def disable_mobile_data(self):
        """
        Disables the mobile data of the device
        """
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "svc", "data", "disable"])


    def accept_install(self):
        """
        Accepts the install of the payload
        """
        time.sleep(1)
        #tab
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e", "shell", "input", "keyevent", "61"])
        time.sleep(1)
        #tab
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e","shell", "input", "keyevent", "61"])
        time.sleep(.5)
        #enter
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e","shell", "input", "keyevent", "66"])


    def get_contacts(self):
        """
        Gets the contacts from the device
        """
        #creates the temporary file that we ne
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb -e shell content query --uri content://contacts/phones/  --projection display_name:number:notes >> "+STORAGE_ROOT+"/data/contacts.txt"])
        LogHandler.LogHandler().logMessage("Contacts Obtained using adb")
        return output
    
    def get_calllogs(self):
        """
        Gets the Call logs from the file
        """
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb -e shell content query --uri content://call_log/calls/ --projection number:date:type:duration:name >> "+STORAGE_ROOT+"/data/calllog.txt"])
        LogHandler.LogHandler().logMessage("Call Logs Obtained using adb")
        return output
    
    def get_sms(self):
        """
        Gets the SMS from the device
        """
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb -e shell content query --uri content://sms/ --projection address:body:type:status:date >> "+STORAGE_ROOT+"/data/sms.txt"])
        LogHandler.LogHandler().logMessage("SMS Obtained using adb")
        return output
    
    def get_device_info(self):
        """
        Gets basic device info as soon as possible so that the front end can start displaying.
        The info is stored in .argus/artifacts/device_info.json
        """
        # Get the battery level
        code, battery_level = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "dumpsys", "battery"])
        index = battery_level.find("level:")+7
        battery_level = battery_level[index:index+2]
        vnet_status = "Active"
        # Get the android version of the device
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.build.version.release"])
        android_version = output.strip()
        # Get the device model
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.product.marketname"])
        device_model = output.strip()
        # Get the device manufacturer
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "shell", "getprop", "ro.product.brand"])
        device_manufacturer = output.strip()
        data_sync_status = "Syncing"
        # Get a screenshot of the home screen
        code, output = self.command_handler.execute_as_bash([DEPENDENCY_PATH+"adb exec-out screencap -p >> "+ARTIFACTS_PATH+"homescreen.png"])
        # create the json file and store it
        device_name = "Iphonee"
        device = Device.objects.create(
            device_name=device_name,
            vnet_status=vnet_status,
            battery_level=int(battery_level),
            android_version=int(android_version),
            device_model=device_model,
            device_manufacturer=device_manufacturer,
            screenshot=True
        )
        device.save()
        adbstatus = ADBStatus.objects.get(pk=1)
        adbstatus.connec_status = "Device Connected"
        adbstatus.save()
        # device_info = {"battery_level":battery_level, "vnet_status":vnet_status, "android_version":android_version, "device_model":device_model, "device_manufacturer":device_manufacturer, "data_sync_status":data_sync_status, "call_log": False, "contacts": False, "sms": False, "Files": False}
        # with open(ARTIFACTS_PATH+"device_info.json", "w") as f:
        #     json.dump(device_info, f)

    def get_files(self):
        """
        Gets all the files from the device and dump them in one location
        """
        # # Copies all photos from the DCIM folder
        #os.mkdir(ARTIFACTS_PATH="DCIM/")
        # code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e", "pull", "/sdcard/DCIM", ARTIFACTS_PATH+"DCIM"])
        # LogHandler.LogHandler().logMessage("Photos from DCIM directory have been copied to local device")
        # Copies all files from Pictures folder
        if not os.path.exists(ARTIFACTS_PATH+"Pictures/"):
            os.mkdir(ARTIFACTS_PATH+"Pictures/")
        code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e","pull", "/sdcard/Pictures", ARTIFACTS_PATH+"/files/"])
        LogHandler.LogHandler().logMessage("Photos from Pictures directory have been copied to local device")
        # #Copies all the files from whatsapp media folder
        # os.mkdir(ARTIFACTS_PATH="Whatsapp/")
        # code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-e", "pull", "/sdcard/Android/Media/com.whatsapp/WhatsApp/Media/", ARTIFCATS_PATH+"Whatsapp"])
        # LogHandler.LogHandler().logMessage("Photos from Whatsapp directory have been copied to local device")
        # Now we walk over all files and store them in one our django files directory
        for root, dirs, files in os.walk(ARTIFACTS_PATH):
            for file in files:
                try:
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(STORAGE_ROOT+"/files/", file)
                    shutil.copy2(src_path, dst_path)  
                except:
                    pass
                

        


        




