#Classe per le navi, dove tengo il loro max carico e la capienza
from models.CaricoModel import getMaxCaricoForShip
from utils.Imbarco import Imbarco
class Ship:
    __nave_code = ""
    __nave_name = ""
    __capienza_massima = 0
    __infoImbarco = None

    def __init__(self, nave_code, nave_name, imbarco):
        self.__nave_code = nave_code
        self.__nave_name = nave_name
        self.__capienza_massima = getMaxCaricoForShip(nave_code)
        self.__infoImbarco = Imbarco(imbarco)

    def getNaveCode(self):
        return self.__nave_code

    def getNaveName(self):
        return self.__nave_name

    def getCapienzaMassima(self):
        return self.__capienza_massima

    def getDeltaSpazioLibero(self):
        return round(self.__capienza_massima - self.__infoImbarco.getTotMqOccupati(), 2)

    def getInfoImbarco(self):
        return self.__infoImbarco
