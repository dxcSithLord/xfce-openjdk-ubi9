# Iron Bank XFCE Desktop Environment Container
# Based on Iron Bank OpenJDK 21 container with XFCE desktop
# Serves as intermediate container for GUI Java applications

ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/redhat/openjdk/openjdk21-runtime-ubi9-slim
ARG BASE_TAG=1.21

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

# Labels will be set in hardening_manifest.yaml per Iron Bank requirements

# Install EPEL repository following Red Hat best practices and XFCE packages
RUN subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms 2>/dev/null || true && \
    dnf install -y --nodocs https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# Install X11 base system and XFCE components in optimized layers
RUN dnf install -y --nodocs \
        # X11 base system
        xorg-x11-server-Xvfb \
        xorg-x11-xinit \
        xorg-x11-utils \
        xorg-x11-xauth && \
    dnf install -y --nodocs --enablerepo=epel \
        # XFCE core desktop group packages
        xfce4-session \
        xfce4-settings \
        xfce4-panel \
        xfce4-desktop \
        xfce4-terminal \
        xfce4-taskmanager \
        xfce4-whiskermenu-plugin \
        xfce4-screensaver \
        xfce4-appfinder \
        # Window manager and compositor
        xfwm4 \
        xfce4-screenshooter \
        # File manager and utilities
        thunar \
        thunar-archive-plugin \
        thunar-media-tags-plugin \
        file-roller \
        # Text editor
        mousepad \
        # VNC server for remote access
        x11vnc && \
    dnf install -y --nodocs \
        # Essential applications from UBI repositories
        firefox \
        # Audio support
        pulseaudio \
        # Network and system tools
        openssh-clients \
        procps-ng \
        which \
        nano \
        # Process management
        supervisor && \
    # Remove unnecessary build and development packages to reduce attack surface
    dnf remove -y \
        gcc \
        gcc-c++ \
        make \
        rpm-build \
        man-db \
        man-pages 2>/dev/null || true && \
    dnf autoremove -y && \
    dnf clean all && \
    rm -rf /var/cache/dnf /tmp/* /var/tmp/* && \
    # Create necessary directories for XFCE and supervisor
    mkdir -p /etc/supervisor/conf.d /etc/xfce4

# Copy configuration files from build context
COPY config/xfce4-session.rc /etc/xfce4/
COPY config/vnc-startup.sh /usr/local/bin/
COPY scripts/docker-entrypoint.sh /usr/local/bin/
COPY scripts/supervisord.conf /etc/supervisor/conf.d/

# Set proper permissions for scripts, configs, and security hardening
RUN chmod +x /usr/local/bin/vnc-startup.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chmod 644 /etc/xfce4/xfce4-session.rc && \
    # Remove any SETUID/SETGID binaries for security (Iron Bank requirement)
    find / -perm /6000 -type f -exec chmod a-s {} \; 2>/dev/null || true && \
    # Set secure file permissions
    chmod 700 /root 2>/dev/null || true && \
    find /etc -name "*.conf" -exec chmod 644 {} \; 2>/dev/null || true && \
    # Ensure proper ownership of copied files
    chown root:root /usr/local/bin/vnc-startup.sh /usr/local/bin/docker-entrypoint.sh

# Expose VNC port for remote desktop access
EXPOSE 5901

# Set environment variables for VNC and XFCE
ENV DISPLAY=:1 \
    VNC_PORT=5901 \
    VNC_RESOLUTION=1280x1024 \
    VNC_COL_DEPTH=24

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command to start supervisor managing XFCE and VNC
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
