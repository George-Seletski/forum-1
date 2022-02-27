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


HEADER = 1024
PORT = 4040
# SERVER = socket.gethostbyname(socket.gethostname())  #192.168.56.1
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

today = datetime.datetime.today()
time_now = today.strftime("%Y-%m-%d-%H.%M.%S")

fl_cl = False #flag for number of clients


clients = []
aliases = []

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

'''

def handle_client(conn, addr): 
    
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        
        msg_length = conn.recv(HEADER)
        broadcast(msg_length)
        msg_length.decode(FORMAT)

        if msg_length:
            
            msg_length = len(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(msg)
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}]::{msg}[{time_now}]")
            
            
            entities = (str(addr), str(msg), str(time_now))
            sql_insert(con, entities)

            # conn.send("Msg recieved".encode(FORMAT))
    conn.close()
'''
#Function1 that continuosly searches for connections
'''
def send_clients(connection, connectionList, addressList,nm_client):

    while True:
        for j in range(0,nm_client):
            message = connectionList[j].recv(HEADER)
            tmp_msg = message.decode(FORMAT)
            length_ms = int(tmp_msg)
            print('from client ({connectionList[j]}) :: ', tmp_msg)

            #for loop to send message to each
            for i in range(0,nm_client):
                #connectionList[i].sendto(bytes(str(message),encoding='utf8'), addressList[i])
                connectionList[i].sendto(message, addressList[i])

            connectionList[j].close()
'''


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            record = (str(client.decode(FORMAT)),str(message), str(time_now))
            sql_insert(con, record)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

#Function1 that broadcasts msg
def broadcast(message):
    for client in clients:
        client.send(message)

'''def start(): # the main process 
    nm = 0 
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print('Got connection from', addr)
         
        nm += 1
        addr.append(addr)
        conn.append(conn)

        # --------for inserting data on server-window-form--------
        displaying_thread = threading.Thread(target=handle_client, args=(conn,addr))
        displaying_thread.start()

        # -------for broadcasting messages-----------------
        # sending_thread = threading.Thread(target=send_clients,args=(addr_list, connection_list, nm)) 
        # sending_thread.start()

        tmp_row = (str(addr), 'NEW CONNECTION!', str(time_now))
        sql_insert(con, tmp_row)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")'''
    
        
def quit(self): # destruction of window
    self.root.destroy()


def destroy_wind(win,ser_w): #closing the whole app
    ser_w.stop()
    win.quit()

def receive():
    server.listen()
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        # client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



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
        
        time.sleep(2)
        window.mainloop()
        

###############################################################################################
global con 
con = sql_connection() # connection to db
sql_fetch(con)
#print("[STARTING] server is starting...")


server_window = threading.Thread(target=server_wind)
server_window.start()



receive()

