# 🚗🔋 Sistema de Gerenciamento de Recarga Distribuída de Veículos Elétricos (DistributedElectricCarsRechargingManager)

Projeto desenvolvido por **José Victor de Oliveira Correia** e **João Victor Macedo dos Santos Lima** no contexto do PBL 2 da Universidade Estadual de Feira de Santana (UEFS), no Departamento de Tecnologia.

## 📋 Descrição

Este projeto propõe o desenvolvimento de um sistema de reservas e recarga para veículos elétricos durante viagens de longa distância. A arquitetura do sistema simula a interação entre veículos e servidores distribuídos, utilizando tecnologias modernas como:

- Python
- MQTT (Mosquitto)
- API REST (Flask)
- Docker

O sistema é composto por dois principais componentes:

- **Cliente Veículo:** Responsável por enviar requisições de reserva de recarga.
- **Servidores Distribuídos:** Representam empresas de recarga em diferentes estados do Brasil.

## 🔧 Tecnologias Utilizadas

- **Python 3.13.2**
- **MQTT (paho-mqtt)**
- **Flask**
- **Docker e Docker Compose**
- **Faker (geração de dados)**
- **Multithreading com `threading.Lock()`**

## 🛠 Estrutura do Projeto

### Cliente (Veículo)

- `main.py` — Interface principal de interação com o usuário.
- `User.py` — Armazena dados do proprietário.
- `Vehicle.py` — Estrutura do veículo e métodos de manipulação.
- `VehicleUtility.py` — Métodos utilitários (ex: animações, normalizações).
- `VehicleClient.py` — Lógica de comunicação via MQTT com os servidores.
- `Dockerfile`, `docker-compose.yml`, `requirements.txt`
- `data.json`, `reservations.json` — Persistência de dados locais.

### Servidores

- `Server.py` — Implementação da API REST e lógica de reservas.
- `mqttFunctions.py` — Configuração do cliente MQTT.
- `Utils.py`, `RoutesFiles.py`, `ChargingStationsFile.py`, `ChargingPointsFile.py`, `ReservationsFile.py`, `ReservationHelper.py` — Utilitários e bancos de dados simulados (JSON).

## 🧪 Execução

### Pré-requisitos

- Docker e Docker Compose instalados
- Servidores Mosquitto rodando

### Instruções

1. Inicie os containers dos brokers e servidores:
   ```bash
   docker compose up --build
   ```
2. Em outro terminal, execute o cliente veículo:
   ```bash
   cd src/app/Vehicle
   docker compose run --rm vehicle
   ```

⚠️ O container `vehicle_client` exige modo interativo e não deve ser iniciado com `up`.
