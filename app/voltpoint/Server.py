# Servidor da Empresa "VoltPoint", que Atua no Estado da Bahia --------

# Importando as Dependências:
import os # Para Usar Variáveis de Ambiente.
from flask import Flask, request, jsonify # Para Criar a API do Servidor e Seus End-Points.
import json # Para Printar os Erros.
import requests # Para Comunicação com Outros Servidores.
from requests.exceptions import RequestException, ConnectionError, Timeout, HTTPError # Exceções Para Problemas de Conexão.
import urllib3
from ReservationsFile import ReservationsFile # Que Manipula a Persistência de Dados das Reservas.
from ChargingStationsFile import ChargingStationsFile
import ReservationHelper

# Salvando o Nome da Empresa:
companyName = "VoltPoint"

# Criando o Objeto das Reservas no Banco de Dados:
reservationsData = ReservationsFile()

# Criando o Objeto dos Postos de Recarga no Banco de Dados:
chargingStationsData = ChargingStationsFile()

# Criando a Aplicação Flask:
app = Flask(__name__) # "__name__" se tornará "__main__" ao executar.

def sendReservationsToOtherServers(data: json, reservationsRoute: list):
    try:
        # As Informações das Reservas Realizadas Irão Retornar Recursivamente:
        otherCompanyName = reservationsRoute[0]["company"] # Nome da Outra Empresa da Primeira Cidade da Rota.
        print("Redirecionando a Solicitação...\n")
        OTHER_SERVER_IP = os.environ.get(f'{otherCompanyName.upper()}_SERVER_IP')
        OTHER_SERVER_PORT = os.environ.get(f'{otherCompanyName.upper()}_SERVER_PORT')
        otherServerReservations = requests.post(f'http://{OTHER_SERVER_IP}:{OTHER_SERVER_PORT}/reservation', json=data)
        return otherServerReservations # Retornando a Resposta do Outro Servidor.
    # Tratando as Exceções:
    except urllib3.exceptions.NewConnectionError:
        return jsonify({"error": "Não Há Caminho Até o Servidor!"}), 502 # Erro 502: Bad Gateway.
    except (urllib3.exceptions.MaxRetryError, ConnectionError):
        return jsonify({"error": "Servidor Alvo Está Indisponível!"}), 503 # Erro 503: Service Unavailable.
    except Timeout:
        return jsonify({"error": "Timeout!"}), 504 # Erro 504: Gateway Timeout.
    except HTTPError as e:
        status_code = e.response.status_code if e.response else 500 # Erro do HTTP ou Erro Genérico.
        reason = e.response.reason if e.response else "Erro Desconhecido" # Razão do Erro ou Razão Desconhecida.
        return jsonify({"error": f"Erro HTTP: '{reason}'"}), status_code
    except RequestException:
        return jsonify({"error": "Erro Genérico!"}), 500 # Erro 500: Internal Server Error.

# Agendando as Reservas de um Veículo Específico, de Acordo com a Rota (Servidor-Servidor):
@app.route('/reservation', methods=['POST'])
def create_reservation():
    data = request.json # Recebendo os Dados em um Dicionário: data = {vehicleID: int, actualBatteryPercentage: int, batteryCapacity: float, reservationsRoute: list}.
    vehicleID = data.get('vehicleID') # ID do Veículo.
    actualBatteryPercentage = data.get('actualBatteryPercentage') # Porcentagem Atual de Bateria do Veículo.
    batteryCapacity = data.get('batteryCapacity') # Capacidade de Bateria do Veículo em kWh.
    reservationsRoute = data.get('reservationsRoute') # A Rota das Reservas.
    # Verificando Se Existem Reservas Solicitadas na Lista de Rotas para Reservas:
    if not reservationsRoute:
        print("Erro: A Lista da Rota das Reservas Está Vazia!\n")
        return jsonify({"error": "A Lista da Rota das Reservas Está Vazia!"}), 400  # Erro 400: Bad Request - Dados Enviados Errados ou Incompletos.
    bookedReservations = [] # Onde Serão Salvas Todas as Reservas Realizadas, Deste Servidor e dos Outros.
    # Se a Primeira Cidade da Lista de Rotas de Reservas Não For Administrada Por Este Servidor
    # a Lista de Reservas Será Repassada Para o Servidor Correto:
    if reservationsRoute[0]["company"] != companyName.lower():
        otherServerReservations = sendReservationsToOtherServers(data, reservationsRoute)
        # Se Não Conseguir Reservas em Outros Servidores, Nenhum Reserva Será Realizada:
        if 400 <= otherServerReservations.status_code < 500:
            print(f"Erro '{otherServerReservations.status_code}': {otherServerReservations.json().get('error')}\n") # Exibindo a Mensagem de Erro Recebida.
            return jsonify({"error": "Não Foi Possível Conseguir Reservas nos Outros Servidores!"}), 400  # Erro 400: Bad Request - Dados Enviados Errados ou Incompletos.
        else:
            bookedReservations.append(otherServerReservations) # Concatenando as Reservas Realizadas nos Outros Servidores.
            return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).
    # Exibindo as Informações das Reservas Solicitadas:
    print(f"Dados do Veículo '{vehicleID}' Recebidos para Reservas em:\n")
    for city in reservationsRoute:
        print(f"Cidade: {city['name']} | Empresa: {city['company']}\n")
    # Copiando as Reservas Destinadas a Esta Empresa:
    serverReservations = [city for city in reservationsRoute if city["company"] == f"{companyName.lower()}"] # Reservas Para Este Servidor.
    # Removendo as Reservas Destinadas a Esta Empresa da Lista Que Será Passada Para os Outros Servidores:
    reservationsRoute = [city for city in reservationsRoute if city["company"] != f"{companyName.lower()}"] # Reservas Para os Outros Servidores.  
    # Verificando Se Existem Postos de Recarga Cadastrados Neste Servidor:
    if not chargingStationsData.chargingStationsList:
        print("Erro: Não Existem Postos de Recarga Cadastrados Neste Servidor!\n")
        return jsonify({"error": "Não Existem Postos de Recarga Cadastrados Neste Servidor!"}), 404  # Erro 404: Not Found - Recurso Não Encontrado.
    # Realizando as Reservas Deste Servidor.
    # Procurando os Postos de Recarga Que Atuam nas Cidades:
    for cs in chargingStationsData.chargingStationsList:
        for city in serverReservations:
            if cs["city_codename"] == city["codename"]:
                chargingStationID = cs["chargingStationID"] # Salvando o ID do Posto de Recarga.
                chargingPointID = ReservationHelper.chooseChargingPoint(chargingStationID) # Procurando um Ponto de Carregamento no Posto de Recarga.
                # Verificando Se Um Ponto de Carregamento Foi Encontrado:
                if not chargingPointID:
                    print("Erro: Não Existem Pontos de Carregamento Cadastrados Neste Servidor!\n")
                    return jsonify({"error": "Não Existem Pontos de Carregamento Cadastrados Neste Servidor!"}), 404  # Erro 404: Not Found - Recurso Não Encontrado.
                else:
                    # Realizando uma Reserva na Cidade:
                    currentReservation = reservationsData.createReservation(chargingStationID, chargingPointID, vehicleID, actualBatteryPercentage, batteryCapacity)
                    # Verificando Se a Reserva Foi Realizada:
                    if not currentReservation:
                        print(f"Não Foi Possível Realizar a Reserva em '{city["name"]}' Para o Veículo '{vehicleID}'\n")
                        return jsonify({"error": f"Não Foi Possível Realizar a Reserva em '{city["name"]}' Para o Veículo '{vehicleID}"}), 404
                    else:
                        bookedReservations.append(currentReservation) # Salvando a Reserva Realizada na Cidade na Lista de Reservas.
    # Retornando as Reservas, Se Não Houveram Mais Reservas Para Outros Servidores:
    if not reservationsRoute:
        return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).
    # Repassando as Reservas dos Outros Servidores:
    else:
        otherServerReservations = sendReservationsToOtherServers(data, reservationsRoute)
        # Se Não Conseguir Reservas em Outros Servidores, Nenhum Reserva Será Realizada:
        if 400 <= otherServerReservations.status_code < 500:
            print(f"Erro '{otherServerReservations.status_code}': {otherServerReservations.json().get('error')}\n") # Exibindo a Mensagem de Erro Recebida.
            return jsonify({"error": "Não Foi Possível Conseguir Reservas nos Outros Servidores!"}), 400  # Erro 400: Bad Request - Dados Enviados Errados ou Incompletos.
        else:
            bookedReservations.append(otherServerReservations) # Concatenando as Reservas Realizadas nos Outros Servidores.
            return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).

# Criando a Rota para Ler as Reservas de um Veículo Específico (Servidor-Servidor):
@app.route('/reservation', methods=['GET'])
def read_reservations():
    vehicleID = request.args.get('vehicleID') # Salvando o ID Recebido com Parâmetro.
    print(f"ID do Veículo Recebido: {vehicleID}\n")
    foundedReservations = reservationsData.findReservations(int(vehicleID)) # Procurando pelas Reservas do Veículo.
    return jsonify(foundedReservations), 200 # Retornando Sucesso (200).

# Criando a Rota para Excluir uma Reserva de um Veículo Específico (Servidor-Servidor):
@app.route('/reservation', methods=['DELETE'])
def delete_reservation():
    data = request.json # Recebendo os Dados em JSON.
    reservationID = data.get('reservationID') # Salvando o ID da Reserva, Recebido pelo JSON.
    chargingStationID = data.get('chargingStationID') # Salvando o ID do Posto de Recarga, Recebido pelo JSON.
    chargingPointID = data.get('chargingPointID') # Salvando o ID do Ponto de Carregamento, Recebido pelo JSON.
    vehicleID = data.get('vehicleID') # Salvando o ID do Veículo, Recebido pelo JSON.
    print(f"\nDados Recebidos para Reserva: {data}\n")
    deleteStatus = reservationsData.deleteReservation(reservationID, chargingStationID, chargingPointID, vehicleID)
    return jsonify(deleteStatus), 200 # Retornando Sucesso (200).

# Rodando o Servidor no IP da Máquina:
if __name__ == '__main__':
    SERVER_IP = os.environ.get(f'{companyName.upper()}_SERVER_IP') # IP Definido no Docker-Compose.
    SERVER_PORT = int(os.environ.get(f'{companyName.upper()}_SERVER_PORT')) # Porta Definida no Docker-Compose.
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)
