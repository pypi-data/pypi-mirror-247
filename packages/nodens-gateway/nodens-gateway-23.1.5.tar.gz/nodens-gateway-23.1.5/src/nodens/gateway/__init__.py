# __init__.py

from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import yaml
from nodens.gateway import nodens_fns
from nodens.gateway import nodens_thingsboard as nodens_tb
from nodens.gateway import nodens_insight_hub as nodens_ih
import os
from platformdirs import user_config_dir, user_documents_dir
from pathlib import Path
import logging

global APPNAME
global APPAUTHOR
global CWD

# Logging level
# logging.basicConfig(
#     format='[%(asctime)s] [%(levelname)-8s] %(message)s',
#     level=logging.DEBUG,
#     datefmt='%Y-%m-%d %H:%M:%S')
# logging.basicConfig(level=logging.DEBUG)
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('nodens.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.info("INIT")


# Some information
__title__ = "nodens-gateway"
__version__ = "23.1.5"
__author__ = "Khalid Z Rajab"
__author_email__ = "khalid@nodens.eu"
__copyright__ = "Copyright (c) 2023 " + __author__
__license__ = "MIT"

APPNAME = "Gateway"
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
    def __init__(self, search_folders):
        ## ~~~~~~~ DEFAULT CONFIGURATION ~~~~~~~ ##
                
        # Program config #
        self.WRITE_FLAG = 0 # 1 = write data to local storage
        self.PRINT_FREQ = 120 # Connection info print frequency
        self.CLOUD_WRITE_TIME = 15 # Minimum time to wait before sending new data to Cloud (per sensor)

        # Sensor config #
        self.SENSOR_TOPIC = '#'
        self.SENSOR_IP = '10.3.141.1'
        self.SENSOR_PORT = 1883

        # SIEMENS INSIGHTS HUB config #
        self.ENABLE_SIEMENS_IH = 0
        self.IH_TENANT_ID = ''
        self.IH_CLIENT_ID = ''
        self.IH_CERT_DIR = ''
        self.IH_CA_CERT = 'MindSphereRootCA1.pem'
        self.IH_PUBLIC_CERT = "{}_{}.pem".format("(TENANT_ID)","(CLIENT_ID)")
        self.IH_PRIVATE_KEY = "{}_{}.key".format("(TENANT_ID)","(CLIENT_ID)")
        self.IH_HOST = "mindconnectmqtt.eu1.mindsphere.io"
        self.IH_PORT = 8883

        # THINGSBOARD config #
        self.ENABLE_THINGSBOARD = 0
        self.TB_PORT = 1883
        self.TB_HOST = "mqtt.thingsboard.cloud"
        self.TB_KEEPALIVE = 60
        self.TB_PUB_TOPIC = "v1/devices/me/telemetry"
        self.TB_ACCESS_TOKEN_FOLDER = ""
        self.TB_ACCESS_TOKEN_FILENAME = "thingsboard_access.json"


        #_cfg = tomllib.loads(resources.read_text("nodens.gateway", "config.toml"))
        # In future: replace resources.read_text with: files(package).joinpath(resource).read_text(encoding=encoding)
        logger.info("CWD: {}. APPAUTHOR: {}. platformdir: {}".format(CWD, APPAUTHOR, user_config_dir(APPNAME, APPAUTHOR)))
        i = 0
        while i < len(search_folders):
            if os.path.exists(search_folders[i]+"config-gateway.yaml"):
                yaml_file = search_folders[i]+"config-gateway.yaml"
                self.read_config(yaml_file)               
                logger.info("Config file found: {}".format(yaml_file))
                i = -1
                break
            i += 1
        # if os.path.exists(user_config_dir(APPNAME, APPAUTHOR)+"/config-gateway.yaml"):
        #     yaml_file = user_config_dir(APPNAME, APPAUTHOR)+"/config-gateway.yaml"
        #     self.read_config(yaml_file)
            
        #     logger.info("Config file found: {}".format(yaml_file))
        # elif os.path.exists(CWD+"config-gateway.yaml"):
        #     yaml_file = CWD+"config-gateway.yaml"
        #     self.read_config(yaml_file)

        #     logger.info("Config file found: {}".format(yaml_file)) 
        # elif os.path.exists(user_documents_dir()+"/NodeNs/config-gateway.yaml"):    
        #     yaml_file = user_documents_dir()+"/NodeNs/config-gateway.yaml"
        #     self.read_config(yaml_file)

        #     logger.info("Config file found: {}".format(yaml_file)) 
        # elif os.path.exists(user_documents_dir()+"/config-gateway.yaml"):    
        #     yaml_file = user_documents_dir()+"/config-gateway.yaml"
        #     self.read_config(yaml_file)

        #     logger.info("Config file found: {}".format(yaml_file)) 
        # else:
        if i > -1:
            yaml_file = user_config_dir(APPNAME, APPAUTHOR)+"/config-gateway.yaml"
            logger.warning("NO CONFIG FILE FOUND. DEFAULT PARAMETERS USED. CONFIG SAVED: {}".format(yaml_file))

            # Write new yaml config file
            Path(user_config_dir(APPNAME, APPAUTHOR)).mkdir(parents=True, exist_ok=True)
            make_config = {
                "Program": {
                    "WRITE_FLAG": self.WRITE_FLAG,
                    "PRINT_FREQ": self.PRINT_FREQ,
                    "CLOUD_WRITE_TIME": self.CLOUD_WRITE_TIME,
                },
                "Sensor": {
                    "SENSOR_TOPIC": self.SENSOR_TOPIC,
                    "SENSOR_IP": self.SENSOR_IP,
                    "SENSOR_PORT": self.SENSOR_PORT,
                },
                "INSIGHTS_HUB": {
                    "ENABLE_SIEMENS_IH": self.ENABLE_SIEMENS_IH,
                    "IH_TENANT_ID": self.IH_TENANT_ID,
                    "IH_CLIENT_ID": self.IH_CLIENT_ID,
                    "IH_CERT_DIR": self.IH_CERT_DIR,
                    "IH_CA_CERT": self.IH_CA_CERT,
                    "IH_PUBLIC_CERT": self.IH_PUBLIC_CERT,
                    "IH_PRIVATE_KEY": self.IH_PRIVATE_KEY,
                    "IH_HOST": self.IH_HOST,
                    "IH_PORT": self.IH_PORT,
                },
                "THINGSBOARD": {
                    "ENABLE_THINGSBOARD": self.ENABLE_THINGSBOARD,
                    "TB_PORT": self.TB_PORT,
                    "TB_HOST": self.TB_HOST,
                    "TB_KEEPALIVE": self.TB_KEEPALIVE,
                    "TB_PUB_TOPIC": self.TB_PUB_TOPIC,
                    "TB_ACCESS_TOKEN_FOLDER": self.TB_ACCESS_TOKEN_FOLDER,
                    "TB_ACCESS_TOKEN_FILENAME": self.TB_ACCESS_TOKEN_FILENAME,
                }
            }

            # Write config to yaml
            write_yaml(yaml_file, make_config)

    def read_config(self, file):
        # Read configs from yaml file
        _cfg = read_yaml(file)

        # Program config #
        self.WRITE_FLAG = int(_cfg["Program"]["WRITE_FLAG"])
        self.PRINT_FREQ = int(_cfg["Program"]["PRINT_FREQ"])
        self.CLOUD_WRITE_TIME = int(_cfg["Program"]["CLOUD_WRITE_TIME"])

        # Sensor config #
        self.SENSOR_TOPIC = _cfg["Sensor"]["SENSOR_TOPIC"]
        if not bool(self.SENSOR_TOPIC):
            self.SENSOR_TOPIC = '#'
        self.SENSOR_IP = _cfg["Sensor"]["SENSOR_IP"]
        self.SENSOR_PORT = int(_cfg["Sensor"]["SENSOR_PORT"])

        # INSIGHTS_HUB config #
        if "INSIGHTS_HUB" in _cfg:
            self.ENABLE_SIEMENS_IH = int(_cfg["INSIGHTS_HUB"]["ENABLE_SIEMENS_IH"])
            self.IH_TENANT_ID = _cfg["INSIGHTS_HUB"]["IH_TENANT_ID"]
            self.IH_CLIENT_ID = _cfg["INSIGHTS_HUB"]["IH_CLIENT_ID"]
            self.IH_CERT_FOLDER = _cfg["INSIGHTS_HUB"]["IH_CERT_DIR"]
            self.IH_CA_CERT = _cfg["INSIGHTS_HUB"]["IH_CA_CERT"]
            self.IH_PUBLIC_CERT = _cfg["INSIGHTS_HUB"]["IH_PUBLIC_CERT"]
            self.IH_PRIVATE_KEY = _cfg["INSIGHTS_HUB"]["IH_PRIVATE_KEY"]
            self.IH_HOST = _cfg["INSIGHTS_HUB"]["IH_HOST"]
            self.IH_PORT = int(_cfg["INSIGHTS_HUB"]["IH_PORT"])
        elif "MINDSPHERE" in _cfg:
            self.ENABLE_SIEMENS_IH = int(_cfg["MINDSPHERE"]["ENABLE_MS"])
        else:
            self.ENABLE_SIEMENS_IH = 0

        # THINGSBOARD config#
        self.ENABLE_THINGSBOARD = int(_cfg["THINGSBOARD"]["ENABLE_THINGSBOARD"])
        self.TB_PORT = int(_cfg["THINGSBOARD"]["TB_PORT"])
        self.TB_HOST = _cfg["THINGSBOARD"]["TB_HOST"]
        self.TB_KEEPALIVE = int(_cfg["THINGSBOARD"]["TB_KEEPALIVE"])
        self.TB_PUB_TOPIC = _cfg["THINGSBOARD"]["TB_PUB_TOPIC"]
        if "TB_ACCESS_TOKEN_FOLDER" in _cfg["THINGSBOARD"]:
            self.TB_ACCESS_TOKEN_FOLDER = _cfg["THINGSBOARD"]["TB_ACCESS_TOKEN_FOLDER"]
        else:
            self.TB_ACCESS_TOKEN_FOLDER = ""
        if "TB_ACCESS_TOKEN_FILENAME" in _cfg["THINGSBOARD"]:
            self.TB_ACCESS_TOKEN_FILENAME = _cfg["THINGSBOARD"]["TB_ACCESS_TOKEN_FILENAME"]
            if self.TB_ACCESS_TOKEN_FILENAME == "" or self.TB_ACCESS_TOKEN_FILENAME == None:
                self.TB_ACCESS_TOKEN_FILENAME = "thingsboard_access.json"
        else:
            self.TB_ACCESS_TOKEN_FILENAME = "thingsboard_access.json"

# Search folders
search_folders_configs = [user_config_dir(APPNAME, APPAUTHOR)+"/",
                  CWD+"/",
                  user_documents_dir()+"/NodeNs/",
                  user_documents_dir()+"/",]

search_folders_certs = [user_config_dir(APPNAME, APPAUTHOR)+"/certs/",
                  user_config_dir(APPNAME, APPAUTHOR)+"/",
                  CWD+"/certs/",
                  CWD+"/",
                  user_documents_dir()+"/certs/",
                  user_documents_dir()+"/",]

cp = config_program(search_folders_configs)

# Initialisations #
si = nodens_fns.si                  # Sensor info
ew = nodens_fns.EntryWays()         # Entryway monitors
oh = nodens_fns.OccupantHist()      # Occupant history
sm = nodens_fns.SensorMesh()        # Sensor Mesh state
message_pipeline = nodens_fns.MessagePipeline()

# Initialise Siemens Insight Hub
if cp.ENABLE_SIEMENS_IH == 1:
    flag_ih_cert = 1
    # Find CA cert
    if cp.IH_CERT_FOLDER != "" and cp.IH_CERT_FOLDER != None:
        if os.path.exists(cp.IH_CERT_FOLDER+"/"+cp.IH_CA_CERT):
            ih_ca_cert = cp.IH_CERT_FOLDER+"/"+cp.IH_CA_CERT
            logger.info("Insight Hub CA certificate found")
        else:
            logger.warning("Insight Hub CA certificate not found in designated folder. Searching other locations...")
    i = 0
    while i < len(search_folders_certs):
        if os.path.exists(search_folders_certs[i]+"/"+cp.IH_CA_CERT):
            ih_ca_cert = search_folders_certs[i]+"/"+cp.IH_CA_CERT
            logger.info("Insight Hub CA certificate found")
            i=-1
            break
        i += 1
    if i > -1:
        logger.error("\n\INSIGHT HUB: NO CA CERTIFICATES FOUND!\n\n")
        flag_ih_cert = 0

    # Find public certificate
    if cp.IH_CERT_FOLDER != "" and cp.IH_CERT_FOLDER != None:
        if os.path.exists(cp.IH_CERT_FOLDER+"/"+cp.IH_PUBLIC_CERT):
            ih_public_cert = cp.IH_CERT_FOLDER+"/"+cp.IH_PUBLIC_CERT
            logger.info("Insight Hub public certificate found")
        else:
            logger.warning("Insight Hub public certificate not found in designated folder. Searching other locations...")
    i = 0
    while i < len(search_folders_certs):
        if os.path.exists(search_folders_certs[i]+"/"+cp.IH_PUBLIC_CERT):
            ih_public_cert = search_folders_certs[i]+"/"+cp.IH_PUBLIC_CERT
            logger.info("Insight Hub public certificate found")
            i=-1
            break
        i += 1
    if i > -1:
        logger.error("\n\nINSIGHT HUB: NO public CERTIFICATES FOUND!\n\n")
        flag_ih_cert = 0

    # Find private key
    if cp.IH_CERT_FOLDER != "" and cp.IH_CERT_FOLDER != None:
        if os.path.exists(cp.IH_CERT_FOLDER+"/"+cp.IH_PRIVATE_KEY):
            ih_private_key = cp.IH_CERT_FOLDER+"/"+cp.IH_PRIVATE_KEY
            logger.info("Insight Hub CA certificate found")
        else:
            logger.warning("Insight Hub CA certificate not found in designated folder. Searching other locations...")
    i = 0
    while i < len(search_folders_certs):
        if os.path.exists(search_folders_certs[i]+"/"+cp.IH_PRIVATE_KEY):
            ih_private_key = search_folders_certs[i]+"/"+cp.IH_PRIVATE_KEY
            logger.info("Insight Hub CA certificate found")
            i=-1
            break
        i += 1
    if i > -1:
        logger.error("\n\nINSIGHT HUB: NO CA CERTIFICATES FOUND!\n\n")
        flag_ih_cert = 0

    # Connect to Insight Hub
    if flag_ih_cert == 1:
        send_mc = nodens_ih.sendMindConnect(ca_cert = ih_ca_cert, certfile = ih_public_cert, private_key_file = ih_private_key)
    else:
        logger.warning("Insight HUB disabled: certificates not found.")
        cp.ENABLE_SIEMENS_IH = 0


# Initialise Thingsboard
if cp.ENABLE_THINGSBOARD:
    if cp.TB_ACCESS_TOKEN_FOLDER != "" and cp.TB_ACCESS_TOKEN_FOLDER != None:
        if os.path.exists(cp.TB_ACCESS_TOKEN_FOLDER+"/"+cp.TB_ACCESS_TOKEN_FILENAME):
            nodens_tb.TB.get_sensors(cp.TB_ACCESS_TOKEN_FOLDER+"/"+cp.TB_ACCESS_TOKEN_FILENAME)
            logger.info("Thingsboard tokens found")
        else:
            logger.warning("Thingsboard tokens not found in designated folder. Searching other locations...")
    i = 0
    while i < len(search_folders_certs):
        if os.path.exists(search_folders_certs[i]+"/"+cp.TB_ACCESS_TOKEN_FILENAME):
            nodens_tb.TB.get_sensors(search_folders_certs[i]+"/"+cp.TB_ACCESS_TOKEN_FILENAME)
            logger.info("Thingsboard tokens found")
            i=-1
            break
        i += 1
    if i > -1:
        logger.error("\n\nTHINGSBOARD: NO ACCESS TOKENS FOUND. Please locate file: thingsboard_access.json.\n\n")