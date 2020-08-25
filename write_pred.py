from influxdb import InfluxDBClient
import csv
import time
from datetime import datetime
'''
Connection with InfluxDB (Global)
'''
INFLUXDB_HOST = 'influxdb.spinon.com.br'# Servidor InfluxDB
INFLUXDB_PORT = 80                      # Porta do InfluxDB
INFLUXDB_USER = 'foxiot_admin'          # Usuario InfluxDB
INFLUXDB_PASS = 'f@xiotadmin'           # Password InfluxDB
INFLUXDB_DB = 'ufsm_db_test'            # Nome do DB InfluxDB

'''
Init connection with InfluxDB (Global)
'''
print("Iniciando conexao com o influxdb")
client = InfluxDBClient(host=INFLUXDB_HOST,
                        port=INFLUXDB_PORT, 
                        username=INFLUXDB_USER, 
                        password=INFLUXDB_PASS, 
                        database=INFLUXDB_DB)

meter = 'sm45'

with open("/home/ceos/ceos_inference.csv") as file:
     data = [line.split(',') for line in file]
    
write_this = []


for i in range(len(data)-1):

    write_this.append({"measurement": "predictions",
                        "tags": {"meter": meter},
                        "fields": {"forecast": data[i+1][1][:-3]},
                        "time": data[i+1][0]
	              })

client.drop_measurement("predictions")    
client.write_points(write_this, time_precision='s',protocol='json')

print(client.query('SELECT * FROM "predictions"'))
