

from time import sleep
from Funcoes.functions import   iniciaDB, cabecalho , menu , cadastro
 


# Função principal
def main():
    iniciaDB()
    cabecalho()
    cadastro()
    menu()
    
   

if __name__ == "__main__":
    main()
