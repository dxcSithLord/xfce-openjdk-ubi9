# ARM64 Tagging Pattern for Iron Bank Containers

## Overview

This document explains the tagging pattern used for ARM64 versions of Iron Bank container Dockerfiles.

## Key Principles

### 1. Tag is the Sole Platform Indicator

- **BASE_REGISTRY**: Identical across all platforms
- **BASE_IMAGE**: Identical across all platforms
- **BASE_TAG**: ONLY this changes to indicate platform/architecture

### 2. Tag Format Preservation

The BASE_TAG from `hardening_manifest.yaml` is preserved exactly as-is, with `-arm64` appended for ARM64 versions.

**Examples:**
```yaml
# hardening_manifest.yaml
BASE_TAG: "1.21"

# Dockerfile (x86_64)
ARG BASE_TAG=1.21

# Dockerfile.arm64 (ARM64)
ARG BASE_TAG=1.21-arm64
```

```yaml
# hardening_manifest.yaml
BASE_TAG: "9.7"

# Dockerfile (x86_64)
ARG BASE_TAG=9.7

# Dockerfile.arm64 (ARM64)
ARG BASE_TAG=9.7-arm64
```

### 3. Why This Pattern?

**Parsing Simplicity**: The tag can be easily parsed to extract the base version:
- Split on `-arm64` to get the original hardening_manifest.yaml BASE_TAG
- Example: `1.21-arm64` → `1.21`

**Format Preservation**: Dots and dashes in version numbers are kept as-is:
- `1.21` → `1.21-arm64` (NOT `1-21-arm64`)
- This maintains consistency with the hardening_manifest.yaml reference

## Platform-Agnostic Resources

### Resources Section Behavior

The `resources` section in `hardening_manifest.yaml` is typically **platform-agnostic**:
- Resources may be shared across x86_64 and ARM64 builds
- Resources do NOT indicate platform type
- Do NOT rely on `resources[1]` for ARM64 detection

### ARM64 Support Verification

To verify ARM64 support for a base image:

1. **Check for Dockerfile.arm64** in the upstream repository
2. **Check registry tags** in registry1.dso.mil for `-arm64` suffixed tags
3. **Do NOT** check `hardening_manifest.yaml` resources section

## Example Transformation

### Original Dockerfile
```dockerfile
ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/redhat/openjdk/openjdk21-runtime-ubi9-slim
ARG BASE_TAG=1.21

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}
```

### Dockerfile.arm64
```dockerfile
ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/redhat/openjdk/openjdk21-runtime-ubi9-slim
ARG BASE_TAG=1.21-arm64

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}
```

**Note**: Only `BASE_TAG` changed. Registry and image path remain identical.

## Automated Generation

The `generate-arm64-dockerfile` skill has been updated to follow this pattern:

```bash
# The skill will:
# 1. Read BASE_TAG from hardening_manifest.yaml
# 2. Append "-arm64" to create ARM64 version
# 3. Preserve all other Dockerfile content unchanged
```

## References

- **Skill**: `~/.claude/skills/generate-arm64-dockerfile/SKILL.md`
- **Repository**: `/home/sithlord/src/xfce-openjdk-ubi9`
- **Example**: `Dockerfile.arm64` (manually verified correct pattern)
