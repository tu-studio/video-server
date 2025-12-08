import socket, json
import time

# mockup simulating schedcontrol.py in showcontrol project

def wrap_cmd(cmd, args={}):
    args["command"] = cmd
    return args
    # return {"command": cmd}

def send_udp_broadcast(cmd, ip="192.168.2.2", port=9000, args={}):
    cmd = wrap_cmd(cmd)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # <-- UDP
    msg = json.dumps(cmd).encode("utf-8")
    sock.sendto(msg, (ip, port))
    sock.close()

def pause():
    send_udp_broadcast(["set_property", "pause", "yes"])

def resume():
    send_udp_broadcast(["set_property", "pause", "no"])

def load(path):
    send_udp_broadcast(["loadfile", path, "replace"])

def play_video(index, start_paused=False):
    # Set all video players to the correct video
    send_udp_broadcast(["playlist-play-index", index])

    if not start_paused:
        time.sleep(0.03)
        send_udp_broadcast(["set_property", "pause", "no"], args={"async": True})


load("/home/pi/vid.mp4")
# resume()
# pause()
play_video(2)

