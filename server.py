import socket
import pickle

from rsa import *

def option(verified,encrypted_message,sign_message,client_public):
    print '1. Verify\n2. Encrypted Message\n3. Digital Signed Message\n4. Public Key of Client\n5. Continue\n ' 
    while True:
        ch = input('Choice :')
        if ch == 1:
            print '\nVerification -> ' + str(verified)
        
        elif ch == 2:
            print '\nEncrypted Message ->' + encrypted_message

        elif ch == 3:
            print '\nDigital Signed Message -> ' + sign_message
        
        elif ch == 4:
            print '\nClient Key -> ' + str(client_public)
       
        else:
            break

def encrypt_option(message,conn,private,public):
    print '1. Encrypt\n2. Digital Sign\n3. Both\n ' 
    while True:
        ch = input('Choice :')
        if ch == 1:
            encrypted_message = encrypt(message,public)
            conn.send(str(1))
            conn.send(encrypted_message)
            break
            
        elif ch == 2 :
            sign_message = sign (message, private)
            conn.send(str(2))
            conn.send(message)
            conn.send(sign_message)
            break
        
        elif ch == 3:
            encrypted_message = encrypt(message,public)
            sign_message = sign (encrypted_message, private)
            conn.send(str(3))
            conn.send(encrypted_message)
            conn.send(sign_message)
            break
       
        else:
            break
        
def server_program():
    
    public, private = newkeys(1024)
    
    # get the hostname
    host = socket.gethostname()
    port = 5003  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print "Connection from: " + str(address)

    conn.send(exportKey(public)) 
    client_public = importKey(conn.recv(2048))
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        ch = conn.recv(1024)
        
        if ch == '1':
            encrypted_message = conn.recv(1024)
            message = decrypt(encrypted_message,private)
            if not message:
                # if data is not received break
                break
        
            print "\nFrom connected user: " + str(message)

            option('False',encrypted_message,'Not Signed',client_public)
            
        elif ch == '2':

            message = conn.recv(1024)
            sign_message = conn.recv(1024)
            verified = verify(message,client_public,sign_message)
            if not message:
                # if data is not received break
                break
        
            print "\nFrom connected user: " + str(message)

            option(verified,'Not Encrypted',sign_message,client_public)
        
        elif ch == '3':
            
            encrypted_message = conn.recv(1024)
            sign_message = conn.recv(1024)
            verified = verify(encrypted_message,client_public,sign_message)
            message = decrypt(encrypted_message,private)
            if not message:
                # if data is not received break
                break
        
            print "\nFrom connected user: " + str(message)

            option(verified,encrypted_message,sign_message,client_public)
        
        
        message = raw_input(' -> ')

        encrypt_option(message,conn,private,client_public)
        
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
