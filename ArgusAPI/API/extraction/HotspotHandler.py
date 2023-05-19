from .CommandHandler import CommandHandler
from . import DEPENDENCY_PATH
import threading

class HotspotHandler:
    """
    This class is used to...
    1. create the network interface
    2. Configure the interface
    3. Start the hotspot
    4. Stop the hotspot
    5. Remove the network interface
    6. Configure and manage the hotspot and the devices connected to it
    """

    physical_interface_name: str = None
    """
    The name of the physical network interface.
    """

    server_ip: str = "10.42.0.1"
    """
    This is the default IP that the Network Manager Assigns to our hotspot server
    """

    device_ip = "10.42.0.228"

    device_connected = False
    """
    Tells us if the device is conncted to the server
    """


    def __init__(self) -> None:
        pass

    def create_network_interface(self) -> None:
        """
        Creates the network interface for the hotspot if it doesn't exist.
        """
         # get the physical network interface name
        code, output = CommandHandler().executeCommand(["iw", "dev"])
        # only obtain the name of the device
        self.physical_interface_name = output.split()[2].strip()
        # create the hotspot
        code, output = CommandHandler().executeCommand(["nmcli", "dev", "wifi", "hotspot", "ifname", self.physical_interface_name, "con-name", "argusVnet", "ssid", "argusVnet", "password", "argusVnet"])

    def continue_if_connected(self) -> None:
        """
        Is a blocking function that is designed to only allow execution after it has detected a connection on the ip address using nmap
        """
        # FIrst we start a thread that will listen to the tcpdump and check if a device is connected
        # Then we start a thread that will ping the server and check if the ping is received
        threading.Thread(target=self.tcp_dump).start()
        while not self.device_connected:
            code, output = CommandHandler().executeCommand([DEPENDENCY_PATH+"adb", "shell", "ping", "-c", "1", self.server_ip])
        # This means the device is now connected
        return



    def tcp_dump(self):
        """
        This function will run a tcpdump on the server and check if a device is connected to the hotspot
        """
        print("lsdhfkisdhf")
        code, output = CommandHandler().executeCommand(["pkexec","tcpdump", "-i", self.physical_interface_name, "icmp", "-c", "1", "-v"])
        output = output.split()
        self.device_ip = output[17].strip()
        print(output, self.device_ip)
        self.device_connected = True
        
        
       
             
