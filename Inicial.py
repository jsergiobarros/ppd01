import threading
import time
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
PLACAR=[0,0,0]
port = 50000
bot = [0, 0, 0, 0, 0, 0, 0] #array que receberá os botões
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
    def prt(self,x):
        print("serve",x)
def getNome(x):  # função de pegar o nome e definir o jogador. se for vazio nao entra
    global User, Peca
    #User = entry1.get()
    Peca = x
    if len(User) < 1:
        messagebox.showerror(title="Digite um Nome", message="Nome Inválido")
    else:
        win.destroy()

def obj():
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
    print(ip,port)
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
    placar = Label(janela, text=f'Você: {PLACAR[0]} Empate: {PLACAR[1]} Adversário {PLACAR[2]}')
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
button1 = Button(image=foto1, borderwidth=0, command= lambda:getNome(1))
button2 = Button(image=foto2, borderwidth=0, command=lambda: getNome(2))
#canvas1.create_window(200, 100, window=label1)
#canvas1.create_window(200, 140, window=entry1)
canvas1.create_window(200, 180, window=label2)
canvas1.create_window(250, 220, window=button2)
canvas1.create_window(150, 220, window=button1)


win.mainloop()  # fim de janela de usuário


def desiste():
    pass
def empate():
    pass



def getTxt(name):
    jogo.insertTxt(jogo,f"{User}: {caixa.get()}\n", 'Vermelho' if Peca == 2 else 'Azul')
    # enviar mensagem
    jsonsnd = {"comando": "mensagem", "User": User, "texto": caixa.get(), "cor": 'Vermelho' if Peca == 2 else 'Azul'}
    #connect.send(jsonsnd.encode('utf-8'))
    # enviar mensagem
    caixa.delete(0, END)

janela = Tk()
piece = []#aray que recebe as figuras
if User == "":
    janela.destroy()
else:
    piece = [PhotoImage(file="bola0.png"), PhotoImage(file="bola1.png"), PhotoImage(file="bola2.png")]

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
for i in range(7):
    bot[i] = Button(janela, image=piece[0], borderwidth=0)
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
"""def desliga():
    connect.send("encerrar".encode('utf-8'))
    connect.close()
    janela.destroy()
janela.protocol("WM_DELETE_WINDOW", desliga)"""



janela.mainloop()













