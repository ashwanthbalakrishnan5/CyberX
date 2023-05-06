# Sets up the current path that this module can be found at
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

DEPENDENCY_PATH = os.path.join(CURRENT_PATH, "dependencies")

LOG_FILE_PATHS = os.path.expanduser("~") + "/.argus/logs/"


