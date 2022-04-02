import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
import Pyro4
import Pyro4.naming
ip=socket.gethostbyname(socket.gethostname())
port = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nameServer=0
win = Tk()
win.geometry("400x300")
win.resizable(False, False)
win.title("Servidor")
def iniciar ():
    global nameServer
    port = box.get()
    port = int(port)
    result = sock.connect_ex((ip, port))
    if result:
        nameserver = Pyro4.naming.startNSloop
        nameServer = threading.Thread(target= lambda: nameserver(ip, port))
        nameServer.start()
        label["text"]= f"Servidor de nomes rodando no IP {ip} e porta: {port}"
        label1["text"] = ""
        label1.grid(pady=20, row=1)
        button.destroy()
        box.destroy()
        cadastrados = threading.Thread(target=update)
        cadastrados.start()

    else:
        messagebox.showerror(title="Porta ja utilizada",message="Porta ja em uso\ntente outra")

def update():
    while True:
        time.sleep(3)
        aux=str(Pyro4.locateNS(ip, port).list())
        aux=aux.split(", '")
        text=""
        for i in range(1, len(aux)):
            text+=aux[i].split("':")[0]+"\n"
        label1["text"] = text

canvas = Canvas(win,width=400, height=300)
label =Label(canvas,text=f"Servidor de nomes rodando no IP {ip} \n escolha a porta:")
label1 =Label(canvas,text=f"Servidor de nomes rodando no IP {ip} \n escolha a porta:")
box = Entry(canvas, width=20)
button = Button(canvas,text="iniciar servidor",command=iniciar)
box.insert(0,port)
label.grid(pady=20,row=0)

box.grid(pady=20,row=1)
button.grid(pady=20, row=2)
canvas.pack()

win.mainloop()
