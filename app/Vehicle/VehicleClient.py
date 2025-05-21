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

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.messageArrived = threading.Event()
        self.message = None

    # Método que inicia requisição de reserva, utilizando dados do veículo e as informações de origem e destino para envio por meio da comunicação MQTT
    def sendRequest(self, dataFilePath: str, reservationsFilePath: str , vehicle: Vehicle, Route: list[str]):

        utility = VehicleUtility() # Classe utilitária para tratamento e exibição amigável de dados
        
        # Dicionário utilizado para selecionar os dados pertinentes para o servidor ao pedir a reserva
        vData = {
                    "vehicleID": vehicle.vid ,
                    "actualBatteryPercentage": vehicle.currentEnergy ,
                    "batteryCapacity" : vehicle.maximumBattery ,
                    "departureCityCodename" : Route[0] ,
                    "arrivalCityCodename" : Route[1]
        }

        # Cria um json baseado no dicionário "vData" e envia as informações para o servidor correspondente.
        request = json.dumps(vData, indent=4).encode('utf-8')

        try:
                
            # self.client.user_data_set(request)
            self.client.connect(self.serverHOST, self.serverPORT, 60)

            self.client.loop_start()

            self.messageArrived.clear()

            self.client.publish("vehicle/create_reservations/server", request)
            print(" Requisição enviada, aguardando resposta...")

            received = self.mensagem_chegou.wait(timeout=20)

            
            self.client.loop_stop()
            self.client.disconnect()

            if received:
                vehicle.updateCredit(dataFilePath, self.cost, "-")
                vehicle.keepReservations(reservationsFilePath,self.reservations)

        except Exception as e:

            print(" Erro de conexão com o server ! ")
            time.sleep(1)
            utility.clearTerminal()

    # Método "on_connect": Estabelece a comunicação com o servidor para receber as reservas realizadas pelo servidor(es)
    def on_connect(self, client, userdata, flags, rc):

        utility = VehicleUtility()
 
        if rc == 0:

            
            print(f" \u2705 Conexão estabelecida, aguardando resposta...")
            client.subscribe("server/create_reservations/vehicle") # Realiza a inscrição para receber o dado esperado

        else:
            print(f" \u274C Falha na conexão. Código de retorno: {rc}")
            
            time.sleep(5)
            utility.clearTerminal()

            try:
                client.reconnect() # Tentando reconexão caso ocorra desconexão

            except Exception as e:
                print(" \u274C Erro ao tentar reconectar:", e)
                time.sleep(2)


    # Método on_message: Trata a mensagem recebida pelo(s) servidor(es)
    def on_message(self, client, userdata, msg):

        payload = msg.payload.decode()
        print(" Mensagem recebida:", repr(payload))
        time.sleep(30)

        self.message = json.loads(msg.payload.decode())


        if type(self.message) == list:

            for r in self.message:
                self.cost += int(r['price'])
                self.reservations.append(r)
        
        elif type(self.message) == dict:

            error = self.message["error"]
            print("Erro ao realizar reserva. Tipo de erro: " + error)

    
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
