import socket
import threading
from secret import *
import time

PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", PORT))
sock.listen(3)

global srv_conn
srv_conn_lock = threading.Lock()

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
    global srv_conn
    try:
        msg = recv_timeout(conn)
    except (TimeoutError, BufferError):
        conn.close()
        return
    try:
        msg = bytes.decode(msg).strip()
    except UnicodeDecodeError:
        print("Unable to decode message from ", addr)
        return
    if not msg.endswith(PASSWORD):
        conn.close()
        return
    if msg.startswith("pi"):
        # is Pi
        srv_conn_lock.acquire()
        srv_conn = conn
        srv_conn_lock.release()
        conn.send(bytearray("Connected as Pi", 'utf-8'))
        return
    # is client
    if srv_conn:
        try:
            srv_conn_lock.acquire()
            srv_conn.send(bytearray("Open", 'utf-8'))
        except socket.error:
            conn.send(bytearray("Error sending to Pi", 'utf-8'))
        finally:
            srv_conn_lock.release()
    else:
        conn.send(bytearray("No Pi connected", 'utf-8'))

    conn.close()

while True:
    try:
        conn, addr = sock.accept()
        print("Accepting connection from", addr)
        threading._start_new_thread(on_new_client, (conn, addr))
    except socket.timeout:
        pass
