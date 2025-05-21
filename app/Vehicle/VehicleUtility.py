''' Classe responsável por manter métodos de definição de informações e simulações do veículo '''
from dataclasses import dataclass

import time
import os
import unicodedata # Biblioteca usada para tratar acentuações e caracteres

@dataclass
class VehicleUtility:


    @staticmethod
    def clearTerminal():
       os.system('cls' if os.name == 'nt' else 'clear')
    
    def endAnimation(self):

        loadPoints = ["...", "..", ".", ""]

        for p in loadPoints:
            print(f"Encerando o programa {p} ")
            time.sleep(1)
            self.clearTerminal()
    
    def defineRoute(self, origin: str, destination: str): 
        
        '''
        Método responsável por determinar os codinomes das cidades de origem e de destino 
        baseado nas respostas do usuário

        '''
        route = []

        route.append(origin)
        route.append(destination)


        for t in range( len(route) ) : 

            local = route[t]

            if local == "1":
                route[t] = "v_conquista"
                
            elif local == "2":
                route[t] = "jequie"
                
            elif local == "3":
                route[t] = "feira"
                
            elif local == "4":
                    route[t] = "e_cunha"

            elif local == "5":
                route[t] = "ibo"
                
            elif local == "6":
                route[t] = "barro"
                
            elif local == "7":
                route[t] = "jaguaribe"
                
            elif local == "8":
                route[t] = "russas"
                
            elif local == "9":
                route[t] = "fortaleza"
                
            else:
                route[t] = "false"
        
        if route[0] == "false" or route[1] == "false" :
            return False

        return route
    
    def writeReplyBack(self, wrongActions: bool, repeat: bool):

        reply = input("\n O que deseja agora: \n 1. Voltar para o início. \n 2. Fechar programa. \n ->")

        if reply == "1" :
            wrongActions = False
            repeat = True
            self.clearTerminal()

        else:
            wrongActions = False
            repeat = False
            self.endAnimation()

    def nomalizeName(self, fakeName: list[str]):

        genericName = []

        for n in fakeName:

            #Normalizando o primeiro nome e depois o sobrenome
            unormalizatedName = unicodedata.normalize('NFD', n) # Separação de caractere e acentuação
            normalizatedName = ''.join(c for c in unormalizatedName if not unicodedata.combining(c)) # Remoção das acentuações
            NameWithoutCedilhado = normalizatedName.replace('ç', 'c').replace('Ç', 'C') # Substituição dos caracteres "ç" e "Ç" por "c" e "C", respectivamente
            name = NameWithoutCedilhado.encode('ASCII', 'ignore').decode('ASCII')

            genericName.append(name)

        return genericName
    
    def startAnimation(self):

        title = "\t ------------- veHI : Sistema de recarga para veículos elétricos -------------\n"
        time.sleep(2)

        '''# Listas que guardam o conjunto de emojis e símbolos (str) para realizar a animação inicial
        animation = []
        landscape = []

        '''
        '''
        Emojis utilizados:

        - 💨 : \U0001F4A8
        - 🚗 : \U0001F697
        - 🌳 : \U0001F333
        - ☀️ : \u2600\ufe0f
        - ☁️ : \u2601\ufe0f
        '''
         
        '''   
        animation.append("\t ------------------------------------------------------------------------------ \n\t \t -- \t\t -- \t\t -- \t\t -- \t\t -- \U0001F697\U0001F4A8 \n \t ------------------------------------------------------------------------------")
        animation.append("\t ------------------------------------------------------------------------------ \n\t -- \t\t -- \t\t -- \U0001F697\U0001F4A8 -- \t\t -- \t\t -- \t \n \t ------------------------------------------------------------------------------")
        animation.append("\t ------------------------------------------------------------------------------ \n\t \U0001F697\U0001F4A8 -- \t\t -- \t\t -- \t\t -- \t\t -- \t \n \t ------------------------------------------------------------------------------")
        animation.append("\t ------------------------------------------------------------------------------ \n\t \t -- \t\t -- \t\t -- \t\t -- \t\t -- \U0001F697\U0001F4A8 \n \t ------------------------------------------------------------------------------")
        animation.append("\t ------------------------------------------------------------------------------ \n\t -- \t\t -- \t\t -- \U0001F697\U0001F4A8 -- \t\t -- \t\t -- \t \n \t ------------------------------------------------------------------------------")
        animation.append("\t ------------------------------------------------------------------------------ \n\t \U0001F697\U0001F4A8 -- \t\t -- \t\t -- \t\t -- \t\t -- \t \n \t ------------------------------------------------------------------------------")
        
        landscape.append("\t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f")
        landscape.append("\t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333")
        landscape.append("\t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f \t \u2601\ufe0f \t \U0001F333 \t \U0001F333")
        landscape.append("\t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f \t \u2601\ufe0f \t \U0001F333")
        landscape.append("\t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f \t \u2601\ufe0f")
        landscape.append("\t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \U0001F333 \t \U0001F333 \t \U0001F333 \t \u2601\ufe0f \t \u2600\ufe0f")
        

        for x in range(len(animation)):

            print(title)
            print(landscape[x])
            print(animation[x])
            time.sleep(0.8)
            self.clearTerminal()
    '''

