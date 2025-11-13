# Iron Bank Container Files - Download Guide

## Download Instructions

All files are now available as individual downloads. The "Download all" button should now work, or you can download files individually using the links below.

## File Organization

### Directory Structure (for reference)
```
xfce/                          # XFCE Container Repository
├── Dockerfile                 → xfce-Dockerfile
├── hardening_manifest.yaml    → xfce-hardening_manifest.yaml
├── testing_manifest.yaml      → xfce-testing_manifest.yaml
├── README.md                  → xfce-README.md
├── LICENSE                    → xfce-LICENSE
├── config/
│   ├── xfce4-session.rc      → xfce-config-xfce4-session.rc
│   └── vnc-startup.sh        → xfce-config-vnc-startup.sh
└── scripts/
    ├── docker-entrypoint.sh  → xfce-scripts-docker-entrypoint.sh
    └── supervisord.conf       → xfce-scripts-supervisord.conf

archimate/                     # ArchiMate Container Repository  
├── Dockerfile                 → archimate-Dockerfile
├── hardening_manifest.yaml    → archimate-hardening_manifest.yaml
├── testing_manifest.yaml      → archimate-testing_manifest.yaml
├── README.md                  → archimate-README.md
├── LICENSE                    → archimate-LICENSE
├── config/
│   ├── archi.desktop         → archimate-config-archi.desktop
│   └── archi-launcher.desktop → archimate-config-archi-launcher.desktop
├── scripts/
│   └── start-archi.sh        → archimate-scripts-start-archi.sh
└── kasm/
    ├── kasm-xfce4-session.rc → archimate-kasm-xfce4-session.rc
    ├── kasm-panel.xml        → archimate-kasm-panel.xml
    └── kasm-supervisord.conf → archimate-kasm-supervisord.conf
```

## Individual File Downloads

### 📁 XFCE Container Files

#### Core Files
- **[xfce-Dockerfile](computer:///mnt/user-data/outputs/xfce-Dockerfile)** - Main container definition
- **[xfce-hardening_manifest.yaml](computer:///mnt/user-data/outputs/xfce-hardening_manifest.yaml)** - Iron Bank manifest with EPEL
- **[xfce-testing_manifest.yaml](computer:///mnt/user-data/outputs/xfce-testing_manifest.yaml)** - Testing configuration
- **[xfce-README.md](computer:///mnt/user-data/outputs/xfce-README.md)** - Complete documentation
- **[xfce-LICENSE](computer:///mnt/user-data/outputs/xfce-LICENSE)** - License information

#### Configuration Files
- **[xfce-config-xfce4-session.rc](computer:///mnt/user-data/outputs/xfce-config-xfce4-session.rc)** - XFCE session config
- **[xfce-config-vnc-startup.sh](computer:///mnt/user-data/outputs/xfce-config-vnc-startup.sh)** - VNC startup script

#### Scripts
- **[xfce-scripts-docker-entrypoint.sh](computer:///mnt/user-data/outputs/xfce-scripts-docker-entrypoint.sh)** - Container entrypoint
- **[xfce-scripts-supervisord.conf](computer:///mnt/user-data/outputs/xfce-scripts-supervisord.conf)** - Process management

### 📁 ArchiMate Container Files

#### Core Files
- **[archimate-Dockerfile](computer:///mnt/user-data/outputs/archimate-Dockerfile)** - ArchiMate with KASM user
- **[archimate-hardening_manifest.yaml](computer:///mnt/user-data/outputs/archimate-hardening_manifest.yaml)** - Iron Bank manifest
- **[archimate-testing_manifest.yaml](computer:///mnt/user-data/outputs/archimate-testing_manifest.yaml)** - KASM testing
- **[archimate-README.md](computer:///mnt/user-data/outputs/archimate-README.md)** - KASM documentation
- **[archimate-LICENSE](computer:///mnt/user-data/outputs/archimate-LICENSE)** - License information

#### Application Configuration
- **[archimate-config-archi.desktop](computer:///mnt/user-data/outputs/archimate-config-archi.desktop)** - Desktop shortcut
- **[archimate-config-archi-launcher.desktop](computer:///mnt/user-data/outputs/archimate-config-archi-launcher.desktop)** - Menu launcher

#### Scripts
- **[archimate-scripts-start-archi.sh](computer:///mnt/user-data/outputs/archimate-scripts-start-archi.sh)** - ArchiMate startup

#### KASM Configuration
- **[archimate-kasm-xfce4-session.rc](computer:///mnt/user-data/outputs/archimate-kasm-xfce4-session.rc)** - KASM session config
- **[archimate-kasm-panel.xml](computer:///mnt/user-data/outputs/archimate-kasm-panel.xml)** - Panel configuration
- **[archimate-kasm-supervisord.conf](computer:///mnt/user-data/outputs/archimate-kasm-supervisord.conf)** - Auto-launch config

### 📋 Documentation
- **[PROJECT_ORGANIZATION.md](computer:///mnt/user-data/outputs/PROJECT_ORGANIZATION.md)** - Complete project overview

## Reconstruction Instructions

After downloading, recreate the proper directory structure:

### For XFCE Container:
```bash
mkdir -p xfce/{config,scripts}
mv xfce-Dockerfile xfce/Dockerfile
mv xfce-hardening_manifest.yaml xfce/hardening_manifest.yaml
mv xfce-testing_manifest.yaml xfce/testing_manifest.yaml
mv xfce-README.md xfce/README.md
mv xfce-LICENSE xfce/LICENSE
mv xfce-config-xfce4-session.rc xfce/config/xfce4-session.rc
mv xfce-config-vnc-startup.sh xfce/config/vnc-startup.sh
mv xfce-scripts-docker-entrypoint.sh xfce/scripts/docker-entrypoint.sh
mv xfce-scripts-supervisord.conf xfce/scripts/supervisord.conf
chmod +x xfce/config/vnc-startup.sh xfce/scripts/docker-entrypoint.sh
```

### For ArchiMate Container:
```bash
mkdir -p archimate/{config,scripts,kasm}
mv archimate-Dockerfile archimate/Dockerfile
mv archimate-hardening_manifest.yaml archimate/hardening_manifest.yaml
mv archimate-testing_manifest.yaml archimate/testing_manifest.yaml
mv archimate-README.md archimate/README.md
mv archimate-LICENSE archimate/LICENSE
mv archimate-config-archi.desktop archimate/config/archi.desktop
mv archimate-config-archi-launcher.desktop archimate/config/archi-launcher.desktop
mv archimate-scripts-start-archi.sh archimate/scripts/start-archi.sh
mv archimate-kasm-xfce4-session.rc archimate/kasm/kasm-xfce4-session.rc
mv archimate-kasm-panel.xml archimate/kasm/kasm-panel.xml
mv archimate-kasm-supervisord.conf archimate/kasm/kasm-supervisord.conf
chmod +x archimate/scripts/start-archi.sh
```

## Container Submission Order

1. **XFCE Container** - Submit first (dependency)
2. **ArchiMate Container** - Submit after XFCE approval

## Ready for Iron Bank Submission

Both containers are fully compliant with Iron Bank requirements and ready for submission with proper EPEL repository integration and KASM user configuration.
