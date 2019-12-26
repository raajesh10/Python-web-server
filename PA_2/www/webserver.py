import socket
import os
import sys
import _thread
sys.argv
port = int ( sys.argv[1] )
host_name = socket.gethostname()
host = socket.gethostbyname( host_name )
print ('Current server location:' + host_name + ':' + host )
http_html = 'HTTP/1.1 200 Document Follows\r\nContent-Type:text/html\r\nContent-Length:'
http_jpg = 'HTTP/1.1 200 Document Follows\r\nContent-Type:image/jpg\r\nContent-Length:'
http_png = 'HTTP/1.1 200 Document Follows\r\nContent-Type:image/png\r\nContent-Length:'
http_gif = 'HTTP/1.1 200 Document Follows\r\nContent-Type:image/gif\r\nContent-Length:'
http_css = 'HTTP/1.1 200 Document Follows\r\nContent-Type:text/css\r\nContent-Length:'
http_js = 'HTTP/1.1 200 Document Follows\r\nContent-Type:applicaton/javascript\r\nContent-Length:'
http_icon ='HTTP/1.1 200 Document Follows\r\nContent-Type:image/vnd.microsoft.icon\r\nContent-Length:'
http_txt = 'HTTP/1.1 200 Document Follows\r\nContent-Type:image/plaintext\r\nContent-Length:'
http_error = 'HTTP/1.1 500 Internal Server Error \r\nContent-Type:text/html\r\nContent-Length:42\r\n\r\n<html><h1>Error 500: Internal Server Error</h1>\n</html>'
mover = '\r\n\r\n'

def sender ( file_name , client_sock , addr ):
    new_path = file_name.replace('/' , '\\')
    file_path = 'C:\\Users\\Admin\\Desktop\\www\\' + new_path
    x = int ( os.path.isfile( file_path ) )
    if ( x == 0 ):
        print('File not found!!!!!!!!!!!!!!!!! Sorry...............................')
        client_sock.send(http_error.encode('utf-8'))
        #break
    else:
        print('File found........................Loading data')
        data_len = str ( os.path.getsize( file_path ))
        if '.png' in file_name :
            client_msg = http_png + data_len + mover
            print(' sending .png file ***********')
        elif '.gif' in file_name:
            client_msg = http_gif + data_len + mover
            print(' sending .gif file************')
        elif '.jpg' in file_name:
            client_msg = http_jpg + data_len + mover
            print('sending .jpg file************')
        elif '.css' in file_name:
            client_msg = http_css + data_len + mover
            print('sending .css file************')
        elif '.js' in file_name:
            client_msg = http_js + data_len + mover
            print('sending .js file*************')
        elif '.html' in file_name:
            client_msg = http_html + data_len + mover
            print('sending .html file*************')
        elif '.txt' in file_name:
            client_msg = http_txt + data_len + mover
            print('sending .txt file************')
        elif '.ico' in file_name:
            client_msg = http_icon + data_len + mover
            print('sending .ico file***********')

        client_sock.send( client_msg.encode('utf-8'))
        file = open( file_path , 'rb')
        output_data = file.read(1024)
        while(output_data):
            if(client_sock.send(output_data)):
                output_data = file.read(1024)
                print('.................Loading data..................')
        print('@@@@@@@@@Loading data, completed@@@@@@@@')
        file.close()
        
def handler ( client_sock , addr ):
    while True:
        data = client_sock.recv(1024)
        if not data: break
        data = data.decode('utf-8')
        data = data.split()
        print(' ### Requested file_path from server:' + data[1] + '###' + '.......................................................')
        if ( (data[1] == '/') or ('index.html' in data[1])):
            print('sending index.html file*********')
            data_len = str (os.path.getsize('index.html'))
            client_msg = http_html + data_len + mover
            client_sock.send(client_msg.encode('utf-8'))
            file = open('index.html' , 'rb')
            output_data = file.read(1024)
            while(output_data):
                if(client_sock.send(output_data)):
                    output_data = file.read(1024)
                    print( '............. Loading index.html............. ')
            print ('$$$$$$$$$Loading index.html complete$$$$$$$$')
            file.close()
        else:
            print (' transfering control to func sender' )
            sender( data[1] , client_sock , addr )   


server_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
server_sock.bind(( host , port ))
server_sock.listen(10)
while True:
    ( client_sock , addr ) = server_sock.accept()
    _thread.start_new_thread(handler , ( client_sock , addr ))


