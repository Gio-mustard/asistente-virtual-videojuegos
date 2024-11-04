import pywhatkit.misc

from subprocess import call
#Clase para ejecutar comandos en la PC
#De momento esta en duro funcional para Windows hohoh
class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website):
        pywhatkit.misc.search(website)