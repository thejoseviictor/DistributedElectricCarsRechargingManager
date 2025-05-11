# Testando as APIs dos Servidores:
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

response = requests.post('http://localhost:64352/reservation', json=data_post)
response = requests.get('http://localhost:64352/reservation', json=data_get)
response = requests.delete('http://localhost:64352/reservation', json=data_delete)
print(response.json())
