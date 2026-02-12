# NetOpsForge Automation Packs

Automation packs are reusable YAML-defined automation units that encapsulate network operations tasks.

## 📦 What is a Pack?

A pack is a self-contained automation definition that includes:
- **Metadata**: Name, description, version, author
- **Target Selection**: Which devices to run against
- **Commands**: What to execute
- **Parsing**: How to interpret output
- **Validation**: Health checks and assertions
- **Error Handling**: What to do when things go wrong
- **Logging**: Audit trail and debugging

## 🏗️ Pack Structure

```yaml
metadata:
  name: pack-name
  description: "What this pack does"
  operation_type: read  # or write
  requires_ticket: false  # true for write operations

execution:
  mode: observe
  timeout_seconds: 30

targets:
  cmdb_query:
    device_type: router
    vendor: cisco

authentication:
  credential_ref: "cisco_readonly"

commands:
  - name: command_name
    command: "show version"
    parser: textfsm

output:
  format: json
  fields:
    - field1
    - field2
```

## 📚 Available Packs

| Pack Name | Description | Type | Vendor | Documentation |
|-----------|-------------|------|--------|---------------|
| `cisco-ios-health-check` | Comprehensive health check (connectivity, version, CPU, memory, interfaces) | READ | Cisco | [📖 Docs](../docs/packs/cisco-ios-health-check.md) |
| `cisco-interface-status` | Check interface status | READ | Cisco | - |

## 🚀 Using a Pack

### With Augment (Recommended)
```
Ask Augment: "Run the cisco-interface-status pack on core-rtr-01"
```

### With NetOpsForge CLI
```bash
netopsforge run pack cisco-interface-status --device core-rtr-01
```

## 🛠️ Creating a New Pack

1. **Copy the template**:
   ```bash
   cp packs/cisco-interface-status.yml packs/my-new-pack.yml
   ```

2. **Edit the pack**:
   - Update metadata
   - Define targets
   - Specify commands
   - Configure output

3. **Test in observe mode**:
   ```bash
   netopsforge run pack my-new-pack --mode observe --device test-device
   ```

4. **Submit PR**:
   - Create feature branch
   - Commit your pack
   - Open PR with Linear issue reference

## 🔒 Security Guidelines

### ✅ DO:
- Use `credential_ref` for all authentication
- Set `operation_type: write` for configuration changes
- Set `requires_ticket: true` for write operations
- Include validation checks
- Log all operations

### ❌ DON'T:
- Hardcode passwords or API keys
- Skip validation for write operations
- Bypass ticket requirements
- Disable logging

## 📖 Pack Development Guide

See [docs/pack-development.md](../docs/pack-development.md) for detailed guide.

## 🏷️ Pack Categories

- **monitoring**: Health checks, status queries
- **configuration**: Device configuration changes
- **troubleshooting**: Diagnostic commands
- **reporting**: Data collection and reporting
- **compliance**: Compliance checks and audits

## 🔗 Integration with Linear

Packs can automatically create Linear issues on errors:

```yaml
linear_integration:
  auto_create_issue_on_error: true
  issue_labels:
    - network-automation
  issue_priority: medium
```

## 📝 Naming Conventions

Pack filenames should follow this pattern:
```
{vendor}-{function}-{specifics}.yml

Examples:
- cisco-interface-status.yml
- arista-vlan-config.yml
- juniper-bgp-check.yml
```

## 🧪 Testing Packs

Always test packs before submitting:

1. **Syntax validation**: `yamllint packs/my-pack.yml`
2. **Observe mode test**: Run against test device
3. **Error handling**: Test with unreachable device
4. **Output validation**: Verify parsed output

## 🤝 Contributing

All pack contributions are welcome! See [CONTRIBUTING.md](../docs/CONTRIBUTING.md).

