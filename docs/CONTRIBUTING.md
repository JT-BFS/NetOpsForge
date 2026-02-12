# Contributing to NetOpsForge

Thank you for contributing to NetOpsForge! This guide will help you submit automation packs, recipes, and improvements.

## 🎯 What Can You Contribute?

- **Automation Packs**: Reusable automation units
- **Recipes**: Multi-step runbooks
- **CMDB Updates**: Device inventory additions
- **Documentation**: Guides and examples
- **Bug Fixes**: Fixes for existing automation
- **Feature Requests**: Ideas for new capabilities

## 🚀 Getting Started

### 1. Set Up Your Environment

```bash
# Clone the repository
git clone https://github.com/your-org/NetOpsForge.git
cd NetOpsForge

# Install dependencies (when available)
pip install -r requirements.txt

# Validate your setup
yamllint --version
```

### 2. Create a Linear Issue

Before starting work:
1. Create a Linear issue describing what you'll build
2. Add appropriate labels (pack, recipe, documentation, etc.)
3. Assign it to yourself

### 3. Create a Feature Branch

```bash
# Branch naming convention: feature/{linear-issue-id}-{description}
git checkout -b feature/NET-123-add-vlan-check-pack
```

## 📦 Contributing a Pack

### Step 1: Create the Pack

```bash
# Copy template
cp packs/cisco-interface-status.yml packs/my-new-pack.yml

# Edit the pack
code packs/my-new-pack.yml
```

### Step 2: Follow Pack Guidelines

- Use `credential_ref` for authentication
- Set correct `operation_type` (read/write)
- Set `requires_ticket: true` for write operations
- Include usage examples
- Add validation checks
- Document error handling

### Step 3: Test Your Pack

```bash
# Validate YAML
yamllint packs/my-new-pack.yml

# Test (when runner available)
netopsforge run pack my-new-pack --device test-device --mode observe
```

### Step 4: Submit PR

```bash
git add packs/my-new-pack.yml
git commit -m "Add pack for VLAN verification (NET-123)"
git push origin feature/NET-123-add-vlan-check-pack
```

Open PR on GitHub with:
- Reference to Linear issue
- Description of what the pack does
- Testing notes
- Screenshots/output examples

## 📖 Contributing a Recipe

### Step 1: Plan the Workflow

Document:
- What operational task does this automate?
- What packs are needed?
- What's the step-by-step flow?
- What reports should be generated?

### Step 2: Create the Recipe

```bash
cp recipes/network-health-check.yml recipes/my-new-recipe.yml
code recipes/my-new-recipe.yml
```

### Step 3: Define Steps

```yaml
steps:
  - step: 1
    name: "First step"
    pack: pack-name
    targets:
      cmdb_query: {...}
    on_failure: continue
```

### Step 4: Test and Submit

Same process as packs - validate, test, submit PR.

## 🗄️ Contributing CMDB Updates

### Adding Devices

```yaml
# In cmdb/devices.yml
- hostname: new-device-01
  management_ip: 10.0.0.10
  device_type: router
  vendor: cisco
  platform: ios-xe
  tags:
    - production
    - allow_execute
  credential_ref: cisco_readonly
```

### Guidelines

- Include all required fields
- Use appropriate tags
- Reference existing credentials
- Document in PR why device is being added

## 📝 Contributing Documentation

Documentation improvements are always welcome:

- Fix typos or unclear instructions
- Add examples
- Improve explanations
- Add diagrams or screenshots

## 🔍 Code Review Process

### What Reviewers Look For

1. **Security**:
   - No hardcoded credentials
   - Proper use of `credential_ref`
   - Appropriate `allow_execute` tags

2. **Quality**:
   - Valid YAML syntax
   - Complete metadata
   - Error handling
   - Documentation

3. **Testing**:
   - Tested in observe mode
   - Output validated
   - Error scenarios tested

4. **Standards**:
   - Naming conventions followed
   - Consistent with existing patterns
   - Linear issue referenced

### Review Timeline

- Initial review: Within 2 business days
- Follow-up reviews: Within 1 business day
- Approval required: At least 1 team member

## ✅ PR Checklist

Before submitting your PR:

- [ ] Linear issue created and referenced
- [ ] Feature branch created with proper naming
- [ ] YAML syntax validated
- [ ] No hardcoded secrets
- [ ] Tested in observe mode (for packs)
- [ ] Documentation updated
- [ ] Examples included
- [ ] PR template filled out completely
- [ ] All CI checks passing

## 🏷️ Labeling

PRs are automatically labeled based on files changed:
- `pack`: Changes to packs/
- `recipe`: Changes to recipes/
- `cmdb`: Changes to cmdb/
- `documentation`: Changes to docs/
- `size/xs|s|m|l|xl`: Based on lines changed

## 🚫 What NOT to Contribute

- Hardcoded credentials or secrets
- Untested automation
- Write operations without proper safeguards
- Changes that bypass governance policies
- Automation without documentation

## 🤝 Getting Help

Need help with your contribution?

- **Ask in chat**: Tag @NetOps team
- **Linear**: Comment on your issue
- **GitHub**: Open a discussion
- **Documentation**: Check existing guides

## 🎉 Recognition

Contributors are recognized in:
- Monthly team meetings
- Linear project updates
- Internal documentation

Thank you for making NetOpsForge better!

