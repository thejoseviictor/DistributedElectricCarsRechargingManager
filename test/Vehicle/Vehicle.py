import paho.mqtt.client as mqtt
import json

BROKER_IP = "localhost"
BROKER_PORT = 1883
TOPIC_SUBSCRIBER = "server/create_reservations/vehicle"
TOPIC_PUBLISHER = "vehicle/create_reservations/server"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Broker com Sucesso!\n")
        client.subscribe(TOPIC_SUBSCRIBER)
        reservationData = {
            "vehicleID": 1,
            "actualBatteryPercentage": 100,
            "batteryCapacity": 51,
            "departureCityCodename": "v_conquista",
            "arrivalCityCodename": "e_cunha"
        }
        client.publish(TOPIC_PUBLISHER, json.dumps(reservationData))
    else:
        print(f"Falha na Conexão! Código de Retorno: {rc}\n")

def on_message(client, userdata, msg):
    print(f"[Recebido] Tópico: {msg.topic} | Mensagem: {msg.payload.decode()}\n")

def on_publish(client, userdata, mid):
    print("Mensagem Publicada Com Sucesso!\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.reconnect_delay_set(min_delay=3,max_delay=30)
client.connect_async(BROKER_IP, int(BROKER_PORT), 60)

client.loop_start()

try:
    while True:
        pass 
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
