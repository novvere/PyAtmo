#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Send netatmo data to mqtt broker
#
import logging
import Netatmo
import time, json
import pprint
import paho.mqtt.publish as publish # sudo pip3 install paho-mqtt


def main():
    pp = pprint.PrettyPrinter(indent=4)
    
    #logging.basicConfig(level=logging.DEBUG)   # DEBUG level
    logging.basicConfig(level=logging.INFO)   # INFO level

    netatmo = Netatmo.Netatmo("PyAtmo.conf")
    
    logging.debug("getAccessToken")
    netatmo.getAccessToken()
    
    logging.debug("getHomesData")

    HomesData = netatmo.getHomesData()
    HomeStatus = netatmo.getHomeStatus()

    for room in HomeStatus["rooms"]:               
        topic = "netatmo/%s/%s/therm_measured_temperature" % (netatmo.home["name"], netatmo.getRoomName(room["id"])) 
        logging.debug("payload: " + str(room["therm_measured_temperature"]))
        publish.single(topic, room["therm_measured_temperature"], hostname=netatmo.config["mqtt"]["server"])
    
    
if __name__ == "__main__":
    main()
