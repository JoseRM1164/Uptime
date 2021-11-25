import socket
import ssl
from datetime import datetime
import pickle

import subprocess
import platform

from correo import alertas

class Servidor():
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()
        
        self.history = []
        self.alert = False

    def check_connection(self):
        msg = ""
        success = False
        now = datetime.now()


        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} esta en linea en el puerto {self.port} con {self.connection}"
                success = True
                self.alert = False
            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} esta en linea en el puerto {self.port} con {self.connection}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.name} esta en linea en el puerto {self.port} con {self.connection}"
                    success = True
                    self.alert = False
        except socket.timeout:
            msg = f"el servidor: {self.name} esta fuera de linea en el puerto {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"Error: {e}"

        
        if success == True and self.alert == False:
            #alertas
            self.alert = True
            alertas(self.name,f"{now} A01336986 la pagina esta arriba","alejandrofloresm@tec.mx")
            alertas(self.name,f"{now} A01336986 la pagina esta arriba","alejandrofloresm@gmail.com")
            alertas(self.name,f"{now} A01336986 la pagina esta arriba","pepemon060498@gmail.com")

        self.create_history(msg,success,now)

    def create_history(self, msg, success, now):
        history_max = 50
        self.history.append((msg,success,now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
                return False


if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pickle", "rb"))
    except:
        servers = [ 
            Servidor("la.maquina.ninja", 80, "ping", "high"),
        ]

    for server in servers:
        server.check_connection()
        print(len(server.history))
        print(server.history[-1])

    pickle.dump(servers, open("servers.pickle", "wb"))
