# This is a sample Python script.
from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket

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

def recieveMsg(client):
    pass #thread de envio de dados
def sendMsg(client):
    pass #thread de recebimento de dados
'''
Vazia = 2


def move(x):
    global Vazia
    bot[Vazia]["image"] = piece[1]
    bot[0]["image"] = piece[0]
    Vazia = 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


tabuleiro = [0, 0, 0, 0, 0, 0, 0]
adv = 1
j = 0


def preenche(x):
    global adv, j, Vazia
    print(x, adv, j, tabuleiro)
    if j < 6:
        if tabuleiro[x] == 0:
            tabuleiro[x] = adv
            bot[x]["image"] = piece[adv]
            j = j + 1
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


def prt(x):
    print(x)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(tabuleiro)
    vencedor()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

janela = Tk()
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
bot = [0, 0, 1, 0, 2, 0, 0]
func = [0, 0, 0, 0, 0, 0, 0]
bot[0] = Button(janela, image=piece[tabuleiro[0]], borderwidth=0, command=lambda: preenche(0))

bot[1] = Button(janela, image=piece[tabuleiro[1]], borderwidth=0, command=lambda: preenche(1))
bot[2] = Button(janela, image=piece[tabuleiro[2]], borderwidth=0, command=lambda: preenche(2))
bot[3] = Button(janela, image=piece[tabuleiro[3]], borderwidth=0, command=lambda: preenche(3))

bot[4] = Button(janela, image=piece[tabuleiro[4]], borderwidth=0, command=lambda: preenche(4))
bot[5] = Button(janela, image=piece[tabuleiro[5]], borderwidth=0, command=lambda: preenche(5))
bot[6] = Button(janela, image=piece[tabuleiro[6]], borderwidth=0, command=lambda: preenche(6))
adv = 1

bot[0].place(x=200, y=20)

bot[1].place(x=130, y=100)
bot[2].place(x=200, y=100)
bot[3].place(x=270, y=100)

bot[4].place(x=60, y=180)
bot[5].place(x=200, y=180)
bot[6].place(x=340, y=180)
chat = Text(janela, width=700, height=10)
chat.place(x=0, y=320)

janela.mainloop()
