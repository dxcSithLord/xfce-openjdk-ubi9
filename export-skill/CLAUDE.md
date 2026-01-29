# Claude Code Configuration for Archimate-UBI9

This file configures Claude Code skills and behaviors for the Archimate-UBI9 repository.

## Skills

### Iron Bank Tree Traversal

**Trigger phrases**: "traverse iron bank tree", "analyze container dependencies", "map container layers", "check iron bank dependencies", "ironbank skill"

**Skill file**: `.claude/skills/ironbank-tree-traversal.md`

**Helper script**: `.claude/skills/ironbank_tree.py`

This skill traverses Iron Bank container dependency trees by:
1. Parsing `hardening_manifest.yaml` files to identify base images
2. Recursively fetching parent container manifests from repo1.dso.mil
3. Detecting version updates and deprecated images
4. Generating Mermaid diagrams of the container hierarchy
5. Creating prioritized update task plans

**Environment Variables**:
- `IRONBANK_REPO_URL` - Base URL for Iron Bank GitLab (default: `https://repo1.dso.mil/dsop`)

### Iron Bank Review

**Trigger phrases**: "iron bank review", "review for iron bank", "check iron bank compliance"

This skill reviews repositories for Iron Bank submission readiness.

## Repository Context

This repository (`Archimate-UBI9`) builds an ArchiMate container based on:

**Base Image**: `ironbank/opensource/xfce/xfce-openjdk21`
**Source**: https://github.com/dxcSithLord/xfce-openjdk-ubi9

### Container Dependency Chain

```
Archimate-UBI9 (this repo)
    └── xfce-openjdk21 (dxcSithLord/xfce-openjdk-ubi9)
        └── openjdk21-ubi9 (Iron Bank)
            └── ubi9 (Iron Bank)
```

## ArchiMate Version Information

### Current Version: 5.7.0

**Download URL**: `https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux-5.7.0.tgz`

**SHA-1 Verification**: [Archi-5.7.0-SUMSSHA1](https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-5.7.0-SUMSSHA1)

### Verification Process

```bash
# Download ArchiMate
curl -LO https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux-5.7.0.tgz

# Download SHA-1 checksums
curl -LO https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-5.7.0-SUMSSHA1

# Verify download
grep "Archi-Linux-5.7.0.tgz" Archi-5.7.0-SUMSSHA1 | sha1sum -c -

# Generate SHA256 for hardening_manifest.yaml
sha256sum Archi-Linux-5.7.0.tgz
```

## Usage Examples

### Traverse Container Dependencies
```
User: traverse iron bank tree for this repository
User: map the container layers
User: check dependencies for base image updates
```

### Review for Iron Bank Compliance
```
User: review this repository for iron bank
User: check iron bank compliance
User: what updates are needed for iron bank submission
```

### Run Python Helper Directly
```bash
# Analyze local manifest
python .claude/skills/ironbank_tree.py hardening_manifest.yaml

# Analyze with JSON output for automation
python .claude/skills/ironbank_tree.py hardening_manifest.yaml --json
```

## hardening_manifest.yaml Template

```yaml
apiVersion: v1
name: "opensource/archi/archimate-ubi9"

tags:
- "5.7.0-xfce4.18-ubi9.7"
- "5.7.0"
- "latest"

args:
  BASE_IMAGE: "ironbank/opensource/xfce/xfce-openjdk21"
  BASE_TAG: "4.18-openjdk21.0.10-ubi9.7"
  ARCHI_VERSION: "5.7.0"
  ARCHI_FILENAME: "Archi-Linux-5.7.0.tgz"

labels:
  org.opencontainers.image.title: "ArchiMate Tool"
  org.opencontainers.image.description: "ArchiMate enterprise architecture modeling tool on UBI9"
  org.opencontainers.image.licenses: "MIT"
  org.opencontainers.image.url: "https://www.archimatetool.com/"
  org.opencontainers.image.vendor: "Phillip Beauvoir"
  org.opencontainers.image.version: "5.7.0"
  mil.dso.ironbank.image.keywords: "archimate,modeling,enterprise-architecture,togaf,java"
  mil.dso.ironbank.image.type: "opensource"
  mil.dso.ironbank.product.name: "archimate"

resources:
- url: "https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux-5.7.0.tgz"
  filename: "Archi-Linux-5.7.0.tgz"
  validation:
    type: sha256
    value: "<CALCULATE_AFTER_SHA1_VERIFICATION>"

maintainers:
- email: "<your-email>"
  name: "<your-name>"
  username: "<your-gitlab-username>"
  cht_member: false
```
