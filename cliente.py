import asyncio
import json
import os
import socket
import string
from tkinter import *
import Pyro4
@Pyro4.expose
def jogar(Thread):
    print("jogou")
print(socket.gethostbyname(socket.gethostname()))
#ns = Pyro4.locateNS(host='192.168.56.1',port=50000)
def callback():
    return False
async def obj():
    myip=socket.gethostbyname(socket.gethostname())
    ns = Pyro4.locateNS(host="192.168.0.8",port=50000)
    daemon = Pyro4.Daemon(host=myip)
    uri = daemon.register(jogar)
    ns.register("Usear",uri)
    daemon.requestLoop()


#task = asyncio.create_task( obj())
async def main():
    task = asyncio.create_task(obj())
    print("ns")
asyncio.run(main())
print("ns")
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
#daemon.requestLoop()


