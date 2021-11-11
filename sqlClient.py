import sqlite3
from sqlite3 import *
from sqlite3 import Error


def sql_connection(): # connection to database file 
    try:
        con = sqlite3.connect('clients.db',check_same_thread=False)
        return con
    except sqlite3.Error:
        print(sqlite3.Error)

def sql_table(con): #creation database
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE CLIENTS(name_client text, passw text)")
    con.commit()
    return True

def sql_insert(con, entities): # inserting into database
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO CLIENTS(name_client,passw) VALUES(?,?)', entities)
    con.commit()

def sql_fetch(con): # check if the database is created already
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists CLIENTS(name_client,passw)')
    con.commit()
    return False

    
    
