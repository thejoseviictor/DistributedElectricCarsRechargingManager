# ElectricCarsRechargingManager

# Arquitetura do Veículo:

<br><br> O sistema e conexão cliente do contêiner “Veículo”, implementado no arquivo “main.py” <br><br> através do “socket” em Python, é responsável simular o sistema de um veículo elétrico, <br><br>sua conta de usuário com as informações necessárias  e estabelecer comunicação com o <br><br>servidor “Nuvem” quando necessário.


# Estrutura de arquivos do Veículo:

## 1. main.py (main Vehicle):

<br><br>É a classe de início do sistema, nela há a estruturação de uma interface de interação <br><br>amigável ao usuário. Através do conceito POO, os processos foram divididos em classes e os <br><br>devidos objetos responsáveis pela lógica de comunicação, pela formatação e exibição de <br><br>dados, preenchimento e geração de informações e o fluxo geral do sistema são formados <br><br>nesse arquivo.

## 2. User.py

<br>Classe responsável por guardar as informações do proprietário do veículo. As variáveis que a <br>compõem são: 

<br><br>. cpf : CPF do proprietário;
<br><br>. name: Nome do proprietário;
<br>. email: Email do proprietário;
<br>. password: Senha de acesso do proprietário no sistema.

<br>Com exceção da variável “name”, as outras 3 são utilizadas para realizar o processo de login <br>de usuário na “main.py”, onde a informação login pode ser identificada pelo cpf ou email e a <br>senha por password, respectivamente.

## 3. Vehicle.py

<br>É a classe responsável por estruturar as informações do veículo. As variáveis e métodos <br>existentes são:

<br><br>Variáveis:
<br><br>. vid: ID do veículo;
<br><br>. owner: Proprietário do veículo;
<br><br>. licensePlate: Número de placa do veículo;
<br><br>. moneyCredit: Crédito do veículo;
<br><br>. currentEnergy: Energia atual do veículo;
<br><br>. criticalEnergy: Porcentagem de energia definida como crítica;
<br><br>. distanceFromDestination: Distância até o trajeto do veículo;
<br><br>. distanceFromChargingStation: Distância até o posto mais próximo;
<br><br>. maximumBattery : Capacidade máxima da bateria do veículo;
<br><br>. coordinates: Lista para guardar as coordenadas do veículo;
<br><br>. reservations: Lista responsável por guardar as reservas realizadas entre o posto e <br><br>veículo.

<br><br>Métodos: 

<br><br>. definePosition: Responsável por guardar as coordenadas na lista “coordinates”;
<br><br>. archiveReservation: Responsável por guardar as reservas;
<br><br>. showReservation: Responsável por exibir todas as reservas feitas com o tempo.

## 4. VehicleUtility.py

<br>Classe responsável por ter métodos de utilidade para o sistema, os  seus métodos são:
<br><br>. defineCoordinates: Gera 2 coordenadas aleatórias para o veículo;
<br><br>. simulation: Simula o processo de gasto de bateria e pedido de reserva para a nuvem;
<br><br>. clearTerminal: Realiza a limpeza do terminal, com o objetivo de deixar o fluxo de <br><br> exibição mais fluida e menos poluído;
<br><br>. endAnimation: Gera uma pequena animação de encerramento do sistema. 

## 5. VehicleClient.py 

<br>Classe responsável pela comunicação entre cliente Veículo e servidor Nuvem. Os métodos e <br>veículos  são: 

<br><br>Variáveis:

<br>. server_host: Host do server Nuvem
<br>. server_port: int: Porta do server Nuvem

<br><br>Métodos: 

<br><br>. sendRequest: Responsável por estabelecer a comunicação  socket TCP/IP, enviar e receber <br><br>as informações pertinentes através de arquivos JSON.

## 6. Dockerfile e docker-compose.yml: 

<br>Dockerfile é o arquivo utilizado como para estruturar a imagem do container do sistema e o <br>docker-compose.yml é utilizado para estruturar um roteiro de execução desse container 

<br><br>. A imagem base utilizada foi "python:3.13.2";
<br><br>. Os arquivos para gerar a imagem são copiadas do diretório "src/Vehicle";
<br><br>. O arquivo principal a ser executado é "main.py";
<br><br>. O nome do container do servidor será "vehicle_client";
<br><br>. A variável de ambiente “SERVER_HOST=cloud” e “SERVER_PORT=64352” foram definidas para <br><br>importação e estabelecer a comunicação com o servidor;
<br><br>. A rede ao qual o cliente estará conectado é "recharging_manager";
<br><br>. “stdin_open”  e  “tty” são definidos como true para permitir a execução do sistema de <br><br>modo interativo (-it).

<br>Para executar o docker-compose.yml é preciso executá-lo com o seguinte roteiro:
<br><br>. docker network create recharging_manager
<br><br>. docker compose run --rm vehicle
<br><br>obs:
<br><br>. Caso a network já esteja estabelecida, o passo 1 pode ser ignorado;
<br><br>. O passo 2 não pode ser substituído por docker compose up –build pois, o container <br><br>vehicle_client depende do modo interativo para funcionar corretamente, e o passo citado <br><br>acima não permite esse modo;
<br><br>. Tenha certeza que os outros containers (Posto e Nuvem) estejam sendo executados <br><br>anteriormente para que a comunicação e a troca de informações ocorra corretamente;
<br><br>O passo 2 deve ser executado diretamente do diretório onde se encontra.

