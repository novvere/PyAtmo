#
# Test Netatmo  class
#
import logging
import Netatmo


def main():
    logging.basicConfig(level=logging.DEBUG)
    netatmo = Netatmo.Netatmo("PyAtmo.conf")   
    home=netatmo.getHomesData()
    netatmo.getHomeStatus()

   
    
if __name__ == "__main__":
    main()