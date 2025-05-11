# Testando as APIs dos Servidores:
import os
import requests

data_post = {
    "vehicleID": 12, 
    "actualBatteryPercentage": 30,
    "batteryCapacity": 200
}

data_get = {
    "vehicleID": 12
}

data_delete = {
    "reservationID": 1, 
    "chargingStationID": 1,
    "chargingPointID": 1,
    "vehicleID": 12
}

# Recebendo e Formatando o IP dos Servidores Providos pelas Variáveis de Ambiente:
# Obs: "strip" foi usado para remover as aspas.
ECOCHARGE_SERVER_IP = os.environ.get('ECOCHARGE_SERVER_IP').strip('"\'')
EFLUX_SERVER_IP = os.environ.get('EFLUX_SERVER_IP')
VOLTPOINT_SERVER_IP = os.environ.get('VOLTPOINT_SERVER_IP')

response = requests.post(f'http://{VOLTPOINT_SERVER_IP}:64123/reservation', json=data_post)
print(response.json())

response = requests.get(f'http://{VOLTPOINT_SERVER_IP}:64123/reservation', params=data_get)
print(response.json())

response = requests.delete(f'http://{VOLTPOINT_SERVER_IP}:64123/reservation', json=data_delete)
print(response.json())
