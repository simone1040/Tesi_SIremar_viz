from models.CaricoModel import *
from matplotlib import pyplot as plt
from utils.Costants import *
from utils.MyLogger import writeLog
import pandas as pd



#Funzione che viene chiamata quando si clicca il tasto di generazione del grafico, che viene salvato sull'assets
def image_statistics_filtered(filter):
    list_of_ship_name = []
    dataframe_to_plot = DATAFRAME_APPLICATION["dataframe_prenotazioni"]
    #PRENDO IL DATABASE DELLE ROUTE CAPPELLI COSI DA POTER FORMARE IL NUOVO DATABASE DA CUI SI EFFETTUA IL PLOT

    for key, values in filter.items():
        if values != "":
            if key == "ship":
                writeLog(levelLog.INFO,"CaricoManager","Sto filtrando per le seguenti navi --> {}".format(filter["ship"]))
                dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["ship_code"].isin(filter["ship"])]
            if key == "departure_port_code":
                port_name = from_port_code_get_name(filter["departure_port_code"])
                dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["departure_port_name"] == port_name]
            if key == "arrival_port_code":
                port_name = from_port_code_get_name(filter["arrival_port_code"])
                dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["arrival_port_name"] == port_name]
            if key == "booking_ticket_departure_timestamp":
                booking_ticket_departure_timestamp = filter["booking_ticket_departure_timestamp"]
                dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["booking_ticket_departure_timestamp"] >= booking_ticket_departure_timestamp]
            if key == "booking_ticket_arrival_timestamp":
                booking_ticket_arrival_timestamp = filter["booking_ticket_arrival_timestamp"]
                dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["booking_ticket_departure_timestamp"] <= booking_ticket_arrival_timestamp]
    #Ordino le righe per il departure timestamp
    dataframe_to_plot = dataframe_to_plot.sort_values(by = ["booking_ticket_departure_timestamp"])
    if not dataframe_to_plot.empty:
        fig = plt.figure(figsize=(IMAGE_WIDTH/IMAGE_INFO["dpi_monitor"], IMAGE_HEIGHT/IMAGE_INFO["dpi_monitor"]), dpi=IMAGE_INFO["dpi_monitor"])
        dataframe_to_plot["booking_ticket_departure_timestamp"] = dataframe_to_plot["booking_ticket_departure_timestamp"].apply(lambda x: x.split(" ")[0])
        for values in dataframe_to_plot.ship_code.unique():
            #INIZIO DATAFRAME PER IL LIMITE CHE COSI PRENDE L'INTERO GRAFICO
            dataframe_lim = pd.DataFrame(dataframe_to_plot.booking_ticket_departure_timestamp.unique(),columns =['booking_ticket_departure_timestamp'])
            dataframe_lim["metri_garage_navi_spazio_totale"] = dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["metri_garage_navi_spazio_totale"].iloc[0]
            #FINE
            #INIZIO PRENDO IL NOME DELLA NAVE E LO APPENDO DUE VOLTE PERCHE LO USO DUE VOLTE NEL PLOT
            ship_name = get_ship_name(values)
            list_of_ship_name.append(ship_name)
            list_of_ship_name.append(ship_name)
            #FINE
            #INIZIO PLOT DEL LIMITE E DEI PUNTI
            plt.plot(dataframe_lim["booking_ticket_departure_timestamp"],
                     dataframe_lim["metri_garage_navi_spazio_totale"],label=ship_name)

            plt.plot(dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["booking_ticket_departure_timestamp"],
                 dataframe_to_plot[dataframe_to_plot["ship_code"] == values]["tot_mq_occupati"], 'o',label=ship_name)
            #FINE

        plt.title("Mq occupati da imbarchi dal " + booking_ticket_departure_timestamp + " al " + booking_ticket_arrival_timestamp, loc="center")
        plt.xlabel('Data di partenza')
        plt.legend()
        ax = fig.gca()  # get the current axis
        for i, p in enumerate(ax.get_lines()):  # this is the loop to change Labels and colors
            if p.get_label() in list_of_ship_name[:i]:  # check for Name already exists
                idx = list_of_ship_name.index(p.get_label())  # find ist index
                p.set_c(ax.get_lines()[idx].get_c())  # set color
                p.set_label('_' + p.get_label())  # hide label in auto-legend
        fig.canvas.draw()
        label_month = ""
        labels = []
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            text = label.get_text()
            exploded_text = text.split("-")
            month = str(exploded_text[1])
            if month == "12":
                month = "00"
            if label_month == "":
                label_month = month
                labels.append(text)
            elif label_month < month:
                label_month = month
                labels.append(text)
        plt.legend()
        plt.xticks(labels,rotation=30)
        plt.ylabel('Mq')
        plt.grid()
        return fig
    else:
        return None



