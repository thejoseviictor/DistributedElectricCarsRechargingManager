# Funções do MQTT do Servidor ---------------------------------------------------------------------------------------------------------------------------------------

# Importando as Dependências:
import os # Para Usar Variáveis de Ambiente.
import json # Para Printar os Erros.
import requests # Para Comunicação com Outros Servidores.
import paho.mqtt.client as mqtt # Funções do MQTT.
import time # Para o Loop de Tentativa de Conexão Com o Broker.
from Server import SERVER_IP, SERVER_PORT # IP e Porta do Servidor.
from Utils import handleHTTPExceptions # Exceções Para Problemas de Conexão.
import ReservationHelper # Funções para Gerar Parâmetros para Reservas.

# Salvando as Informações do MQTT:
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST') # Variável de Ambiente do Docker Compose.
MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT') # Variável de Ambiente do Docker Compose.
# Salvando os Tópicos "Subscriber" e "Publisher":
# Formato Reconhecido = "from/action/to"
MQTT_TOPICS_SUBSCRIBER = {
    "vehicle/create_reservations/server",
    "vehicle/get_reservations/server",
    "vehicle/delete_reservations/server"
}
MQTT_TOPICS_PUBLISHER = {
    "server/create_reservations/vehicle",
    "server/get_reservations/vehicle",
    "server/delete_reservations/vehicle"
}

# Descobrindo em Qual Tópico Publicar no MQTT:
def findPublisherTopic(action: str, destination: str):
    for topic in MQTT_TOPICS_PUBLISHER:
        topicParts = topic.split("/")
        if len(topicParts) == 3:
            if topicParts[1] == action and topicParts[2] == destination:
                return topic
    return None

# Função para Criar Reservas, Recebida por um Tópico do MQTT:
def mqttCreateReservations(client, action: str, vehicleData: dict):
    publisherTopic = findPublisherTopic(action, "vehicle") # Descobrindo em Qual Tópico Publicar.
    if publisherTopic:
        # Separando as Informações do Parâmetro em Variáveis:
        vehicleID = vehicleData["vehicleID"] # ID do Veículo.
        actualBatteryPercentage = vehicleData["actualBatteryPercentage"] # Porcentagem Atual de Bateria do Veículo.
        batteryCapacity = vehicleData["batteryCapacity"] # Capacidade de Bateria do Veículo em kWh.
        departureCityCodename = vehicleData["departureCityCodename"] # Apelido da Cidade de Partida.
        arrivalCityCodename = vehicleData["arrivalCityCodename"] # Apelido da Cidade de Destino.

        # Descobrindo a Rota da Cidade de Partida para a Cidade de Destino:
        reservationsRoute = ReservationHelper.chooseChargingStations(vehicleID, departureCityCodename, arrivalCityCodename, actualBatteryPercentage, batteryCapacity)

        # Formatando a Mensagem do Post para API:
        reservationsPost = {
            "vehicleID": vehicleID,
            "actualBatteryPercentage": actualBatteryPercentage,
            "batteryCapacity": batteryCapacity,
            "reservationsRoute": reservationsRoute
        }

        # Solicitando a Reserva Através da API Local do Servidor via HTTP:
        try:
            response = requests.post(f'http://{SERVER_IP}:{SERVER_PORT}/reservation', json=reservationsPost, timeout=5)
            # Verificando a Resposta da API:
            if response.ok: # Atalho Para os Status de Sucesso, de 200 até 300.
                result = response.json() # Convertendo a Resposta do Flask Para Dicionário.
                client.publish(publisherTopic, str(result)) # Enviando a Resposta no MQTT como String.
                print(f"Resposta Enviada Via MQTT: {result}\n")
            else:
                try:
                    errorMessage = response.json().get("error") # Copiando a Mensagem de Erro do HTTP.
                except ValueError:
                    errorMessage = "Erro Desconhecido"
                client.publish(publisherTopic, str({"error": errorMessage}))
                print(f"Erro na Solicitação HTTP ({response.status_code}): {errorMessage}\n")
        # Tratando as Exceções, Se o Servidor Não Responder:
        except Exception as e:
            response, status_code = handleHTTPExceptions(e)
            errorMessage = response.json().get("error")
            client.publish(publisherTopic, str({"error": errorMessage}))
            print(f"Exceção na Solicitação HTTP ({status_code}): {errorMessage}\n")

# Função para Ler as Reservas de um Veículo, Recebida por um Tópico do MQTT:
def mqttGetReservations(client, action: str, vehicleData: dict):
    pass

# Função para Excluir as Reservas de um Veículo, Recebida por um Tópico do MQTT:
def mqttDeleteReservations(client, action: str, vehicleData: dict):
    pass

# Usada Para Conectar ou Reconectar ao Broker:
def connectToBroker(client):
    while True:
        try:
            print("Tentando Conectar ao Broker...\n")
            client.connect(MQTT_BROKER_HOST, int(MQTT_BROKER_PORT), 60) # Conectando ao BROKER, Com "Keep Alive" (Avisos) de 60 Segundos.
            break
        except ConnectionRefusedError:
            print("Conexão Com o Broker Recusada! Tentando Novamente em 3 Segundos...\n")
            time.sleep(3)

# Função "callback" ao Conectar-se ao Broker MQTT:
def onConnect(client, userdata, flags, rc): # Assinatura Padrão da Função.
    if rc == 0:
        print("Conectado ao Broker Com Sucesso!\n")
    else:
        print(f"Falha na Conexão Com o Broker! Código de Retorno: {rc}\n")

# Função "callback" ao Perder Conexão Com o Broker MQTT:
def onDisconnect(client, userdata, rc):
    if rc != 0:
        print("Conexão Com o Broker Perdida!\n")
        client.loop_stop() # Finalizando o Loop da Conexão Anterior.
        connectToBroker(client)
        client.loop_start() # Iniciando o Loop de Recebimento das Mensagens.

# Função "callback" ao Receber uma Mensagem do MQTT:
def onMessage(client, userdata, message): # Assinatura Padrão da Função.
    # Manipulando a Mensagem:
    decodedMessage = message.payload.decode() # Decodificando a Mensagem, Convertendo Bytes em String.
    print(f"Mensagem MQTT Recebida: {decodedMessage}\n")
    jsonMessage = json.loads(decodedMessage) # Transformando a Mensagem em Dicionário.

    # Salvando o Tópico e Separando a Ação:
    topic = message.topic.split("/") # Salvando as Partes do Tópico em uma Lista: ["from", "action", "to"]
    if len(topic) == 3: # Formato de Tópico Conhecido: ["from", "action", "to"]
        topic_action = topic[1] # Salvando a Ação do Tópico.
    else:
        topic_action = "unknown" # Formato de Tópico Desconhecido.
    
    # Tópico de Criação de Reservas:
    if topic_action == "create_reservations":
        expectedKeys = ["vehicleID", "actualBatteryPercentage", "batteryCapacity", "departureCityCodename", "arrivalCityCodename"] # Chaves Esperadas na Mensagem.
        if all(key in jsonMessage for key in expectedKeys): # Verificando Se Todas as Chaves Estão Presentes.
            mqttCreateReservations(client, topic_action, jsonMessage) # Passando as Informações do Veículo Para a Função.
        else:
            missingKeys = [key for key in expectedKeys if key not in jsonMessage]
            print(f"O Agendamento das Reservas Foi Impedido, Pois Não Foram Enviadas as Seguintes Informações: {missingKeys}\n")
    
    # Tópico para Retornar as Reservas do Veículo:
    elif topic_action == "get_reservations":
        expectedKey = "vehicleID" # Chave Esperada na Mensagem.
        if expectedKey in jsonMessage: # Verificando Se a Chave Está Presente.
            mqttGetReservations(client, topic_action, jsonMessage) # Passando as Informações do Veículo Para a Função.
        else:
            print(f"Não Foi Possível Verificar as Reservas do Veículo, Pois a Seguinte Informação Não Foi Enviada: {expectedKey}\n")
    
    # Tópico para Excluir as Reservas do Veículo:
    elif topic_action == "delete_reservations":
        expectedKey = "vehicleID" # Chave Esperada na Mensagem.
        if expectedKey in jsonMessage: # Verificando Se a Chave Está Presente.
            mqttDeleteReservations(client, topic_action, jsonMessage) # Passando as Informações do Veículo Para a Função.
        else:
            print(f"Não Foi Possível Excluir as Reservas do Veículo, Pois a Seguinte Informação Não Foi Enviada: {expectedKey}\n")
    
    # Ação Desconhecida no Tópico:
    else:
        print(f"Ação Desconhecida no Tópico: {message.topic}\n")

# Configurando e Iniciando o MQTT:
def startMQTT():
    client = mqtt.Client() # Salvando o Cliente MQTT.
    client.on_connect = onConnect # Salvando a Função de "callback", Que Será Passada Como Parâmetro ao Conectar-se ao Broker.
    client.on_disconnect = onDisconnect # Salvando a Função de "callback", Que Será Passada Como Parâmetro ao Perder Conexão Com o Broker.
    client.on_message = onMessage # Salvando a Função de "callback", Que Será Passada Como Parâmetro ao Receber uma Mensagem.
    # Tentando Conectar ao Broker:
    connectToBroker(client)
    # Increvendo o Servidor nos Tópicos do MQTT:
    for topic in MQTT_TOPICS_SUBSCRIBER:
        client.subscribe(topic)
    client.loop_start() # Iniciando o Loop de Recebimento das Mensagens.
