from lrucache import LRUCache
import socket, json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# for reusing the same port without waiting for TIME_WAIT to expire
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 9000))

# Will listen to only one connection at a time
s.listen(1)

LRU = LRUCache(5)

get_flag = False
post_flag = False

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
    	conn.send(lru_response)
    elif request_method == "POST":
    	LRU.set(json_data["username"], json_data["fullname"])

    conn.close()
