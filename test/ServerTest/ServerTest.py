# Um Servidor, Para Testar as APIs dos Outros Servidores:

import os
import requests

dataPost = {
    "vehicleID": 25,
    "actualBatteryPercentage": 50,
    "batteryCapacity": 51,
    "reservationsRoute": [
        {
            "codename": "v_conquista",
            "name": "Vitória da Conquista - BA",
            "location": 0,
            "company": "voltpoint"
        },
        {
            "codename": "jequie",
            "name": "Jequié - BA",
            "location": 154,
            "company": "voltpoint"
        }
    ]
}

dataGet = {
    "vehicleID": 25
}

dataDelete = {
    "reservationID": 1, 
    "chargingStationID": 1,
    "chargingPointID": 1,
    "vehicleID": 25
}

# Recebendo os IP e Portas dos Outros Servidores Providos pelas Variáveis de Ambiente:
ECOCHARGE_SERVER_IP = os.environ.get('ECOCHARGE_SERVER_IP')
ECOCHARGE_SERVER_PORT = os.environ.get('ECOCHARGE_SERVER_PORT')
EFLUX_SERVER_IP = os.environ.get('EFLUX_SERVER_IP')
EFLUX_SERVER_PORT = os.environ.get('EFLUX_SERVER_PORT')
VOLTPOINT_SERVER_IP = os.environ.get('VOLTPOINT_SERVER_IP')
VOLTPOINT_SERVER_PORT = os.environ.get('VOLTPOINT_SERVER_PORT')

response = requests.post(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', json=dataPost)
print(response.json())

response = requests.get(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', params=dataGet)
print(response.json())

response = requests.delete(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', json=dataDelete)
print(response.json())
