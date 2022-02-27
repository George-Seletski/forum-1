#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
import sqlite3
from sqlite3 import *

#----Now comes the sockets part----
HOST = "192.168.56.1"
PORT = PORT = 4950

msg_list = []
my_msg = ''
msg = ''

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

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

def sql_delete_row(con, object_del):
     cursorObj = con.cursor()
     querry = 'DELETE from users where name_client = ' + str(object_del)
     cursorObj.execute(querry)
     con.commit()
     print("Record deleted successfully ")

############################################################################
def delete2():
    screen2.destroy()
#############################################################################
def register(screen):
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

def user_not_found():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title('ERROR')
    screen4.geometry("200x150")
    Label(screen4,text="User not found!").pack()
    screen4.destroy()

def password_not_found():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title('ERROR')
    screen4.geometry("150x100")
    Label(screen4,text="password not found").pack()

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
    print('OK! INFOR FROM DB UPLOADED!')
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
            # print('USER IS HERE!')
            if str(password1) in row:
                # print('PAS IS HERE!')
                chat(str(username1))
                #chat_thr = threading.Thread(target=chat_window, args=(username1))
                #chat_thr.start()
               
                delete2()
            else:
                password_not_found()
        else:
           user_not_found()

def delete_mainScren():
    # send(DISCONNECT_MSG)
    screen.destroy()
#############################################################################
def receive():
    """Handles receiving of messages."""
    global msg
    global msg_list
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, str(msg))
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global msg
    global my_msg
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf-8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def chat(name_win):

    global messages_frame
    global msg_list
    global my_msg
    global top

    top = Toplevel(screen)
    messages_frame = tkinter.Frame(top)
    top.title(name_win)
    
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    temp_list = msg_list
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    return msg_list

receive_thread = Thread(target=receive)
receive_thread.start()
#____________MAIN____________________________
global screen    
screen = tkinter.Tk()

screen.geometry("300x250")
screen.title("Login & Register")
Label(screen, text="Client", bg="grey", width ="300", height="2", font=("Calibri", 13)).pack()
Label(screen, text="").pack()

Button(screen, text="Login", height="2", width="30", command=login).pack()
Label(screen, text="").pack()
Button(screen, text="Register", height="2", width="30", command=register).pack()
    
Label(screen, text="").pack()
Button(screen, text="CloseApp", height="2", width="30", command=delete_mainScren).pack()

    



tkinter.mainloop()  # Starts GUI execution.