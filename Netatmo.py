
import configparser
import requests
import logging

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
        self.home =None

        self.config = configparser.ConfigParser() 
        self.configFilePath=configFile
        self.loadConfigFile(self.configFilePath)   


    def loadConfigFile(self, configPath):    
        logging.info("Loading config from "+configPath)    
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
        payload["scope"] =self.config["security"]["scope"]

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
           
            self.config["security"]["scope"]=response.json()["scope"]
            self.config["security"]["access_token"]=response.json()["access_token"]
            self.config["security"]["refresh_token"]=response.json()["refresh_token"]
            self.writeConfigFile(self.configFilePath)

            logging.debug("Your access token is: %s", self.accessToken)
            logging.debug("Your refresh token is: %s", self.refreshToken)
            logging.debug("Your scopes are: %s", self.config["security"]["scope"])
            
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)
            print(payload)
            logging.error(error.response.status_code, error.response.text)
            logging.error(payload)

    def post(self, command, headers=None, data=None):
        headers = {'Authorization': 'Bearer ' + self.config["security"]["access_token"]}   

        try:     
            response = requests.post(Netatmo.baseUrl+command,  headers=headers, data=data)       
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
            if(currentHome["name"] == homeName):
                self.home=currentHome
                return currentHome
        
        

    def getHomeStatus(self, homeName=None, homeId=None):
        params={}

        if(self.home != None):
            params["home_id"]=self.home["id"]
        else:
            params["home_id"]=homeId
        
        response=self.post("homestatus", data=params)
        print (response.json())

    def getHomeModules(self, homeName, homeId=None):
        print("TODO")
