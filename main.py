# This is a sample Python script.
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket
from tkinter.scrolledtext import ScrolledText

User = ''
Peca=0
# inicio de janela de usuário
win = Tk()
win.resizable(False, False)
win.title("Tsoro Yematatu")
def getNome(x):
    global User,Peca
    User = entry1.get()
    Peca=x
    print(Peca)
    if len(User) < 1:
        messagebox.showerror(title="Digite um Nome", message="Nome Inválido")
    else:
        win.destroy()
canvas1 = Canvas(win, width=400, height=300)
canvas1.pack()
label1 = Label(win, text='Digite seu nome:')
label2 = Label(win, text='Escolha suas Peças:')
entry1 = Entry(win)
foto1 = PhotoImage(file="bola1.png")
foto2 = PhotoImage(file="bola2.png")
button1 = Button(image=foto1,borderwidth=0, command=lambda: getNome(1))
button2 = Button(image=foto2,borderwidth=0, command=lambda: getNome(2))

canvas1.create_window(200, 100, window=label1)
canvas1.create_window(200, 140, window=entry1)
canvas1.create_window(200, 180, window=label2)
canvas1.create_window(250, 220, window=button2)
canvas1.create_window(150, 220, window=button1)
win.mainloop()
win = Tk()
canvas1 = Canvas(win, width=400, height=300)
canvas1.pack()
label1 = Label(win, text=f'{User}:aguardando adversário:')
canvas1.create_window(200, 100, window=label1)
win.resizable(False, False)
win.title("Tsoro Yematatu")
win.mainloop()
# fim de janela de usuário
janela = Tk()
if User=="":
    janela.destroy()
janela.resizable(False, False)
'''
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:#primeiro que conectar sera servidor
        client.bind(('localhost', 50000))
        client.listen(1)
        conn,addr=client.accept()
        print(conn, addr)
        
    except:#segundo a conectar sera cliente
        client.connect(('localhost', 50000))
        name = input("nome")
        client.send()
        print('x')
    thread1 = 
    thread2 =
    thread1.start()  
    thread2.start
def recieveMsg(client):
     #thread de receber de dados
    while True:
        jsonReceived = client.recv(1024)
        print "Json received -->", jsonReceived
def sendMsg(client):
    while True:
        x=input("digita\n") #thread de envio de dados
        jsonResult = {"first":"You're", "second":x}
        jsonResult = json.dumps(jsonResult)
        client.send(jsonResult) 
'''
Vazia = 2


def move(x):
    global Vazia
    if x == 1 and (Vazia == 5 or Vazia == 6):
        pass
    elif x == 2 and (Vazia == 4 or Vazia == 6):
        pass
    elif x == 3 and (Vazia == 5 or Vazia == 4):
        pass
    elif x == 4 and (Vazia == 2 or Vazia == 3):
        pass
    elif x == 5 and (Vazia == 1 or Vazia == 3):
        pass
    elif x == 6 and (Vazia == 1 or Vazia == 2):
        pass
    else:
        bot[Vazia]["image"] = piece[tabuleiro[x]]
        bot[x]["image"] = piece[0]
        tabuleiro[x], tabuleiro[Vazia] = 0, tabuleiro[x]
        Vazia = x
        vencedor()
        print(tabuleiro)


tabuleiro = [0, 0, 0, 0, 0, 0, 0]
adv = 1
j = 0


def preenche(x):
    global adv, j, Vazia
    if j < 6:
        if tabuleiro[x] == 0:
            tabuleiro[x] = adv
            bot[x]["image"] = piece[adv]
            j = j + 1
            #enviar movimentação
            vencedor()
            if j == 6:
                Vazia = tabuleiro.index(0)
            if adv == 1:
                adv = 2
            elif adv == 2:
                adv = 1
        else:
            return 0
    else:
        move(x)
        print("x")  # jogo comeca


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


def lbds():
    bot[0]["command"] = lambda: preenche(0)
    bot[1]["command"] = lambda: preenche(1)
    bot[2]["command"] = lambda: preenche(2)
    bot[3]["command"] = lambda: preenche(3)
    bot[4]["command"] = lambda: preenche(4)
    bot[5]["command"] = lambda: preenche(5)
    bot[6]["command"] = lambda: preenche(6)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(tabuleiro)
    vencedor()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


piece = [PhotoImage(file="bola0.png"), PhotoImage(file="bola1.png"), PhotoImage(file="bola2.png")]
janela.geometry("700x350")
janela.title("Tsoro Yematatu")

canvas = Canvas(janela, width=700, height=350)
canvas.create_line(210, 20, 370, 200, fill="black", width=2)
canvas.create_line(220, 20, 60, 200, fill="black", width=2)
canvas.create_line(217, 20, 217, 200, fill="black", width=2)
canvas.create_line(130, 105, 270, 105, fill="black", width=2)
canvas.create_line(60, 185, 340, 185, fill="black", width=2)
canvas.pack(pady=10)
bot = [0, 0, 0, 0, 0, 0, 0]


def popUp():
    messagebox.askquestion(title="inicie o jogo ", message="inicie o jogo primeiro")


bot[0] = Button(janela, image=piece[tabuleiro[0]], borderwidth=0, command=lambda: preenche(0))

bot[1] = Button(janela, image=piece[tabuleiro[1]], borderwidth=0, command=lambda: preenche(1))
bot[2] = Button(janela, image=piece[tabuleiro[2]], borderwidth=0, command=lambda: preenche(2))
bot[3] = Button(janela, image=piece[tabuleiro[3]], borderwidth=0, command=lambda: preenche(3))

bot[4] = Button(janela, image=piece[tabuleiro[4]], borderwidth=0, command=lambda: preenche(4))
bot[5] = Button(janela, image=piece[tabuleiro[5]], borderwidth=0, command=lambda: preenche(5))
bot[6] = Button(janela, image=piece[tabuleiro[6]], borderwidth=0, command=lambda: preenche(6))
adv = 1
bott = Button(janela, text='Desistir', command=lbds)
bott2 = Button(janela, text='Reiniciar', command=lbds)
bott.place(x=60, y=300)
bott2.place(x=120, y=300)

bot[0].place(x=200, y=20)

bot[1].place(x=130, y=100)
bot[2].place(x=200, y=100)
bot[3].place(x=270, y=100)

bot[4].place(x=60, y=180)
bot[5].place(x=200, y=180)
bot[6].place(x=340, y=180)
chat = ScrolledText(janela, width=35, height=17,state='disabled')
chat.place(x=400, y=10)
chat.see('end')
caixa = Entry(janela, width=35)

caixa.place(x=400, y=300)
def getTxt(name):
    chat.configure(state='normal')
    chat.insert(END,f"{User}: {caixa.get()}\n")
    #enviar mensagem
    caixa.delete(0, END)
    chat.see('end')
    chat.configure(state='disabled')
caixa.bind('<Return>',getTxt)
inputValue = caixa.get()
print(inputValue)
chat.insert(END, inputValue)

janela.mainloop()
