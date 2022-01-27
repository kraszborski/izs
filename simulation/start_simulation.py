import sys, time
sys.path.append("..")
from config.izs_config import *
import psycopg2

def insertPosition(source_table, sensor_id, current_position, current_floor, current_temperature, current_speed):
    query = "INSERT INTO public.positions (geom, sensor_id, current_floor, current_temperature, current_speed) SELECT geom, '" + str(sensor_id) + "'::int, '" + str(current_floor) + "'::float, '" + str(current_temperature) + "'::float, '" + str(current_speed) + "'::float FROM " + source_table + " WHERE id = " + str(current_position) + ";"
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(e)
        print(query)

position = 0
temperature = 98
while True:
    if position >= 418:
        print("Ending simulation")
        exit(0)
    print("Getting information from sensors")
    insertPosition("simulace2", 1, position, 6, temperature, 1)
    insertPosition("simulace2", 2, position + 10, 6, temperature, 1)
    insertPosition("simulace3", 3, position + 20, 7, temperature - 10, 1)
    insertPosition("simulace3", 4, position + 30, 7, temperature - 10, 1)
    position += 1
    temperature += 0.1
    time.sleep(5)
