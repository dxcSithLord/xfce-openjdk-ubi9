#!/bin/bash
# Docker entrypoint script for XFCE base container
# Sets up environment for XFCE desktop with EPEL packages

set -e

# Function to log messages with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ENTRYPOINT: $1"
}

log "Starting XFCE base container with EPEL repositories..."

# Verify EPEL repository is available
if rpm -q epel-release >/dev/null 2>&1; then
    log "EPEL repository confirmed available"
else
    log "WARNING: EPEL repository not detected"
fi

# Create supervisor socket directory with correct permissions
mkdir -p /tmp/supervisor /tmp/runtime-root
chmod 755 /tmp/supervisor /tmp/runtime-root

# Set up environment variables for X11 and XFCE
export HOME=${HOME:-/root}
export USER=${USER:-root}
export LOGNAME=${LOGNAME:-root}
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/runtime-root}
export XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-x11}

# Ensure proper font cache
if command -v fc-cache >/dev/null 2>&1; then
    log "Updating font cache..."
    fc-cache -f -v >/dev/null 2>&1 || true
fi

log "Environment setup complete"

# Execute the command passed to the container
log "Executing command: $*"
exec "$@"
