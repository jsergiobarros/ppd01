import json
import os
import socket
import string

import Pyro4
@Pyro4.expose
class jogo():
    def jogar(self):
        print("jogou")
ns = Pyro4.locateNS(host='192.168.0.19',port=50000)
ip=socket.gethostbyname(socket.gethostname())
daemon = Pyro4.Daemon(host=ip)

uri = daemon.register(jogo)
ns.register("ussaa",uri)
#uri = ns.lookup('us')
#print(uri)
print(ns)
aux = str(ns.list())
aux=aux.split(", '")
for i in range (1,len(aux)):
    print(aux[i].split("':")[0])
print(aux)
print(str(ns.list()))
