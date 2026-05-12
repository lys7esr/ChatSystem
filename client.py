#importing required modules
import socket
import threading
print('=====CLIENT IS RUNNING=====')

nickname = input('Choose a nickname:')

if nickname == 'admin':  #if admin want to login
    password = input('Enter password for admin login:')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))

stop_thread = False 

def receive():
    while True:
        global stop_thread
        
        if stop_thread:
            break
        
        try:
            message = client.recv(1024).decode('ascii')
            
            if message=='NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection refused! Wrong password!')
                        stop_thread = True  #i.e. password is wrong and you can't enter
                        
                elif next_message == 'BAN':    #if person is banned
                    print('Connection refused because you were banned by admin!')
                    client.close()
                    stop_thread = True
                
            else:
                print(message)
                
        except:
            print('An error occurred!')
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))   #sent to server that next message is KICK
                    
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))   #sent to server that next message is BAN
                    
            else:
                print('Commands can only be executed by admin')  #if nickname is not admin but still wants to execute commands
                
        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)   #running two threads simultaneously
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


