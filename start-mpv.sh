#!/usr/bin/env bash

# Detect connector from /sys/class/drm/card1-* that is "connected"
CONNECTED=$(for c in /sys/class/drm/card1-*; do
    [ -f "$c/status" ] || continue
    if grep -q "connected" "$c/status"; then
        basename "$c" | cut -d- -f2-
    fi
done | head -n1)

# Fallback if nothing was found
if [ -z "$CONNECTED" ]; then
    CONNECTED="HDMI-A-1"
fi

# echo "Using connector: $CONNECTED"

SOCKET=/tmp/mpvsocket
mpv \ 
    --terminal=no \
    --vo=drm \
    --drm-device=/dev/dri/card1 \
    --drm-connector="$CONNECTED" \
    --input-ipc-server=$SOCKET \
    --idle=yes
    "$@"
