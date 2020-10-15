#!/usr/bin/python3
import time
import csv
import os
import datetime
from influxdb import InfluxDBClient

'''
Connection with InfluxDB (Global)
'''
INFLUXDB_HOST = 'influxdb.spinon.com.br'# Servidor InfluxDB
INFLUXDB_PORT = 80               		# Porta do InfluxDB
INFLUXDB_USER = 'foxiot_admin'          # Usuario InfluxDB
INFLUXDB_PASS = 'f@xiotadmin'           # Password InfluxDB
INFLUXDB_DB = 'ufsm_db_test'            # Nome do DB InfluxDB

'''
Config period of download

YEAR = '2020'                      # Year
MONTH = '08'                       # Month
MONTH_DAY_START = '01'             # Day 01
MONTH_DAY_END = '03'               # Day 02
'''

today = datetime.datetime.now().strftime("%d %m %Y %H %M").split(" ")
yesterday = (datetime.datetime.now() - datetime.timedelta(21)).strftime('%d %m %Y %H %M').split(" ")

YEAR_NOW = today[2]                        # Year
MONTH_NOW = today[1]                       # Month
MONTH_DAY_END = today[0]               # Day 02

HOUR_NOW = today[3]
MINUTE_NOW = today[4]

YEAR_THEN = yesterday[2]                        # Year
MONTH_THEN = yesterday[1]                       # Month
MONTH_DAY_START = yesterday[0]         # Day 01

'''
Config list of devices
'''
DEV_LIST = ['sm45']

'''
Init connection with InfluxDB (Global)
'''
print("Iniciando conexao com o influxdb")
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USER, password=INFLUXDB_PASS, database=INFLUXDB_DB)

'''
Function Main
'''
def main():

    '''
    Variables
    '''
    percent = 0
    percentCounter = 0
    deviceDataEnpty = ""

    #timeStart = "time > now() - 1h"
    dataStart = "time > '" + YEAR_THEN + "-" + MONTH_THEN + "-" + MONTH_DAY_START + "T" + HOUR_NOW + ":" + MINUTE_NOW + ":00Z'"
    dataEnd = "time < '" + YEAR_NOW + "-" + MONTH_NOW + "-" + MONTH_DAY_END + "T" + HOUR_NOW + ":" + MINUTE_NOW + ":00Z'" 

    print("Iniciando consulta")

    print()

    for index in DEV_LIST:

        try:
            query = 'SELECT mean("PA") + mean("PB") + mean("PC") AS "Value" FROM "payload_fields" WHERE ("device_id" = \'' + index + '\') AND ' + dataStart + ' AND ' + dataEnd + ' GROUP BY time(1m)'
            results = client.query(query)

            print(query)

            exported_data = list(results.get_points())

            header_list = list(exported_data[0].keys())
        except:
            deviceDataEnpty += " " + index 
            continue

        dirName = "csv/" + MONTH_NOW + "_" +YEAR_NOW
        
        if os.path.exists(dirName):
            os.system("rm -r" + dirName)

        elif not os.path.exists(dirName):
            os.makedirs(dirName)

        with open(dirName + "/" + MONTH_NOW + "_" + YEAR_NOW + "_" + index + ".csv", "a", newline='') as fp:
            writer = csv.writer(fp, dialect='excel')
            writer.writerow(exported_data[0].keys())
            for line in exported_data:
                writer.writerow(line.values())
   
        percentCounter += 1
        print("Processo: {0:.2f}".format((percentCounter / len(DEV_LIST)) * 100.0) + " %")

    if (deviceDataEnpty != ""):
        print("Disitivos sem dados no período: " + deviceDataEnpty)
    print("Consulta finalizada")

if __name__ == "__main__":
    main()
