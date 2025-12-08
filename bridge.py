from pythonosc import dispatcher, osc_server
import socket, json

SOCK = "/tmp/mpvsocket"
PORT = 9000
IP = "0.0.0.0"

def mpv(cmd):
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(SOCK)
        s.sendall((json.dumps(cmd) + "\n").encode())

def load(_, path):
    print(f"load {path}")
    mpv({"command": ["loadfile", path, "replace"]})

def pause(_):
    print("pause")
    mpv({"command": ["set_property", "pause", True]})

def resume(_):
    print("resume")
    mpv({"command": ["set_property", "pause", False]})

def stop(_):
    print("stop")
    mpv({"command": ["stop"]})

disp = dispatcher.Dispatcher()
disp.map("/load", load)
disp.map("/pause", pause)
disp.map("/resume", resume)
disp.map("/stop", stop)
server = osc_server.ThreadingOSCUDPServer((IP, PORT), disp)
server.serve_forever()
