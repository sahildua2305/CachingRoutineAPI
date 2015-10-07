import socket, json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9000))
get_data = {"method"  : "GET",
		"username": "sahild"}
post_data = {"method" : "POST",
		"username": "sahildu",
		"fullname": "Sahil Du"}
s.send(json.dumps(get_data))
# s.send(json.dumps(post_data))
recv_data = s.recv(1024)
print recv_data
s.close()