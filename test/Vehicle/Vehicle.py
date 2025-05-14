import paho.mqtt.client as mqtt

BROKER_IP = "localhost"
BROKER_PORT = 1883
TOPIC_SUBSCRIBER = "server/create_reservations/vehicle"
TOPIC_PUBLISHER = "vehicle/create_reservations/server"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao Broker com Sucesso!\n")
        client.subscribe(TOPIC_SUBSCRIBER)
    else:
        print(f"Falha na Conexão! Código de Retorno: {rc}\n")

def on_message(client, userdata, msg):
    print(f"[Recebido] Tópico: {msg.topic} | Mensagem: {msg.payload.decode()}\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_forever()

reservationData = {
    "vehicleID": 1,
    "actualBatteryPercentage": 100,
    "batteryCapacity": 51,
    "departureCityCodename": "v_conquista",
    "arrivalCityCodename": "e_cunha"
}
client.publish(TOPIC_PUBLISHER, str(reservationData))

try:
    while True:
        pass 
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
