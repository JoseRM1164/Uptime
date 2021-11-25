import pickle
from Uptime import Servidor

servers = pickle.load( open( "servers.pickle", "rb" ) )

print("Crea un nuevo servidor")

servername = input("Url: ")
port = int(input("Puerto en integer: "))
connection = input("Ingresa si es ping/plain/ssl: ")
priority = input("Que prioridad tiene? high/low: ")

new_server = Servidor(servername, port, connection, priority)
servers.append(new_server)

pickle.dump(servers, open("servers.pickle", "wb" ))