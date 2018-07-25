#
# Test Netatmo  class
#
import logging
import Netatmo


def main():
    logging.basicConfig(level=logging.DEBUG)
    netatmo = Netatmo.Netatmo("PyAtmo.conf")   
    formentor=netatmo.getHomesData("Formentor")
    netatmo.getHomeStatus(homeId=formentor["id"])

   
    
if __name__ == "__main__":
    main()