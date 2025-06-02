import socket

host = "127.0.0.1"   #definovanie IP
port = 65432         #definovanie portu

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   #Vytvorenie socketu
    s.connect((host,port))                                     #Pripojenie socketu na IP a port
    while True:                        #Cyklus prihlasovania
        for i in range(2):             #Cyklus na zadanie mena a hesla
            poziadvaka = s.recv(1024).decode()  #Prijma poziadavku od servera
            odpoved = input(poziadvaka)         #Zadanie odpovede na poziadavku
            s.sendall(odpoved.encode())         #Poslanie odpovede serveru
        data = s.recv(1024).decode()    #Prijmanie spravy od servera po zadani mena a hesla
        if "Zadali ste spravne meno a heslo." in data:
            print(data)
            break
        elif "Zadali ste nespravne heslo" in data:
            print(data)
        else:
            print(data)

    poziadvaka = s.recv(1024).decode()  #Prijmanie poziadavky na zadanie spravy
    odpoved = input(poziadvaka)         #Zadanie spravy
    s.sendall(odpoved.encode())         #Poslanie spravy serveru
