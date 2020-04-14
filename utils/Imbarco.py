class Imbarco:
    __departure_timestamp = ""
    __departure_port_name = ""
    __arrival_port_name = ""
    __tot_mq_occupati = ""

    def __init__(self, imbarco):
        self.__departure_timestamp = imbarco["booking_ticket_departure_timestamp"]
        self.__departure_port_name = imbarco["departure_port_name"]
        self.__arrival_port_name = imbarco["arrival_port_name"]
        self.__tot_mq_occupati = imbarco["tot_mq_occupati"]

    def getDepartureTimestamp(self):
        return self.__departure_timestamp

    def getDeparturePortName(self):
        return self.__departure_port_name

    def getArrivalPortName(self):
        return self.__arrival_port_name

    def getTotMqOccupati(self):
        return self.__tot_mq_occupati
