# Iron Bank Repository Review Report

**Repository**: xfce-openjdk-ubi9
**Review Date**: 2026-01-29
**Reviewer**: Automated Iron Bank Compliance Review

---

## Executive Summary

This repository contains two Iron Bank container hardening projects:
1. **XFCE + OpenJDK 21** - Base container with XFCE desktop environment
2. **ArchiMate Tool for KASM** - Enterprise architecture modeling tool for KASM Workspaces

The review identified **critical issues** requiring immediate attention before Iron Bank submission, along with several **version updates** available for key components.

---

## Critical Issues (Must Fix)

### 1. Placeholder SHA256 Checksums

**Severity**: CRITICAL - Pipeline will fail

Both hardening manifests contain placeholder values instead of actual SHA256 checksums:

**xfce-hardening_manifest.yaml:46**
```yaml
validation:
  type: sha256
  value: "PLACEHOLDER_EPEL_HASH_NEEDS_CALCULATION"
```

**archimate-hardening_manifest.yaml:47**
```yaml
validation:
  type: sha256
  value: "PLACEHOLDER_HASH_NEEDS_CALCULATION"
```

**Required Action**: Calculate actual SHA256 checksums from downloaded resources before submission.

### 2. Placeholder Maintainer Information

**Severity**: HIGH - Submission will be rejected

Both manifests use placeholder maintainer information:
```yaml
maintainers:
- email: "admin@example.com"
  name: "Container Admin"
  username: "container.admin"
```

**Required Action**: Replace with actual Iron Bank container owner information.

---

## Version Updates Available

### OpenJDK 21

| Current | Latest | Status |
|---------|--------|--------|
| 21.0.5 | **21.0.10** | Update Available |

- Latest release: January 20, 2026
- Contains critical security patches (CPU)
- Next release: 21.0.11 scheduled for April 21, 2026

**Source**: [OpenJDK January 2026 Critical Patch Update](https://foojay.io/today/openjdk-january-2026-critical-patch-update-and-patch-set-update-released/)

### ArchiMate Tool (Archi)

| Current | Latest | Status |
|---------|--------|--------|
| 5.4.0 | **5.7.0** | Update Available |

- Latest release: September 23, 2025
- Supports ArchiMate 3.2 specification
- Multiple releases since 5.4.0 with bug fixes and improvements

**Source**: [Archi 5.7 Released](https://www.archimatetool.com/blog/2025/09/23/archi-5-7-released/)

### UBI 9

| Current | Latest | Status |
|---------|--------|--------|
| 9.6 | **9.7** | Update Available |

UBI 9.7 is now available. Red Hat rebuilds UBI images on a 6-weekly cadence. This update should be coordinated with the Iron Bank OpenJDK base image updates.

---

## Iron Bank Compliance Review

### Required Files Checklist

| File | XFCE Container | ArchiMate Container |
|------|----------------|---------------------|
| Dockerfile | Present | Present |
| hardening_manifest.yaml | Present | Present |
| testing_manifest.yaml | Present | Present |
| LICENSE | Present | Present |
| README.md | Present | Present |

### Security Hardening Review

#### XFCE Container (xfce-Dockerfile)

| Requirement | Status | Notes |
|-------------|--------|-------|
| SETUID/SETGID removal | PASS | Line 87: `find / -perm /6000 -type f -exec chmod a-s {} \;` |
| Build tools removed | PASS | Line 62-68: Removes gcc, make, rpm-build, man-db |
| Cache cleanup | PASS | Line 70-71: `dnf clean all && rm -rf /var/cache/dnf` |
| Proper file permissions | PASS | Line 89-92: Secure permissions set |
| Root directory secured | PASS | Line 89: `chmod 700 /root` |

#### ArchiMate Container (archimate-Dockerfile)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Non-root user | PASS | Line 65: `USER 1001` (kasmuser) |
| SETUID/SETGID removal | PASS | Line 43: Removes from /opt/archi |
| Numeric UID | PASS | Uses 1001 (supports random UID) |
| Workspace isolation | PASS | Dedicated ArchiMateWorkspace directory |
| Temp file cleanup | PASS | Line 45: `rm -rf /tmp/* /var/tmp/*` |
| Security context defined | PASS | testing_manifest.yaml includes proper securityContext |

### Dockerfile Best Practices

#### Positive Findings

1. **ARG usage for base images**: Both Dockerfiles properly use ARG for registry, image, and tag
2. **Layer optimization**: Package installs combined in single RUN statements
3. **No secrets in image**: No hardcoded credentials or sensitive data
4. **Proper COPY usage**: Files copied with appropriate permissions
5. **ENTRYPOINT/CMD separation**: Proper use of entrypoint and default command

#### Items to Address

1. **EPEL repository URL**: The EPEL RPM URL should be added to hardening_manifest.yaml resources for offline builds
2. **Subscription manager**: Line 14 attempts subscription-manager which may fail in offline Iron Bank builds

### Testing Manifest Review

#### XFCE testing_manifest.yaml

| Test Category | Tests | Status |
|---------------|-------|--------|
| EPEL Repository | 2 tests | Complete |
| XFCE Desktop | 4 tests | Complete |
| VNC Server | 2 tests | Complete |
| Java Runtime | 2 tests | Complete |
| Security Compliance | 2 tests | Complete |
| Font Installation | 2 tests | Complete |
| Configuration | 2 tests | Complete |
| Kubernetes Config | Complete | Includes probes, resources, env |

#### ArchiMate testing_manifest.yaml

| Test Category | Tests | Status |
|---------------|-------|--------|
| KASM User Config | 4 tests | Complete |
| ArchiMate Installation | 4 tests | Complete |
| XFCE Desktop | 2 tests | Complete |
| Java Runtime | 2 tests | Complete |
| Startup Script | 3 tests | Complete |
| Desktop Config | 3 tests | Complete |
| EPEL Inheritance | 2 tests | Complete |
| Kubernetes Config | Complete | Includes securityContext |

**Assessment**: Testing manifests are comprehensive and well-structured.

### License Compliance

| Component | License | Status |
|-----------|---------|--------|
| XFCE Desktop | GPL-2.0-or-later | Documented |
| OpenJDK | GPL-2.0 with Classpath Exception | Documented |
| Red Hat UBI | Red Hat EULA | Documented |
| ArchiMate Tool | MIT | Documented |
| x11vnc | GPL-2.0+ | Documented |
| Supervisor | BSD-like | Documented |
| Container configs/scripts | Apache 2.0 | Documented |

**Assessment**: License documentation is complete and accurate.

---

## Recommendations

### Immediate Actions (Before Submission)

1. **Calculate SHA256 checksums** for all external resources:
   - EPEL release package
   - ArchiMate Linux archive

2. **Update maintainer information** with actual Iron Bank container owner details

3. **Verify base image paths** match current Iron Bank repository structure:
   - Check: `ironbank/redhat/openjdk/openjdk21-ubi9` vs `ironbank/redhat/openjdk/openjdk21.x/openjdk21-ubi9`

### Version Updates

1. **OpenJDK 21**: Update from 21.0.5 to 21.0.10 when Iron Bank base image is available
   - Monitor: [Iron Bank OpenJDK Repository](https://repo1.dso.mil/dsop/redhat/openjdk/)

2. **ArchiMate Tool**: Update from 5.4.0 to 5.7.0
   - New download URL: `https://github.com/archimatetool/archi/releases/download/v5.7.0/Archi.Linux.gtk.x86_64.tar.gz`
   - Update tags, hardening_manifest, and README files

### Documentation Updates

1. Update README files to reflect new versions
2. Update Kubernetes deployment examples with new image tags
3. Ensure all version references are consistent across files

---

## Files Requiring Updates

### For Version Updates

| File | Changes Required |
|------|------------------|
| xfce-hardening_manifest.yaml | BASE_TAG, tags (ubi9.6→ubi9.7), SHA256 hash |
| xfce-Dockerfile | BASE_TAG |
| xfce-README.md | Version references (ubi9.6→ubi9.7) |
| archimate-hardening_manifest.yaml | BASE_TAG, tags (ubi9.6→ubi9.7), ArchiMate URL, SHA256 hash |
| archimate-Dockerfile | BASE_TAG (ubi9.6→ubi9.7) |
| archimate-README.md | Version references (ubi9.6→ubi9.7) |
| PROJECT_ORGANIZATION.md | UBI version reference |

### Files Affected by UBI 9.7 Update

The following files contain references to UBI 9.6 that need updating to 9.7:

| File | Line | Current Value |
|------|------|---------------|
| xfce-hardening_manifest.yaml | 10 | `4.18-openjdk21.0.5-ubi9.6` |
| xfce-README.md | 14, 102, 164 | Multiple UBI 9.6 references |
| archimate-hardening_manifest.yaml | 10, 18 | Tags and BASE_TAG with ubi9.6 |
| archimate-Dockerfile | 7 | `BASE_TAG=4.18-openjdk21.0.5-ubi9.6` |
| archimate-README.md | 16, 46, 106 | Multiple UBI 9.6 references |
| PROJECT_ORGANIZATION.md | 80 | UBI 9.6 reference |

### For Immediate Fixes

| File | Issue |
|------|-------|
| xfce-hardening_manifest.yaml | Placeholder SHA256 hash |
| archimate-hardening_manifest.yaml | Placeholder SHA256 hash |
| Both hardening manifests | Placeholder maintainer info |

---

## Iron Bank Pipeline Considerations

1. **Offline Build Environment**: Ensure all resources are listed in hardening_manifest.yaml
2. **EPEL Repository Access**: EPEL packages are allowed through Iron Bank's proxied package managers
3. **Base Image Dependencies**: Verify openjdk21-ubi9 base image exists and is approved in Iron Bank
4. **SBOM Generation**: Pipeline will automatically generate SPDX/CycloneDX SBOMs

---

## References

- [Iron Bank Documentation](https://docs-ironbank.dso.mil/)
- [Iron Bank Pipeline](https://docs-ironbank.dso.mil/quickstart/pipeline/)
- [Hardening Manifest Schema](https://repo1.dso.mil/ironbank-tools/ironbank-pipeline/-/blob/master/schema/hardening_manifest.schema.json)
- [DoD Container Hardening Guide](https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/Final_DevSecOps_Enterprise_Container_Hardening_Guide_1.2.pdf)
- [OpenJDK Release Schedule](https://wiki.openjdk.org/display/JDKUpdates/JDK+21u)
- [ArchiMate Tool Downloads](https://www.archimatetool.com/download/)

---

## Summary

| Category | Status |
|----------|--------|
| Required Files | PASS |
| Security Hardening | PASS |
| Testing Coverage | PASS |
| License Compliance | PASS |
| Version Currency | **UPDATES AVAILABLE** (OpenJDK 21.0.10, ArchiMate 5.7.0, UBI 9.7) |
| Resource Checksums | **FAIL - Placeholders** |
| Maintainer Info | **FAIL - Placeholders** |

**Overall Assessment**: Repository structure and security hardening are well-implemented. Critical issues with placeholder values must be resolved before Iron Bank submission. Version updates are recommended (OpenJDK 21.0.5→21.0.10, ArchiMate 5.4.0→5.7.0, UBI 9.6→9.7) to ensure latest security patches.
