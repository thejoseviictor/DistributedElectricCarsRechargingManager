# Esta Classe é Responsável por Armazenar os Dados dos Postos de Recarga da Empresa em um Arquivo ".json" no Servidor.
# "Charging Station" Representa as Unidades (Postos) de uma Empresa Específica.

import json
import os

class ChargingStationsFile:
    # Inicializando a Classe e seus Atributos:
    def __init__(self, json_file="charging_stations.json"):
        os.makedirs("data", exist_ok=True) # Criando a Pasta "data", Se Não Existir.
        self.json_file = os.path.join("data", json_file) # Salvando o Banco de Dados na Pasta "data".
        self.chargingStationsList = [] # Lista dos Postos de Recarga.
        self.readChargingStations() # Recuperando os Dados do Arquivo ".json"

    # Lendo os Pontos de Recarga no Arquivo ".json":
    def readChargingStations(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r", encoding="utf-8") as file:
                self.chargingStationsList = json.load(file) # Salvando os Dados do Arquivo ".json" na Lista.
    
    # Procurando um Posto de Recarga Específico:
    def findChargingStation(self, chargingStationID: int):
        self.readChargingStations() # Atualizando a Memória de Execução Com o Banco de Dados em "charging_stations.json".
        # Percorrendo a Lista:
        for cs in self.chargingStationsList:
            if cs["chargingStationID"] == chargingStationID:
                return cs
        else:
            print(f"Posto de Recarga com ID '{chargingStationID}' Não Foi Encontrado!\n")
            return None

    # Listando os Postos de Recarga Cadastrados no Arquivo ".json":
    def listChargingStations(self):
        self.readChargingStations() # Atualizando a Memória de Execução Com o Banco de Dados em "charging_stations.json".
        return self.chargingStationsList

    # Salvando a Lista no Arquivo ".json":
    def saveChargingStations(self):
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(self.chargingStationsList, file, indent=4)

    # Atualizando a Cidade de um Posto de Recarga Específico:
    def updateChargingStation(self, chargingStationID: int, city_codename: str, city_name: str):
        updateStatus = False # Vai Salvar o Status da Atualização.
        cs = self.findChargingStation(chargingStationID) # Chamando a Função de Procurar na Lista.
        if cs: # cs = Charging Station.
            cs["city_codename"] = city_codename
            cs["city_name"] = city_name
            updateStatus = True
        # Exibindo as Mensagens de Status:
        if updateStatus:
            self.saveChargingStations() # Salvando no Arquivo ".json".
            print(f"A Cidade do Posto de Recarga com ID '{chargingStationID}' Foi Alterada para '{city_name}' com Sucesso!\n")
            return updateStatus # Retornando o Status.
        else:
            return updateStatus # Retornando o Status.
    
    # Gerando um ID para Novo Posto de Recarga:
    # Os IDs Não Podem Ser Iguais.
    # IDs Novos: Maior ID + 1.
    def generateChargingStationID(self):
        startID = 1 # Um ID Inicial Que Será Usado Como Comparador.
        for cs in self.chargingStationsList:
            # ID Maior ou Igual (Para o Primeiro ID dos Postos de Recarga):
            if cs["chargingStationID"] >= startID:
                startID = cs["chargingStationID"] + 1
        return startID
    
    # Criando um Novo Posto de Recarga e Salvando no Arquivo ".json":
    def createChargingStation(self, city_codename: str, city_name: str):
        self.readChargingStations() # Atualizando a Memória de Execução Com o Banco de Dados em "charging_stations.json".
        chargingStationID = self.generateChargingStationID()
        # Salvando na Lista:
        self.chargingStationsList.append({
            "chargingStationID": chargingStationID, 
            "city_codename": city_codename, 
            "city_name": city_name})
        self.saveChargingStations() # Salvando no Arquivo ".json".
        print(f"Posto de Recarga com ID '{chargingStationID}' em '{city_name}' Foi Salvo com Sucesso!\n")
        return chargingStationID # Retornando o ID do Posto de Recarga Criado.
    
    # Removendo um Posto do Arquivo ".json":
    def deleteChargingStation(self, chargingStationID: int):
        self.readChargingStations() # Atualizando a Memória de Execução Com o Banco de Dados em "charging_stations.json".
        newChargingStationsList = [] # Lista de Backup dos Postos.
        foundStatus = False # Salva o Status de Posto de Recarga Encontrado.
        for cs in self.chargingStationsList:
            # Copiando os Postos de Recarga com ID Diferente para uma Nova Lista:
            if cs["chargingStationID"] != chargingStationID:
                newChargingStationsList.append(cs)
            # Atualizando o Status, Se o Posto a Ser Removido For Encontrado na Lista:
            else:
                foundStatus = True
        self.chargingStationsList = newChargingStationsList # Restaurando a Lista de Postos.
        self.saveChargingStations() # Salvando no Arquivo ".json".
        # Exibindo as Mensagens de Status:
        if foundStatus:
            print(f"Posto de Recarga com ID '{chargingStationID}' Foi Removido com Sucesso!\n")
            return foundStatus # Retornando o Status.
        else:
            print(f"Posto de Recarga com ID '{chargingStationID}' Não Foi Encontrado!\n")
            return foundStatus # Retornando o Status.
