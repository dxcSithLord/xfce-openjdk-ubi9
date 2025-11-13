#!/bin/bash
# VNC startup script for XFCE desktop environment
# Starts XFCE with VNC server for remote access
# Enhanced for Iron Bank compliance and EPEL-based XFCE

set -e

# Set default values if not provided
VNC_PORT=${VNC_PORT:-5901}
VNC_RESOLUTION=${VNC_RESOLUTION:-1280x1024}
VNC_COL_DEPTH=${VNC_COL_DEPTH:-24}
DISPLAY=${DISPLAY:-:1}

# Function to log messages with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] VNC: $1"
}

log "Starting XFCE desktop with VNC server (EPEL-based)..."

# Kill any existing X servers on this display
log "Cleaning up any existing X servers on display $DISPLAY..."
pkill -f "Xvfb $DISPLAY" || true
pkill -f "x11vnc.*$DISPLAY" || true
sleep 2

# Start Xvfb (virtual framebuffer X server)
log "Starting Xvfb on display $DISPLAY with resolution ${VNC_RESOLUTION}x${VNC_COL_DEPTH}..."
Xvfb $DISPLAY -screen 0 ${VNC_RESOLUTION}x${VNC_COL_DEPTH} -ac +extension GLX +render -noreset &
XVFB_PID=$!

# Wait for X server to be fully ready
log "Waiting for X server to be ready..."
sleep 5

# Verify X server is running
if ! xdpyinfo -display $DISPLAY >/dev/null 2>&1; then
    log "ERROR: X server failed to start on display $DISPLAY"
    kill $XVFB_PID 2>/dev/null || true
    exit 1
fi

log "X server successfully started on display $DISPLAY"

# Set the DISPLAY environment variable for all processes
export DISPLAY

# Start x11vnc VNC server
log "Starting x11vnc VNC server on port $VNC_PORT..."
x11vnc -display $DISPLAY \
       -forever \
       -shared \
       -rfbport $VNC_PORT \
       -bg \
       -nopw \
       -cursor arrow \
       -o /tmp/x11vnc.log

# Wait for VNC server to start
sleep 3

# Verify VNC server is running
if ! pgrep -f "x11vnc.*$DISPLAY" > /dev/null; then
    log "ERROR: VNC server failed to start"
    kill $XVFB_PID 2>/dev/null || true
    exit 1
fi

log "VNC server successfully started on port $VNC_PORT"

# Setup XFCE environment
log "Setting up XFCE environment..."
export DISPLAY
export XDG_SESSION_TYPE=x11
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p "$XDG_RUNTIME_DIR"

# Start XFCE session
log "Starting XFCE desktop session..."
exec xfce4-session
