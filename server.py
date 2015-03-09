__author__ = 'UlugbekRozimboev'

import select
import socket
import sys

def main():
    # Yangi socket yaratamiz
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # nonblocking qilamiz
    # bu read, write larda kutib turmaslik uchun kerak
    sock.setblocking(0)

    # qaysi interface ni tinglashni ko'rsatamiz port bilan birga
    sock.bind(("127.0.0.1", 8899))

    # bir vaqtning o'zida nechta client ulana olishini ko'rsatamiz
    sock.listen(10)

    # bular select.select uchun kerak
    # ya'ni nonblocked socketlarda kernel eventlar
    # bilan ishlash kerak. Ya'ni yadro socketdan kelgan
    # ma'lumotlardan kelib chiqib ushbu massivlarga
    # kerakli connection.id larni beradi
    inputs = [ sock ]
    outputs = []

    # asosiy sikl
    while inputs:
        # yanro eventini kutamiz
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        # kelgan xatlarni olamiz va ulangan
        # barcha clientlarga tarqatamiz
        for s in readable:
            # agar server socket bo'lsa
            if s is sock:
                # yangi clientni olamiz
                conn, addr = sock.accept()
                print( "Yangi client %s" % str(addr) )
                print('Connected with ' + addr[0] + ':' + str(addr[1]))

                # nonblocking qilamiz
                # conn.setblocking(0)

                # va umumiy ro'yxatga qo'shamiz
                inputs.append(conn)
            else:
                # ma'lumotni o'qiymiz
                data = s.recv(1024).decode()
                print(data)

                # agar ma'lumotni o'qishda xatolik bo'lsa
                # clientni ro'yxatdan o'chiramiz va socketni yopamiz
                if not data:
                    s.close()
                    inputs.remove(s)
                    continue

                # server va o'zidan boshqa clientlarga jo'natamiz
                for c in inputs:
                    if not c is sock and not c is s:
                        c.send(data.encode())

if (__name__ == "__main__"):
        main()
