#importing required modules
import threading
import socket
print('=====SERVER IS RUNNING=====')

host = '127.0.0.1' #localhost
port = 55555    #can use any number between 0 to 65535

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #connecting to IPv4 addresses and TCP socket
server.bind((host,port))    #binding host and port
server.listen()   #can set limit of the clients server can isten to

clients = []
nicknames = []

def broadcast(message):     #broadcasting message to every client connected
    for client in clients:
        client.send(message)

def handle(client):     #handle client one by one in endless loop till it disconnects
    while True:
        try:
            msg=message = client.recv(1024)  #msg to check commands 
            
            if msg.decode('ascii').startswith('KICK'):   
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]   #starts from 'KICK_' 
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))  #if it's not admin
                    
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]   #starts with 'BAN_'
                    print(name_to_ban)
                    ban_user(name_to_ban)
                    with open ('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')     #creating a text file so banned user can't enter again
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused!'.encode('ascii'))   #if it's not admin

            else:
                broadcast(message)
            
        except:
            if client in clients:   #to exclude banned and kicked users
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
                broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

def receive():  
    while True:
        client, address = server.accept()  #adress includes tuple of host and port
        print(f'Connected with {str(address)}')
        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        
        with open('bans.txt','r') as f:
            bans = f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))   
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':   #checking the password
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client connected is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        
        thread = threading.Thread(target = handle, args = (client,))   #defining a thread for each client, need to process messages at same time
        thread.start()

def kick_user(name):  #defining kick function
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

def ban_user(name):
    if name == 'admin':
        print("You can't ban yourself")
        return
    elif name in nicknames:
        name_index = nicknames.index(name)
        client_to_ban = clients[name_index]
        clients.remove(client_to_ban)
        client_to_ban.send('You were banned by the admin!'.encode('ascii'))
        client_to_ban.close()
        nicknames.remove(name)
        broadcast(f'{name} was banned by the admin!'.encode('ascii'))
    else:
        print(f'User {name} not found')

print('Server is listening....')
receive()

