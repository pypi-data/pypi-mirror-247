# __init__.py

from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import yaml
from nodens.update import nodens_fns
import os
from platformdirs import user_config_dir
from pathlib import Path
import logging

global APPNAME
global APPAUTHOR
global CWD

# Logging level
logging.basicConfig(level=logging.DEBUG)

# Some information
__title__ = "nodens-update"
__version__ = "23.1.0"
__author__ = "Khalid Z Rajab"
__author_email__ = "khalid@nodens.eu"
__copyright__ = "Copyright (c) 2023 " + __author__
__license__ = "MIT"

APPNAME = "Update"
APPAUTHOR = "NodeNs"
CWD = os.getcwd() + '/'


# Read parameters from the config file
def read_yaml(file_path):
    with open(file_path, "r") as yaml_file:
        return yaml.safe_load(yaml_file)
    
# Write parameters to config file
def write_yaml(file_path, data):
    with open(file_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

class config_program:
    def __init__(self):
        ## ~~~~~~~ DEFAULT CONFIGURATION ~~~~~~~ ##
                
        # Sensor config #
        self.SENSOR_ROOT = '807d3abc9ba0'
        self.SENSOR_TARGET = self.SENSOR_ROOT
        self.SENSOR_IP = '10.3.141.1'
        self.SENSOR_PORT = 1883
        self.SENSOR_TOPIC = 'mesh/' + self.SENSOR_ROOT + '/toDevice'

        # Data transmit config #
        self.SCAN_TIME = 60 # Seconds between scans
        self.FULL_DATA_FLAG = 0 # 1 = Capture full-data for diagnostics
        self.FULL_DATA_TIME = 60 # Seconds between full-data captures

        # Radar config #
        self.RADAR_SEND_FLAG = 0 # 1 = Send radar config
        # Note: Sensor located at origin (X,Y) = (0,0). Z-axis is room height. By default, sensor points along Y-axis.
        self.ROOM_X_MIN = "-5"
        self.ROOM_X_MAX = "5"
        self.ROOM_Y_MIN = "0.25"
        self.ROOM_Y_MAX = "10"
        self.ROOM_Z_MIN = "-0.5"
        self.ROOM_Z_MAX = "2"
        # Static monitoring area
        self.MONITOR_X = str(float(self.ROOM_X_MIN) + 0.5) + "," + str(float(self.ROOM_X_MAX) - 0.5)
        self.MONITOR_Y = "0.5 ," + str(float(self.ROOM_Y_MAX) - 0.5)
        self.MONITOR_Z = "-0.5, 2" #str(self.ROOM_Z_MIN + 0.5) + "," + str(self.ROOM_Z_MAX - 0.5)
        # Notes on sensor orientation. 
        # Default: (Yaw,Pitch) = (0,0) which points along the Y-axis.
        # Units: degrees.
        # Yaw: rotation around Z-axis (side-to-side). Clockwise is +ve.
        # Pitch: rotation around X-axis (up-down). Upwards is +ve.
        self.SENSOR_YAW = 0
        self.SENSOR_PITCH = 0
        self.SENSITIVITY = 1
        self.OCC_SENSITIVITY = 1

        # Entry config #
        self.ENTRY_FLAG = 0
        self.ENTRY_X = []
        self.ENTRY_Y = []

        # In future: replace resources.read_text with: files(package).joinpath(resource).read_text(encoding=encoding)
        print("CWD: {}. APPAUTHOR: {}. platformdir: {}".format(CWD, APPAUTHOR, user_config_dir(APPNAME, APPAUTHOR)))
        if os.path.exists(user_config_dir(APPNAME, APPAUTHOR)+"/config-update.yaml"):
            yaml_file = user_config_dir(APPNAME, APPAUTHOR)+"/config-update.yaml"
            self.read_config(yaml_file)
            
            logging.info("Config file found: {}".format(yaml_file))
        elif os.path.exists(CWD+"config-update.yaml"):
            yaml_file = CWD+"config-update.yaml"
            self.read_config(yaml_file)

            logging.info("Config file found: {}".format(yaml_file))          
        else:
            yaml_file = user_config_dir(APPNAME, APPAUTHOR)+"/config-update.yaml"
            logging.warning("NO CONFIG FILE FOUND. DEFAULT PARAMETERS USED. CONFIG SAVED: {}".format(yaml_file))

            # Write new yaml config file
            Path(user_config_dir(APPNAME, APPAUTHOR)).mkdir(parents=True, exist_ok=True)
            make_config = {
                "SENSOR": {
                    "ROOT_ID": self.SENSOR_ROOT,
                    "SENSOR_ID": self.SENSOR_TARGET,
                    "SENSOR_IP": self.SENSOR_IP,
                    "SENSOR_PORT": self.SENSOR_PORT,
                },
                "DATA_TRANSMIT": {
                    "TRANSMIT_TIME": self.SCAN_TIME,
                    "FULL_DATA_FLAG": self.FULL_DATA_FLAG,
                    "FULL_DATA_TIME": self.FULL_DATA_TIME,
                },
                "RADAR": {
                    "RADAR_SEND_FLAG": self.RADAR_SEND_FLAG,
                    "ROOM_X_MIN": self.ROOM_X_MIN,
                    "ROOM_X_MAX": self.ROOM_X_MAX,
                    "ROOM_Y_MIN": self.ROOM_Y_MIN,
                    "ROOM_Y_MAX": self.ROOM_Y_MAX,
                    "ROOM_Z_MIN": self.ROOM_Z_MIN,
                    "ROOM_Z_MAX": self.ROOM_Z_MAX,
                    "MONITOR_X": self.MONITOR_X,
                    "MONITOR_Y": self.MONITOR_Y,
                    "MONITOR_Z": self.MONITOR_Z,
                    "SENSOR_YAW": self.SENSOR_YAW,
                    "SENSOR_PITCH": self.SENSOR_PITCH,
                    "SENSITIVITY": self.SENSITIVITY,
                    "OCC_SENSITIVITY": self.OCC_SENSITIVITY,
                },
                "ENTRYWAYS": {
                    "ENTRY_FLAG": self.ENTRY_FLAG,
                    "ENTRY_X": self.ENTRY_X,
                    "ENTRY_Y": self.ENTRY_Y,
                }
            }

            # Write config to yaml
            write_yaml(yaml_file, make_config)

    def read_config(self, file):
        # Read configs from yaml file
        _cfg = read_yaml(file)

        # sENSOR config #
        self.SENSOR_ROOT = (_cfg["SENSOR"]["ROOT_ID"])
        self.SENSOR_TARGET = (_cfg["SENSOR"]["SENSOR_ID"])
        self.SENSOR_IP = (_cfg["SENSOR"]["SENSOR_IP"])
        self.SENSOR_PORT = int(_cfg["SENSOR"]["SENSOR_PORT"])
        self.SENSOR_TOPIC = 'mesh/' + self.SENSOR_ROOT + '/toDevice'

        # Data transmit config #
        self.SCAN_TIME = float(_cfg["DATA_TRANSMIT"]["TRANSMIT_TIME"])
        self.FULL_DATA_FLAG = int(_cfg["DATA_TRANSMIT"]["FULL_DATA_FLAG"])
        self.FULL_DATA_TIME = float(_cfg["DATA_TRANSMIT"]["FULL_DATA_TIME"])

        # Radar config #
        self.RADAR_SEND_FLAG = int(_cfg["RADAR"]["RADAR_SEND_FLAG"])
        self.ROOM_X_MIN = float(_cfg["RADAR"]["ROOM_X_MIN"])
        self.ROOM_X_MAX = float(_cfg["RADAR"]["ROOM_X_MAX"])
        self.ROOM_Y_MIN = float(_cfg["RADAR"]["ROOM_Y_MIN"])
        self.ROOM_Y_MAX = float(_cfg["RADAR"]["ROOM_Y_MAX"])
        self.ROOM_Z_MIN = float(_cfg["RADAR"]["ROOM_Z_MIN"])
        self.ROOM_Z_MAX = float(_cfg["RADAR"]["ROOM_Z_MAX"])
        self.MONITOR_X = (_cfg["RADAR"]["MONITOR_X"])
        self.MONITOR_Y = (_cfg["RADAR"]["MONITOR_Y"])
        self.MONITOR_Z = (_cfg["RADAR"]["MONITOR_Z"])
        self.SENSOR_YAW = float(_cfg["RADAR"]["SENSOR_YAW"])
        self.SENSOR_PITCH = float(_cfg["RADAR"]["SENSOR_PITCH"])
        self.SENSITIVITY = (_cfg["RADAR"]["SENSITIVITY"])
        self.OCC_SENSITIVITY = (_cfg["RADAR"]["OCC_SENSITIVITY"])

        # Entryways config#
        self.ENTRY_FLAG = int(_cfg["ENTRYWAYS"]["ENTRY_FLAG"])
        self.ENTRY_X = (_cfg["ENTRYWAYS"]["ENTRY_X"])
        self.ENTRY_Y = (_cfg["ENTRYWAYS"]["ENTRY_Y"])

cp = config_program()

# Initialisations #
si = nodens_fns.si                  # Sensor info
ew = nodens_fns.EntryWays()         # Entryway monitors
oh = nodens_fns.OccupantHist()      # Occupant history
sm = nodens_fns.SensorMesh()        # Sensor Mesh state
