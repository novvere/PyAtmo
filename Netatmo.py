import os
import configparser
import requests
import logging
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Netatmo:
    commands = {"HomesData",      
                "HomeStatus",
                "Setthermmode", 
                "Setroomthermpoint", 
                "Getroommeasure", 
                "Switchhomeschedule", 
                "Synchomeschedule", 
                "Createnewhomeschedule", 
                "Deletehomeschedule", 
                "Renamehomeschedule "}

    baseUrl ="https://api.netatmo.com/api/"

    def __init__(self, configFile):        
        self.accessToken = None
        self.refreshToken = None
        self.home = None
        self.modules = None
        self.rooms = None
        self.home_id = None
        self.config = configparser.ConfigParser()
        self.configFilePath=configFile
        self.loadConfigFile(self.configFilePath)


    '''
    NATherm1 = thermostat
    NRV = valve
    NAPlug = relay
    NACamera = welcome camera
    NOC = pr
    '''
    def NAtypes(argument):
        switcher = {
            'NATherm1': 'thermostat',
            'NRV': 'valve',
            'NAPlug': 'relay',
            'NACamera': 'welcome camera',
            'NOC': 'pr'
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "Invalid type")
           
    def loadConfigFile(self, configPath):
        if(os.path.isfile('./'+configPath)):
            logging.info("Loading config from "+configPath)
        else:
            logging.error("Can't load config from "+configPath)
            exit(1)
        self.config.read(configPath)

    def writeConfigFile(self, configPath):
        logging.info("Writing config to "+configPath)
        with open(configPath, 'w') as outputFile:
            self.config.write(outputFile)

    def getAccessToken(self):
        logging.info("Getting access token")
        payload={}
        payload["grant_type"]="password"
        payload["username"]=self.config["security"]["username"]
        payload["password"]=self.config["security"]["password"]
        payload["client_id"]=self.config["security"]["client_id"]
        payload["client_secret"]=self.config["security"]["client_secret"]
        payload["scope"]=self.config["security"]["scope"]

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            logging.debug("token response.json(): %s", response.text)
            
            scope=str(response.json()["scope"])
            access_token=response.json()["access_token"]
            refresh_token=response.json()["refresh_token"]
            self.accessToken = access_token
            self.refreshToken = refresh_token
            
            self.config.add_section('token')
            self.config.set('token', 'scope', scope)

            #self.writeConfigFile(self.configFilePath)

            logging.debug("Your access token is: %s", self.accessToken)
            logging.debug("Your refresh token is: %s", self.refreshToken)
            logging.debug("Your scopes are: %s", self.config["security"]["scope"])
            
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)
            print(payload)
            logging.error(error.response.status_code, error.response.text)
            logging.error(payload)

    def post(self, command, headers=None, data=None):
        #headers = {'Authorization': 'Bearer ' + self.config["security"]["access_token"]}
        headers = {'Authorization': 'Bearer ' +  self.accessToken }

        try:     
            response = requests.post(Netatmo.baseUrl+command,  headers=headers, data=data)       
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)            
            logging.error(error.response.status_code)
            logging.error(error.response.text)
            raise

    def postdata(self, command, headers=None, data=None):
        headers = {'Authorization': 'Bearer ' +  self.accessToken }
        params={}
        params["home_id"]=self.home_id

        try:     
            response = requests.post(Netatmo.baseUrl+command,  headers=headers, data=params)       
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)            
            logging.error(error.response.status_code)
            logging.error(error.response.text)
            raise


    def getHomesData(self, homeName=None, homeId=None, gatewayType=None):

        response=self.post("homesdata")

        for currentHome in response.json()["body"]["homes"]:
            #print("config home name:" + self.config["home"]["name"])
            #print("currentHome name:" + currentHome["name"])

            if(currentHome["name"] == homeName or currentHome["id"]== homeId or currentHome["name"]==self.config["home"]["name"]):
                self.home=currentHome
                self.home_id=currentHome["id"]
                '''
                print("self.home_id:" + self.home_id)
                print("currentHome id:" + currentHome["id"])
                print("homename:" + currentHome["name"])
                '''
                return currentHome

    # https://dev.netatmo.com/resources/technical/reference/energy/homestatus
    # GET /api.netatmo.com/api/homestatus?home_id=[HOME_ID] 
    def getHomeStatus(self, homeName=None, homeId=None):
        params={}
        params["home_id"]=self.home_id
        response=self.postdata("homestatus", data=params)
        home = response.json()["body"]["home"]
        
        return home

    def getHomeModules(self, homeName, homeId=None):
        print("getHomeModules")
