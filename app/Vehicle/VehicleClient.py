# Classe responsável pela comunicação entre cliente (Veículo) e servidor (Nuvem)


from dataclasses import dataclass
from Vehicle import Vehicle
from VehicleUtility import VehicleUtility

import paho.mqtt.client as mqtt
import os
import socket
import json
import time

@dataclass
class VehicleClient:
    
    serverHOST = 'localhost'
    serverPORT = 1883

    reservations = []
    cost: float

    # Método que inicia requisição de reserva, utilizando dados do veículo e as informações de origem e destino para envio por meio da comunicação MQTT
    def sendRequest(self, dataFilePath: str, vehicle: Vehicle, Route: list[str]):

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

        # Variaveis utilizadas para tratar a repetição e número de reconexões
        reconections = 0
        maxReconections = 3

        while reconections < maxReconections :

            try:

                client = mqtt.Client()
                client.connect(self.serverHOST, self.serverPORT, 60)

                print("Conexão ", reconections + 1, " : Conexão estabelecida com servidor ")
                time.sleep(2)
                utility.clearTerminal
                
                client.user_data_set(request)
                client.on_connect = self.receiveReservation
                utility.clearTerminal()
                client.on_message = self.waitInformation
                
                client.loop_forever()

                print("Reserva realizada !")
                time.sleep(2)

                vehicle.updateCredit(dataFilePath, self.cost, "-")


            except Exception as e:

                print("Conexão ", reconections + 1 , " : Erro de conexão com o server")
                time.sleep(1)
                utility.clearTerminal()
                reconections += 1
                

                if reconections == 3:
                    print("Falha nas " , reconections ,  "tentativas de conexão : Sistema indisponivel ")
                    time.sleep(2)
                    utility.clearTerminal()
                    break
            

    # Método "on_connect": Estabelece a comunicação com o servidor para receber as reservas realizadas pelo servidor(es)
    def receiveReservation(self, client, userdata, flags, rc, properties):

        utility = VehicleUtility()
 
        if rc == 0:

            client.publish("vehicle/create_reservations/server", userdata)
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
                time.sleep(5)



    def waitInformation(self, client, userdata, msg):
        
        self.cost = 0.0

        data = json.loads(msg.payload.decode())

        if type(data) == list:

            for r in data:
                cost += int(r['price'])
                self.reservations.append(r)
        
        elif type(data) == dict:

            error = data["error"]
            print("Erro ao realizar reserva. Tipo de erro: " + error)

        client.disconnect()

    def defineIP(self): # Método extra, para definir o IP (que define a região de qual servidor onde o veículo está)
        
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
