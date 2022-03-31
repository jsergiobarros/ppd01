import threading
import time
from random import randint
from tkinter import messagebox
from tkinter import *
import socket
from tkinter.scrolledtext import ScrolledText

import Pyro4

adv=0
User=0
Adversario=0
Peca =0
ip=socket.gethostbyname(socket.gethostname())
ns=0
PLACAR=[0,0,0]
port = 50000
bot = [0, 0, 0, 0, 0, 0, 0] #array que receberá os botões
tabuleiro = [0, 0, 0, 0, 0, 0, 0, 0]
Vazia=0
j=0
@Pyro4.expose
class jogo:
    @Pyro4.expose
    def insertTxt(self,txt, clr):  ###INSERIR MENSAGEM
        chat.configure(state='normal')
        chat.tag_config('Vermelho', foreground="red")
        chat.tag_config('Azul', foreground="blue")
        chat.insert(END, txt, clr)
        chat.see('end')
        chat.configure(state='disabled')

    @Pyro4.expose
    def define(self, nome, peca):
        global win,Peca,adv
        adversario(nome)
        if Peca == peca:
            Peca = randint(1, 2)
            if Peca==1:
                Adversario.definePeca(2)
            else:
                Adversario.definePeca(1)
        adv = randint(1, 2)
        Adversario.defineAdv(adv)
        time.sleep(0.5)
        canvas2.destroy()
        ajustaTela()
        popUp()



    @Pyro4.expose
    def definePeca(self,peca):
        global Peca
        Peca=peca

    @Pyro4.expose
    def defineAdv(self,numero):
        global adv
        adv=numero

    @Pyro4.expose
    def prt(self):
        print("conectou")







    @Pyro4.expose
    def preenche(self,x): #função de preenchimento e movimentação
        global j, Vazia, adv, Peca
        if j < 6:
            if tabuleiro[x] == 0:
                tabuleiro[x] = adv
                bot[x]["image"] = piece[adv]
                j = j + 1
                if j == 6:
                    Vazia = tabuleiro.index(0)
            else:
                return
        else:  # jogo comeca
            if tabuleiro[x] == adv:
                aux = move(x)
                if aux:
                    return
            else:
                return
        mudaAdv()
        if adv==Peca:
            retorna()
        else:
            lbds()




def move(x): #função de movimentação
    global Vazia
    if x == 1 and (Vazia == 5 or Vazia == 6): #peças escolhidas não podem ir para o vazio
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
    else: #movimentação é possivel
        bot[Vazia]["image"] = piece[tabuleiro[x]]
        bot[x]["image"] = piece[0]
        tabuleiro[x], tabuleiro[Vazia] = 0, tabuleiro[x]
        Vazia = x
        vencedor()
        return False
def mudaAdv(): #mudança da vez, e atualização da indicação visual
    global adv
    if adv == 1:
        adv = 2
    else:
        adv = 1
    bott2['image'] = piece[adv]

def vencedor(): #conferir se houve um vencedor
    aux = 0
    if tabuleiro[0] == tabuleiro[1] == tabuleiro[4] and tabuleiro[0] != 0:
        aux = tabuleiro[0]
    elif tabuleiro[0] == tabuleiro[2] == tabuleiro[5] and tabuleiro[0] != 0:
        aux = tabuleiro[0]
    elif tabuleiro[0] == tabuleiro[3] == tabuleiro[6] and tabuleiro[0] != 0:
        aux = tabuleiro[0]
    elif tabuleiro[1] == tabuleiro[2] == tabuleiro[3] and tabuleiro[1] != 0:
        aux = tabuleiro[1]
    elif tabuleiro[4] == tabuleiro[5] == tabuleiro[6] and tabuleiro[4] != 0:
        aux = tabuleiro[4]
    else:
        return
    messagebox.showinfo(title="Vencedor", message=f"o jogador {'Azul' if aux == 1 else 'Vermelho'} venceu o jogo")
    if aux == Peca:
        PLACAR[0] += 1
    else:
        PLACAR[2] += 1
    atualizaPlacar()
    start()


def start():
    global tabuleiro, j
    tabuleiro = [0, 0, 0, 0, 0, 0, 0]
    j = 0
    for i in range(7):
        bot[i]['image'] = piece[0]

def adversario(name):
    global Adversario,ns
    Adversario = Pyro4.Proxy(ns.lookup(name))
    ns.remove(name)

def getNome(x):  # função de pegar o nome e definir o jogador. se for vazio nao entra
    global Adversario, User, Peca, ns
    Peca = x
    aux = str(ns.list())
    aux = aux.split(", '")
    if len(aux)<=2:
        canvas1.destroy()
        canvas2.pack()
        return
    Adversario=Pyro4.Proxy(ns.lookup(aux[1].split("':")[0]))
    Adversario.define(User,Peca)
    canvas1.destroy()
    ajustaTela()
    time.sleep(0.5)
    popUp()

def popUp():
    cor = ["azul", "vermelho"]
    messagebox.showinfo(title="definição de peça",
                        message=f"sua peça é: {cor[Peca - 1]} \ne quem inicia é {cor[adv - 1]}")

def obj():
    global ip, ns
    ip=socket.gethostbyname(socket.gethostname())
    ns = Pyro4.locateNS(host=ip,port=port)
    daemon = Pyro4.Daemon(host=ip)
    uri = daemon.register(jogo)
    ns.register(User,uri)
    daemon.requestLoop()

def getIp():
    global ip, port, server,User
    ip = boxIp.get()
    port = boxPort.get()
    User = boxName.get()
    if len(User) < 1:
        messagebox.showerror(title="Digite um Nome", message="Nome Inválido")
        return
    port = int(port)
    try:
        ns=Pyro4.locateNS(ip,port)
        try:
            ns.lookup(User)
            messagebox.showerror(title="Digite um Nome", message="Nome já Cadastrado")
            return
        except:
            export = threading.Thread(target=obj)
            export.start()
            canvas0.destroy()
            canvas1.pack()
    except:
        if messagebox.askyesno(title="Servidor nao iniciado",message=f"Servidor nao iniciado em {ip}: {port}\nDeseja iniciar?"):
            import SN

def atualizaPlacar():
    placar = Label(canvas, text=f'Você: {PLACAR[0]} Empate: {PLACAR[1]} Adversário {PLACAR[2]}')
    placar.place(x=140, y=270)

win = Tk()  # tela inicial, de selecionar peça e definir nome de usuário
win.geometry("400x300")
win.resizable(False, False)
win.title("Tsoro Yematatu")
canvas0=Canvas(win, width=400, height=300)
boxIp = Entry(canvas0, width=20)
boxIp.insert(0,socket.gethostbyname(socket.gethostname()))
labIp = Label(canvas0, text="Digite o IP do servidor:")
labPort = Label(canvas0, text="Digite a Porta")
boxPort = Entry(canvas0, width=20)
labName= Label(canvas0, text="Digite digite seu nome")
boxName = Entry(canvas0, width=20)
boxPort.insert(0,port)
button = Button(canvas0,text="Iniciar",command=getIp)
labIp.grid(pady=20,row=0)
boxIp.grid(pady=0,row=1)
labPort.grid(pady=20,row=2)
boxPort.grid(pady=0,row=3)
labName.grid(pady=20,row=4)
boxName.grid(pady=0,row=5)
button.grid(pady=10, row=6)
canvas0.pack()


canvas1 = Canvas(win, width=400, height=300)
label1 = Label(win, text='Digite o outro:')
label2 = Label(win, text='Escolha suas Peças:')
entry1 = Entry(win)
foto1 = PhotoImage(file="bola1.png")
foto2 = PhotoImage(file="bola2.png")
foto0 = PhotoImage(file="bola0.png")
button1 = Button(image=foto1, borderwidth=0, command= lambda:getNome(1))
button2 = Button(image=foto2, borderwidth=0, command=lambda: getNome(2))
canvas1.create_window(200, 180, window=label2)
canvas1.create_window(250, 220, window=button2)
canvas1.create_window(150, 220, window=button1)

canvas2 = Canvas(win,width=400, height=300)
label3 = Label(canvas2,text="Aguardando Jogador")
label3.grid(pady=30,row=1)

def ajustaTela():
    canvas.pack()
    win.geometry("700x350")
    win.title(f"Tsoro Yematatu: jogador: {User}")
    bott["image"]=piece[Peca]
    bott2["image"] = piece[adv]
    if adv == Peca:
        retorna()
    else:
        lbds()


def desiste():
    print(Adversario)
    pass
def empate():
    pass

def lbds(): #função de vez adversário
    bot[0]["command"] = aguarde
    bot[1]["command"] = aguarde
    bot[2]["command"] = aguarde
    bot[3]["command"] = aguarde
    bot[4]["command"] = aguarde
    bot[5]["command"] = aguarde
    bot[6]["command"] = aguarde

def aguarde():#mensagem de bloqueio de movimento na vez errada
    messagebox.showinfo(title="não é sua vez", message="aguarde sua vez jogador")

def retorna(): #função de vez jogador
    bot[0]["command"] = lambda: ativo(0)
    bot[1]["command"] = lambda: ativo(1)
    bot[2]["command"] = lambda: ativo(2)
    bot[3]["command"] = lambda: ativo(3)
    bot[4]["command"] = lambda: ativo(4)
    bot[5]["command"] = lambda: ativo(5)
    bot[6]["command"] = lambda: ativo(6)

def ativo(x):
    jogo.preenche(jogo,x)
    Adversario.preenche(x)

def getTxt(name):
    global Adversario
    jogo.insertTxt(jogo,f"{User}: {caixa.get()}\n", 'Vermelho' if Peca == 2 else 'Azul')
    Adversario.insertTxt(f"{User}: {caixa.get()}\n", 'Vermelho' if Peca == 2 else 'Azul') # enviar mensagem
    caixa.delete(0, END)



piece = []#aray que recebe as figuras
if User == "":
    win.destroy()
else:
    piece = [foto0, foto1, foto2]

win.resizable(False, False)


canvas = Canvas(win, width=700, height=350)
canvas.create_line(210, 20, 370, 200, fill="black", width=2)
canvas.create_line(220, 20, 60, 200, fill="black", width=2)
canvas.create_line(217, 20, 217, 200, fill="black", width=2)
canvas.create_line(130, 105, 270, 105, fill="black", width=2)
canvas.create_line(60, 185, 340, 185, fill="black", width=2)

for i in range(7):
    bot[i] = Button(canvas, image=foto0, borderwidth=0)
bott = Button(canvas,  borderwidth=0, state=DISABLED)
labelb1 = Label(canvas, text='Sua peça:')
bott2 = Button(canvas, image=piece[adv], borderwidth=0, state=DISABLED)
labelb2 = Label(canvas, text='Peça da vez:')
bott3 = Button(canvas, text='Desistir', command=desiste)
bott4 = Button(canvas, text='Empate', command=empate)
bott.place(x=20, y=30)
labelb1.place(x=10, y=10)
bott2.place(x=80, y=30)
labelb2.place(x=70, y=10)
bott3.place(x=140, y=300)
bott4.place(x=240, y=300)

atualizaPlacar()
bot[0].place(x=200, y=20)

bot[1].place(x=130, y=100)
bot[2].place(x=200, y=100)
bot[3].place(x=270, y=100)

bot[4].place(x=60, y=180)
bot[5].place(x=200, y=180)
bot[6].place(x=340, y=180)
chat = ScrolledText(canvas, width=35, height=17, state='disabled')
chat.place(x=400, y=10)
caixa = Entry(canvas, width=35)
caixa.place(x=400, y=300)
caixa.bind('<Return>', getTxt)
#fechar janela fecha a o socket e encerra a janela do adversário
"""def desliga():
    export.join()
    win.destroy()
win.protocol("WM_DELETE_WINDOW", desliga)"""


win.mainloop()  # fim de janela de usuário














