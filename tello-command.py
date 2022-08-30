#!/usr/bin/python3


import threading
import socket
import time

tello_ip = "192.168.10.1"


command_port = 8889


host_ip = "0.0.0.0"


response_port = 9000

print('\n Programa para Enviar comandos a Tello iniciado\n')

class Tello:
    def __init__(self):
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host_ip, response_port))  # Bind for receiving

    def terminate(self):
        self._running = False
        self.sock.close()

    def recv(self):
        """ Handler for Tello response message """
        while self._running:
            try:
                msg, _ = self.sock.recvfrom(1024)  # Read 1024-bytes from UDP socket
                print("response: {}".format(msg.decode(encoding="utf-8")))
            except Exception as err:
                print(err)

    def send(self, msg):
        """ Handler for send message to Tello """
        msg = msg.encode(encoding="utf-8")
        self.sock.sendto(msg, (tello_ip, command_port))
        print("message: {}".format(msg))  # Print message


""" Start new thread for receive Tello response message """
t = Tello()
recvThread = threading.Thread(target=t.recv)
recvThread.start()

while True:
    try:
        
        msg = input()
        t.send(msg)

        if (msg == 'pruebas'):
            print('\nIngresando zona de pruebas')
            while True:
                t.send('command')
                time.sleep(5)


        if (msg == 'bye'):
            t.terminate()
            recvThread.join()
            print("\nGood Bye\n")
            break
        

    except KeyboardInterrupt:
        t.terminate()
        recvThread.join()
        break
