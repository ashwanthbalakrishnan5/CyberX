import extraction.AdbHandler
import time

# start the adb server
adb_handler = extraction.AdbHandler.AdbHandler()
adb_handler.start_server()
time.sleep(2)
# notify if a device is connected
adb_handler.notify_if_device_connected(lambda x: print(x))