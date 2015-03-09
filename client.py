__author__ = 'UlugbekRozimboev'

import socket
import select
import threading
import sys

def read_thread(sock):
    while True:
        data = sock.recv(1024).decode()
        print(data)

def main():
    # nickni kiritish, bo'sh bo'lmasligini tekshirish
    while True:
        nick = input("Nick: ")
        if nick:
            print("hello %s" % nick)
            break

    print('yangi socket yaratamiz')
    # yangi socket yaratamiz
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # non blocking qilamiz
    # sock.setblocking(0)

    # serverga bog'lanamiz
    print('connection')
    try:
        sock.connect(('127.0.0.1', 8899))
        print('trying...')
    except:
        print("Bog'lanishda xatolik yuz berdi")
        return

    # yangi patok, kelgan xatlarni o'qib turishi uchun
    thread = threading.Thread(target = read_thread, args = (sock, ))
    thread.start()

    while True:
        data = input("Siz:n ")
        sock.send((nick + ": " + data).encode())


if (__name__ == "__main__"):
        main()