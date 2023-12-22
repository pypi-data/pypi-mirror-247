# __main__.py

import sys
import logging
from pathlib import Path
from datetime import datetime as dt
from time import sleep as sleep
import threading
import concurrent.futures

import nodens.gateway as nodens
from nodens.gateway import nodens_fns, nodens_mesh, nodens_serv, nodens_thingsboard


def sensor_thread(pipeline_thingsboard,pipeline_insight_hub):
    #def __init__(self):
    # Get time
    T0 = dt.utcnow()
    

    #######################################
    # Connect to sensor mesh MQTT

    logger.debug("Mesh. sensor ip = {}. sensor port = {}. sensor topic = {}.".format(nodens.cp.SENSOR_IP,
                                                                                        nodens.cp.SENSOR_PORT, 
                                                                                        nodens.cp.SENSOR_TOPIC))
    nodens_mesh.MESH.end()
    nodens_mesh.MESH.connect(nodens.cp.SENSOR_IP,
                                nodens.cp.SENSOR_PORT,
                                60,
                                nodens.cp.SENSOR_TOPIC,
                                nodens_serv.on_message_sensorN)   

    logger.info("Connected to mesh")
    
    while 1:
        sleep(0.1)

        # Check message pipeline for messages to send
        idx = [i for i,val in enumerate(nodens.message_pipeline.flag_send) if val == 1]
        for i in range(len(idx)):

            if nodens.cp.ENABLE_THINGSBOARD:
                pipeline_thingsboard.set_message(nodens.message_pipeline.message[idx[i]], "Producer")

            if nodens.cp.ENABLE_SIEMENS_IH:
                pipeline_insight_hub.set_message(nodens.message_pipeline.message[idx[i]], "Producer")

            nodens.message_pipeline.clear(idx[i])


        if nodens_mesh.MESH.client.connect_status == 0:
            logger.debug("MESH: Time to reconnect")
            nodens_mesh.MESH.end()
            nodens_mesh.MESH.connect(nodens.cp.SENSOR_IP,
                                        nodens.cp.SENSOR_PORT,
                                        60,
                                        nodens.cp.SENSOR_TOPIC,
                                        nodens_serv.on_message_sensorN)  
            
    logger.info("EXIT WHILE LOOP")

#     #RunMQTT()

def thingsboard_thread(pipeline):
    """Function to trigger publish to Thingsboard Cloud service"""
    logger.info("Pipeline to Thingsboard connected")
    while 1:
        message = pipeline.get_message("Consumer")
    #sleep(0.1)
        nodens_thingsboard.TB.prepare_data(message)
        nodens_thingsboard.TB.multiline_payload(message['addr'])

def insights_hub_thread(pipeline):
    """Function to trigger publish to Thingsboard Cloud service"""
    logger.info("Pipeline to Siemens Insights Hub connected")
    while 1:
        message = pipeline.get_message("Consumer")

        nodens.send_mc.send_mindconnect_payload(mqtt_data=message, sensor_data='')

class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    From example: https://realpython.com/intro-to-python-threading/#producer-consumer-threading
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        return message

    def set_message(self, message, name):
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()


if __name__ == "__main__":
    print("Start main 2")
    # Logging #
    # logging.basicConfig(
    #     format='%(asctime)s %(levelname)-8s %(message)s',
    #     level=logging.DEBUG,
    #     datefmt='%Y-%m-%d %H:%M:%S')
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

    logger.info('Starting NodeNs gateway. Version = {}'.format(nodens.__version__))
    


    pipeline_thingsboard = Pipeline()
    pipeline_insight_hub = Pipeline()
    
    thread_sensors = threading.Thread(target=sensor_thread, args=(pipeline_thingsboard,pipeline_insight_hub,), daemon=True)
    thread_thingsboard = threading.Thread(target=thingsboard_thread, args=(pipeline_thingsboard,), daemon=True)
    thread_insights_hub = threading.Thread(target=insights_hub_thread, args=(pipeline_insight_hub,), daemon=True)

    thread_sensors.start()
    if nodens.cp.ENABLE_THINGSBOARD:
        thread_thingsboard.start()
    if nodens.cp.ENABLE_SIEMENS_IH:
        nodens.send_mc.connect_to_mindconnect()
        thread_insights_hub.start()

    while True:
        sleep(1)
