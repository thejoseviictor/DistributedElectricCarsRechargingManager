'''
Grupo: João Macedo, José Vitor

Componente Curricular: TEC502 - MI - Concorrência e conectividade 

Concluido em: 11/04/2025;

Declaro que este código foi elaborado por mim e pelo meu grupo de forma individualmente 
e não contém nenhum trecho de código de outro colega ou de outro autor, tais como provindos 
de livros e  apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de 
código de outra autoria que não a minha está destacado com uma citação para o autor e a fonte 
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

'''

''' Classe main do veiculo'''

#--------------------------------------------------------------------------------------------------------------

from faker import Faker # Biblioteca utilizada para a geração de dados fictícios

import time # Biblioteca usada para fluxos e simulações de tempo
import random # Biblioteca usada para gerar dados e valores aleatórios
import re  # Biblioteca que permite buscas, substituições e manipulação em str

import sys # Bibliotecas usadas para trabalhar com caminhos, fluxo entre diretórios e entradas 
import os  # e saidas diretamente com o sistema/terminal
from pathlib import Path

import turtle
import json # Biblioteca usada para trabalhar com arquivos .json e importar dados fictícios para o sistema


#--------------------------------------------------------------------------------------------------------------

# Importação de classes base para o funcionamnto do sistema:

from Vehicle import Vehicle
from VehicleUtility import VehicleUtility
from User import User
from VehicleClient import VehicleClient

#--------------------------------------------------------------------------------------------------------------

# Variaveis usadas para fluxo entre caminhos e diretórios de pastas e arquivos de persistência de dados

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))) # Adiciona dinamicamente o diretório absoluto em sys.path

BASE_DIR = Path(__file__).resolve().parent # Caminho do script "main.py"
DATA_PATH = BASE_DIR / 'dataPath' # Caminho da pasta "dataPath"

#Definindo o caminho de cada arquivo de dados
dataFilePath = DATA_PATH / 'data.json'
reservationsFilePath = DATA_PATH / 'reservations.json'
brokersFilePath = DATA_PATH / 'brokers.json'

# Métodos utilitários --------------------------------------------------------------------------

''' Classe de utilidades, nela há a chamada para processos de comunicação,
    processos de exibição amigável ao úsuario e entre outro processos
'''
utility = VehicleUtility() 

#------------------------------------------------------------------------------------------------

# Início do sistema

repeat = True # Variavel usada para lidar com o fluxo de repetição do programa
firstLogin = True # Variavel para indicar que apenas um login é preciso.

while(repeat):

    utility.clearTerminal()

    utility.startAnimation() # Função para gerar uma pequena animação de inicio do programa
    
    print(" Bem vindo(a)! \n")
    time.sleep(2)

    wrongOption = True # Variavel para determinar se o 

    while wrongOption:

        userType = input("\t 1 - LOGIN / ENTRAR NA CONTA \n \t 2 - CRIAR CONTA \n\t ->")
        utility.clearTerminal()

        wrongData = True  # Váriavel usada para permitir ou não a entrada no sistema de acordo com os dados de login e senha

        if userType == "1" :
            
            #Criando template das 2 classes, para serem preenchidas com os dados 
            ownerTemplate = User(cpf="", name="", email="", password="")
            vehicle = Vehicle( vid= "", owner=ownerTemplate, licensePlate="", moneyCredit=0.0, currentEnergy=0, criticalEnergy=0, distanceFromDestination=0, distanceFromChargingStation=0, maximumBattery=0)
            
            vehicle.loadingData(dataFilePath, reservationsFilePath)


            if firstLogin :

                '''
                Os dados são carregados de data.json, a partir da ultima geração de dados ficticios
                obs: O arquivo "data.json" tem os dados salvos
                '''
                #------------------------------------------------------------------------------------
                
                while(wrongData):

                    print(vehicle.owner.__dict__) # Printando as informações necessárias para LOGIN
                    login = input("\n LOGIN (CPF ou Email): \t ")
                    utility.clearTerminal()

                    print(vehicle.owner.__dict__)
                    password = input("\n SENHA: ")
                    utility.clearTerminal()


                    if (login == vehicle.owner.cpf or login == vehicle.owner.email) and password == vehicle.owner.password:
                        print (" Login realizado com sucesso ! ")
                        time.sleep(3)
                        utility.clearTerminal()
                        wrongData = False
                        firstLogin = False

                    else :
                        print(" Login ou senha incorreta. Tente novamente !")
                        time.sleep(3)
                        utility.clearTerminal()
                        wrongData = True

            wrongOption = False

        elif userType == "2" :

            # Definindo os objetos e as suas informações:

            fake = Faker("pt_BR") # Biblioteca usada para gerar dados aleatórios para usuário e veiculo
            
            # User ----------------------------------------------------------------------------------------------------------------

            cpf = re.sub(r'\D', '', fake.cpf())
            

            genericFirstName = fake.first_name()
            genericLastName = fake.last_name()
            name = genericFirstName + " " + genericLastName
            

            # Lista e variavel para determinar um domínio aleatório para o email
            genericDomain = ["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com", "@bol.com"]
            randomDomain = random.randint(0,4)

            email = re.sub(r"\s+", "", genericFirstName.lower() + "." + genericLastName.lower() + genericDomain[randomDomain])

            # Senha aleatória 
            password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
            # Parâmetros: Tamanho(8), caracteres especiais(s), números(s), letras maiusculas(s), letras minusculas(s)

            user = User(cpf = cpf, name = name, email = email , password = password)


            # Vehicle -------------------------------------------------------------------------------------------------------------

            genericID = random.randint(1,99999) # Gera um ID aleatório de 5 dígitos para o veículo
            vid = str(genericID).zfill(5)

            owner = user
            licensePlate = fake.license_plate()
            moneyCredit = round(10000, 2) # O valor de crédito do veiculo inicia com R410.000
            currentEnergy = 100
            criticalEnergy = 20 # Foi definido que a energia critica do veículo é 20%

            maximumBattery = random.randint(30,50) # A capacidade máxima da bateria é gerada aleatoriamente entre o valor de 30 a 50 (kWh) 

            vehicle = Vehicle(vid = vid, owner = owner, licensePlate = licensePlate, moneyCredit = moneyCredit, currentEnergy = currentEnergy, criticalEnergy = criticalEnergy, distanceFromDestination = 0, distanceFromChargingStation = 0, maximumBattery = maximumBattery)

            # ---------------------------------------------------------------------------------------------

            reservations = []

            with open(reservationsFilePath, 'w') as f: # Limpando as reservas da conta anterior do arquivo "reservations.json" 
                json.dump(reservations, f, indent=4)

            # ---------------------------------------------------------------------------------------------
        
            vehicle.savingLoginData(dataFilePath) # Salvando os dados pertinentes
            # obs: O arquivo "data.json" tem os dados salvos

            # ---------------------------------------------------------------------------------------------
            
            wrongOption = False
            
        else :
            print("Digite uma opção válida !")
            wrongOption = True

    print(" O que deseja fazer? \n")
    reply = input(" Digite: \n\t 1. Fazer reserva \n\t 2. Ver histórico de reservas \n\t 3. Voltar para o inicio \n\t 4. Sair do programa \n\t -> ")
    utility.clearTerminal()

    '''
    Apresenta 3 opções de execução do programa:
    
    1. A opção 1 é para realizar a reserva, onde a origem e o destino da viagem é determinado e passado para o servidor via comunicação MQTT

    2. A opção 2 é usada para ver a(s) reserva(s) do veículo já realizadas
    
    obs: Dentro da opção 2, após ver a reserva, há a opção de voltar para o início o encerrar o programa definitivamente

    3. A opção 3 é para encerrar o sistema completamente. 

    '''

    if reply == "1" :

        wrongCities = True

        while wrongCities:

            utility.clearTerminal()

            print("\t Digite o local de origem: \n")
            origin = input("\t 1 - Vitória da Conquista \n \t 2 - Jequié \n \t 3 - Feira de Santana \n \t 4 - Euclides da Cunha \n \t 5 - Ibó \n \t 6 - Barro \n \t 7 - Jaguaribe \n \t 8 - Russas \n \t 9 - Fortaleza  \n \t  ->")
            
            utility.clearTerminal()

            print("\t Digite o local de destino: \n")
            destination = input("\t 1 - Vitória da Conquista \n \t 2 - Jequié \n \t 3 - Feira de Santana \n \t 4 - Euclides da Cunha \n \t 5 - Ibó \n \t 6 - Barro \n \t 7 - Jaguaribe \n \t 8 - Russas \n \t 9 - Fortaleza  \n \t  ->")
            
            utility.clearTerminal()

            route = utility.defineRoute(origin, destination)

            if route == False:
                print("\t Digite dados validos ! ")

                time.sleep(3)
                utility.clearTerminal()

                wrongCities = True

            else:
                wrongCities = False

        vClient = VehicleClient()
        vClient.connectMQTT()
        vClient.sendRequest(vehicle, route)
        realized = vClient.waitInformation(vehicle)

        if realized == True:
            print("Reserva realizada !")
            repeat = True

        else:
            print("Reserva não realizada!")
            repeat = True
            time.sleep(3)

    
    elif reply == "2" :

        vehicle.showReservation()

        reply = input("\n O que deseja agora: \n 1. Voltar para o início. \n 2. Fechar programa. \n ->")

        if reply == "1" :
            repeat = True
            utility.clearTerminal()

        else:
            repeat = False
            utility.endAnimation()

    elif reply == "3":
        repeat = True

    elif reply == "4":
        repeat = False
        utility.endAnimation()

    else:
        utility.clearTerminal()
        print("Digite uma opção válida !")
        time.sleep(3)
        
        