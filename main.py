# This is a sample Python script.
import json
import threading
import tkinter
from random import random, randint
from tkinter import *
from tkinter import ttk, messagebox
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket
from tkinter.scrolledtext import ScrolledText

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = 0
adv = 0


def popUp(msg):
    cor=["azul","vermelho"]
    messagebox.showinfo(title="definição de peça", message=f"sua peça é: {cor[msg-1]} \ne quem inicia é {cor[adv-1]}")


def chatBox(msg):
    chat.configure(state='normal')
    chat.insert(END, f"{msg['User']}: {msg['texto']}\n")
    chat.see('end')
    chat.configure(state='disabled')


def recieveMsg(conn):
    # thread de receber de
    global Peca, adv
    con = True
    while con:
        jsonReceived = conn.recv(2048)
        jsonReceived = jsonReceived.decode('utf-8')
        print(f"comando recebido: {jsonReceived}\n")
        obj = json.loads(jsonReceived)
        if obj['comando'] == "mensagem": #receber mensagem
            chatBox(json.loads(jsonReceived))

        elif obj['comando'] == "inicio": #comando de inicio, decidir quem começa e peça no caso de igual
            if obj['peca'] != Peca and obj['adv'] == adv:
                popUp(Peca)
            else:
                if obj['peca'] == Peca:
                    Peca = randint(1, 2)
                    obj['peca'] = Peca
                if obj['adv'] != adv:
                    adv = randint(1, 2)
                    obj['adv'] = adv
                obj = json.dumps(obj)
                connect.send(obj.encode('utf-8'))

        elif obj['comando'] == "peca": #Movimentação de peças
            print(f"movimento { obj['movimento']}")
            print(tabuleiro, adv)
            preenche(obj['movimento'],obj['peca'])
            print(tabuleiro, adv)
            retorna()
            mudaAdv()
        elif obj['comando'] == "desistencia":  # recebimento de comando de desistencia
            pass
        elif obj['comando'] == "empate":  # recebimento de comando de desistencia
            pass

def conectar():
    global connect, adv
    print(connect)
    try:  # primeiro que conectar sera servidor
        client.bind(('localhost', 50000))
        print("escutando")
        client.listen(1)
        connect, addr = client.accept()
        thread1 = threading.Thread(target=recieveMsg, args=[connect])
        thread1.start()
        adv = randint(1, 2)
        jsonsnd = {"comando": "inicio", "User": User, "peca": Peca, "adv": adv}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))

    except:  # segundo a conectar sera cliente
        client.connect(('localhost', 50000))
        connect = client
        thread1 = threading.Thread(target=recieveMsg, args=[connect])
        thread1.start()
        adv = randint(1, 2)
        jsonsnd = {"comando": "inicio", "User": User, "peca": Peca, "adv": adv}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))


def getTxt(name):
    chat.configure(state='normal')
    chat.insert(END, f"{User}: {caixa.get()}\n")
    # enviar mensagem
    jsonsnd = {"comando": "mensagem", "User": User, "texto": caixa.get()}
    jsonsnd = json.dumps(jsonsnd)
    connect.send(jsonsnd.encode('utf-8'))
    # enviar mensagem
    caixa.delete(0, END)
    chat.see('end')
    chat.configure(state='disabled')


User = ''
Peca = 0
# inicio de janela de usuário
win = Tk()
win.resizable(False, False)
win.title("Tsoro Yematatu")


def getNome(x):
    global User, Peca
    User = entry1.get()
    Peca = x
    print(Peca)
    if len(User) < 1:
        messagebox.showerror(title="Digite um Nome", message="Nome Inválido")
    else:
        # CODIGO DE CONECTAR E DESTRUIR
        win.destroy()
        conectar()
        # send(client, f'{User}')


canvas1 = Canvas(win, width=400, height=300)
canvas1.pack()
label1 = Label(win, text='Digite seu nome:')
label2 = Label(win, text='Escolha suas Peças:')
entry1 = Entry(win)
foto1 = PhotoImage(file="bola1.png")
foto2 = PhotoImage(file="bola2.png")
button1 = Button(image=foto1, borderwidth=0, command=lambda: getNome(1))
button2 = Button(image=foto2, borderwidth=0, command=lambda: getNome(2))
canvas1.create_window(200, 100, window=label1)
canvas1.create_window(200, 140, window=entry1)
canvas1.create_window(200, 180, window=label2)
canvas1.create_window(250, 220, window=button2)
canvas1.create_window(150, 220, window=button1)
win.mainloop()
janela = Tk()
# fim de janela de usuário

Vazia = 2


def move(x):
    global Vazia

    if x == 1 and (Vazia == 5 or Vazia == 6):
        return True
    elif x == 2 and (Vazia == 4 or Vazia == 6):
        return True
    elif x == 3 and (Vazia == 5 or Vazia == 4):
        return True
    elif x == 4 and (Vazia == 2 or Vazia == 3):
        return True
    elif x == 5 and (Vazia == 1 or Vazia == 3):
        return True
    elif x == 6 and (Vazia == 1 or Vazia == 2):
        return True
    else:
        bot[Vazia]["image"] = piece[tabuleiro[x]]
        bot[x]["image"] = piece[0]
        tabuleiro[x], tabuleiro[Vazia] = 0, tabuleiro[x]
        Vazia = x
        vencedor()
        return False


tabuleiro = [0, 0, 0, 0, 0, 0, 0]
j = 0
bot = [0, 0, 0, 0, 0, 0, 0]

def mudaAdv():
    global adv
    if adv == 1:
        adv = 2
    else:
        adv=1
    bott2['image']=piece[adv]


def preenche(x,peca):
    global j, Vazia, adv,Peca
    if j < 6:
        if tabuleiro[x] == 0:
            tabuleiro[x] = peca
            bot[x]["image"] = piece[peca]
            j = j + 1
            if j == 6:
                Vazia = tabuleiro.index(0)
        else:
            return
    else:
        if tabuleiro[x] == adv:
            aux = move(x)
            if aux:
                return
        else:
            return
        print("x")  # jogo comeca
    if Peca == peca:
        mudaAdv()
        jsonsnd = {"comando": "peca", "User": User, "peca": Peca, "movimento": x}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))
    vencedor()
    lbds()
    # enviar movimentação


def vencedor():
    if tabuleiro[0] == tabuleiro[1] == tabuleiro[4] and tabuleiro[0] != 0:
        print("win")
    elif tabuleiro[0] == tabuleiro[2] == tabuleiro[5] and tabuleiro[0] != 0:
        print("win")
    elif tabuleiro[0] == tabuleiro[3] == tabuleiro[6] and tabuleiro[0] != 0:
        print("win")
    elif tabuleiro[1] == tabuleiro[2] == tabuleiro[3] and tabuleiro[1] != 0:
        print("win")
    elif tabuleiro[4] == tabuleiro[5] == tabuleiro[6] and tabuleiro[4] != 0:
        print("win")


def aguarde():
    messagebox.showinfo(title="não é sua vez", message="aguarde sua vez jogador")

def desistir():
    quit= messagebox.askyesno(title="Desistir", message="Deseja mesmo desistir?")
    print(quit)
    if quit:
        jsonsnd = {"comando": "desistir"}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))

def empate():
    draw= messagebox.askyesno(title="Desistir", message="Deseja mesmo desistir?")
    print (draw)
    if draw:
        jsonsnd = {"comando": "empate"}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))

def lbds():
    bot[0]["command"] = aguarde
    bot[1]["command"] = aguarde
    bot[2]["command"] = aguarde
    bot[3]["command"] = aguarde
    bot[4]["command"] = aguarde
    bot[5]["command"] = aguarde
    bot[6]["command"] = aguarde
def retorna():
    bot[0]["command"] = lambda: preenche(0, Peca)
    bot[1]["command"] = lambda: preenche(1, Peca)
    bot[2]["command"] = lambda: preenche(2, Peca)
    bot[3]["command"] = lambda: preenche(3, Peca)
    bot[4]["command"] = lambda: preenche(4, Peca)
    bot[5]["command"] = lambda: preenche(5, Peca)
    bot[6]["command"] = lambda: preenche(6, Peca)

if User == "":
    janela.destroy()
janela.resizable(False, False)
janela.geometry("700x350")
janela.title(f"Tsoro Yematatu: jogador: {User}")

canvas = Canvas(janela, width=700, height=350)
canvas.create_line(210, 20, 370, 200, fill="black", width=2)
canvas.create_line(220, 20, 60, 200, fill="black", width=2)
canvas.create_line(217, 20, 217, 200, fill="black", width=2)
canvas.create_line(130, 105, 270, 105, fill="black", width=2)
canvas.create_line(60, 185, 340, 185, fill="black", width=2)
canvas.pack(pady=10)
piece = [PhotoImage(file="bola0.png"), PhotoImage(file="bola1.png"), PhotoImage(file="bola2.png")]

for i in range(7):
    bot[i] = Button(janela, image=piece[0], borderwidth=0)

if Peca == adv:
    retorna()
else:
    lbds()

bott = Button(janela, image=piece[Peca], borderwidth=0, state=DISABLED)
labelb1 = Label(janela, text='Sua peça:')
bott2 = Button(janela, image=piece[adv], borderwidth=0, state=DISABLED)
labelb2 = Label(janela, text='Peça da vez:')
bott3 = Button(janela, text='Desistir', command=desistir)
bott4 = Button(janela, text='Empate', command=empate)
bott.place(x=60, y=300)
labelb1.place(x=50, y=270)
bott2.place(x=120, y=300)
labelb2.place(x=110, y=270)
bott3.place(x=180, y=300)
bott4.place(x=240, y=300)

bot[0].place(x=200, y=20)

bot[1].place(x=130, y=100)
bot[2].place(x=200, y=100)
bot[3].place(x=270, y=100)

bot[4].place(x=60, y=180)
bot[5].place(x=200, y=180)
bot[6].place(x=340, y=180)
chat = ScrolledText(janela, width=35, height=17, state='disabled')
chat.place(x=400, y=10)
caixa = Entry(janela, width=35)
caixa.place(x=400, y=300)
caixa.bind('<Return>', getTxt)
janela.mainloop()
