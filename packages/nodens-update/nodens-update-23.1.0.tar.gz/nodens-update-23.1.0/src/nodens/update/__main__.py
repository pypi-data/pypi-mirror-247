# __main__.py

import sys
import logging
from pathlib import Path
from datetime import datetime as dt
from time import sleep as sleep

import nodens.update as nodens
from nodens.update  import nodens_fns, nodens_mesh, nodens_quick_serv

def main():
    """The main NodeNs script"""

    ###############################################################################
    # Main script
    # Create the main window

    # Logging #
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting NodeNs sensor update. Version = {}".format(nodens.__version__))

    class SendMQTTUpdate():
        def __init__(self):
            # Get time
            
        
            #######################################
            # Connect to sensor mesh MQTT

            logging.debug("Mesh. sensor ip = {}. sensor port = {}. sensor topic = {}.".format(nodens.cp.SENSOR_IP,
                                                                                              nodens.cp.SENSOR_PORT, 
                                                                                              nodens.cp.SENSOR_TOPIC))
            print("HERE")
            nodens_mesh.MESH.end()
            nodens_mesh.MESH.connect(nodens.cp.SENSOR_IP,
                                     nodens.cp.SENSOR_PORT,
                                     60,
                                     "#",
                                     nodens_quick_serv.on_message_quick)   

            print("Connected to mesh")
            sleep(1)
            (payload,nodens_fns.rcp,nodens.ew) = nodens_fns.parse_config(nodens.ew,nodens.cp)
            print(payload)
            

            nodens_mesh.MESH.multiline_payload(nodens.cp.SENSOR_IP,
                                               nodens.cp.SENSOR_PORT,
                                               60, 
                                               nodens.cp.SENSOR_TOPIC,
                                               nodens_quick_serv.on_message_quick, 
                                               payload)

    SendMQTTUpdate()




if __name__ == "__main__":
    main()