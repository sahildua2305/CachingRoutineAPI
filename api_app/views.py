from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import User, FlatchatUser
import socket, json

# Signup view
@csrf_exempt
def signup_view(request):
	if request.method == "POST":
		try:
			username = request.POST['username']
			password = request.POST['password']
		except KeyError as kerr:
			# Insufficient number of arguments
			return JsonResponse({"error": "missing {}".format(kerr.args[0])}, status = 400)
		if username in ("signup", "login", "logout"):
			return JsonResponse({"error": "username can't be '{}'".format(username)}, status = 400)
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			# No user exists with this username
			# Create new user with given login credentials
			default_user = User.objects.create_user(username = username, password = password)
			default_user.save()
			flatchat_user = FlatchatUser(user = default_user, data = "")
			flatchat_user.save()
			return JsonResponse({"msg": "signup successful"}, status = 200)
		else:
			# A user already exists with the given username
			return JsonResponse({"msg": "username '{}' already exists".format(username)}, status = 400)
	else:
		# Method not allowed
		return JsonResponse({"msg": "method '{}' not allowed".format(request.method)}, status = 405)

# Login View
@csrf_exempt
def login_view(request):
	if request.method == "POST":
		try:
			username = request.POST['username']
			password = request.POST['password']
		except KeyError as kerr:
			# Insufficient number of arguments
			return JsonResponse({"error": "missing {}".format(kerr.args[0])}, status=400)
		# Try to authenticate the user with given login credentials
		login_user = authenticate(username = username, password = password)
		if login_user is not None:
			# Trigger login for given login credentials
			login(request, login_user)
			return JsonResponse({"msg": "login successful"}, status = 200)
		else:
			# Wrong login credentials
			return JsonResponse({"msg": "wrong login credentials"}, status = 400)
	else:
		# Method not allowed
		return JsonResponse({"msg": "method '{}' not allowed".format(request.method)}, status = 405)

# Logout view
@csrf_exempt
def logout_view(request):
	if request.method == "POST":
		try:
			username = request.POST['username']
		except KeyError as kerr:
			# Insufficient number of arguments
			return JsonResponse({"msg": "missing{}".format(kerr.args[0])}, status = 400)
		# Trigger a logout action on the given request
		logout(request)
		return JsonResponse({"msg": "logout successful"}, status = 200)
	else:
		# Method not allowed
		return JsonResponse({"msg": "method '{}' not allowed".format(request.method)}, status = 405)

# Get/Update Data view
@csrf_exempt
def user_data_view(request, username):
	if not request.user.is_authenticated():
		# Is the user isn't authenticated already
		return JsonResponse({"msg": "permission denied"}, status = 403)
	if request.method == "GET":
		# make GET request to port 9000 and read the response
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("localhost", 9000))
		get_data = {"method"   : "GET",
					"username" : username}
		s.send(json.dumps(get_data))
		recv_data = s.recv(1024)
		s.close()
		if recv_data != "-1":
			# user data found in cache
			return JsonResponse({"msg": "user data retrieved successfully", "data": recv_data}, status=200)
		else:
			# user data not found in cache
			# Find from db
			query = ""
			fetched_data = ""
			# make POST request to save the data in cache
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(("localhost", 9000))
			post_data = {"method"  : "POST",
						"username" : username,
						"userdata" : fetched_data}
			s.send(json.dumps(post_data))
			s.close()
		# Return the user data
		return JsonResponse({"msg": "user data retrieved successfully", "data": request.user.flatchatuser.data}, status=200)
	elif request.method == "POST":
		try:
			data = request.POST['data']
		except KeyError as kerr:
			# Insufficient number of arguments
			return JsonResponse({"msg": "missing {}".format(kerr.args[0])}, status = 400)
		# Update the user data
		request.user.flatchatuser.data = data
		request.user.flatchatuser.save()
		return JsonResponse({"msg": "user data updated successfully"}, status = 200)
	else:
		# Method not allowed
		return JsonResponse({"msg": "method '{}' not allowed".format(request.method)}, status = 405)
