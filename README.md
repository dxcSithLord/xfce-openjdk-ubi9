# XFCE Desktop with OpenJDK 21 Container

## Overview

This Iron Bank compliant container provides XFCE desktop environment with OpenJDK 21 runtime using EPEL repositories. It serves as an intermediate base image for GUI Java applications requiring a desktop environment and VNC remote access capabilities.

## Container Hierarchy

```
XFCE + OpenJDK 21 Container (this)
    ↓ inherits from
OpenJDK 21 Container (Iron Bank)
    ↓ inherits from
UBI 9.6 (Iron Bank approved base)
```

## Features

- **XFCE 4.18 Desktop Environment**: Complete lightweight desktop from EPEL
- **OpenJDK 21 Runtime**: Inherited from Iron Bank OpenJDK container
- **VNC Remote Access**: x11vnc server for remote desktop connectivity
- **EPEL Repository**: Properly configured for XFCE package management
- **Iron Bank Security Compliance**: All security hardening inherited
- **GUI Application Support**: Ready for Java GUI applications

## Base Image Dependencies

- **Base**: `registry1.dso.mil/ironbank/redhat/openjdk/openjdk21-runtime-ubi9-slim:1.21`
- **EPEL Repository**: EPEL 9 for XFCE packages
- **Security**: All Iron Bank security measures inherited

## Installed Components

### EPEL Repository Setup
- CodeReady Builder repository enabled
- EPEL release package installed from Fedora Project
- Repository validation and verification

### XFCE Desktop Environment
- XFCE Session Manager and Settings
- XFCE Panel with Whisker Menu
- XFCE Window Manager (xfwm4)
- XFCE Terminal and Desktop
- Thunar File Manager with plugins
- Mousepad text editor

### VNC Server
- x11vnc server for remote access
- Xvfb virtual framebuffer
- Supervisor process management

### Inherited from Base
- OpenJDK 21 runtime and development tools
- Liberation and DejaVu font packages
- Security hardening and compliance

## EPEL Repository Management

### Repository Configuration
The container follows Red Hat best practices for EPEL setup:

```bash
# Enable CodeReady Builder (CRB) repository
subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms

# Install EPEL release package
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm

# Verify EPEL installation
rpm -qi epel-release

# List available XFCE packages
dnf --enablerepo=epel group list | grep -i xfce
```

### Package Sources
- **UBI 9 Packages**: Base system, Java runtime, core utilities
- **EPEL Packages**: XFCE desktop environment components
- **Security**: All packages validated through Iron Bank pipeline

## Kubernetes Deployment

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xfce-openjdk
spec:
  replicas: 1
  selector:
    matchLabels:
      app: xfce-openjdk
  template:
    metadata:
      labels:
        app: xfce-openjdk
    spec:
      containers:
      - name: xfce-openjdk
        image: registry1.dso.mil/ironbank/opensource/xfce/xfce-openjdk21:4.18-openjdk21.0.5-ubi9.6
        ports:
        - containerPort: 5901
          name: vnc
          protocol: TCP
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: VNC_RESOLUTION
          value: "1280x1024"
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
      volumes:
      - name: tmp-volume
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: xfce-openjdk-service
spec:
  selector:
    app: xfce-openjdk
  ports:
  - port: 5901
    targetPort: 5901
    name: vnc
  type: ClusterIP
```

### Resource Requirements

| Component | Minimum | Recommended | Maximum |
|-----------|---------|-------------|---------|
| **CPU** | 250m | 500m | 1000m |
| **Memory** | 512Mi | 1Gi | 2Gi |
| **Storage** | 2Gi | 4Gi | 8Gi |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISPLAY` | `:1` | X11 display number |
| `VNC_PORT` | `5901` | VNC server port |
| `VNC_RESOLUTION` | `1280x1024` | Screen resolution |
| `VNC_COL_DEPTH` | `24` | Color depth |
| `JAVA_HOME` | `/usr/lib/jvm/java-21-openjdk` | Java installation directory |

## Usage as Base Image

### Example Dockerfile for Java GUI Application

```dockerfile
# Use XFCE + OpenJDK base image
ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/xfce/xfce-openjdk21
ARG BASE_TAG=4.18-openjdk21.0.5-ubi9.6

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

# Install your Java GUI application
COPY myapp.jar /opt/
COPY config/ /etc/myapp/

# Configure application startup
COPY scripts/start-app.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-app.sh

# Application-specific environment
ENV APP_HOME=/opt

# Start application
CMD ["start-app.sh"]
```

## Network Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| `5901` | TCP | VNC Server for remote desktop |

## Security Features

### Iron Bank Compliance
- ✅ Iron Bank approved base images
- ✅ Security hardening inherited from base
- ✅ SETUID/SETGID binary removal
- ✅ Minimal attack surface
- ✅ Package updates and cache cleanup

### EPEL Security
- EPEL packages validated through Iron Bank pipeline
- Repository signatures verified
- Package integrity maintained

### Additional Security
- VNC server runs without authentication by default (configure for production)
- Desktop environment optimized for container use
- Minimal privileged operations

## Troubleshooting

### Common Issues

**EPEL Repository Issues**
- Verify EPEL release package installation: `rpm -qi epel-release`
- Check repository availability: `dnf repolist | grep epel`
- Validate package signatures during installation

**VNC Connection Fails**
- Verify port 5901 is accessible
- Check X server startup in logs: `tail -f /tmp/xfce4.log`
- Ensure XFCE session starts correctly

**Java Applications Won't Display**
- Verify DISPLAY environment variable is set
- Check Java application uses correct display
- Ensure X11 forwarding if needed

**Desktop Performance Issues**
- Increase memory allocation
- Adjust VNC color depth and resolution
- Monitor CPU usage during GUI operations

### Log Files

- **Supervisor**: `/tmp/supervisord.log`
- **XFCE**: `/tmp/xfce4.log` 
- **VNC Server**: `/tmp/x11vnc.log`

## License

Components under various licenses:
- **XFCE**: GPL-2.0-or-later
- **OpenJDK**: GPL-2.0 with Classpath Exception (inherited)
- **Red Hat UBI**: Red Hat Universal Base Image EULA (inherited)
- **EPEL**: Various licenses per package

## References

- [XFCE Documentation](https://docs.xfce.org/)
- [EPEL Repository](https://fedoraproject.org/wiki/EPEL)
- [OpenJDK Documentation](https://openjdk.org/)
- [Iron Bank](https://repo1.dso.mil)
- [Red Hat CodeReady Builder](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/package_management_guide/enabling-additional-repositories_managing-repositories)
