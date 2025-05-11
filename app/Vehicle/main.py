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

from faker import Faker # Biblioteca utilizada para a geração de dados fictícios
import time # Biblioteca usada para fluxos e simulações de tempo
import random # Biblioteca usada para gerar dados e valores aleatórios

'''
Bibliotecas usadas para trabalhar com o fluxo entre diretórios e entradas 
e saidas diretamente com o sistema/terminal
'''
import sys 
import os 

import json # Biblioteca usada para trabalhar com arquivos .json e importar dados fictícios para o sistema

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importação de classes base para o funcionamnto do sisteema
from Vehicle import Vehicle
from VehicleUtility import VehicleUtility
from User import User
from VehicleClient import VehicleClient

repeat = True # Variavel usada para lidar com o fluxo de repetição do programa

base = os.path.dirname(os.path.abspath(__file__)) # Pgando o caminho absoluto do arquivo
filePathReservations= os.path.join(base, "dataPath", "arquivo.json") # Variavel que guarda o caminho do arquivo "reservations.json"


# Métodos utilitários --------------------------------------------------------------------------

''' Classe de utilidades, nela há a chamada para processos de comunicação,
    processos de exibição amigável ao úsuario e entre outro processos
'''
utility = VehicleUtility() 

#------------------------------------------------------------------------------------------------


# Início do sistema

firstLogin = True # Variavel para indicar que apenas um login é preciso.

while(repeat):

    utility.clearTerminal()

    print(" ---------- veHI : Sistema de recarga para veículos elétricos ----------\n")
    
    time.sleep(3)
    utility.clearTerminal()

    print(" Bem vindo(a)! \n")
    time.sleep(2)

    userType = input("\t 1 - LOGIN / ENTRAR NA CONTA \n \t 2 - CRIAR CONTA \n")
    utility.clearTerminal()

    wrongDate = True  # Váriavel usada para permitir ou não a entrada no sistema de acordo com os dados de login e senha

    if userType == 1 :
        
        if(firstLogin):

            ''' 
            Os dados são carregados de data.json, a partir da ultima geração de dados ficticios
            obs: O arquivo "data.json" tem os dados salvos
            '''
            vehicle = Vehicle()
            vehicle.loadingData()

            #------------------------------------------------------------------------------------
            while(wrongDate):

                login = input("LOGIN (CPF ou Email): \t ")
                utility.clearTerminal()
                password = input("SENHA: \t ")
                utility.clearTerminal()


                if (login == vehicle.owner.cpf or login == vehicle.owner.email) and password == vehicle.owner.password:
                    print (" Login realizado com sucesso ! ")
                    time.sleep(3)
                    utility.clearTerminal()
                    wrongDate = False
                    firstLogin = False

                else :
                    print(" Login ou senha incorreta. Tente novamente !")
                    time.sleep(3)
                    utility.clearTerminal()
                    wrongDate = True
 
    if userType == 2 :

        # Definindo os objetos e as suas informações:

        fake = Faker("pt_BR") # Biblioteca usada para gerar dados aleatórios para usuário e veiculo
        
        # User ----------------------------------------------------------------------------------------------------------------

        cpf = fake.cpf(False) # Por padrão, .cpf() tem como paramêtro TRUE, o que determina o cpf com formatações(com . e -) 

        genericFirstName = fake.first_name()
        genericLastName = fake.last_name()
        name = genericFirstName + " " + genericLastName

        # Lista e variavel para determinar um domínio aleatório para o email
        genericDomain = ["@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com", "@bol.com"]
        randomDomain = random.randint(0,4)

        email = genericFirstName.lower() + "." + genericLastName.lower() + genericDomain(randomDomain)

        # Senha aleatória 
        password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
        # Parâmetros: Tamanho(8), caracteres especiais(s), números(s), letras maiusculas(s), letras minusculas(s)

        user = User(cpf = cpf, name = name, email = email , password = password)


        # Vehicle -------------------------------------------------------------------------------------------------------------

        genericID = random.randint(1,99999) # Gera um ID aleatório de 5 dígitos para o veículo
        vid = str(genericID).zfill(5)

        owner = user
        licensePlate = fake.license_plate()
        moneyCredit = round(random.uniform(100.0, 1000.0), 2)
        currentEnergy = 100
        criticalEnergy = 20 # Foi definido que a energia critica do veículo é 20%

        maximumBattery = random.randint(30,50) # A capacidade máxima da bateria é gerada aleatoriamente entre o valor de 30 a 50 (kWh) 

        vehicle = Vehicle(vid = vid, owner = owner, licensePlate = licensePlate, moneyCredit = moneyCredit, currentEnergy = currentEnergy, criticalEnergy = criticalEnergy, distanceFromDestination = 0, distanceFromChargingStation = 0, maximumBattery = maximumBattery)

        # ---------------------------------------------------------------------------------------------
        
        open(filePathReservations, "w").close() # Limpando as reservas da conta anterior do arquivo "reservations.json" 

        # ---------------------------------------------------------------------------------------------
    
        vehicle.savingLoginDates() # Salvando os dados pertinentes
        # obs: O arquivo "data.json" tem os dados salvos

        # ---------------------------------------------------------------------------------------------


    print(" O que deseja fazer? \n")
    reply = input(" Digite: \n 1. Fazer reserva \n 2. Ver histórico de reservas \n 3. Sair \n\n -> ")
    utility.clearTerminal()

    '''
    Apresenta 3 opções de execução do programa:
    
    1. A opção 1 é para realizar a reserva, onde a origem e o destino da viagem é determinado e passado para o servidor via comunicação MQTT

    2. A opção 2 é usada para ver a(s) reserva(s) do veículo já realizadas
    
    obs: Dentro da opção 2, após ver a reserva, há a opção de voltar para o início o encerrar o programa definitivamente

    3. A opção 3 é para encerrar o sistema completamente. 

    '''

    if reply == "1" :

        print("\t Digite o local de origem: \n")

        origin = input("\t 1 - Vitória da Conquista \n \t 2 - Jequié \n \t 3 - Feira de Santana \n \t 4 - Euclides da Cunha \n \t 5 - Ibó \n \t 6 - Barro \n \t 7 - Jaguaribe \n \t 8 - Russas \n \t 9 - Fortaleza  \n \t  ->")
        utility.clearTerminal()

        print("\t Digite o local de destino: \n")
        destination = input("\t 1 - Vitória da Conquista \n \t 2 - Jequié \n \t 3 - Feira de Santana \n \t 4 - Euclides da Cunha \n \t 5 - Ibó \n \t 6 - Barro \n \t 7 - Jaguaribe \n \t 8 - Russas \n \t 9 - Fortaleza  \n \t  ->")

        route = utility.defineRoute(origin, destination)

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

    else:
        repeat = False
        utility.endAnimation()