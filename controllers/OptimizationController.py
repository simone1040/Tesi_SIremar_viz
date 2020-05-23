from utils.Costants import DATAFRAME_APPLICATION, SOGLIA_SPAZIO_LIBERO, SOGLIA_UGUAGLIANZA_CARICO, SHIP_TO_OPTIMIZE, \
    OPTIMIZE
from utils.UtilsFunction import format_date_to_view
from utils.Ship import Ship
import pandas as pd


class OptimizationController():
    __optscreen = None
    __data = None

    def __init__(self, opt_screen):
        self.__optscreen = opt_screen
        self.__data = opt_screen.data

    def optimize_carico(self):
        ship_array = []
        # Prendo i max mq occupati per la nave selezionata presa in esame
        imbarco_data = self.get_max_carico_nave_per_periodo(self.__data["ship_code_selected"])
        if imbarco_data.empty:
            return ship_array

        #Ship per la nave selezionata
        ship_selezionata = Ship(self.__data["ship_code_selected"], self.__data["ship_name_selected"], imbarco_data)

        # Stampo il max carico
        self.__optscreen.writeToTextArea("Metratura {} --> {} mq".format(ship_selezionata.getNaveName(), ship_selezionata.getCapienzaMassima()))

        #Setto il max carico raggiunto dalla nave e lo stampo
        self.__optscreen.writeToTextArea("Max metratura raggiunta dalla nave {} è {} mq giorno {} "
                                         .format(ship_selezionata.getNaveName(), ship_selezionata.getInfoImbarco().getTotMqOccupati(), format_date_to_view(
            ship_selezionata.getInfoImbarco().getDepartureTimestamp())))

        #Stampo spazio libero che rimane prendendo il massimo carico
        self.__optscreen.writeToTextArea(
            "Minimo spazio inutilizzato in un viaggio --> {} mq".format(ship_selezionata.getDeltaSpazioLibero()))
        ship_selezionata.setOptimize(SHIP_TO_OPTIMIZE)
        ship_array.append(ship_selezionata)
        for ship_code_proposta, ship_name_proposta in zip(self.__data["ship_code_to_optimize"], self.__data["ship_name_to_optimize"]):
            imbarco_data_proposta = self.get_max_carico_nave_per_periodo(ship_code_proposta)
            if not imbarco_data_proposta.empty:
                ship_proposta = Ship(ship_code_proposta, ship_name_proposta, imbarco_data_proposta)
                if self.optimize_carico_ship(ship_selezionata, ship_proposta):
                    ship_proposta.setOptimize(OPTIMIZE)
                    self.__optscreen.writeToTextArea(
                        "La nave --> {} ottimizza i carichi della nave {} selezionata".format(
                            ship_proposta.getNaveName(), ship_selezionata.getNaveName()))
                ship_array.append(ship_proposta)
        return ship_array

    def get_max_carico_nave_per_periodo(self, nave_code):
        max_mq_occupati_trip = pd.DataFrame()
        periodo_partenza = self.__data["booking_ticket_departure_timestamp"]
        periodo_arrivo = self.__data["booking_ticket_arrival_timestamp"]
        dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
        #Dal dataframe caricato, prendo il carico massimo per la nave ed il periodo selezionato
        df_mq_occupati_ship = dataframe_to_plot[(dataframe_to_plot["ship_code"] == nave_code) &
                                                (dataframe_to_plot[
                                                     "booking_ticket_departure_timestamp"] >= periodo_partenza) &
                                                (dataframe_to_plot["booking_ticket_departure_timestamp"] <= periodo_arrivo)].reset_index()
        if df_mq_occupati_ship.shape[0] > 0:
            max_mq_occupati_trip = df_mq_occupati_ship.iloc[df_mq_occupati_ship["tot_mq_occupati"].idxmax()]
        return max_mq_occupati_trip

    def optimize_carico_ship(self, ship_selezionata, ship_proposta):
        #CASO1
        toRet = False
        if ship_selezionata.getInfoImbarco().getTotMqOccupati() + SOGLIA_SPAZIO_LIBERO < ship_selezionata.getCapienzaMassima():
            #CASO 1.1 MAX_CAPIENZA < MAX_CAPIENZA_NAVE_PROPOSTA
            if ship_selezionata.getCapienzaMassima() < ship_proposta.getCapienzaMassima():
                if ship_selezionata.getInfoImbarco().getTotMqOccupati() > ship_proposta.getInfoImbarco().getTotMqOccupati():
                    toRet = True
            #CASO 1.2 MAX_CAPIENZA_NAVE_SELEZIONATA >= MAX_CAPIENZA_NAVE_PROPOSTA
            elif(ship_selezionata.getCapienzaMassima() >= ship_proposta.getCapienzaMassima()):
                if ship_selezionata.getInfoImbarco().getTotMqOccupati() + SOGLIA_SPAZIO_LIBERO < ship_proposta.getCapienzaMassima():
                    if ship_selezionata.getInfoImbarco().getTotMqOccupati() < ship_proposta.getInfoImbarco().getTotMqOccupati():
                        toRet = True
        #CASO2
        elif ship_selezionata.getInfoImbarco().getTotMqOccupati() + SOGLIA_SPAZIO_LIBERO >= ship_selezionata.getCapienzaMassima():
            #CASO 2.1
            if ship_selezionata.getCapienzaMassima() < ship_proposta.getCapienzaMassima():
                if ship_selezionata.getInfoImbarco().getTotMqOccupati() > ship_proposta.getInfoImbarco().getTotMqOccupati():
                    toRet = True
        return toRet
