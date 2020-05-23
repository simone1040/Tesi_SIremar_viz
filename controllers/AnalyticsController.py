from models.CaricoModel import get_ship_with_same_tratta, from_port_code_get_name, getMaxCaricoForShip, get_ship_name
from utils.Costants import DATAFRAME_APPLICATION, levelLog, SOGLIA_CONSIDERAZIONE_ORARIO, SOGLIA_SPAZIO_LIBERO
from collections import defaultdict
from datetime import datetime
from utils.ReportSum import ReportSum

class AnalyticsController:
    __data = None
    __AnalyticsScreen = None
    CASI_TOTALI = "casi_totali"
    CASI_POSITIVI = "casi_positivi"

    def __init__(self, an_screen):
        self.__AnalyticsScreen = an_screen
        self.__data = an_screen.data

    def getNaviWithSameTripAndHour(self,departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp):
        return get_ship_with_same_tratta(departure_port_code, arrival_port_code, departure_timestamp, arrival_timestamp)


    def checkKeyExist(self,dict,first_level_key,second_level_key, nave_1, nave_2):
        if first_level_key in dict.keys():
            if second_level_key not in dict[first_level_key]:
                dict[first_level_key][second_level_key][self.CASI_TOTALI] = 0
                dict[first_level_key][second_level_key][self.CASI_POSITIVI] = 0
                dict[first_level_key][second_level_key][nave_1] = 0
                dict[first_level_key][second_level_key][nave_2] = 0
        else:
            dict[first_level_key][second_level_key][self.CASI_TOTALI] = 0
            dict[first_level_key][second_level_key][self.CASI_POSITIVI] = 0
            dict[first_level_key][second_level_key][nave_1] = 0
            dict[first_level_key][second_level_key][nave_2] = 0
        return dict

    def analyze_two_ship_cargo(self, nave_code_1, nave_code_2):
        d = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        periodo_partenza = self.__data["booking_ticket_departure_timestamp"]
        periodo_arrivo = self.__data["booking_ticket_arrival_timestamp"]
        porto_partenza = self.__data["departure_port_code"]
        porto_arrivo = self.__data["arrival_port_code"]
        #Capienza_massima nave_1 e nave_2
        capienza_nave_1 = getMaxCaricoForShip(nave_code_1)
        capienza_nave_2 = getMaxCaricoForShip(nave_code_2)
        #Devo prendere il nome del porto dal codice
        porto_partenza_nome = from_port_code_get_name(porto_partenza)
        porto_arrivo_nome = from_port_code_get_name(porto_arrivo)
        #Prendo nome nave 1 e nome nave 2
        nome_nave_1 = get_ship_name(nave_code_1)
        nome_nave_2 = get_ship_name(nave_code_2)
        dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
        #Dal dataframe caricato, prendo le date in maniera univoca
        df_carichi = dataframe_to_plot[((dataframe_to_plot["ship_code"] == nave_code_2) | (dataframe_to_plot["ship_code"] == nave_code_1)) &
                                       (dataframe_to_plot["departure_port_name"] == porto_partenza_nome) &
                                       (dataframe_to_plot["arrival_port_name"] == porto_arrivo_nome) &
                                       (dataframe_to_plot["booking_ticket_departure_timestamp"] >= periodo_partenza) &
                                       (dataframe_to_plot["booking_ticket_departure_timestamp"] <= periodo_arrivo)]\
            .reset_index().sort_values(by=["booking_ticket_departure_timestamp"])
        df_carichi["only_date"] = df_carichi["booking_ticket_departure_timestamp"].apply(lambda x: x.split(" ")[0])
        df_carichi["only_hour"] = df_carichi["booking_ticket_departure_timestamp"].apply(lambda x: x.split(" ")[1])
        unique_date = df_carichi["only_date"].unique()
        #Iterando per la data, prendo i carichi giorno per giorno e li analizzo
        for data in unique_date:
            carichi_per_data = df_carichi[df_carichi["only_date"] == data]
            for i in range(0, len(carichi_per_data)):
                for j in range(i + 1, len(carichi_per_data)):
                    data_i = datetime.strptime(carichi_per_data.iloc[i]["booking_ticket_departure_timestamp"], '%Y-%m-%d %H:%M:%S')
                    data_j = datetime.strptime(carichi_per_data.iloc[j]["booking_ticket_departure_timestamp"], '%Y-%m-%d %H:%M:%S')
                    diff = data_j - data_i
                    if datetime.strptime(str(diff), '%H:%M:%S') <= SOGLIA_CONSIDERAZIONE_ORARIO:
                        #INIZIALIZZO IL DIZIONARIO
                        hour_i = carichi_per_data.iloc[i]["only_hour"]
                        hour_j = carichi_per_data.iloc[j]["only_hour"]
                        d = self.checkKeyExist(d, hour_i, hour_j, nave_code_1, nave_code_2)
                        # Aggiungo 1 ai casi totali
                        d[hour_i][hour_j][self.CASI_TOTALI] = d[hour_i][hour_j][self.CASI_TOTALI] + 1
                        #Sommo i mq occupati dai due viaggi
                        sum_mq = round(carichi_per_data["tot_mq_occupati"].sum(), 2)
                        #CONTROLLO CHE RIENTRI NEL CARICO DELLE 2 NAVI + SOGLIA
                        if capienza_nave_1 >= sum_mq + SOGLIA_SPAZIO_LIBERO or capienza_nave_2 >= sum_mq + SOGLIA_SPAZIO_LIBERO:
                            d[hour_i][hour_j][self.CASI_POSITIVI] = d[hour_i][hour_j][self.CASI_POSITIVI] + 1
                            if capienza_nave_1 >= sum_mq + SOGLIA_SPAZIO_LIBERO:
                                d[hour_i][hour_j][nome_nave_1] = d[hour_i][hour_j][nome_nave_1] + 1
                            if capienza_nave_2 >= sum_mq + SOGLIA_SPAZIO_LIBERO:
                                d[hour_i][hour_j][nome_nave_2] = d[hour_i][hour_j][nome_nave_2] + 1
        return ReportSum(nome_nave_1, nome_nave_2, d)

    def getStatistics(self):
        array_of_report = []
        ship_code = self.__data["ship_code_selected"]
        ship_name = self.__data["ship_name_selected"]
        for i in range(0, len(ship_code)):
            for j in range(i+1, len(ship_code)):
                self.__AnalyticsScreen.writeToTextArea("Analisi carichi delle seguenti navi: {} | {}".format(ship_name[i], ship_name[j]))
                d = self.analyze_two_ship_cargo(ship_code[i], ship_code[j])
                array_of_report.append(d)
        return array_of_report






