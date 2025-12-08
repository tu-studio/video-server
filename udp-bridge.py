#!/usr/bin/env python3
import socket
import json

# TODO: move to config file
BLANK_PATH = "media/blank.mp4"
SOCK = "/tmp/mpvsocket"
UDP_IP = "0.0.0.0"
UDP_PORT = 9000
BUFFER_SIZE = 4096

def mpv(cmd):
    try:
        with socket.socket(socket.AF_UNIX) as s:
            s.connect(SOCK)
            s.sendall((json.dumps(cmd) + "\n").encode())
    except Exception as e:
        print("Failed to send to mpv:", e)

# Handlers
def fallback(cmd_json):
    print("fallback:", cmd_json)
    if isinstance(cmd_json, dict) and "command" in cmd_json:
        mpv(cmd_json)
    elif isinstance(cmd_json, list):
        mpv({"command": cmd_json})
    else:
        print("Unknown command format:", cmd_json)

def load(path):
    print(f"load {path}")
    mpv({"command": ["loadfile", path, "replace"]})
    # resume()

def pause():
    print("pause")
    mpv({"command": ["set_property", "pause", True]})

def resume():
    print("resume")
    mpv({"command": ["set_property", "pause", False]})

def stop():
    print("stop")
    mpv({"command": ["stop"]})

def blank(_=""):
    load(BLANK_PATH)
    pause()

HANDLERS = {
    "load": load,
    "pause": pause,
    "resume": resume,
    "stop": stop,
    "blank": blank,
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening for UDP on {UDP_IP}:{UDP_PORT}...")

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        try:
            msg = json.loads(data.decode("utf-8").strip())
        except Exception as e:
            print("Invalid JSON:", data)
            continue

        # If msg is a dict with a "command" key, relay directly
        if isinstance(msg, dict) and "command" in msg:
            fallback(msg)
            continue

        # If msg is a simple dict with a key matching handler
        if isinstance(msg, dict):
            for key, val in msg.items():
                if key in HANDLERS:
                    HANDLERS[key](val)
                else:
                    fallback(msg)
        # If msg is a string command
        elif isinstance(msg, str) and msg in HANDLERS:
            HANDLERS[msg]()
        else:
            fallback(msg)

    except Exception as e:
        print("Error handling UDP message:", e)

