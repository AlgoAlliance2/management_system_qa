import socket
import requests
import time

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

ports = [3000, 3001, 8080, 5173]

print("Checking ports...")
for p in ports:
    status = "OPEN" if check_port(p) else "CLOSED"
    print(f"Port {p}: {status}")

print("\nChecking API endpoint /api/auth/ ...")
try:
    # Try to hit a known endpoint, e.g. /api or just root implies 404 but connection works
    r = requests.get('http://localhost:8080/api/auth', timeout=5)
    print(f"Response from 8080: {r.status_code}")
except Exception as e:
    print(f"Error 8080: {e}")

try:
    r = requests.get('http://localhost:3001/api/auth', timeout=5)
    print(f"Response from 3001: {r.status_code}")
except Exception as e:
    print(f"Error 3001: {e}")
