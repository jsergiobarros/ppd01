# This is a sample Python script.
from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import socket

'''host = "localhost"
port = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen()
conn, end = sock.accept()'''

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


tabuleiro = [0, 0, 0, 0, 0, 0, 0]


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
    tabuleiro[2] = '1.1.1'
    tabuleiro[1] = '1.1.1'
    tabuleiro[3] = '1.1.1'
    print(tabuleiro)
    vencedor()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
janela = Tk()
janela.geometry("700x350")
janela.title("Tsoro Yematatu")
bot=[0,0,0,0,0,0,0]
bot[0]= Button(janela,bg="red",width=3,borderwidth=0)
bot[1]= Button(janela,bg="red",width=3,borderwidth=0)
bot[2]= Button(janela,bg="red",width=3,borderwidth=0)
bot[3]= Button(janela,bg="red",width=3,borderwidth=0)
bot[4]= Button(janela,bg="red",width=3,borderwidth=0)
bot[5]= Button(janela,bg="red",width=3,borderwidth=0)
bot[6]= Button(janela,bg="red",width=3,borderwidth=0)

bot[0].place(x=200,y=20)

bot[1].place(x=130,y=100)
bot[2].place(x=200,y=100)
bot[3].place(x=270,y=100)

bot[4].place(x=60,y=200)
bot[5].place(x=200,y=200)
bot[6].place(x=340,y=200)
chat=Text(janela,width=700,height=10)
chat.place(x=0,y=320)
canvas=Canvas(janela, width=500, height=100)
canvas.create_line(100,200,200,35, fill="green", width=5)
canvas.place()
janela.mainloop()