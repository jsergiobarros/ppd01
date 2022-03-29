import json
import threading
import time
import socket
from random import randint
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import Pyro4


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #criação do socket client, será usado tanto em caso de servidor ou cliente
connect = 0 # variavel que receberá o socket
adv = 0 #variavel de controle de rodada
PLACAR = [0, 0, 0] #variavel para mostrar o placar para os usuários
draw = False #variavel de controle de empate
User = ''# variavel de nome de usuário
Peca = 0 #qual a peça do usuário
Vazia = 2 #variavel de controle de casa vazia
tabuleiro = [0, 0, 0, 0, 0, 0, 0] #estado do tabuleiro
j = 0 #variavel controle
bot = [0, 0, 0, 0, 0, 0, 0] #array que receberá os botões


def popUp(msg):
    cor = ["azul", "vermelho"]
    messagebox.showinfo(title="definição de peça",
                        message=f"sua peça é: {cor[msg - 1]} \ne quem inicia é {cor[adv - 1]}")


def chatBox(msg):#função de inserir mensagem na caixa de texto
    chat.configure(state='normal')
    chat.tag_config('Vermelho', foreground="red")
    chat.tag_config('Azul', foreground="blue")
    chat.insert(END, f"{msg['User']}: {msg['texto']}\n",msg['cor'])

    chat.see('end')
    chat.configure(state='disabled')


def recieveMsg(conn): #thread principal e unica de comunicação
    """comunicação é feita recebendo um json em forma de string, e fazer o tratamento de comandos
    mensagem troca de mensagem
    inicio, define por sorteio as peças (em caso dos jogadores selecionarem a mesma)
    movimento, que recebe o movimento realizado pelo outro jogador
    empate sujere o empate para o outro jogador
    desiste, jogador A desiste e concede vitória ao jogador B, pode ser realizada em qualquer momento do jogo e esse reiniciará"""
    # thread de receber de
    global Peca, adv, draw
    while True:
        jsonReceived = conn.recv(2048)
        jsonReceived = jsonReceived.decode('utf-8')
        if jsonReceived ==  "encerrar":
            connect.close()
            janela.destroy()
        obj = json.loads(jsonReceived)
        if obj['comando'] == "mensagem":  # receber mensagem
            chatBox(json.loads(jsonReceived))
        elif obj['comando'] == "inicio":  # comando de inicio, decidir quem começa e peça no caso de igual
            if obj['adv'] != 0:
                adv = obj['adv']
            if obj['peca'] != Peca:
                time.sleep(0.5)
                popUp(Peca)
            else:
                if obj['peca'] == Peca:
                    Peca = randint(1, 2)
                    obj['peca'] = Peca
                obj = json.dumps(obj)
                connect.send(obj.encode('utf-8'))

        elif obj['comando'] == "peca":  # Movimentação de peças
            preenche(obj['movimento'], obj['peca'])
            retorna()
            mudaAdv()

        elif obj['comando'] == "desiste":  # recebimento de comando de desistencia e considera o vencedor
            start()
            PLACAR[0] += 1
            atualizaPlacar()
            messagebox.showinfo(title="Venceu", message="O jogador desistiu, Você venceu!")

        elif obj['comando'] == "empate":  # recebimento de comando de de empate,
            if obj['confirma']:
                if draw:
                    start()
                    PLACAR[1] += 1
                    atualizaPlacar()
                    draw = False
                else:
                    if empate():
                        start()
                        PLACAR[1] += 1
                        atualizaPlacar()
                        draw = False


def conectar():
    global connect, adv
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
        # adv = randint(1, 2)
        jsonsnd = {"comando": "inicio", "User": User, "peca": Peca, "adv": 0}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))


def getTxt(name):  # pegar mensagem e enviar da caixa de texto
    chat.configure(state='normal')
    chat.tag_config('Vermelho', foreground="red")
    chat.tag_config('Azul', foreground="blue")
    chat.insert(END, f"{User}: {caixa.get()}\n",'Vermelho' if Peca==2 else 'Azul')
    # enviar mensagem
    jsonsnd = {"comando": "mensagem", "User": User, "texto": caixa.get(), "cor":'Vermelho' if Peca==2 else 'Azul'}
    jsonsnd = json.dumps(jsonsnd)
    connect.send(jsonsnd.encode('utf-8'))
    # enviar mensagem
    caixa.delete(0, END)
    chat.see('end')
    chat.configure(state='disabled')



# inicio de janela de usuário

win = Tk() #tela inicial, de selecionar peça e definir nome de usuário


def getNome(x): #função de pegar o nome e definir o jogador. se for vazio nao entra
    global User, Peca
    User = entry1.get()
    Peca = x
    if len(User) < 1:
        messagebox.showerror(title="Digite um Nome", message="Nome Inválido")
    else:
        win.destroy()
        conectar()
        while connect == 0:
            pass


win.resizable(False, False)
win.title("Tsoro Yematatu")
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
win.mainloop()  # fim de janela de usuário

janela = Tk()#inicio de janela principal

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


def preenche(x, peca): #função de preenchimento e movimentação
    global j, Vazia, adv, Peca
    if j < 6:
        if tabuleiro[x] == 0:
            tabuleiro[x] = peca
            bot[x]["image"] = piece[peca]
            j = j + 1
            if j == 6:
                Vazia = tabuleiro.index(0)
        else:
            return
    else: # jogo comeca
        if tabuleiro[x] == adv:
            aux = move(x)
            if aux:
                return
        else:
            return
    if Peca == peca:
        mudaAdv()
        jsonsnd = {"comando": "peca", "User": User, "peca": Peca, "movimento": x}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))
    vencedor()
    lbds()
    # enviar movimentação


def atualizaPlacar():
    placar = Label(janela, text=f'Você: {PLACAR[0]} Empate: {PLACAR[1]} Adversário {PLACAR[2]}')
    placar.place(x=140, y=270)


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


def aguarde():#mensagem de bloqueio de movimento na vez errada
    messagebox.showinfo(title="não é sua vez", message="aguarde sua vez jogador")


def desistir():#codigo de desistir e conceder a vitória
    quit = messagebox.askyesno(title="Desistir", message="Deseja mesmo desistir?")
    if quit:
        jsonsnd = {"comando": "desistir"}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))


def empate():#codigo de empate
    global draw
    draw = messagebox.askyesno(title="Empatar", message="Deseja empatar?")
    if draw:
        jsonsnd = {"comando": "empate", "confirma": draw}
        jsonsnd = json.dumps(jsonsnd)
        connect.send(jsonsnd.encode('utf-8'))
    return draw


def lbds(): #função de vez adversário
    bot[0]["command"] = aguarde
    bot[1]["command"] = aguarde
    bot[2]["command"] = aguarde
    bot[3]["command"] = aguarde
    bot[4]["command"] = aguarde
    bot[5]["command"] = aguarde
    bot[6]["command"] = aguarde


def retorna(): #função de vez jogador
    bot[0]["command"] = lambda: preenche(0, Peca)
    bot[1]["command"] = lambda: preenche(1, Peca)
    bot[2]["command"] = lambda: preenche(2, Peca)
    bot[3]["command"] = lambda: preenche(3, Peca)
    bot[4]["command"] = lambda: preenche(4, Peca)
    bot[5]["command"] = lambda: preenche(5, Peca)
    bot[6]["command"] = lambda: preenche(6, Peca)


piece = []#aray que recebe as figuras
if User == "":
    janela.destroy()
else:
    piece = [PhotoImage(file="bola0.png"), PhotoImage(file="bola1.png"), PhotoImage(file="bola2.png")]
#configuraçao de janela
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


def desiste():#função de enviar desistencia
    jsonsnd = {"comando": "desiste"}
    jsonsnd = json.dumps(jsonsnd)
    connect.send(jsonsnd.encode('utf-8'))
    start()
    PLACAR[2] += 1
    atualizaPlacar()

#função de reinicio
def start():
    global tabuleiro, j
    tabuleiro = [0, 0, 0, 0, 0, 0, 0]
    j = 0
    for i in range(7):
        bot[i]['image'] = piece[0]


for i in range(7):
    bot[i] = Button(janela, image=piece[0], borderwidth=0)

if Peca == adv:
    retorna()
else:
    lbds()
#botões de controle e de jogo
bott = Button(janela, image=piece[Peca], borderwidth=0, state=DISABLED)
labelb1 = Label(janela, text='Sua peça:')
bott2 = Button(janela, image=piece[adv], borderwidth=0, state=DISABLED)
labelb2 = Label(janela, text='Peça da vez:')
bott3 = Button(janela, text='Desistir', command=desiste)
bott4 = Button(janela, text='Empate', command=empate)
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
chat = ScrolledText(janela, width=35, height=17, state='disabled')
chat.place(x=400, y=10)
caixa = Entry(janela, width=35)
caixa.place(x=400, y=300)
caixa.bind('<Return>', getTxt)
#fechar janela fecha a o socket e encerra a janela do adversário
def desliga():
    connect.send("encerrar".encode('utf-8'))
    connect.close()
    janela.destroy()
janela.protocol("WM_DELETE_WINDOW", desliga)
janela.mainloop()


