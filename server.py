# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:54:00 2024

@author: Pietro
"""

import sys
import http.server
import socketserver
import os

class myRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
       content_types = {".html": "text/html", ".png": "image/png"}
       file_path = self.path[1:]
       if not file_path:
           file_path = "index.html"

       # Controlla se il file esiste
       if os.path.exists(file_path) and os.path.isfile(file_path):
           ext = os.path.splitext(file_path)[1]
           if ext in content_types:
               self.send_response(200)
               self.send_header("Content-Type", content_types[ext])
           else:
               # Se il file non è un'immagine o una paginal html invia un errore 415
               self.send_response(415)
               self.end_headers()
               self.wfile.write(b"Unsupported file type. Only .html and .png are supported.")
               return

           # Invia l'header
           self.end_headers()

           # Legge e invia il contenuto del file
           try:
               with open(file_path, "rb") as file:
                   self.wfile.write(file.read())
           except Exception:
               # Se accade un errore nella lettura del file invia un errore 500
               self.send_response(500)
               self.end_headers()
               self.wfile.write(b"Internal server error")

       else:
           # Se il file non esiste invia un errore 404
           self.send_response(404)
           self.end_headers()
           self.wfile.write(b"File not found")


if sys.argv[1:]:
    hostIP = str(sys.argv[1])
else:
    print("Error: Need host IP as first argument")
    sys.exit(1)
    
port = int(sys.argv[2]) if sys.argv[2:] else 8080
if not (1 <= port <= 65535):
    print("Error: Port must be an integer between 1 and 65535")
    sys.exit(1)
    
socketserver.ThreadingTCPServer.allow_reuse_address = True

try:
    server = socketserver.ThreadingTCPServer((hostIP, port), myRequestHandler)
except OSError as e:
    print("Failed to start server: ", e)
    sys.exit(1)

server.daemon_threads = True
        

# entra nel loop infinito
print(f"Server open:\nIP address: {hostIP}\nport: {port}")
try:
    while True:
        sys.stdout.flush()
        server.serve_forever()
except KeyboardInterrupt:
    print('Exiting http server (Ctrl+C pressed)')
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally: #si assicura che il server venga chiuso correttamente
    server.server_close()