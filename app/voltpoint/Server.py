# Servidor da Empresa "VoltPoint", que Atua no Estado da Bahia --------

# Importando as Dependências:
from flask import Flask, request, jsonify # Para Criar a API do Servidor e Seus End-Points.
import requests # Para Comunicação com Outros Servidores.
from ReservationsFile import ReservationsFile # Que Manipula a Persistência de Dados das Reservas.

# Criando o Objeto das Reservas:
reservations = ReservationsFile()

# Criando a Aplicação Flask:
app = Flask(__name__) # "__name__" se tornará "__main__" ao executar.

# Criando a Rota, Solicitada por Outro Servidor, para Criar uma Reserva para um Veículo Específico:
@app.route('/reservation', methods=['POST'])
def create_reservation():
    data = request.json # Recebendo os Dados em JSON.
    vehicleID = data.get('vehicleID') # Salvando o ID do Veículo, Recebido pelo JSON.
    actualBatteryPercentage = data.get('actualBatteryPercentage') # Salvando a Porcentagem de Bateria do Veículo, Recebido pelo JSON.
    batteryCapacity = data.get('batteryCapacity') # Salvando a Capacidade Total de Bateria do Veículo em kWh, Recebido pelo JSON.
    print(f"\nDados Recebidos para Reserva: {data}\n")

    chargingStationID = 1 # Precisa criar a lógica de escolha do posto.
    chargingPointID = 1 # Precisa criar a lógica de escolha do ponto.
    
    createdReservation = reservations.createReservation(chargingStationID, chargingPointID, vehicleID, actualBatteryPercentage, batteryCapacity)
    return jsonify(createdReservation)

# Criando a Rota, Solicitada por Outro Servidor, para Ler as Reservas de um Veículo Específico:
@app.route('/reservation', methods=['GET'])
def read_reservations():
    data = request.json # Recebendo os Dados em JSON.
    vehicleID = data.get('vehicleID') # Salvando o ID do Veículo, Recebido pelo JSON.
    print(f"\nDados Recebidos para Reserva: {data}\n")
    foundedReservations = reservations.findReservations(vehicleID) # Procurando pelas Reservas do Veículo.
    return jsonify(foundedReservations)

# Criando a Rota, Solicitada por Outro Servidor, para Excluir uma Reserva de um Veículo Específico:
@app.route('/reservation', methods=['DELETE'])
def delete_reservation():
    data = request.json # Recebendo os Dados em JSON.
    reservationID = data.get('reservationID') # Salvando o ID da Reserva, Recebido pelo JSON.
    chargingStationID = data.get('chargingStationID') # Salvando o ID do Posto de Recarga, Recebido pelo JSON.
    chargingPointID = data.get('chargingPointID') # Salvando o ID do Ponto de Carregamento, Recebido pelo JSON.
    vehicleID = data.get('vehicleID') # Salvando o ID do Veículo, Recebido pelo JSON.
    print(f"\nDados Recebidos para Reserva: {data}\n")
    deleteStatus = reservations.deleteReservation(reservationID, chargingStationID, chargingPointID, vehicleID)
    return jsonify(deleteStatus)

# Rodando o Servidor:
if __name__ == '__main__':
    app.run(debug=True)
