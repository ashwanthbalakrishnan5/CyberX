from .CommandHandler import CommandHandler
from . import DEPENDENCY_PATH
import time

class WhatsappHandler:
    """
    This class will be able to extract all whatsapp messagea and media from a device and generate neat HTML records of it
    """

    command_handler = CommandHandler()

    def extract(self):
        # Step 1: Start the rooted emulator as a background process
        # self.command_handler.execute_as_bash("gnome-terminal ~/Android/Sdk/emulator/emulator -avd ArgusVDe")
        # Start listenting in adb to see if the emulator is online
        self.command_handler.executeCommand([DEPENDENCY_PATH+"adb", "-s" ,"emulator-5554", "wait-for-device"])
        time.sleep(2)
        # Make sure we uninstall whatsapp before we install it again
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s", "emulator-5554" ,"uninstall","com.whatsapp"])
        # Install the new whatsapp apk and also grant all permissions to reduce our workload
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s", "emulator-5554", "install " + DEPENDENCY_PATH + "whatsapp.apk", "-g"])
        # Start the whatsapp app
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s" ,"emulator-5554","shell", "am", "start", "-n", "com.whatsapp/com.whatsapp.Main"])
        # Wait for the app to start
        time.sleep(5)
        # Select the default english language
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s" ,"emulator-5554", "shell", "input" ,"touchscreen" ,"tap", "1280", "2880"])
        # Accept the rooted popup by pressing tab and then enter
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb" ,"-s", "emulator-5554", "shell" ,"input", "keyevent", "61"])
        time.time(1)
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s", "emulator-5554", "shell", "input" ,"keyevent", "66"])
        #Accept the terms and conditions
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s" ,"emulator-5554", "shell", "input" ,"touchscreen" ,"tap", "750", "2100"])
        # Get the phone number from the user
        phone_number = input("Please enter the phone number of the device you want to extract: ")
        # Enter the phone number into whatsapp
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s","emulator-5554", "shell", "input", "text " + phone_number])
        # ENter the area code
        self.command_handler.executeCommand([DEPENDENCY_PATH + "adb", "-s" ,"emulator-5554", "shell", "input", "touchscreen", "tap", "350" "750"])
        # Enter the tab command twice to get to the next button
        self.command_handler.executeCommand(DEPENDENCY_PATH + "adb -s emulator-5554 shell input keyevent 61")
        time.sleep(1)
        self.command_handler.executeCommand(DEPENDENCY_PATH + "adb -s emulator-5554 shell input keyevent 61")
        time.sleep(6)
        # tab to the okay button and accept that the number is correct
        self.command_handler.executeCommand(DEPENDENCY_PATH + "adb -s emulator-5554 shell input keyevent 61")
        time.sleep(1)
        #again tab
        self.command_handler.executeCommand(DEPENDENCY_PATH + "adb -s emulator-5554 shell input keyevent 61")
        time.sleep(1)
        # enter
        self.command_handler.executeCommand(DEPENDENCY_PATH + "adb -s emulator-5554 shell input keyevent 66")

