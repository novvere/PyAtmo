#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Test Netatmo  class
#
import logging
import Netatmo
import time, json
import pprint
from colored import fg, bg, attr # sudo pip3 install colored

def main():
    pp = pprint.PrettyPrinter(indent=4)
    
    #logging.basicConfig(level=logging.DEBUG)   # DEBUG level
    logging.basicConfig(level=logging.INFO)   # INFO level

    netatmo = Netatmo.Netatmo("PyAtmo.conf")
    
    logging.info("getAccessToken")
    netatmo.getAccessToken()
    
    logging.info("getHomesData")
    HomesData = netatmo.getHomesData()

    logging.info("getHomesData() modules:")
    for module in HomesData["modules"]:
        #pp.pprint(module)
        print ('%s%s# MAC id %s %s' % (fg('blue'), attr('bold'), module["id"], attr('reset')))

        print("\tname: " + module["name"])
        type = str(module["type"])
        print("\ttype: " + module["type"])
        
        #print("\tsetup_date: " + str(module["setup_date"]))
        epoch = module["setup_date"]   # 1490157520.05
        date = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
        print("\tsetup_date: " + str(date))

        
        if 'room_id' in module:
            print("\troom_id: " + str(module["room_id"]))
            
        # modules_bridged
        if 'bridge' in module:
            print("\tbridge: " + str(module["bridge"]))            
        
        # modules_bridged
        if 'modules_bridged' in module:
            print("\tmodules_bridged: " + str(module["modules_bridged"]))            
        print("\n")

    print("")
    logging.info("getHomesData() rooms:")
    rooms = HomesData["rooms"]
    
    rooms2 = []
    for room in rooms:
        #pp.pprint(room)
        if 'module_ids' in room:
            print("# room id:" + room["id"] + "#")
            print("\tname: " + room["name"])
            print("\ttype: " + room["type"])
            print("\tmodule_ids: " + str(room["module_ids"]))
            print("\n")
            room_id = int(room["id"])
            room_name = room["name"]
    
    
    ##################################################
    logging.info("getHomeStatus")
    HomeStatus = netatmo.getHomeStatus()

    #pp.pprint(HomeStatus["modules"])
    #print(HomeStatus["modules"])
    
    for module in HomeStatus["modules"]:
        #print("# MAC id" + module["id"] + "#")
        print ('%s%s# MAC id %s %s' % (fg('blue'), attr('bold'), module["id"], attr('reset')))
        '''
        NATherm1 = thermostat
        NRV = valve
        NAPlug = relay
        NACamera = welcome camera
        NOC = presence camera
        '''
        type = str(module["type"])
        print("\ttype: " + module["type"])
        
        if 'anticipating' in module:
            print("\tanticipating: " + str(module["anticipating"]))
        if 'boiler_status' in module:
            print("\tboiler_status: " + str(module["boiler_status"]))
        if 'boiler_valve_comfort_boost' in module:
            print("\tboiler_valve_comfort_boost: " + str(module["boiler_valve_comfort_boost"]))
        if 'firmware_revision' in module:
            print("\tfirmware_revision: " + str(module["firmware_revision"]))
        if 'battery_state' in module:
            print("\tbattery_state: " + str(module["battery_state"]))
        if 'battery_level' in module:
            print("\tbattery_level: " + str(module["battery_level"]))
        if 'rf_strength' in module:
            print("\trf_strength: " + str(module["rf_strength"]))
        if 'wifi_strength' in module:
            print("\twifi_strength: " + str(module["wifi_strength"]))
        if 'reachable' in module:
            print("\treachable: " + str(module["reachable"]))
            # Check if module reachable
            if (module["reachable"]== False):
                print ('%s%s \tUnreachable %s' % (fg('red'), attr('bold'), attr('reset')))
            else:
                print ('%s%s \tReachable %s' % (fg('green'), attr('bold'), attr('reset')))
    
    print("\n")
    '''
    print("HomesData rooms")
    pp.pprint(rooms)
    '''
    print("HomeStatus rooms")
    #pp.pprint(HomeStatus["rooms"])
    for room in HomeStatus["rooms"]:
        print("# room id: " + room["id"] + " #")
        room_id = room["id"]
        if 'therm_measured_temperature' in room:
            print("\ttherm_measured_temperature: " + str(room["therm_measured_temperature"]))
        if 'therm_setpoint_temperature' in room:
            print("\ttherm_setpoint_temperature: " + str(room["therm_setpoint_temperature"]))
        if 'heating_power_request' in room:
            print("\theating_power_request: " + str(room["heating_power_request"]))
        if 'anticipating' in room:
            print("\tanticipating: " + str(room["anticipating"]))
        if 'open_window' in room:
            print("\topen_window: " + str(room["open_window"]))
            print("\n")
    
    
if __name__ == "__main__":
    main()
