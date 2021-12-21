from tkinter import *
import os
from os import listdir
import socket
import threading
import time
import sqlite3
from sqlite3 import *
from tkinter import scrolledtext
# import sqlClient as sqlC


DISCONNECT_MSG = "!DISCONNECT"
HEADER = 256
PORT = 5050
SERVER = "192.168.56.1"
FORMAT = 'utf-8'
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
#nm_clnt = 0

global rT

def send_nickname(nm):
    nickn = nm.encode(FORMAT)
    nm_length = len(nickn)
    send_nm_l = str(nm_length).encode(FORMAT)
    send_nm_l += b' ' * (HEADER - len(send_nm_l))
    client.send(send_nm_l)
    client.send(nickn)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    #client.send(nm_clnt.to_bytes(2))
    #print(client.recv(2048).decode(FORMAT))

def sql_connection(): # connection to database file 
    try:
        con = sqlite3.connect('users.db',check_same_thread=False)
        print('OK_sql_connection!')
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con): #creation database
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE users(name_client text, passw text)")
    print('OK_sql_table!')
    con.commit()
    return True

def sql_insert(con, entities): # inserting into database
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO users(name_client,passw) VALUES(?,?)', entities)
    #print(cursorObj.execute('SELECT * FROM CLIENTS').rowcount)
    print('OK_sql_insrtn!')
    con.commit()

def sql_fetch(con): # check if the database is created already
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists users(name_client,passw)')
    con.commit()
    return False

def sql_fetchall(con, text): # pasting query results from db in server-window(TXT)
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM loggy')
    rows = cursorObj.fetchall() #getting all data from sql query
    for row in rows:
        text.insert(INSERT,row)
        text.insert(INSERT,'\n')




rT = threading.Thread(target = send, args = ("RecvThread",client))

def delete2():
    screen2.destroy()

def delete3():
    screen3.destroy()

def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")

    global username
    global password

    username =StringVar()
    password = StringVar()

    global username_entry
    global password_entry

    Label(screen1, text="please enter details below").pack()
    Label(screen1, text="").pack()

    Label(screen1, text="Username * ").pack()
    username_entry = Entry(screen1, textvariable=username)
    username_entry.pack()
  
    Label(screen1, text="Password * ").pack()
    password_entry = Entry(screen1, textvariable=password)
    password_entry.pack()

    Label(screen1, text="").pack()

    Button(screen1, text="Register", width=10, height=1, command=register_user).pack()
    # print("Register  session started")
    
global conn
conn = sql_connection()

def register_user():
    
    username_info = username.get()
    passsword_info = password.get()
    
    info = (str(username_info), str(passsword_info))
    
    sql_fetch(conn)
    sql_insert(conn, info)
    
    #thread = threading.Thread(target=sql_insert,args=(conn, info)) 

    username_entry.delete(0,END)
    password_entry.delete(0,END)

    #thread.start()

    Label(screen1 ,text="Registration is sucessful!!!").pack()
    
def password_not_found():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title('ERROR')
    screen4.geometry("150x100")
    Label(screen4,text="password not found").pack()


def click_tosend():
    res = str(txt_msg.get())
    send(res)
    txt_msg.delete(0,END)
    
def delete_mainScren():
    # send(DISCONNECT_MSG)
    screen.destroy()

def click_toDisconnect():
    delete3()
    send(DISCONNECT_MSG)
    

def chat_window(name):

    global screen3
    global txt_msg
    global tmp_name

    tmp_name  = name

   

    send_nickname(name)

    rT.start()

    screen3 = Toplevel(screen)
    
    screen3.title(name)
    screen3.geometry("700x750")

    txt = scrolledtext.ScrolledText(screen3,width=70, height = 25)
    txt.pack()

    Label(screen3,text="Your message:").pack()
    Label(screen3,text="").pack()

    txt_msg = Entry(screen3, width=50)
    txt_msg.pack()
    Label(screen3,text="").pack()

    Button(screen3, text="Send", height="2", width="30", command= click_tosend).pack()
    Label(screen3, text="").pack()

    Button(screen3, text="CloseApp", height="2", width="30", command=click_toDisconnect).pack()
    screen3.update(1)

    rT.join()
    





def user_not_found():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title('ERROR')
    screen4.geometry("200x150")
    Label(screen4,text="User not found!").pack()
    screen4.destroy()

def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    Label(screen2, text="Please enter details below to login").pack()
    Label(screen2,text="").pack()

    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen2,text="Username * ").pack()
    username_entry1 = Entry(screen2, textvariable=username_verify)
    username_entry1.pack()

    Label(text="").pack()

    Label(screen2,text="Password * ").pack()
    password_entry1 = Entry(screen2, textvariable=password_verify)
    password_entry1.pack()
   
    Button(screen2, text="Login", height="1", width="10", command=login_verify).pack()
    

            
def check_data_in_db():
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    print('OK! CHECK_DATA!')
    rows = cursor.fetchall()
    return rows
      


def login_verify():
    #global username1

    username1 = username_verify.get()
    password1 = password_verify.get()

    username_entry1.delete(0, END)
    password_entry1.delete(0,END)

    # user_list = check_data_in_db()

    for row in check_data_in_db():
        if str(username1) in row:
            if str(password1) in row:
                chat_window(username1)
                delete2()
            else:
                password_not_found()
        else:
           user_not_found()
           # pass
    
    
        



def main_screen():
    global screen
    
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Login & Register")
    Label(screen, text="Client", bg="grey", width ="300", height="2", font=("Calibri", 13)).pack()
    Label(screen, text="").pack()

                    

    
    #time.sleep(5)

    Button(screen, text="Login", height="2", width="30", command=login).pack()
    Label(screen, text="").pack()
    Button(screen, text="Register", height="2", width="30", command=register).pack()
    
    Label(screen, text="").pack()
    Button(screen, text="CloseApp", height="2", width="30", command=delete_mainScren).pack()

    

    screen.mainloop()



main_screen()

