#!/usr/bin/env bash

# detect connector from /sys/class/drm/card1-* that is connected
# potentially unneeded
# if this does not work in HUFO, could be a place to check
CONNECTED=$(for c in /sys/class/drm/card1-*; do
    [ -f "$c/status" ] || continue
    if grep -q "connected" "$c/status"; then
        basename "$c" | cut -d- -f2-
    fi
done | head -n1)

# fallback if nothing was found
CONNECTED="${CONNECTED:-"HDMI-A-1"}"
SOCKET="${SOCKET:-"/tmp/mpvsocket"}"
PLAYLIST="${PLAYLIST:-"$HOME/videos/playlist.txt"}"

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
