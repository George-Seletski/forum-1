# forum-1


### Description of the process:
Server gets data from a client and then he shows the window with published messages from the client(users.db).

After user signed up in system. The client's program record all gotten info from user in <em>"users.db" database (his nickname & password)</em>. 
Then if user write something on forum, the server will receive message from the plugged client.<br>
While the reciveng it should to check the user's name in the "users.db". After that it shows messages on its window. All messages forum app keeps in "loggy.db".

### How to launch:
to start server
```
python server_gui.py
```
to start clinet
```
python client_dir/client_app_sql.py
```