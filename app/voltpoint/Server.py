# Servidor da Empresa "VoltPoint", que Atua no Estado da Bahia -------------------------------------------------------------------------------------------------------

# Importando as Dependências:
import os # Para Usar Variáveis de Ambiente.
from flask import Flask, request, jsonify # Para Criar a API do Servidor e Seus End-Points.
import threading # Para Criar Múltiplas Instâncias.
from ReservationsFile import ReservationsFile # Que Manipula a Persistência de Dados das Reservas.
from ChargingStationsFile import ChargingStationsFile # Que Manipula a Persistência de Dados dos Postos de Recarga.
import ReservationHelper # Funções para Gerar Parâmetros para Reservas.
import mqttFunctions # Função para Configurar e Inicializar o MQTT.
from Utils import sendReservationsToOtherServers # Função Para Enviar Solicitações de Reservas Para Outros Servidores.

# Salvando o Nome da Empresa:
companyName = os.environ.get('COMPANY_NAME') # Variável de Ambiente do Docker Compose.

# Salvando o IP e Porta do Servidor Desta Empresa:
SERVER_IP = os.environ.get(f'{companyName.upper()}_SERVER_IP') # IP Definido no Docker-Compose.
SERVER_PORT = int(os.environ.get(f'{companyName.upper()}_SERVER_PORT')) # Porta Definida no Docker-Compose.

# Criando o Objeto das Reservas no Banco de Dados:
reservationsData = ReservationsFile()

# Criando o Objeto dos Postos de Recarga no Banco de Dados:
chargingStationsData = ChargingStationsFile()

# Criando a Aplicação Flask:
app = Flask(__name__) # "__name__" se tornará "__main__" ao executar.

# Rota Para Agendar as Reservas de um Veículo Específico, de Acordo com a Lista da Rota de Reservas (Servidor-Servidor):
@app.route('/reservation', methods=['POST'])
def createReservations():
    # Tratando os Dados Recebidos:
    data = request.json # Recebendo os Dados em um Dicionário: data = {vehicleID: int, actualBatteryPercentage: int, batteryCapacity: float, reservationsRoute: list}.
    vehicleID = data.get('vehicleID') # ID do Veículo.
    actualBatteryPercentage = data.get('actualBatteryPercentage') # Porcentagem Atual de Bateria do Veículo.
    batteryCapacity = data.get('batteryCapacity') # Capacidade de Bateria do Veículo em kWh.
    reservationsRoute = data.get('reservationsRoute') # A Rota das Reservas.

    # Verificando Se Existem Reservas Solicitadas na Lista de Rotas para Reservas:
    if not reservationsRoute:
        print("Erro: A Lista da Rota das Reservas Está Vazia!\n")
        return jsonify({"error": "A Lista da Rota das Reservas Está Vazia!"}), 400  # Erro 400: Bad Request - Dados Enviados Errados ou Incompletos.
    
    # Exibindo as Informações das Reservas Solicitadas:
    print(f"Dados do Veículo '{vehicleID}' Recebidos para Reservas em:\n")
    for city in reservationsRoute:
        print(f"Cidade: {city['name']} | Empresa: {city['company']}\n")
    
    bookedReservations = [] # Onde Serão Salvas Todas as Reservas Realizadas, Deste Servidor e dos Outros, Para Serem Retornadas.

    # Se a Primeira Cidade da Lista de Rotas de Reservas Não For Administrada Por Este Servidor
    # a Lista de Reservas Será Repassada Para o Servidor Correto:
    if reservationsRoute[0]["company"] != companyName.lower():
        response, status_code = sendReservationsToOtherServers(data, reservationsRoute)
        # Se Não Conseguir Reservas em Outros Servidores, Nenhum Reserva Será Realizada:
        if 400 <= status_code < 505:
            print(f"Erro '{status_code}': {response.get_json().get('error')}\n") # Exibindo a Mensagem de Erro Recebida.
            # Limpando as Reservas Realizadas no Servidor Atual:
            for rs in bookedReservations:
                reservationsData.deleteReservation(rs["reservationID"], rs["chargingStationID"], rs["chargingPointID"], rs["vehicleID"])
            # Retornando a Mensagem de Erro:
            return jsonify({"error": "Não Foi Possível Conseguir Reservas nos Outros Servidores!"}), status_code
        else:
            bookedReservations.append(response.get_json()) # Concatenando as Reservas Realizadas nos Outros Servidores.
            return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).
    
    # Copiando as Reservas Destinadas ao Servidor Desta Empresa:
    serverReservations = [city for city in reservationsRoute if city["company"] == f"{companyName.lower()}"] # Reservas Para Este Servidor.

    # Isolando as Reservas Destinadas aos Servidores das Outras Empresas:
    reservationsRoute = [city for city in reservationsRoute if city["company"] != f"{companyName.lower()}"] # Reservas Para os Outros Servidores.

    # Verificando Se Existem Postos de Recarga Cadastrados Neste Servidor:
    if not chargingStationsData.chargingStationsList:
        print("Erro: Não Existem Postos de Recarga Cadastrados Neste Servidor!\n")
        return jsonify({"error": "Não Existem Postos de Recarga Cadastrados Neste Servidor!"}), 404  # Erro 404: Not Found - Recurso Não Encontrado.
    
    # Realizando as Reservas Deste Servidor.
    # Procurando os Postos de Recarga Que Atuam nas Cidades Solicitadas:
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
                    currentReservation = reservationsData.createReservation(chargingStationID, chargingPointID, city["name"], city["codename"], companyName,
                                                                            vehicleID, city["actualBatteryPercentage"], batteryCapacity, city["timeToReach"])
                    # Verificando Se a Reserva Foi Realizada:
                    if not currentReservation:
                        print(f"Não Foi Possível Realizar a Reserva em '{city["name"]}' Para o Veículo '{vehicleID}'\n")
                        return jsonify({"error": f"Não Foi Possível Realizar a Reserva em '{city["name"]}' Para o Veículo '{vehicleID}"}), 404 # Erro 404: Not Found
                    else:
                        bookedReservations.append(currentReservation) # Salvando a Reserva na Lista de Reservas Que Será Retornada.
    
    # Retornando as Reservas, Se Não Houveram Mais Reservas Para Outros Servidores:
    if not reservationsRoute:
        return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).
    
    # Repassando as Reservas Que Sobraram Para os Outros Servidores:
    else:
        response, status_code = sendReservationsToOtherServers(data, reservationsRoute)
        # Se Não Conseguir Reservas em Outros Servidores, Nenhum Reserva Será Realizada:
        if 400 <= status_code < 505:
            print(f"Erro '{status_code}': {response.get_json().get('error')}\n") # Exibindo a Mensagem de Erro Recebida.
            # Limpando as Reservas Realizadas no Servidor Atual:
            for rs in bookedReservations:
                reservationsData.deleteReservation(rs["reservationID"], rs["chargingStationID"], rs["chargingPointID"], rs["vehicleID"])
            # Retornando a Mensagem de Erro:
            return jsonify({"error": "Não Foi Possível Conseguir Reservas nos Outros Servidores!"}), status_code
        else:
            bookedReservations.append(response.get_json()) # Concatenando as Reservas Realizadas nos Outros Servidores.
            return jsonify(bookedReservations), 200 # Retornando Todas as Reservas Realizadas Com Sucesso (200).

# Rota para Ler as Reservas de um Veículo Específico (Servidor-Servidor):
@app.route('/reservation', methods=['GET'])
def readReservations():
    vehicleID = request.args.get('vehicleID') # Salvando o ID Recebido com Parâmetro.
    print(f"ID do Veículo Recebido: {vehicleID}\n")
    foundedReservations = reservationsData.findReservations(int(vehicleID)) # Procurando pelas Reservas do Veículo.
    return jsonify(foundedReservations), 200 # Retornando Sucesso (200).

# Rota para Excluir uma Reserva de um Veículo Específico (Servidor-Servidor):
@app.route('/reservation', methods=['DELETE'])
def deleteReservations():
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
    # Iniciando o MQTT em Outra Thread:
    mqtt_thread = threading.Thread(target=mqttFunctions.startMQTT) # Configurando a Thread do MQTT.
    mqtt_thread.daemon = True # Thread "Daemon" Que Se Encerrará Junto Com o Servidor.
    mqtt_thread.start() # Iniciando a Thread do MQTT.

    # Iniciando o Servidor HTTP (Flask):
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True, threaded=True) # Threaded = O Flask Pode Tratar Múltiplas Requisições Ao Mesmo Tempo.
