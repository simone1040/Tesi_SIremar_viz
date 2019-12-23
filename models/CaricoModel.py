from utils.SQLManager import SQLManager

def getMaxCaricoNave():
    sql = "SELECT tab_metri_garage_navi.*,ship_name,ship_code " \
          "FROM tab_metri_garage_navi " \
          "INNER JOIN tab_ship on tab_metri_garage_navi.ship_id = tab_ship.ship_id " \
          "order by ship_id"
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def getMaxCaricoForShip(ship_code):
    sql = "SELECT metri_garage_navi_spazio_totale " \
          "FROM tab_metri_garage_navi " \
          "INNER JOIN tab_ship on tab_metri_garage_navi.ship_id = tab_ship.ship_id " \
          "WHERE ship_code = '{}' ".format(ship_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    if not df.empty:
        return df["metri_garage_navi_spazio_totale"].iloc[0]
    else:
        return 0


def get_distinct_tratte():
    sql = "SELECT booking_ticket_departure_port_code,booking_ticket_arrival_port_code " \
          "FROM tab_booking_ticket " \
          "GROUP BY booking_ticket_departure_port_code,booking_ticket_arrival_port_code "
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_distinct_ship():
    sql = "SELECT ship_code,ship_name " \
          "FROM tab_ship " \
          "ORDER BY ship_name"
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_ship_name(ship_code):
    sql = "SELECT ship_name " \
          "FROM tab_ship " \
          "WHERE ship_code='{}'" \
          "ORDER BY ship_code".format(ship_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    if not df.empty:
        return df["ship_name"].iloc[0]
    else:
        return ship_code

def from_port_code_get_name(port_code):
    sql = "SELECT port_name " \
          "FROM tab_port " \
          "WHERE port_code='{}' ".format(port_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    port_name = df["port_name"].iloc[0]
    return port_name

#Tramite la route Cappelli prendo indistintamente solo i primi viaggi per il range selezionato
def get_distinct_first_trip(data_inizio,data_fine):
    sql = "SELECT route_cappelli_trip_code,route_cappelli_departure_timestamp,route_cappelli_route_code,route_cappelli_next_route_code," \
          "route_cappelli_departure_port_code,route_cappelli_arrival_port_code,route_cappelli_ship_code " \
          "FROM tab_route_cappelli " \
          "WHERE route_cappelli_progressive = 1 " \
          "AND DATE(route_cappelli_departure_timestamp) >= '{}' " \
          "AND DATE(route_cappelli_departure_timestamp) <= '{}' ".format(data_inizio, data_fine)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df

def get_trip_from_route_code(route_code):
    sql = "SELECT route_cappelli_trip_code,route_cappelli_departure_timestamp,route_cappelli_route_code,route_cappelli_next_route_code," \
          "route_cappelli_departure_port_code,route_cappelli_arrival_port_code,route_cappelli_ship_code " \
          "FROM tab_route_cappelli " \
          "WHERE route_cappelli_route_code = '{}' ".format(route_code)
    df = SQLManager.get_istance().execute_query(string_sql=sql)
    return df.iloc[0]