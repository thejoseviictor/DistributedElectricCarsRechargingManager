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

reservation_post = {
    "vehicleID": 1,
    "actualBatteryPercentage": 20,
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

# Recebendo os IP e Portas dos Servidores Providos pelas Variáveis de Ambiente:
ECOCHARGE_SERVER_IP = os.environ.get('ECOCHARGE_SERVER_IP')
ECOCHARGE_SERVER_PORT = os.environ.get('ECOCHARGE_SERVER_PORT')
EFLUX_SERVER_IP = os.environ.get('EFLUX_SERVER_IP')
EFLUX_SERVER_PORT = os.environ.get('EFLUX_SERVER_PORT')
VOLTPOINT_SERVER_IP = os.environ.get('VOLTPOINT_SERVER_IP')
VOLTPOINT_SERVER_PORT = os.environ.get('VOLTPOINT_SERVER_PORT')

response = requests.post(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', json=data_post)
print(response.json())

response = requests.get(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', params=data_get)
print(response.json())

response = requests.delete(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', json=data_delete)
print(response.json())

response = requests.post(f'http://{VOLTPOINT_SERVER_IP}:{VOLTPOINT_SERVER_PORT}/reservation', json=reservation_post)
print(response.json())
