# Classe responsável pela comunicação entre cliente (Veículo) e servidor (Nuvem)

from dataclasses import dataclass
from Vehicle import Vehicle
from VehicleUtility import VehicleUtility

import paho.mqtt.client as mqtt
import os
import socket
import json
import time
import threading

@dataclass
class VehicleClient:

    def __init__(self):
           
        self.serverHOST = 'localhost'
        self.serverPORT = 1883
        self.cost = 0.0
        self.reservations = []

        self.messageArrived = threading.Event()
        self.message = None
        self.request = None

        self.utility = VehicleUtility()

    # Método que inicia requisição de reserva, utilizando dados do veículo e as informações de origem e destino para envio por meio da comunicação MQTT
    def sendRequest(self, dataFilePath: str, reservationsFilePath: str , vehicle: Vehicle, Route: list[str]):
  
        # Dicionário utilizado para selecionar os dados pertinentes para o servidor ao pedir a reserva
        vData = {
                    "vehicleID": vehicle.vid ,
                    "actualBatteryPercentage": vehicle.currentEnergy ,
                    "batteryCapacity" : vehicle.maximumBattery ,
                    "departureCityCodename" : Route[0] ,
                    "arrivalCityCodename" : Route[1]
        }

        # Cria um json baseado no dicionário "vData" e envia as informações para o servidor correspondente.
        self.request = json.dumps(vData, indent=4).encode('utf-8')

        try:
                
            client = mqtt.Client()
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.on_publish = self.on_publish

            client.reconnect_delay_set(min_delay=3,max_delay=30)
            client.connect_async(self.serverHOST, self.serverPORT, 60)

            client.loop_start()

            self.messageArrived.clear()

            
            print(" Requisição enviada, aguardando resposta...")

            received = self.messageArrived.wait(timeout=20)

            client.loop_stop()
            client.disconnect()

            if received:
                vehicle.updateCredit(dataFilePath, self.cost, "-")
                vehicle.keepReservations(reservationsFilePath,self.reservations)

        except Exception as e:

            print(" Erro de conexão com o server ! ")
            time.sleep(1)
            self.utility.clearTerminal()

    # Método "on_connect": Estabelece a comunicação com o servidor para receber as reservas realizadas pelo servidor(es)
    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            
            print(f" \t Conexão estabelecida ! ")
            client.subscribe("server/create_reservations/vehicle") # Realiza a inscrição para receber o dado esperado
            
            client.publish("vehicle/create_reservations/server", self.request)

        else:
            print(f" \u274C Falha na conexão. Código de retorno: {rc}")
            time.sleep(5)
            self.utility.clearTerminal()

            try:
                client.reconnect() # Tentando reconexão caso ocorra desconexão

            except Exception as e:
                print(" \u274C Erro ao tentar reconectar:", e)
                time.sleep(2)


    # Método on_message: Trata a mensagem recebida pelo(s) servidor(es)
    def on_message(self, client, userdata, msg):

        rMessage = msg.payload.decode()
        print(" Mensagem recebida:", repr(rMessage))
        time.sleep(5)

        self.message = json.loads(rMessage)
        print(self.message)

        for r in self.message.values():

            try:
                self.cost += int(r['price'])

            except Exception as e:
                self.cost += 0
                
            self.reservations.append(r)
        
        self.messageArrived.set()
    
    def on_publish(self, client, userdata, mid):
        print("\n\t Requisição publicada com sucesso! ")
        time.sleep(2)
        self.utility.clearTerminal()

    
    # Método extra, para definir o IP (que define a região de qual servidor onde o veículo está)
    def defineIP(self): 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Identificando a rota atual
        ip = s.getsockname()[0] # Guardando ip da máquina utilizada
        s.close()

        base = os.path.dirname(os.path.abspath(__file__)) # Pegando o caminho absoluto do arquivo
        filePathServer = os.path.join(base, "dataPath", "brokers.json")# Variavel que guarda o caminho do arquivo "data.json"
        
        with open(filePathServer, 'r') as f:
                data = json.load(f)

        for s in data :
            if str(data["ip"]) == ip:
                self.nameCompanie = str(s["nameServer"])
                self.serverIP = str(s["ip"])
                self.serverPort = int(s["port"])
