import socket, threading
from prihlasenie2 import prihlasovanie

host = "127.0.0.1"  #definovanie IP
port = 65432        #definovanie portu

def handle_client(conn, addr):    #funkcia na spracovanie klienta
    with conn:
        print(f"Na server sa pripojilo zariadenie {addr}")  
        try:   
            while True:            #cyklus spravobvania klienta
                while True:                                #cyklus prihlasovania
                    conn.sendall(b"Zadajte meno: ")        #posiela poziadavku klientovy na zadanie mena
                    meno = conn.recv(1024).decode()        #prijma zadanie mena od klienta
                    conn.sendall(b"Zadajte heslo: ")       #posiela poziadavku klientovy na zadanie hesla
                    heslo = conn.recv(1024).decode()       #prijma zadanie hesla od klienta
                    sprava = prihlasovanie(meno, heslo)    #vola funkciu prihlasovanie s menom a heslom, ktora vrati spravu
                    if "Zadali ste spravne meno a heslo." in sprava:      #ak je sprava o spravnom mene a hesle
                        conn.sendall(b"Zadali ste spravne meno a heslo")  #posle klientovi spravu o spravnom mene a hesle
                        break                                             #prerusi cyklus
                    elif "Zadali ste nespravne heslo" in sprava:          #ak je sprava o nespravnom hesle
                        conn.sendall(b"Zadali ste nespravne heslo")       #posle klientovi spravu o nespravnom hesle
                    else:
                        conn.sendall(b"Uzivatel s tymto menom neexistuje") #posle klientovi spravu o neexistujucom uzivatelovi

                conn.sendall(b"Zadajte spravu na nastenku: ")                            #posiela poziadavku klientovy na zadanie spravy
                sprava = conn.recv(1024).decode()                                        #prijma zadanie spravy od klienta
                print(f"klient {addr} pridal spravu: {sprava}, server ukoncil spojenie") #Vypise spravu od klienta
                conn.sendall(b"Sprava bola prijata serverom, server ukoncuje spojenie")  #posle klientovi spravu o prijati spravy a ukonceni spojenia
                break              #ukonci cyklus spravovania klienta

        except ConnectionResetError:     #ak klient ukonci spojenie
            print(f"klient {addr} ukoncil spojenie") 


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    #vytvorenie socketu
    s.bind((host,port))                                         #pripajanie socketu na IP a port
    s.listen()                                                  #nastavenie socketu na pocuvanie prichadzajucich spojeni
    print("server bezi...")

    while True:                                                #nekonecny cyklus na spracovanie prichadzajucich spojeni
        conn, addr = s.accept()                                #prijatie prichadzajuceho spojenia
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # vytvorenie noveho vlakna pre klienta
        thread.start()                                                     # spustenie vlakna, ktore bude spracovavat klienta
            
