import socket
import pickle
from rsa import *

def option(verified,encrypted_message,sign_message,server_public):
    print '1. Verify\n2. Encrypted Message\n3. Digital Signed Message\n4. Public Key of Server\n5. Continue\n ' 
    while True:
        ch = input('Choice :')
        if ch == 1:
            print '\nVerification -> ' + str(verified)
        
        elif ch == 2 :
            print '\nEncrypted Message -> ' + encrypted_message
        
        elif ch == 3:
            print '\nDigital Signed Message -> ' + sign_message

        elif ch == 4:
           print '\nServer Key -> ' + str(server_public)
           
        else:
            break

def encrypt_option(message,client_socket,private,public):
    print '1. Encrypt\n2. Digital Sign\n3. Both\n ' 
    while True:
        ch = input('Choice :')
        if ch == 1:
            encrypted_message = encrypt(message,public)
            client_socket.send(str(1))
            client_socket.send(encrypted_message)
            break
            
        elif ch == 2 :
            sign_message = sign (message, private)
            client_socket.send(str(2))
            client_socket.send(message)
            client_socket.send(sign_message)
            break
        
        elif ch == 3:
            encrypted_message = encrypt(message,public)
            sign_message = sign (encrypted_message, private)

            client_socket.send(str(3))
            client_socket.send(encrypted_message)
            client_socket.send(sign_message)
            break
       
        else:
            break
            
def client_program():
    public, private = newkeys(1024)
    
    host = socket.gethostname()  # as both code is running on same pc
    port = 5003  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    server_public = importKey(client_socket.recv(2048))
    client_socket.send(exportKey(public))
    
    message = raw_input(" -> ")  # take input
    encrypted_message=encrypt(message, server_public)
    sign_message = sign (encrypted_message, private)

    while message != '':

        encrypt_option(message,client_socket,private,server_public)

        ch = client_socket.recv(1024)

        if ch == '1':
            
            encrypted_message = client_socket.recv(1024)
            message = decrypt(encrypted_message,private)
            print '\nReceived from server: ' + message

            option('False',encrypted_message,'Not Signed',server_public)
            
        elif ch == '2':

            message = client_socket.recv(1024)
            sign_message = client_socket.recv(1024)
            verified = verify(message,server_public,sign_message)
            print '\nReceived from server: ' + message

            option(verified,'Not Encrypted',sign_message,server_public)
        
        elif ch == '3':
            
            encrypted_message = client_socket.recv(1024)
            sign_message = client_socket.recv(1024)
            verified = verify(encrypted_message,server_public,sign_message)
            message = decrypt(encrypted_message,private)
            print '\nReceived from server: ' + message

            option(verified,encrypted_message,sign_message,server_public)
        


        message = raw_input(" -> ")  # again take input

        
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
