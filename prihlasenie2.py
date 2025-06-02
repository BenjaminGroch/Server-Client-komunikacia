import sqlite3, time, hashlib

con = sqlite3.connect('users_file.db')     #Vytvaranie suboru ak nie je, ak je tak pripajanie na subor
cur = con.cursor()                         #Vytvaranie kurzoru na pracu v subore

cur.execute('''CREATE TABLE IF NOT EXISTS users_table
                    (username text PRIMARY KEY, password text, name text, last_login time)''')  #Vytvaranie tabulky do suboru + vytvaranie stlpcov
                               

def vytvaranie_pouzivatelov(username,password,name):
    login_time = None                                                #login time je none lebo pri vytvarani sa uzivatel neprihlasuje automaticky
    sifrovane_heslo = hashlib.sha256(password.encode()).hexdigest()  #sifrovanie zadaneho hesla
    cur.execute('INSERT OR IGNORE INTO users_table VALUES (?, ?, ?, ?)',(username,sifrovane_heslo,name,login_time))    #Ukladanie udajov do tabulky uzivatelov
    con.commit()

def prihlasovanie(username,password):
    conn = sqlite3.connect("users_file.db", timeout=10)                                                         #Prepajanie na subor s uzivatelmi + timeout 10 sekund koli vlaknam
    cur = conn.cursor()                                                                                         #Vytvaranie kurzoru na pracu v subore                                       
    cur.execute("SELECT password FROM users_table WHERE username = ?", (username,))                             #Kontrola ci je uzivatel v databaze
    heslo_v_databaze = cur.fetchone()                                                                           #Ukladanie hesla uzivatela do premennej (na kontrolu)
    if heslo_v_databaze:                                                                                        #Ak je heslo ulozene (True)
        ulozene = heslo_v_databaze[0]                                                                           #Meni heslo na string
        if ulozene == hashlib.sha256(password.encode()).hexdigest():                                            #Ak sa heslo s databazou zhoduje s zadanim heslom
            login_time = time.strftime("%H:%M:%S", time.localtime())                                            #Uklada momentalny cas
            cur.execute("UPDATE users_table SET last_login = ? WHERE username = ?", (login_time, username))     #Meni login time na momentalny cas
            conn.commit()
            sprava = "Zadali ste spravne meno a heslo."                                                         #Vytvara spravu o spravnom mene a hesle
        else:
            sprava = "Zadali ste nespravne heslo"                                                               #Vytvara spravu o nespravnom hesle
    else:
        sprava = "Uzivatel s tymto menom neexistuje"                                                            #Vytvara spravu o neexistujucom uzivatelovi
    conn.close()

    return sprava
 
if __name__ == "__main__":                                    #Hlavny blok programu, ktory sa spusti pri spusteni suboru (generovanie pouzivatelov do databazy)
    vytvaranie_pouzivatelov("Admin","Admin","Admin")
    vytvaranie_pouzivatelov("Jozef123","Admin","Jozef A")
    vytvaranie_pouzivatelov("Fero123","Admin","Fero A")
    vytvaranie_pouzivatelov("Jozef1234","Admin","Jozef B")
    vytvaranie_pouzivatelov("Fero12345","Admin","Fero B")
    vytvaranie_pouzivatelov("Gabor1234","Admin","Gabor")
