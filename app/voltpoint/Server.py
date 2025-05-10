# Servidor da Empresa "VoltPoint", que Atua no Estado da Bahia --------

# Importando as Dependências:
from flask import Flask, request, jsonify # Para Criar a API do Servidor e Seus End-Points.
import requests # Para Comunicação com Outros Servidores.
from ReservationsFile import ReservationsFile # Que Manipula a Persistência de Dados das Reservas.

# Criando o Objeto das Reservas:
reservations = ReservationsFile()

# Criando a Aplicação Flask:
app = Flask(__name__) # "__name__" se tornará "__main__" ao executar.

# Criando a Rota para Ler as Reservas de um Veículo Específico:
@app.route('/reservation', methods=['GET'])
def read_reservations():
    vehicleID = request.args.get('vehicleID') # Salvando o ID Recebido com Parâmetro.
    foundedReservations = reservations.findReservation(int(vehicleID)) # Procurando pelas Reservas do Veículo.
    return jsonify(foundedReservations)

# Rodando o Servidor:
if __name__ == '__main__':
    app.run(debug=True)
