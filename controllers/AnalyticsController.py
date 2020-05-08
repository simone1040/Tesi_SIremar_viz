from models.CaricoModel import get_ship_with_same_tratta, from_port_code_get_name
from utils.Costants import DATAFRAME_APPLICATION, levelLog
from utils.MyLogger import writeLog
import pandas as pd

class AnalyticsController:
    __data = None
    __AnalyticsScreen = None

    def __init__(self, an_screen):
        self.__AnalyticsScreen = an_screen
        self.__data = an_screen.data

    def getNaviWithSameTripAndHour(self,departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp):
        return get_ship_with_same_tratta(departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp)


    def analyze_two_ship_cargo(self, nave_code_1, nave_code_2):
        total_case = 0
        positive_case = 0
        periodo_partenza = self.__data["booking_ticket_departure_timestamp"]
        periodo_arrivo = self.__data["booking_ticket_arrival_timestamp"]
        porto_partenza = self.__data["departure_port_code"]
        porto_arrivo = self.__data["arrival_port_code"]
        #Devo prendere il nome del porto dal codice
        porto_partenza_nome = from_port_code_get_name(porto_partenza)
        porto_arrivo_nome = from_port_code_get_name(porto_arrivo)
        dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
        #Dal dataframe caricato, prendo le date in maniera univoca
        df_carichi = dataframe_to_plot[((dataframe_to_plot["ship_code"] == nave_code_2) | (dataframe_to_plot["ship_code"] == nave_code_1)) &
                                       (dataframe_to_plot["departure_port_name"] == porto_partenza_nome) &
                                       (dataframe_to_plot["arrival_port_name"] == porto_arrivo_nome) &
                                       (dataframe_to_plot["booking_ticket_departure_timestamp"] >= periodo_partenza) &
                                       (dataframe_to_plot["booking_ticket_departure_timestamp"] <= periodo_arrivo)].reset_index()
        unique_date = df_carichi["booking_ticket_departure_timestamp"].unique()
        #Iterando per la data, prendo i carichi giorno per giorno e li analizzo
        print(df_carichi.head(10))

        for data in unique_date:
            carichi_per_data = df_carichi[dataframe_to_plot["booking_ticket_departure_timestamp"] == data]
            print(carichi_per_data.head(5))
        return True

    def getStatistics(self):
        analyzed_ship = self.__data["ship_code_selected"]
        for ship_code_first, ship_name_first in zip(self.__data["ship_code_selected"], self.__data["ship_name_selected"]):
            for ship_code_two, ship_name_two in zip(self.__data["ship_code_selected"], self.__data["ship_name_selected"]):
                if ship_code_first != ship_code_two and ship_code_two in analyzed_ship:
                    res = self.analyze_two_ship_cargo(ship_code_first,ship_code_two)
            analyzed_ship.remove(ship_code_first)





