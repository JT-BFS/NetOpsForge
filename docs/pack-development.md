# Pack Development Guide

Complete guide to creating automation packs for NetOpsForge.

## 🎯 What You'll Learn

- Pack structure and schema
- Best practices for pack development
- Testing and validation
- Submitting packs via PR

## 📦 Pack Anatomy

A pack is a YAML file with these sections:

### 1. Metadata
```yaml
metadata:
  name: pack-name
  display_name: "Human Readable Name"
  description: "What this pack does"
  version: "1.0.0"
  category: monitoring|configuration|troubleshooting
  vendor: cisco|arista|juniper
  platforms:
    - ios
    - ios-xe
  operation_type: read|write
  requires_ticket: false|true
  tags:
    - tag1
    - tag2
```

### 2. Execution Parameters
```yaml
execution:
  mode: observe|execute
  timeout_seconds: 30
  retry_count: 2
  retry_delay_seconds: 5
```

### 3. Target Selection
```yaml
targets:
  cmdb_query:
    device_type: router
    vendor: cisco
    tags:
      - production
```

### 4. Authentication
```yaml
authentication:
  method: credential_ref
  credential_ref: "cisco_readonly"
```

**NEVER hardcode credentials!**

### 5. Commands
```yaml
commands:
  - name: command_name
    description: "What this command does"
    command: "show version"
    parser: textfsm|regex|raw
    parser_template: "template_name.textfsm"
```

### 6. Output Handling
```yaml
output:
  format: json|yaml|text|table
  save_to_file: true
  file_path: "./output/{pack_name}-{timestamp}.json"
  fields:
    - field1
    - field2
```

### 7. Validation
```yaml
validation:
  checks:
    - name: check_name
      description: "What to check"
      condition: "field == 'expected'"
      severity: warning|critical
```

### 8. Error Handling
```yaml
error_handling:
  on_connection_failure:
    action: retry|fail|continue
    max_retries: 3
  on_command_failure:
    action: log_and_continue
```

## 🛠️ Development Workflow

### Step 1: Plan Your Pack

Answer these questions:
- What operational task does this automate?
- Is it READ or WRITE?
- What devices does it target?
- What commands will it run?
- How should output be parsed?

### Step 2: Create Pack File

```bash
# Copy template
cp packs/cisco-interface-status.yml packs/my-new-pack.yml

# Edit the pack
code packs/my-new-pack.yml
```

### Step 3: Define Metadata

```yaml
metadata:
  name: my-new-pack
  display_name: "My New Pack"
  description: "Does something useful"
  version: "1.0.0"
  operation_type: read  # Start with read!
  requires_ticket: false
```

### Step 4: Configure Commands

```yaml
commands:
  - name: show_something
    command: "show something"
    parser: textfsm
```

### Step 5: Test Locally

```bash
# Validate YAML syntax
yamllint packs/my-new-pack.yml

# Test against a device (when runner is available)
netopsforge run pack my-new-pack --device test-device-01 --mode observe
```

### Step 6: Add Validation

```yaml
validation:
  checks:
    - name: verify_output
      description: "Ensure output is valid"
      condition: "status == 'up'"
      severity: warning
```

### Step 7: Document Usage

```yaml
examples:
  - name: "Basic usage"
    description: "Run on a single device"
    command: |
      netopsforge run pack my-new-pack --device device-01
```

### Step 8: Submit PR

```bash
# Create branch
git checkout -b feature/add-my-new-pack

# Commit
git add packs/my-new-pack.yml
git commit -m "Add my-new-pack for XYZ functionality"

# Push
git push origin feature/add-my-new-pack

# Open PR on GitHub
```

## ✅ Pack Checklist

Before submitting your pack:

- [ ] YAML syntax is valid (`yamllint`)
- [ ] No hardcoded credentials
- [ ] Uses `credential_ref`
- [ ] Metadata is complete
- [ ] Commands are documented
- [ ] Output format is defined
- [ ] Error handling is configured
- [ ] Examples are included
- [ ] Tested in observe mode
- [ ] Linear issue referenced in PR

## 🎨 Best Practices

### Naming Conventions
- **Pack files**: `{vendor}-{function}.yml`
- **Pack names**: `{vendor}-{function}`
- **Command names**: `{action}_{object}`

Examples:
- `cisco-interface-status.yml`
- `arista-vlan-config.yml`
- `juniper-bgp-check.yml`

### Operation Types

**READ Operations:**
- `operation_type: read`
- `requires_ticket: false`
- Use read-only credentials
- Safe to run anytime

**WRITE Operations:**
- `operation_type: write`
- `requires_ticket: true`
- Require ServiceNow CHG ticket
- Include rollback commands
- Test extensively first

### Error Handling

Always handle errors gracefully:
```yaml
error_handling:
  on_connection_failure:
    action: retry
    max_retries: 3
  on_command_failure:
    action: log_and_continue
  on_parsing_failure:
    action: return_raw
```

## 🧪 Testing

### Local Testing
```bash
# Syntax check
yamllint packs/my-pack.yml

# Dry run
netopsforge run pack my-pack --dry-run

# Test on single device
netopsforge run pack my-pack --device test-device --mode observe
```

### CI/CD Testing
GitHub Actions automatically:
- Validates YAML syntax
- Scans for hardcoded secrets
- Checks pack structure
- Runs security scans

## 🔗 Linear Integration

Packs can integrate with Linear:

```yaml
linear_integration:
  auto_create_issue_on_error: true
  issue_labels:
    - network-automation
    - pack-name
  issue_priority: medium
```

## 📖 Additional Resources

- [Recipe Development Guide](recipe-creation.md)
- [CMDB Setup](cmdb-setup.md)
- [Contributing Guidelines](CONTRIBUTING.md)

