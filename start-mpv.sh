#!/usr/bin/env bash

# Detect connector from /sys/class/drm/card1-* that is "connected"
CONNECTED=$(for c in /sys/class/drm/card1-*; do
    [ -f "$c/status" ] || continue
    if grep -q "connected" "$c/status"; then
        basename "$c" | cut -d- -f2-
    fi
done | head -n1)

# Fallback if nothing was found
CONNECTED="${CONNECTED:-"HDMI-A-1"}"
SOCKET="${SOCKET:-"/tmp/mpvsocket"}"
PLAYLIST="${PLAYLIST:-"/home/pi/playlist.txt"}"

exec mpv \
    --input-ipc-server=$SOCKET \
    --hwdec=auto \
    --ao=jack \
    --fs \
    --loop-playlist \
    --video-output-levels=limited \
    --audio-channels=stereo \
    --volume=80 \
    --playlist=$PLAYLIST \
    --terminal=no \
    --vo=drm \
    --drm-device=/dev/dri/card1 \
    --drm-connector="$CONNECTED" \
    --idle=yes \

