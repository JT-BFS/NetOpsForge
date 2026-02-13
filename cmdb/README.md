# NetOpsForge CMDB

Configuration Management Database for network device inventory and credentials.

## 🔒 **IMPORTANT: Keep Your CMDB Private!**

**Your real `devices.yml` file should NEVER be committed to a public repository!**

This directory contains:
- ✅ `devices.example.yml` - Template for your device inventory (safe to commit)
- ✅ `README.md` - This documentation (safe to commit)
- ❌ `devices.yml` - **YOUR REAL INVENTORY** (git-ignored, never committed)

### **First-Time Setup:**

1. **Copy the example template:**
   ```bash
   Copy-Item cmdb\devices.example.yml cmdb\devices.yml
   ```

2. **Edit `devices.yml` with your real devices:**
   - Replace example IPs with your actual management IPs
   - Update hostnames, platforms, and credentials
   - Add/remove devices as needed

3. **Verify it's git-ignored:**
   ```bash
   git status
   # devices.yml should NOT appear in the list
   ```

4. **Never commit `devices.yml`:**
   - The `.gitignore` file prevents this automatically
   - Only `devices.example.yml` should be in the repo

## 📋 Overview

The CMDB contains:
- **Device Inventory**: All network devices available for automation
- **Device Groups**: Logical groupings for bulk operations
- **Sites/Locations**: Physical location information
- **Credential References**: Pointers to credentials in Windows Credential Manager

## 🗄️ Structure

```
cmdb/
├── devices.example.yml  # Template (committed to repo)
├── devices.yml          # YOUR REAL INVENTORY (git-ignored!)
└── README.md            # This file
```

## 🔧 Device Schema

Each device entry includes:

```yaml
- hostname: device-name
  management_ip: 10.0.0.1
  device_type: router|switch|firewall
  device_role: core-router|distribution-switch|access-switch
  vendor: cisco|arista|juniper
  platform: ios|ios-xe|nxos|eos|junos
  model: Model name
  site: Site code
  tags:
    - production
    - allow_execute
  credential_ref: credential_name
```

## 🏷️ Important Tags

### `allow_execute`
- **Required** for devices that can accept WRITE operations
- Devices without this tag can only be used for READ operations
- Acts as a safety mechanism

### `production`
- Marks production devices
- May have additional safety checks

### Custom Tags
Add custom tags for your organization:
- `critical`
- `maintenance-window-sunday`
- `backup-required`

## 🔐 Credential Management

### Storage
Credentials are **NEVER** stored in CMDB files. Only references are stored.

Actual credentials live in **Windows Credential Manager**:
```
Target: NetOpsForge/cisco_readonly
Username: netops_ro
Password: <actual password>
```

### Adding Credentials to Windows Credential Manager

**PowerShell:**
```powershell
# Create a credential
$cred = Get-Credential -UserName "netops_ro"

# Store in Credential Manager
cmdkey /generic:"NetOpsForge/cisco_readonly" /user:$cred.UserName /pass:$cred.GetNetworkCredential().Password
```

**GUI Method:**
1. Open Control Panel → Credential Manager
2. Click "Windows Credentials"
3. Click "Add a generic credential"
4. Internet or network address: `NetOpsForge/cisco_readonly`
5. User name: `netops_ro`
6. Password: `<password>`
7. Click OK

### Credential Types

- `username_password`: Standard SSH/Telnet credentials
- `api_key`: API tokens for REST APIs
- `certificate`: Certificate-based authentication

## 🎯 Device Groups

Device groups allow bulk operations:

```yaml
device_groups:
  production-routers:
    description: "All production core routers"
    query:
      device_type: router
      tags:
        - production
```

**Usage in packs:**
```yaml
targets:
  device_group: production-routers
```

## 🔍 CMDB Queries

Packs and recipes can query the CMDB:

```yaml
targets:
  cmdb_query:
    device_type: router
    vendor: cisco
    platform: 
      - ios
      - ios-xe
    tags:
      - production
      - allow_execute
```

## 📝 Adding New Devices

1. **Edit your local `devices.yml`** (NOT the example file):
   ```yaml
   - hostname: new-device-01
     management_ip: 10.0.0.10
     device_type: router
     vendor: cisco
     platform: ios-xe
     tags:
       - production
     credential_ref: cisco_readonly
   ```

2. **Validate YAML**:
   ```bash
   yamllint cmdb/devices.yml
   ```

3. **Test connectivity**:
   ```bash
   netopsforge list devices
   # Verify your new device appears
   ```

**Note:** Since `devices.yml` is git-ignored, you don't submit PRs for device changes. Each team member maintains their own local copy.

## 🔒 Security Best Practices

### ✅ DO:
- Use `credential_ref` for all authentication
- Store credentials in Windows Credential Manager
- Use least-privilege credentials when possible
- Tag devices appropriately (`allow_execute`)
- Document credential scope

### ❌ DON'T:
- Hardcode passwords in CMDB files
- Commit credentials to Git
- Share credential files
- Use admin credentials for read-only operations

## 🧪 Testing CMDB Changes

Before submitting CMDB changes:

1. **Validate YAML syntax**:
   ```bash
   yamllint cmdb/devices.yml
   ```

2. **Test device connectivity**:
   ```bash
   netopsforge test device new-device-01
   ```

3. **Verify credential reference**:
   ```bash
   netopsforge test credential cisco_readonly
   ```

## 🔄 Syncing with ServiceNow (Future)

Future integration will sync CMDB with ServiceNow:
- Automatic device discovery
- Bi-directional sync
- Change tracking

## 📊 CMDB Statistics

View CMDB statistics:
```bash
netopsforge cmdb stats
```

Example output:
```
Total Devices: 42
  Routers: 12
  Switches: 28
  Firewalls: 2

By Vendor:
  Cisco: 35
  Arista: 5
  Juniper: 2

By Site:
  DC1: 25
  DC2: 17
```

## 🤝 Contributing

CMDB updates follow the same PR process as code changes. See [CONTRIBUTING.md](../docs/CONTRIBUTING.md).

