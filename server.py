#  coding: utf-8 
import socketserver, os, time

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data, flush=True)
        data_decoded = self.data.decode('utf-8')
        # print("All data: ", data_decoded)

        request = data_decoded.split('\r\n')[0]
        # print("\nrequest: ", request)

        request_data = request.split(' ')

        method = request_data[0]
        # print("\nmethod: ", method)

        URI = request_data[1]
        # print("\nURI: ",URI)

        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())

        Date = "\r\nDate: "+ date

        Connection = "\r\nConnection: close"

        # only support get requests
        if(method== "GET"):
            if "css" not in URI:
                if "index.html" not in URI:
                    if(URI[-1] == "/"):
                        URI = URI + "index.html"
                    else:
                        # Error code 301
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently"+Date+"\r\nLocation:" + URI +'/' + "\r\nContent-Length: 0" + Connection + "\r\nContent-Type: text/html\r\n",'utf-8'))
                        return
            path = "./www" + URI

        # Error code 405 for methods other than GET
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed" + Date + "\r\nContent-Length: 0" + Connection + "\r\nContent-Type: text/html\r\n",'utf-8'))
            return

        # Status 200 Ok
        if(os.path.exists(path)):
            file = open(path,'r')
            data = file.read()

            if ".html" in URI:
                self.request.sendall(bytearray('HTTP/1.1 200 OK' + Date + "\r\nContent-Length: " + str(len(data)) + Connection + '\r\n'+"Content-Type: text/html\r\n"  +"\r\n"+data,'utf-8'))
                # print('HTTP/1.1 200 OK' + Date + "\r\nContent-Length: " + str(len(data)) + Connection + '\r\n'+"Content-Type: text/html\r\n"  +"\r\n"+data)
            elif ".css" in URI:
                self.request.sendall(bytearray('HTTP/1.1 200 OK' + Date + "\r\nContent-Length: " + str(len(data)) + Connection + '\r\n'+"Content-Type: text/css\r\n"  +"\r\n"+data,'utf-8'))
            
            return
        
        # Error code 404 Not Found!
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found" + Date + "\r\nContent-Length: 0" + Connection + "\r\nContent-Type: text/html\r\n",'utf-8'))
            return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print("Starting Server\n")
    server.serve_forever()