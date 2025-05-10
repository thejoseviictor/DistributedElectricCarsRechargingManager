# Esta Classe é Responsável por Armazenar os Dados dos Pontos de Carregamento dos Postos de Recarga em um Arquivo ".json" na Nuvem.
# "Charging Point" é um Local de Carregamento Dentro de um Posto Específico, nos Carros a Combustão São Conhecidos como "Bombas".

import json
import os

class ChargingPointsFile:
    # Inicializando a Classe e seus Atributos:
    def __init__(self, json_file="charging_points.json"):
        self.json_file = json_file
        self.chargingPointsList = [] # Lista dos Pontos de Carregamento.
        self.readChargingPoints() # Recuperando os Dados do Arquivo ".json"

    # Lendo os Pontos de Carregamento no Arquivo ".json":
    def readChargingPoints(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r", encoding="utf-8") as file:
                self.chargingPointsList = json.load(file) # Salvando os Dados do Arquivo ".json" na Lista.
    
    # Procurando um Ponto de Carregamento de um Posto Específico:
    def findChargingPoint(self, chargingPointID: int, chargingStationID: int):
        # Percorrendo a Lista:
        for cp in self.chargingPointsList: # cp = Charging Point - Ponto de Carregamento.
            if cp["chargingPointID"] == chargingPointID:
                if cp["chargingStationID"] == chargingStationID:
                    return cp
        else:
            print(f"\nPonto de Carregamento com ID '{chargingPointID}', no Posto de Recarga '{chargingStationID}', Não Foi Encontrado!\n")
            return None

    # Listando os Pontos de Carregamento de um Posto, Cadastrados no Arquivo ".json":
    def listChargingPoints(self, chargingStationID: int):
        searchList = [] # Onde Serão Salvos os Pontos de um Posto Específico.
        for cp in self.chargingPointsList: # cp = Charging Point - Ponto de Carregamento.
            if cp["chargingStationID"] == chargingStationID:
                searchList.append(cp)
        return searchList # Retornando os Pontos de um Posto Específico

    # Salvando a Lista de Pontos de Carregamento no Arquivo ".json":
    def saveChargingPoints(self):
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(self.chargingPointsList, file, indent=4)

    # Atualizando os Dados de um Ponto de Carregamento de um Posto Específico:
    def updateChargingPoint(self, chargingPointID: int, chargingStationID: int, power: float, kWhPrice: float, availability: bool):
        updateStatus = False # Vai Salvar o Status da Atualização.
        cp = self.findChargingPoint(chargingPointID, chargingStationID) # Percorrendo a Lista de Pontos de Carregamento.
        if cp:
            cp["power"] = power # Potência do Carregador em kW.
            cp["kWhPrice"] = kWhPrice
            cp["availability"] = availability # "livre", "ocupado" ou "reservado".
            updateStatus = True
        # Exibindo as Mensagens de Status:
        if updateStatus:
            self.saveChargingPoints() # Salvando no Arquivo ".json".
            print(f"\nPonto de Carregamento com ID '{chargingPointID}', no Posto de Recarga '{chargingStationID}', Foi Atualizado com Sucesso!\n")
            return updateStatus # Retornando o Status.
        else:
            return updateStatus # Retornando o Status.
    
    # Gerando um ID para Novo Ponto de Carregamento:
    # Os IDs Não Podem Ser Iguais Para o Mesmo Posto de Recarga.
    # IDs Novos: Maior ID + 1.
    def generateChargingPointID(self, chargingStationID: int):
        startID = 1 # Um ID Inicial Que Será Usado Como Comparador.
        for cp in self.chargingPointsList:
            # Percorrendo Todos os Pontos de Carregamento do Mesmo Posto de Recarga Selecionado:
            if cp["chargingStationID"] == chargingStationID:
                # ID Maior ou Igual (Para o Primeiro ID dos Pontos de Carregamento):
                if cp["chargingPointID"] >= startID:
                    startID = cp["chargingPointID"] + 1
        return startID
    
    # Criando um Novo Ponto de Carregamento e Salvando no Arquivo ".json":
    def createChargingPoint(self, chargingStationID: int, power: float, kWhPrice: float, availabilty: bool):
        # Gerando o ID do Ponto de Carregamento:
        chargingPointID = self.generateChargingPointID(chargingStationID)
        # Salvando na Lista:
        self.chargingPointsList.append({
            "chargingPointID": chargingPointID, 
            "chargingStationID": chargingStationID, 
            "power": power, # Potência do Carregador em kW.
            "kWhPrice": kWhPrice,
            "availability": availabilty # "livre", "ocupado" ou "reservado".
            })
        self.saveChargingPoints() # Salvando no Arquivo ".json".
        print(f"\nPonto de Carregamento com ID '{chargingPointID}', no Posto de Recarga '{chargingStationID}', Foi Salvo com Sucesso!\n")
        return chargingPointID # Retornando o ID do Ponto de Carregamento Criado.
    
    # Removendo um Ponto de Carregamento do Arquivo ".json":
    def deleteChargingPoint(self, chargingPointID: int, chargingStationID: int):
        newChargingPointsList = [] # Lista de Backup dos Pontos de Carregamento.
        foundStatus = False # Salva o Status de Ponto de Carregamento Encontrado.
        for cp in self.chargingPointsList:
            # Atualizando o Status, Se o Ponto de Carregamento a Ser Removido For Encontrado na Lista:
            if cp["chargingPointID"] == chargingPointID and cp["chargingStationID"] == chargingStationID:
                foundStatus = True
            # Copiando os Pontos de Carregamento com ID e Posto de Recarga Diferentes para uma Nova Lista:
            else:
                newChargingPointsList.append(cp)
        self.chargingPointsList = newChargingPointsList # Restaurando a Lista de Pontos de Carregamento.
        self.saveChargingPoints() # Salvando no Arquivo ".json".
        # Exibindo as Mensagens de Status:
        if foundStatus:
            print(f"\nPonto de Carregamento com ID '{chargingPointID}', no Posto de Recarga '{chargingStationID}', Foi Removido com Sucesso!\n")
            return foundStatus # Retornando o Status.
        else:
            print(f"\nPonto de Carregamento com ID '{chargingPointID}', no Posto de Recarga '{chargingStationID}', Não Foi Encontrado!\n")
            return foundStatus # Retornando o Status.
