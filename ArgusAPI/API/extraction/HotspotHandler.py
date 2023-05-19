from .CommandHandler import CommandHandler
from . import DEPENDENCY_PATH

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
        nm = nmap.PortScanner()
        # while True:
        #     nm.scan(self.server_ip+"/32", arguments='-vv -A -n')
        #     print(nm.all_hosts())
        
        
       
             
