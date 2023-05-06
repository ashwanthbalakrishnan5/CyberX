# Use type hinting in all suggestions

from typing import List, Dict
from extraction import DEPENDENCY_PATH, CommandHandler, LogHandler
import subprocess
import threading
import time

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
        subprocess.run(DEPENDENCY_PATH+"/adb kill-server")
        self.server_running = False

    def start_server(self):
        """
        Starts the ADB Server
        """
        self.command_handler.executeCommand([DEPENDENCY_PATH+"/adb", "start-server"])
        self.server_running = True

    def notify_if_device_connected(self, callback):
        """
        Notifies the callback function when a device is connected.
        Will return a warning if multiple devices are connected.
        Runs on its own thread
        """
        threading.Thread(target=self.__notify_if_device_connected, args=(callback,)).start()


    def __notify_if_device_connected(self, callback):
        # Keep listing out the devices that are connected till we detect one
        while True:
            code, output = self.command_handler.executeCommand([DEPENDENCY_PATH+"/adb", "devices"])
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
                        callback("Device Connected No Permission")
                        time.sleep(2)
                        continue
                    #notify the callback
                    LogHandler.LogHandler().logMessage("Detected ADB device with id: "+output[0])
                    callback("Device Connected")
                    break
                else:
                    LogHandler.LogHandler().logMessage("Detected Multiple Devices, using only the first one with id "+output[0])
                    callback("Multiple Devices Connected")
                    break
            else:
                callback("No Devices Connected")
            time.sleep(2)


