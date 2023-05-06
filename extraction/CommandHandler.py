
from extraction.LogHandler import LogHandler
import subprocess
from typing import List, Tuple


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class CommandHandler(metaclass=Singleton):
    """
    Deals with execution of commands, logging info dealing with commands
    and setting up the proper environment to execute commands.

    Is a singleton class.

    """

    log_handler = None
    """
    The log handler for the program.
    """
    

    def __init__(self):
        """
        Initializes the command handler.
        """
        #create an instance of the loghandler
        self.log_handler = LogHandler()

    def executeCommand(self, command: List[str]) -> Tuple[int, str]:
        """
        Executes the given command and returns the process object.

        :param command: The command to execute
        :return: process Return code and output of the commandq
        """

        process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
        output = process.communicate()[0]
        self.log_handler.logCommand(command, output)
        return process.returncode, output

