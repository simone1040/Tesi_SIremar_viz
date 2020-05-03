from models.CaricoModel import get_ship_with_same_tratta
from utils.Costants import DATAFRAME_APPLICATION
import pandas as pd

class AnalyticsController:
    __data = None
    __AnalyticsScreen = None

    def __init__(self, an_screen):
        self.__AnalyticsScreen = an_screen
        self.__data = an_screen.data

    def getNaviWithSameTripAndHour(self,departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp):
        return get_ship_with_same_tratta(departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp)


    def get_max_carico_nave_per_periodo_e_tratta(self,nave_code):
        max_mq_occupati_trip = pd.DataFrame()
        periodo_partenza = self.__data["booking_ticket_departure_timestamp"]
        periodo_arrivo = self.__data["booking_ticket_arrival_timestamp"]
        porto_partenza = self.__data["departure_port_code"]
        porto_arrivo = self.__data["arrival_port_code"]
        dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
        #Dal dataframe caricato, prendo il carico massimo per la nave ed il periodo selezionato
        df_mq_occupati_ship = dataframe_to_plot[(dataframe_to_plot["ship_code"] == nave_code) &
                                                (dataframe_to_plot["departure_port_name"] == porto_partenza) &
                                                (dataframe_to_plot["arrival_port_name"] == porto_arrivo) &
                                                (dataframe_to_plot["booking_ticket_departure_timestamp"] >= periodo_partenza) &
                                                (dataframe_to_plot["booking_ticket_departure_timestamp"] <= periodo_arrivo)].reset_index()
        if df_mq_occupati_ship.shape[0] > 0:
            max_mq_occupati_trip = df_mq_occupati_ship.iloc[df_mq_occupati_ship["tot_mq_occupati"].idxmax()]
        return max_mq_occupati_trip

    def getStatistics(self):
        for ship_code, ship_name in zip(self.__data["ship_code_selected"],self.__data["ship_name_selected"]):
            tot_mq_occupati = self.get_max_carico_nave_per_periodo_e_tratta(ship_code)
            print(tot_mq_occupati)





