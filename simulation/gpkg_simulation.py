from qgis.PyQt.QtCore import QThread
import sys, time, os
from osgeo import ogr

class Simulation(QThread):
    """
    Thread that runs in infinite loop and inserts new rows into positions table
    """
    def __init__(self):
        super(Simulation, self).__init__()


    def insertPosition(self, source_table, sensor_id, current_position, current_floor, current_temperature, current_speed):
        # Here you have to change it to something like 'C:/Users/krystof/PyCharmProjects/izs/db/izs.gpkg'
        geopackage_path = '/home/jencek/Documents/Projekty/Hasici/izs/db/izs.gpkg'

        query = "INSERT INTO positions (geom, sensor_id, current_floor, current_temperature, current_speed) SELECT geom, CAST('" + str(sensor_id) + "' AS INTEGER), CAST('" + str(current_floor) + "' AS FLOAT), CAST('" + str(current_temperature) + "' AS FLOAT), CAST('" + str(current_speed) + "' AS FLOAT) FROM " + source_table + " WHERE fid = " + str(current_position) + ";"
        print(query)
        try:
            # Not sure if we need transaction, but it does not affect the speed, so we can keep. use transaction if always good practise
            conn = ogr.Open(geopackage_path, 1) # open in update mode
            conn.StartTransaction()
            conn.ExecuteSQL(query)
            conn.CommitTransaction()
        except Exception as e:
            print(e)

    def run(self):
        # Here you can set initial values for simulation
        # The limit for temperature is 100, so dangerous situation should happen in about 100 seconds
        position = 1
        temperature = 98
        number_of_positions = 418
        run_me = True

        # This is solution for killing simulation.
        # If you create file on the path specified here, the simulation ends in 5 seconds.
        kill_path = '/tmp/kill_izs.txt'

        # Main infinite loop
        while run_me:
            if position >= number_of_positions or os.path.exists(kill_path):
                print("Ending simulation")
                run_me = False
            else:
                print("Getting information from sensors")
                self.insertPosition("simulace2", 1, position, 6, temperature, 1)
                self.insertPosition("simulace2", 2, position + 10, 6, temperature, 1)
                self.insertPosition("simulace3", 3, position + 20, 7, temperature - 10, 1)
                self.insertPosition("simulace3", 4, position + 30, 7, temperature - 10, 1)
                position += 1
                temperature += 0.1
                time.sleep(5)

simulation = Simulation()
simulation.start()
