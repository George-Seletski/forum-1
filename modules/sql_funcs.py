import sqlite3
from sqlite3 import Error

def sql_connection(): # connection to database file 
    try:
        con = sqlite3.connect('history.db',check_same_thread=False)
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con): #creation database
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE logs(name_client text, msg text, date_time text)")
    con.commit()
    return True

def sql_insert(con, entities): # inserting into database
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO logs(name_client,msg, date_time) VALUES(?,?, ?)', entities)
    con.commit()

def sql_fetch(con): # check if the database is created already
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists logs(name_client,msg, date_time)')
    con.commit()
    return False

def sql_fetchall(con, text):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM logs')
    rows = cursorObj.fetchall()
    for row in rows:
        text.insert(INSERT,row)
        text.insert(INSERT,'\n')

def sql_connection_logs(): # connection to database file 
    try:
        con = sqlite3.connect('logs.db',check_same_thread=False)
        return con
    except sqlite3.Error:
        print(sqlite3.Error)
