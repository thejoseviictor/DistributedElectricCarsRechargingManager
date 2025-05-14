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

    def __init__(self):
        self.client = None

    reservations = []
    defineServer: int

    nameCompanie: str
    serverIP: str
    serverPort: int


    def connectMQTT(self):
        
        reconections = 0
        maxReconections = 3

        while reconections < maxReconections :
                
            try:
                # Criando um client MQTT para o veículo
                self.client = mqtt.Client(userdata=self.reservations)
                self.client.connect(self.serverIP,self.serverPort)
                print("Conexão ", reconections + 1, " : Conexão estabelecida com servidor " + self.nameCompanies(self.defineServer))
                break

            except Exception as e:
                print("Conexão ", reconections + 1 , " : Erro de conexão com o server")
                reconections += 1
                time.sleep(2) 

                if reconections == 2: 
                    print("Falha nas " , reconections + 1 ,  "tentativas de conexão : Sistema indisponivel ")
        
    
    def sendRequest(self, vehicle: Vehicle, Route: list[str]): # Envia uma requisição e dados do client (Veículo) para o servidor (Nuvem).

        try:
            # Dicionário utilizado para selecionar os dados pertinentes para o servidor ao pedir a reserva
            vData = {
                "vehicleID": vehicle.vid ,
                "actualBatteryPercentage": vehicle.currentEnergy ,
                "batteryCapacity" : vehicle.maximumBattery ,
                "departureCityCodename" : Route(0) ,
                "arrivalCityCodename" : Route(1)
            }

            # Cria um json baseado no dicionário "vData" e envia as informações para o servidor correspondente.
            request = json.dumps(vData, indent=4).encode('utf-8')
            self.client.publish("topico/reservation", request)

        except Exception as e:
             print("Erro na reserva ou conexão indisponivel: " + e)
            


    def receiveReservation(self, client, userdata, msg):
 
        try:
            
            print("Conexão estabelecida, esperando resposta... ")
            client.subscribe("topico/answer")
            answer = json.loads(msg.payload.decode()) # transforma JSON string em lista de dicionarios

        except Exception as e:
            
            print(f"Erro na reserva ou conexão indisponivel:{type(e).__name__}: {e}")
            
          
        userdata.append(answer)

        self.client.disconnect()


    def waitInformation(self, vehicle: Vehicle):
        
        utility = VehicleUtility()

        self.client.on_message = self.receiveReservation(vehicle)
        self.client.subscribe("topico/answer")
        
        print("Aguardando resposta ...")
        self.client.loop_forever()

        time.sleep(2)
        utility.clearTerminal()

        vehicle.keepReservations(self.reservations)

        cost : float
        cost = 0

        for r in self.reservations:
            cost += r['price']

        vehicle.updateCredit(cost)

        return True

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

        print("IP: " + self.serverIP)
        print("IP: " + self.serverPort)
        time.sleep(6)