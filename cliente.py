import json
import os
import socket
import string
from tkinter import *
import Pyro4
@Pyro4.expose
def jogar(Thread):
    print("jogou")
ns = Pyro4.locateNS(host='192.168.0.19',port=50000)
ip=socket.gethostbyname(socket.gethostname())
daemon = Pyro4.Daemon(host=ip)

uri = daemon.register(jogar)
ns.register("usaesas",uri)
uri = ns.lookup('b')
print(uri)
print(ns)
#o = Pyro4.Proxy(uri)
#o.prt("xas")
#o.insertTxt("a: mensagem", 'Vermelho' )
#o.jogar()
aux = str(ns.list())
aux=aux.split(", '")
win = Tk()
win.geometry("400x300")
win.resizable(False, False)
win.title("Servidor")

def printURL(url):
    print(url)
for i in range (1,len(aux)):
    print(aux[i].split("':")[0])
    button = Button(width=10, text=aux[i].split("':")[0],command=lambda:printURL(aux[i]))
    button.grid(row=i)
print(aux)
win.mainloop()
print(str(ns.list()))
jogar()
daemon.requestLoop()

