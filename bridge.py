from pythonosc import dispatcher, osc_server
import socket, json

# TODO: move to config file
BLANK_PATH="media/blank.mp4"
SOCK = "/tmp/mpvsocket"
PORT = 9000
IP = "0.0.0.0"

def mpv(cmd):
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(SOCK)
        s.sendall((json.dumps(cmd) + "\n").encode())

def fallback(address, *args):
    print("fallback:", address, args)
    if address[0] == "/":
        address = address[1:]
    command = [ a for a in args ]
    command.insert(0, address)

    mpv({"command": command})

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

def blank(_):
    load("", BLANK_PATH)
    pause("")


disp = dispatcher.Dispatcher()
disp.set_default_handler(fallback)
disp.map("/load", load)
disp.map("/pause", pause)
disp.map("/resume", resume)
disp.map("/stop", stop)
disp.map("/blank", blank)
server = osc_server.ThreadingOSCUDPServer((IP, PORT), disp)
server.serve_forever()
