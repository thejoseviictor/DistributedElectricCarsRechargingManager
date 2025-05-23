# DistributedElectricCarsRechargingManager

## Arquitetura de Sistema dos Servidores:
Os servidores são responsáveis por atender aos agendamentos de reservas para usuários de veículos elétricos em diferentes cidades do país. Através de uma requisição atômica, de servidor para servidor, sem centralização das reservas.
<br><br>Cada servidor pertence a uma empresa específica, que tem seus postos de recarga e que atua em algum estado do Brasil, atualmente: Bahia na empresa “VoltPoint”, Ceará na empresa “E-Flux” e Pernambuco na empresa “EcoCharge”.
<br><br>A lógica principal de cada servidor foi implementada em seu arquivo “Server.py”, através de uma API REST desenvolvida em Flask e comunicação peer-to-peer através do MQTT.
<br><br>A comunicação entre os servidores e os seus clientes (veículos) é realizada através de mensagens MQTT em tópicos de inscrição e publicação. Dessa maneira, os servidores atuam como subcribers, que recebem mensagens, e publishers, que publicam mensagens.
<br><br>Os servidores utilizam multithreading para lidar com a concorrência entre múltiplas conexões simultâneas, e bloqueios do tipo “threading.Lock()” nas funções de agendamento de reservas. Dessa maneira, cada nova requisição feita ao servidor pelo cliente, gera um novo thread para atendê-la. 

## Como Usar os Servidores:
Cada servidor tem o seu próprio Broker Mosquitto, que atuará como um intermediário entre as mensagens do cliente e do servidor, e que deve ser iniciado em um container Docker através do arquivo “docker-compose.yml” em “app/mosquitto”.
<br><br>Antes de iniciar a comunicação com o servidor, ele deve ser alimentado com os dados dos postos de recarga e pontos de carregamento da empresa ao qual ele pertence. Esses dados são armazenandos em um banco de dados nos arquivos “data/charging_stations.json” e “data/charging_points.json”.
<br><br>Cada servidor possui o seu “docker-compose.yml” dentro da sua respectiva pasta em “app”, que pode ser executado através do comando “docker compose up --build”.
<br><br>Antes de iniciar os servidores, indique para cada um deles os endereços IP dos outros, editando as variáveis de ambiente nos arquivos “docker-compose.yml” de cada servidor.

## Estrutura dos Arquivos dos Servidores:
### 1. Server.py:
Arquivo principal, onde está implementada a API REST, através do framework Flask, e a execução do MQTT.
<br><br>Contém a lógica da rota de criação de reservas, que recebe os dados para reservas através da função “on_message” do MQTT em “mqttFuncions.py”, ou de outros servidores, e realiza as manipulações necessárias para agendamento, como agendamento nos seus próprios postos ou redirecionamento para outros servidores, e o retorno das reservas, para serem enviadas via MQTT.

### 2. mqttFunctions.py:
Contém as funções de criação, configuração e inicialização do cliente MQTT, que é executado assincronamente, permitindo a reconexão, caso haja perda de conexão com o Broker Mosquitto. Além do bloqueio dos threads via “threading.Lock()”.

### 3. Utils.py:
Contém funções úteis para tratamento de exceções e redirecionamento de reservas para APIs de outros servidores.

### 4. RoutesFiles.py:
Responsável por criar, atualizar e excluir rotas, com cidades onde o veículo poderá trafegar, através do arquivo “data/routes.json”.
<br><br>Possui também uma função que gera uma rota de acordo com a cidade de partida e destino desejada pelo veículo.

### 5. ChargingStationsFile.py:
Responsável por armazenar, manipular e recuperar os dados dos postos de recarga do servidor, a partir do arquivo "data/charging_stations.json".

### 6. ChargingPointsFile.py:
Lógica semelhante ao arquivo “ChargingStationsFile.py”, porém armazena pontos de carregamento pertencentes a um posto de recarga específico.

### 7. ReservationsFile.py:
Um banco de dados de reservas do servidor no arquivo “data/reservations.json”.

### 8. ReservationHelper.py:
Responsável por calcular em quais cidades o veículo deve parar para recarregar e salvá-las em uma lista de cidades onde agendar reservas, de acordo com as especificações técnicas do veículo e a rota para trafegar escolhida pela função “findRoute” em “RoutesFiles.py”.
<br><br>Possui também uma função que escolhe um ponto de carregamento, para cada posto de recarga na rota de reservas, de acordo com a sua disponibilidade e fila.
