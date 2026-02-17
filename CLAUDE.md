# Claude Code Configuration

This file configures Claude Code skills and behaviors for this repository.

## Development Guidelines

### Workflow Principles

- **Think First**: Always analyze the problem and read relevant codebase files before making changes
- **Verify Before Changes**: Check in before making any major changes to confirm the plan
- **Never Speculate**: If a specific file is referenced, read it before answering. Never make claims about code without investigating first
- **High-Level Communication**: Provide concise, high-level explanations of changes made

### Code Quality Standards

- **Simplicity First**: Make every task and code change as simple as possible
- **Minimal Impact**: Every change should impact as little code as possible
- **Security Focus**: Apply defensive coding practices and security checks from NIST, OWASP to at least FIPS 140-2 standard
- **Coding Standards**: Comply with good coding standards appropriate for the file type
- **Readability**: Prioritize code readability and maintainability

### Documentation Requirements

- **Architecture Documentation**: Maintain documentation describing how the application architecture works inside and out
- **Diagram Format**: All diagrams must be in Mermaid markdown format

### Verification Practices

- **Version Verification**: Verify the current date against any references to "latest" and confirm assumptions about most recent versions from trusted sources
- **Trust Validation**: Ask for clarification if unable to determine trust of source

### Development Process

1. Create a plan first and ask for confirmation before generating code
2. Consider relevant skills available for the task
3. Ensure code meets appropriate security and coding standards
4. Keep changes simple and focused

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
- `IRONBANK_RAW_URL` - Custom URL pattern for fetching raw manifests (use `{path}` placeholder)

### Iron Bank Review

**Trigger phrases**: "iron bank review", "review for iron bank", "check iron bank compliance"

This skill reviews repositories for Iron Bank submission readiness:
1. Validates required files (Dockerfile, hardening_manifest.yaml, etc.)
2. Checks security hardening compliance
3. Reviews testing manifests
4. Identifies version updates available
5. Reports placeholder values that need replacement

## Repository Structure

```
xfce-openjdk-ubi9/
├── .claude/
│   └── skills/
│       ├── ironbank-tree-traversal.md   # Skill documentation
│       └── ironbank_tree.py             # Python helper script
├── Archimate_files.zip                   # Container definition files
├── CLAUDE.md                             # This file
├── DOWNLOAD_GUIDE.md                     # Reconstruction instructions
├── IRONBANK_REVIEW.md                    # Latest review report
└── README.md                             # Repository overview
```

## Container Images in This Repository

1. **XFCE + OpenJDK 21** (`ironbank/opensource/xfce/xfce-openjdk21`)
   - Lightweight GUI desktop with VNC access
   - Based on Iron Bank OpenJDK 21 UBI 9

2. **ArchiMate Tool for KASM** (`ironbank/opensource/archi/archimate-kasm`)
   - Enterprise architecture modeling tool
   - Based on XFCE + OpenJDK 21 container
   - Optimized for KASM Workspaces

## Usage Examples

### Traverse Container Dependencies
```
User: traverse iron bank tree for this repository
User: map the container layers for archimate-kasm
User: check dependencies for ironbank/opensource/xfce/xfce-openjdk21
```

### Review for Iron Bank Compliance
```
User: review this repository for iron bank
User: check iron bank compliance
User: what updates are needed for iron bank submission
```

### Run Python Helper Directly
```bash
# Set custom repo URL if needed
export IRONBANK_REPO_URL="https://your-gitlab.example.com/dsop"

# Analyze local manifest
python .claude/skills/ironbank_tree.py /path/to/hardening_manifest.yaml

# Analyze remote repository
python .claude/skills/ironbank_tree.py opensource/xfce/xfce-openjdk21

# Output JSON for automation
python .claude/skills/ironbank_tree.py opensource/xfce/xfce-openjdk21 --json
```
