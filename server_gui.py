from ctypes import windll
import socket
import sqlite3
import threading
import datetime
from sqlite3 import Error
import time
from tkinter import *
from tkinter import scrolledtext
import tkinter
import random

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

fl_cl = False #flag for number of clients


def sql_connection(): # connection to database file 
    try:
        con = sqlite3.connect('loggy.db',check_same_thread=False)
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con): #creation database
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE logs(name_client text, msg text, date_time text)")
    con.commit()
    
def sql_fetch(con): # check if the database is created already
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists logs(name_client,msg, date_time)')
    con.commit()
    return False

def sql_insert(con, entities): # inserting into database
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO logs(name_client,msg, date_time) VALUES(?,?, ?)', entities)
    con.commit()

    

def sql_fetchall(con, text): # pasting query results from db in server-window(TXT)
    
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM logs')
    rows = cursorObj.fetchall() #getting all data from sql query
    for row in rows:
        text.insert(INSERT,row)
        text.insert(INSERT,'\n')


def handle_client(conn, addr): 
    
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
           
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}]::{msg}[{time_now}]")
            
            
            entities = (str(addr), str(msg), str(time_now))
            sql_insert(con, entities)

            # conn.send("Msg recieved".encode(FORMAT))
    conn.close()

#Function that continuosly searches for connections
'''
def send_clients(connectionList, addressList,nm_client):

    while True:
        for j in range(0,nm_client):
            message = connectionList[j].recv(1024)
            print(str(message,'utf8'))

            #for loop to send message to each
            for i in range(0,nm_client):
                #connectionList[i].sendto(bytes(str(message),encoding='utf8'), addressList[i])
                connectionList[i].sendto(message, addressList[i])

    connection.close()
'''

def start(): # the main process 
    addr_list = []
    server.listen()
    # print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        addr_list.append(addr)
        thread = threading.Thread(target=handle_client,args=(conn, addr))

        tmp_row = (str(addr), 'NEW CONNECTION!', str(time_now))
        sql_insert(con, tmp_row)

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
    
        
def quit(self): # destruction of window
    self.root.destroy()


def destroy_wind(win,ser_w): #closing the whole app
    ser_w.stop()
    win.quit()




def server_wind(): # drawing server
 
    while True:
        window = Tk()
        window.title("FORUM")
        window.geometry('400x250')
                
        #window.update()

        txt = scrolledtext.ScrolledText(window,width=100, height = 50)
        txt.grid(column=0, row = 0)
        # window.updateGUI()
        

        time.sleep(1)

        #time.sleep(5)
        sql_fetchall(con,txt)
        
        # txt.configure(state='disabled')
        time.sleep(2)
        window.mainloop()
        

###############################################################################################
global con 
con = sql_connection() # connection to db
sql_fetch(con)
#print("[STARTING] server is starting...")


server_window = threading.Thread(target=server_wind)
server_window.start()



start()

