import socket
import sqlite3
import threading
import datetime
from sqlite3 import Error
import time
from tkinter import *
from tkinter import scrolledtext
import tkinter

HEADER = 512
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  #192.168.56.1
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

today = datetime.datetime.today()
time_now = today.strftime("%Y-%m-%d-%H.%M.%S")

fl_cl = False
nm_client = 0

def sql_connection(): # connection to database file 
    try:
        con = sqlite3.connect('log_h.db',check_same_thread=False)
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con): #creation database
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE logs(name_client text, msg text, date_time text)")
    con.commit()
    

def sql_insert(con, entities): # inserting into database
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO logs(name_client,msg, date_time) VALUES(?,?, ?)', entities)
    con.commit()
'''
def sql_fetch(con): # check if the database is created already
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists logs(name_client,msg, date_time)')
    con.commit()'''
    

def sql_fetchall(con, text):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM logs')
    rows = cursorObj.fetchall()
    for row in rows:
        text.insert(INSERT,row)
        text.insert(INSERT,'\n')

'''
def handle_client(conn, addr, nm_client): 
    
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
           
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}]{msg} [{time_now}]")

            entities = (str(nm_client), str(msg), str(time_now))
            sql_insert(con, entities)
            
            conn.send("Msg recieved".encode(FORMAT))

    conn.close()

def handle_client(conn, addr): 
    
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        user_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if user_length:
            user_length = int(user_length)
            client_name = conn.recv(user_length).decode(FORMAT)

            if msg_length:
            
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                
                if msg == DISCONNECT_MSG:
                    connected = False

                print(f"[{client_name}]{msg} [{time_now}]")

                entities = (str(client_name), str(msg), str(time_now))
                sql_insert(con, entities)
                
                conn.send("Msg recieved".encode(FORMAT))


    conn.close()
'''

def handle_client(conn, addr, nm_client): 
    
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
           
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}]{msg} [{time_now}]")

            entities = (str(nm_client), str(msg), str(time_now))
            sql_insert(con, entities)
            
            # conn.send("Msg recieved".encode(FORMAT))

    conn.close()

def start(nm_client):
    
    server.listen()
    # print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        nm_client = nm_client + 1
        thread = threading.Thread(target=handle_client,args=(conn, addr,nm_client))

        tmp_row = (str(nm_client), 'CONNECT!', str(time_now))
        sql_insert(con, tmp_row)

        thread.start()
        
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
def quit(self):
    self.root.destroy()


def destroy_wind(win,ser_w):
    ser_w.stop()
    win.quit()

class server_thread(threading.Thread):

    def __init__(self):
        super(server_thread, self).__init__()
        self._stop = threading.Event()
     # function using _stop function
    def stop(self):
        self._stop.set()
 
    def stopped(self):
        return self._stop.isSet()
 
    def run(self):
        while True:
            if self.stopped():
                return
            print("Hello, world!")
            time.sleep(1)
###############################################################################################
global con 
con = sql_connection()


if (nm_client != 0):
    fl_cl = True


print("[STARTING] server is starting...")


    
def server_wind():
    while (fl_cl == False):
        window = Tk()
        window.title("FORUM")
        window.geometry('400x250')
                
        txt = scrolledtext.ScrolledText(window,width=100, height = 70)
        txt.grid(column=0, row = 0)
        #button_cls = tkinter.Button(window, text="quit", command=destroy_wind(window,server_window))
        button_cls = tkinter.Button(window, text="quit", command=window.quit)
        button_cls.grid(column=4, row = 0)
    
        time.sleep(5)
        sql_fetchall(con,txt)
        
        txt.configure(state='disabled')
        time.sleep(10)
        window.mainloop()

server_window = threading.Thread(target=server_wind)
server_window.start()
#server_window = server_thread(target = server_wind)
#server_window.start()

if nm_client > 0:
    server_window.sleep(60)

start(nm_client)

