from models.CaricoModel import getMaxCaricoForShip
from utils.Costants import DATAFRAME_APPLICATION, SOGLIA_SPAZIO_LIBERO,SOGLIA_UGUAGLIANZA_CARICO
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
        # Prendo i max mq occupati per la nave selezionata presa in esame
        imbarco_data = self.get_max_carico_nave_per_periodo(self.__data["ship_code_selected"])
        if imbarco_data.empty:
            return "Nessun carico nel periodo selezionato"

        #Ship per la nave selezionata
        ship_selezionata = Ship(self.__data["ship_code_selected"],self.__data["ship_name_selected"], imbarco_data)

        # Stampo il max carico
        self.__optscreen.writeToTextArea("Metratura {} --> {} mq".format(ship_selezionata.getNaveName(), ship_selezionata.getCapienzaMassima()))

        #Setto il max carico raggiunto dalla nave e lo stampo
        ship_selezionata.setMaxCaricoRaggiunto(ship_selezionata.getInfoImbarco().getTotMqOccupati())

        self.__optscreen.writeToTextArea("Max metratura raggiunta dalla nave {} è {} mq giorno {} "
                                         .format(ship_selezionata.getNaveName(), ship_selezionata.getMaxCaricoRaggiunto(), format_date_to_view(
            ship_selezionata.getInfoImbarco().getDepartureTimestamp())))

        #Stampo spazio libero che rimane prendendo il massimo carico
        self.__optscreen.writeToTextArea(
            "Minimo spazio inutilizzato in un viaggio --> {} mq".format(ship_selezionata.getDeltaSpazioLibero()))

        # Controllo in cui vedo se la nave è gia carica attraverso il controllo della soglia di carico
        if (ship_selezionata.getDeltaSpazioLibero() >= SOGLIA_SPAZIO_LIBERO):
            self.__optscreen.writeToTextArea(
                "Spazio inutilizzato superiore alla soglia, Ottimizzazione in corso")
            # Prendo tutte le navi che hanno una metratura inferiore per il controllo di ottimizzazione
            # Per ogni nave presa effettuo il controllo di ottimizzazione
            for s, s_name in zip(self.__data["ship_code_to_optimize"], self.__data["ship_name_to_optimize"]):
                print("ciao")
                #optimizer_ship = self.search_optimizer_ship(s, s_name, max_carico, max_mq_occupati)
        else:
            self.__optscreen.writeToTextArea(
                "Spazio inutilizzato inferiore alla soglia, ricerca nave con massima metratura superiore")
            # TODO EFFETTUARE IL RAGIONAMENTO AL CONTRARIO

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

    def search_optimizer_ship(self, s, s_name, max_carico_ship_to_optimize, max_mq_occupati_ship_to_optimize):
            #INIZIO Calcolo lo spazio libero che rimane col massimo carico nella nave in esame
            delta_spazio_libero_ship_to_optimize = round(max_carico_ship_to_optimize - max_mq_occupati_ship_to_optimize, 2)
            #CERCO NEL DB I MQ MASSIMI CHE LA NAVE OCCUPA
            max_carico_possibile = getMaxCaricoForShip(s)
            self.__optscreen.writeToTextArea("Metratura {} --> {} mq".format(s_name, max_carico_possibile))
            #Calcolo i mq massimi occupati nella nave nel periodo selezionato
            max_mq_occupati_row = self.get_max_carico_nave_per_periodo(s)
            max_mq_occupati = round(max_mq_occupati_row["tot_mq_occupati"], 2)
            self.__optscreen.writeToTextArea("Max metratura raggiunta dalla nave {} è {} mq giorno {} "
                                       .format(s_name, max_mq_occupati, format_date_to_view(
                max_mq_occupati_row["booking_ticket_departure_timestamp"])))
            #Calcolo lo spazio libero per la nave selezionata
            delta_spazio_libero = round(max_carico_possibile - max_mq_occupati)
            self.__optscreen.writeToTextArea("Minimo spazio inutilizzato in un viaggio --> {} mq".format(delta_spazio_libero))

            #Algoritmo di selezione delle navi con cui posso ottimizzare
            if max_carico_ship_to_optimize > max_mq_occupati:#Caso in cui la nave da ottimizzare ha un carico maggiore
                if(abs(delta_spazio_libero_ship_to_optimize - delta_spazio_libero) <= SOGLIA_UGUAGLIANZA_CARICO):
                    self.__optscreen.writeToTextArea("Le navi sono interscambiabili")
                else:
                    if delta_spazio_libero <= SOGLIA_SPAZIO_LIBERO:
                        self.__optscreen.writeToTextArea("La nave {}, se scambiata ottimizza il carico")
            #else:




