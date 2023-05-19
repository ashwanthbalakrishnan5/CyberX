from . import LOG_FILE_PATHS, ARTIFACTS_PATH
import os
import datetime
import random

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class LogHandler(metaclass=Singleton):
    """
    Used to generate and store text logs for the program.

    Is a singleton class.

    """

    session_number: int
    """
    The current session number.
    """

    log_file = None
    """
    The current log file for the active session
    """

    log_file_path: str = None
    """
    The path to the current log file
    """

    def __init__(self):
        """
        Initializes the log handler.
        """
        # check if the default log directory exists or else create the directory
        if not os.path.exists(LOG_FILE_PATHS):
            os.makedirs(LOG_FILE_PATHS)
        # Make the artifacts path
        if not os.path.exists(ARTIFACTS_PATH):
            os.makedirs(ARTIFACTS_PATH)
        # create the log file for this session
        self.session_number = random.randint(0, 1000000)
        # Create the file based on the current time
        self.log_file_path = LOG_FILE_PATHS + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".txt"
        self.log_file = open(self.log_file_path, "w+")
        self.generateHeader()

    def generateHeader(self):
        """
        Generates the header for the log file.
        """
        self.log_file.write("Argus Log File for Session " + str(self.session_number) + "\n\n")
        self.log_file.write("Session Start Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        self.log_file.write("--------------------------------------------------\n\n")
        self.log_file.flush()

    def logCommand(self, command: str, output: str):
        """
        Logs the command that was executed and its output.
        """
        self.log_file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + " ".join(command) + "\n")
        self.log_file.write("Output:\n")
        self.log_file.write(output)
        self.log_file.write("--------------------------------------------------\n")
        self.log_file.flush()

    def logMessage(self, message: str):
        """
        Logs the given message.
        """
        self.log_file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + message + "\n")
        self.log_file.write("--------------------------------------------------\n")
        self.log_file.flush()


    def logError(self, error: str):
        """
        Logs the given error.
        """
        self.log_file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + error + "\n")
        self.log_file.write("--------------------------------------------------\n")
        self.log_file.flush()