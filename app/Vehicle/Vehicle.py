from dataclasses import dataclass

from User import User
from VehicleUtility import VehicleUtility

import json
import os
import time

@dataclass
class Vehicle:

    vid: str
    owner: User
    licensePlate: str
    moneyCredit: float

    currentEnergy: int
    criticalEnergy: int
    distanceFromDestination: int
    distanceFromChargingStation: int
    maximumBattery : int

    reservations = [] # Guarda as reservas

    base = os.path.dirname(os.path.abspath(__file__)) # Pgando o caminho absoluto do arquivo

    filePathData = os.path.join(base, "dataPath", "arquivo.json")# Variavel que guarda o caminho do arquivo "data.json"
    filePathReservations= os.path.join(base, "dataPath", "arquivo.json") # Variavel que guarda o caminho do arquivo "reservations.json"

    '''
    = os.path.abspath("data.json") 
    = os.path.abspath("reservation.json")
    os.path.join(os.path.dirname(__file__), "date.json"

    '''

    def showReservation(self):

        if self.reservations :

            print("Reservas efetuadas: \n")

            for r in self.reservations:
                
                print(" ---------------------------------------------- ")
                print(f" ID da reserva: {r['reservationID']} \n")
                print(f" ID do posto: {r['chargingStationID']} \n")
                print(f" ID do ponto de recarga: {r['chargingPointID']} \n")
                print(f" Potência do ponto de carregamento: {r['chargingPointPower']} \n")
                print(f" Preço por kWh: {r['kWhPrice']} \n")
                print(f" ID do veículo: {r['vehicleID']} \n")
                print(f" Início da recarga: {r['startDateTime']} \n")
                print(f" Fim da recarga: {r['finishDateTime']} \n")
                print(f" Duração : {r['duration']} \n")
                print(f" Preço : {r['price']} \n")
                print(" ---------------------------------------------- ")
        
        else:

            print("Não há reservas mo momento !")
            time.sleep(3)


    def savingLoginData(self):

            data = {
                
                "cpf" : self.owner.cpf ,
                "name" : self.owner.name ,
                "email" : self.owner.email ,
                "password" : self.owner.password ,
                "vid" : self.vid ,
                "licensePlate" : self.licensePlate ,
                "moneyCredit" : self.moneyCredit ,
                "currentEnergy" : self.currentEnergy ,
                "criticalEnergy" : self.criticalEnergy ,
                "maximumBattery" : self.maximumBattery

            }

            
            with open(self.filePathData, 'w') as f:
                json.dump(data, f, indent=4)

    def updateCredit(self, cost: float):

        credit: float
        credit = self.moneyCredit

        credit -= cost

        self.moneyCredit = credit

        with open(self.filePathData, 'r') as f:
            data = json.load(f)
                
        data["moneyCredit"] = credit

        with open(self.filePathData, 'w') as f:
            json.dump(data, f, indent=4)

    def loadingData(self):

        utility = VehicleUtility()

        try:

            with open(self.filePathData, 'r') as f:
                data = json.load(f)
                    
            self.owner.cpf = str(data["cpf"])
            self.owner.name = str(data["name"])
            self.owner.email = str(data["email"])
            self.owner.password = str(data["password"]) 
            self.vid = str(data["vid"])
            self.licensePlate = str(data["licensePlate"]) 
            self.moneyCredit = float(data["moneyCredit"])
            self.currentEnergy = int(data["currentEnergy"])
            self.criticalEnergy = int(data["criticalEnergy"])
            self.maximumBattery = int(data["maximumBattery"])
            
            with open(self.filePathReservations, 'r') as f:
                listReservations = json.load(f)

            self.reservations = listReservations
        
        except (json.JSONDecodeError, FileNotFoundError):
            print("Não a uma conta registrada, registre-se !")
            time.sleep(5)
            utility.clearTerminal()

    def keepReservations(self, newReservations: list[dict]):

        with open(self.filePathReservations, 'r') as f:
              data = json.load(f)
        
        for r in newReservations:
            self.reservations.append(r)
            data.append(r)
        
        with open(self.filePathReservations, 'w') as f:
            json.dump(data, f, indent=4)
        
        

        
        
        
