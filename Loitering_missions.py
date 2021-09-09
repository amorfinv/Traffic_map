import geopandas
import pandas as pd
import re
import numpy as np
from random import randrange

"""
Loitering mission pseudocode:
1. Read in the initial flight intention
2. select several flights [12, 44, 512]
3. create a polygon around the destination of these flights
4. find all the flights that have a destination or origin in these polygons from the time of departure of the selected flights [12, 44, 512] +- a certain margin 
5. redistribute these flights with the same probility map as for the initial flight intention, without the ports in the loitering polygons

#find flight in flight intention
#retreive departure timestamp and node
#retrieve arrival node
#compute distance
#compute time bounds with margins
#determine loitering polygon based on arrival node 
#determine the number of flights that depart or arrive in this polygon during the lotering time
#remove these flights
#run Make_poisson_tableu_schedule for the number of removed flights, but only for the loitering time and without the lotering area
#add the new flights to the intention in the correct line
"""

#input
selected_flight_labels = [6118,44, 21]
negative_time_margin = 120 #seconds
positive_time_margin = 720 #seconds
loiter_area_side = 1500 #meter: square 500 by 500 meter



flightintention_df = pd.read_csv('Initial_flight_intention.csv')

def dist(x1, y1, x2 , y2):
    dist = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return dist


#retrieve flight info
selected_flights = []
for index, row in flightintention_df.iterrows():
    timestamp = row[3]
    timestamp = float(timestamp[0:2])*60*60 + float(timestamp[3:5])*60 + float(timestamp[6:8])
    row[3] = timestamp
    flightintention_df.iat[index, 3] = timestamp
    send_loc = row[4]
    send_loc = re.findall("\d+\.\d+",send_loc)    
    row[4] = send_loc
    flightintention_df.iat[index, 4] = send_loc
    recieve_loc = row[5]
    recieve_loc = re.findall("\d+\.\d+",recieve_loc)  
    row[5] = recieve_loc
    flightintention_df.iat[index, 5] = recieve_loc
    for label in selected_flight_labels:
        if row[1] == label:
            flight = []
            flight.append(index)  
            flight.append(row[1])
            flight.append(row[3])
            x_send = float(row[4][0])
            y_send = float(row[4][1])            
            flight.append(x_send)
            flight.append(y_send)
            x_rec = float(row[5][0])
            y_rec = float(row[5][1])           
            flight.append(x_rec)
            flight.append(y_rec)
            distance = dist(x_send, y_send, x_rec, y_rec)
            flight.append(distance * 111111)
            selected_flights.append(flight)
#print(selected_flights)
#line_number, label, timestamp, x_send, y_send, x_rec, y_rec, distance

#print(flightintention_df.columns)
#reveal_time, label, actype, timestamp, xy_send, xy_rec, priority

#generate the loiter missions
loiter_missions = []
for flight in selected_flights:
    loiter_mission = []
    x_rec = flight[5]
    y_rec = flight[6]
    x_min = x_rec - ((loiter_area_side/2)/111111)
    x_max = x_rec + ((loiter_area_side/2)/111111)
    y_min = y_rec - ((loiter_area_side/2)/111111)
    y_max = y_rec + ((loiter_area_side/2)/111111)  
    start_time = flight[2] - negative_time_margin
    end_time = flight[2] + positive_time_margin
    loiter_mission.append(start_time)
    loiter_mission.append(end_time)
    loiter_mission.append(x_min)
    loiter_mission.append(x_max)
    loiter_mission.append(y_min)
    loiter_mission.append(y_max)   
    loiter_missions.append(loiter_mission)
#print(loiter_missions)
#start_time, end_time, x_min, x_max, y_min, y_max


#find departing flights to remove from intention
to_be_removed = []
to_be_removed_departing_index = []
to_be_removed_departing = []
for loiter_mission in loiter_missions:
    for index, row in flightintention_df.iterrows():
        if row[3] >= loiter_mission[0] and row[3] <= float(loiter_mission[1]):
            if float(row[4][0]) >= loiter_mission[2] and float(row[4][0]) <= loiter_mission[3]:
                if float(row[4][1]) >= loiter_mission[4] and float(row[4][1]) <= loiter_mission[5]:
                    to_be_removed_departing_index.append(index)
                    flight = []
                    for datapoint in row:
                        flight.append(datapoint)
                    to_be_removed_departing.append(flight)
                    to_be_removed.append(index)
                    
#find arriving flights to remove from intention   
to_be_removed_arriving_index = []
to_be_removed_arriving = []
for loiter_mission in loiter_missions:
    for index, row in flightintention_df.iterrows():
        if row[3] >= loiter_mission[0] and row[3] <= float(loiter_mission[1]):
            if float(row[5][0]) >= loiter_mission[2] and float(row[5][0]) <= loiter_mission[3]:
                if float(row[5][1]) >= loiter_mission[4] and float(row[5][1]) <= loiter_mission[5]:
                    to_be_removed_arriving_index.append(index)
                    flight = []
                    for datapoint in row:
                        flight.append(datapoint)
                    to_be_removed_arriving.append(flight)
                    to_be_removed.append(index)
                    

flightintention_loiter_df = flightintention_df.drop(to_be_removed, axis = 0)
for index, row in flightintention_df.iterrows():
    flightintention_df.iat[index, 4] = '(' + str(flightintention_df.iloc[index, 4])[1:-1].replace("'", "") + ')'
    flightintention_df.iat[index, 5] = '(' + str(flightintention_df.iloc[index, 5])[1:-1].replace("'", "") + ')'
    if index in to_be_removed_departing_index:
        random_loc_selector = randrange(0, len(flightintention_loiter_df))
        new_loc = '(' + str(flightintention_loiter_df.iloc[random_loc_selector, 4])[1:-1].replace("'", "") + ')'
        flightintention_df.iat[index, 4] = new_loc
    if index in to_be_removed_arriving_index:
        random_loc_selector = randrange(0, len(flightintention_loiter_df))
        new_loc = '(' + str(flightintention_loiter_df.iloc[random_loc_selector, 5])[1:-1].replace("'", "") + ')'
        flightintention_df.iat[index, 5] = new_loc


#print(flightintention_df)
flightintention_df.to_csv('Flight_intention_loiter.csv', header = False, index = False)

"""
#Create used nodes geopackage for sending and recieving ports seperately
sending_nodes = []
recieving_nodes = []
for index, row in flightintention_df.iterrows():
    sending_nodes.append(row[4])
    recieving_nodes.append(row[5])

sending_nodes = list(set(sending_nodes))
recieving_nodes = list(set(recieving_nodes))

sending_nodes_float = []
for i in sending_nodes:
    sending_nodes_float.append(re.findall("\d+\.\d+",i))
recieving_nodes_float = []
for i in recieving_nodes:
    recieving_nodes_float.append(re.findall("\d+\.\d+",i))   
#print(sending_nodes_float, recieving_nodes_float)
    
sending_nodes_float_x = []
sending_nodes_float_y = []
for i in sending_nodes_float:
    sending_nodes_float_x.append(i[0])
    sending_nodes_float_y.append(i[1])

recieving_nodes_float_x = []
recieving_nodes_float_y = []
for i in recieving_nodes_float:
    recieving_nodes_float_x.append(i[0])
    recieving_nodes_float_y.append(i[1])

df = pd.DataFrame(
    {'x_send': sending_nodes_float_x,
     'y_send': sending_nodes_float_y})
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.x_send, df.y_send), crs = 'EPSG:4326')
gdf.to_crs(crs = 'EPSG:32633', inplace = True)
gdf.to_file("Sending_nodes.gpkg", layer='Sending_nodes', driver="GPKG")

df = pd.DataFrame(
    {'x_rec': recieving_nodes_float_x,
     'y_rec': recieving_nodes_float_y})
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.x_rec, df.y_rec), crs = 'EPSG:4326')
gdf.to_crs(crs = 'EPSG:32633', inplace = True)
gdf.to_file("Recieving_nodes.gpkg", layer='Recieving_nodes', driver="GPKG")
"""




