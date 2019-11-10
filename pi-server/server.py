import socket
import threading
from secret import *
import time

PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", PORT))
sock.listen(3)

def recv_timeout(conn, timeout=10, max_size=1024):
    conn.setblocking(0)
    ret_val = []
    begin=time.time()
    while True:
        if time.time() - begin > timeout:
            raise TimeoutError("Listen timed out")
        try:
            data = conn.recv(1024)
            if data:
                ret_val.extend(data)
                if ret_val[-1] == 0:
                    return bytes(ret_val)
                if len(ret_val) > max_size:
                    raise BufferError("Max buffer size exceeded")
            else:
                time.sleep(0.1)
        except socket.error:
            pass
    return bytes(ret_val)

def on_new_client(conn, addr):
    try:
        msg = recv_timeout(conn)
    except (TimeoutError, BufferError):
        conn.close()
        return
    if bytes.decode(msg).strip() != PASSWORD:
        conn.close()
        return
    conn.send(bytearray("Logged in!", 'utf-8'))
    conn.close()

while True:
    try:
        conn, addr = sock.accept()
        threading._start_new_thread(on_new_client, (conn, addr))
    except socket.timeout:
        pass