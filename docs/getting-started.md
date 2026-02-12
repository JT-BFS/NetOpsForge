# Getting Started with NetOpsForge

Welcome to NetOpsForge! This guide will help you start using the platform for network automation.

## 🎯 What is NetOpsForge?

NetOpsForge is a governance-first automation platform that combines:
- **AI-powered reasoning** (via Augment)
- **Safe execution** (via governance policies)
- **Reusable automation** (via packs and recipes)
- **Knowledge sharing** (via GitHub and Linear)

## 🏗️ Architecture Overview

```
You → Augment → NetOpsForge → Network Devices
      (Brain)   (Hands)       (Infrastructure)
```

**Augment** understands your intent and plans actions.
**NetOpsForge** safely executes those actions with governance.

## 🚀 Quick Start

### For Network Engineers

#### 1. Browse Available Automation

**Packs** (single operations):
```bash
# List available packs
ls packs/

# View a pack
cat packs/cisco-interface-status.yml
```

**Recipes** (multi-step workflows):
```bash
# List available recipes
ls recipes/

# View a recipe
cat recipes/network-health-check.yml
```

#### 2. Ask Augment to Run Automation

Instead of running commands manually, ask Augment:

**Examples:**
```
"Check interface status on core-rtr-01"
"Run the network health check recipe"
"Show me BGP neighbors on all core routers"
"Verify VLAN configuration on dist-sw-01"
```

Augment will:
1. Find the appropriate pack or recipe
2. Check if it's a READ or WRITE operation
3. For READ: Execute with your awareness
4. For WRITE: Request ServiceNow ticket and explicit YES

#### 3. Review Results

Augment will show you:
- What was executed
- Output from devices
- Any issues found
- Suggested next steps

### For Automation Developers

#### 1. Set Up Your Environment

```bash
# Clone repository
git clone https://github.com/your-org/NetOpsForge.git
cd NetOpsForge

# Install dependencies (when available)
pip install -r requirements.txt

# Validate setup
yamllint --version
```

#### 2. Create Your First Pack

```bash
# Copy template
cp packs/cisco-interface-status.yml packs/my-first-pack.yml

# Edit the pack
code packs/my-first-pack.yml
```

See [Pack Development Guide](pack-development.md) for details.

#### 3. Test Your Pack

```bash
# Validate YAML
yamllint packs/my-first-pack.yml

# Test with Augment
Ask: "Test my-first-pack on test-device-01 in observe mode"
```

#### 4. Submit Your Pack

```bash
# Create Linear issue
# Create feature branch
git checkout -b feature/NET-123-my-first-pack

# Commit and push
git add packs/my-first-pack.yml
git commit -m "Add my first pack (NET-123)"
git push origin feature/NET-123-my-first-pack

# Open PR on GitHub
```

## 🔒 Understanding the Safety Model

### READ Operations (Safe)

**What they are:**
- `show` commands
- Health checks
- Status queries
- Log retrieval

**Requirements:**
- Engineer awareness
- No ServiceNow ticket needed

**Examples:**
- Check interface status
- View BGP neighbors
- Get device inventory

### WRITE Operations (Controlled)

**What they are:**
- Configuration changes
- Device reboots
- Route modifications
- VLAN changes

**Requirements:**
- ✅ Valid ServiceNow ticket (CHG/RITM)
- ✅ Engineer types "YES"
- ✅ Target device tagged `allow_execute`

**Examples:**
- Add VLAN
- Change interface description
- Update ACL

## 📚 Key Concepts

### Packs
Reusable automation units defined in YAML.
- Single operational task
- Self-contained
- Versioned
- Documented

### Recipes
Multi-step workflows combining packs.
- Orchestrate multiple packs
- Generate reports
- Handle dependencies

### CMDB
Device inventory and credentials.
- Device metadata
- Credential references
- Device groups
- Sites/locations

### Credential References
Pointers to credentials in Windows Credential Manager.
- Never hardcoded
- Centrally managed
- Auditable

## 🎓 Learning Path

### Week 1: Explore
- Browse existing packs and recipes
- Ask Augment to run READ operations
- Review generated reports
- Understand the safety model

### Week 2: Create
- Create your first pack (READ operation)
- Test with Augment
- Submit PR
- Get peer review

### Week 3: Contribute
- Create a recipe
- Add devices to CMDB
- Improve documentation
- Help teammates

### Week 4: Advanced
- Create WRITE operation pack
- Integrate with Linear
- Schedule automated checks
- Build complex recipes

## 🔗 Integrations

### Linear
- Track automation work
- Auto-create issues on errors
- Link PRs to issues

### GitHub
- Version control for automation
- CI/CD validation
- Peer review process

### ServiceNow (Planned)
- Change management
- Incident tracking
- CMDB sync

### Notion (Planned)
- Documentation
- Runbooks
- Knowledge base

## 💡 Common Use Cases

### Daily Operations
- Health checks
- Interface monitoring
- BGP neighbor verification
- Device inventory

### Troubleshooting
- Diagnostic data collection
- Log retrieval
- Configuration comparison
- Path tracing

### Change Management
- Pre-change validation
- Configuration deployment
- Post-change verification
- Rollback procedures

### Compliance
- Configuration audits
- Security checks
- Standards validation
- Reporting

## 🆘 Getting Help

### Documentation
- [Pack Development Guide](pack-development.md)
- [Recipe Creation Guide](recipe-creation.md)
- [CMDB Setup](cmdb-setup.md)
- [Contributing Guidelines](CONTRIBUTING.md)

### Ask Augment
```
"How do I create a pack?"
"Show me examples of recipes"
"What packs are available for Cisco devices?"
```

### Team Support
- Linear: Create issue with `question` label
- GitHub: Open discussion
- Chat: Tag @NetOps team

## 🎉 Next Steps

1. **Explore**: Browse packs and recipes
2. **Try**: Ask Augment to run a health check
3. **Learn**: Read the pack development guide
4. **Create**: Build your first pack
5. **Share**: Submit a PR

Welcome to the NetOpsForge community! 🚀

