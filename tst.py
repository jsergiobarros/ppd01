import json
import socket
import threading


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:  # primeiro que conectar sera servidor
        client.bind(('localhost', 50000))
        print("escutando")
        client.listen(1)
        conn, addr = client.accept()
        print(conn, addr)
        thread1 = threading.Thread(target=recieveMsg, args=[conn])
        print("t1")
        thread2 = threading.Thread(target=sendMsg, args=[conn])
        print("t2")
        thread1.start()
        print("t1")
        thread2.start()
        print("t2")
    except:  # segundo a conectar sera cliente
        client.connect(('localhost', 50000))
        name = input("nome\n")

        client.send(name.encode('utf-8'))
        print('x')


def recieveMsg(conn):
    # thread de receber de
    connect=True
    while connect:

        try:
            jsonReceived = conn.recv(1024)
            if jsonReceived:
                print("Json received -->", jsonReceived.decode('utf-8'))
        except:
            print("desconectado")
            connect=False

def sendMsg(conn):
    connect=True
    while connect:
        x = input("digita\n")  # thread de envio de dados
        jsonResult = {"first": "You're", "second": x}
        print(jsonResult)
        try:
            jsonResult = json.dumps(jsonResult)
            conn.send(x.encode())
        except:
            connect=False


main()
