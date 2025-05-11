''' Classe responsável por manter métodos de definição de informações e simulações do veículo '''
from dataclasses import dataclass

import time
import os
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
    
    def defineRoute(origin: str, destination: str): 
        '''
        Método responsável por determinar os codinomes das cidades de origem e de destino 
        baseado nas respostas do usuário

        '''
        
        route = []

        route[0] = origin
        route[1] = destination

        for t in range( len(route) ) : 

            local = route[t]

            match local: 

                case "1":
                    route[t] = "v_conquista"
                
                case "2":
                    route[t] = "jequie"
                
                case "3":
                    route[t] = "feira"
                
                case "4":
                    route[t] = "e_cunha"

                case "5":
                    route[t] = "ibo"
                
                case "6":
                    route[t] = "barro"
                
                case "7":
                    route[t] = "jaguaribe"
                
                case "8":
                    route[t] = "russas"
                
                case "9":
                    route[t] = "fortaleza"
        
        return route
