from lrucache import LRUCache
import socket, json, sys

if len ( sys.argv ) >= 5 :
    server_name = sys.argv[1]
    port_number = sys.argv[2]
    number_of_connections = sys.argv[3]
    size_of_cache = sys.argv[4]
else:
    print "Usage: python cache-routine.py server_name port_number number_of_connections size_of_cache"
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# for reusing the same port without waiting for TIME_WAIT to expire
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_name, port_number))

# Will listen to only one connection at a time
s.listen( number_of_connections )

LRU = LRUCache( size_of_cache )

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    print "DEBUG: " + data

    # convert the received data into JSON
    json_data = json.loads(data)

    """
    fetch the request method
    GET denotes a GET cache request to check for hit/miss
    POST denotes a SAVE request once a miss happens
    """
    request_method = json_data["method"]
    if request_method == "GET":
    	lru_response = LRU.get(json_data["username"])
    	conn.send(str(lru_response))
    elif request_method == "POST":
    	LRU.set(json_data["username"], json_data["userdata"])

    conn.close()
