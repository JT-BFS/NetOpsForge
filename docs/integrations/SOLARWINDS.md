# SolarWinds Orion CMDB Integration

This guide explains how to integrate SolarWinds Orion as your CMDB source for NetOpsForge.

## Overview

The SolarWinds integration allows NetOpsForge to dynamically query your SolarWinds Orion server for network device inventory instead of maintaining a static YAML file. This provides:

- **Real-time inventory** - Always up-to-date device information
- **Centralized management** - Single source of truth for network devices
- **Automatic discovery** - New devices automatically available
- **Rich metadata** - Leverage SolarWinds custom properties
- **Dynamic schema detection** - Automatically discovers available custom properties

## Test Results

✅ **Successfully tested with production SolarWinds Orion instance**
- Retrieved 1,603 network devices
- Automatic custom property discovery working
- Windows Credential Manager integration verified
- All 3 test suites passed (Client Connection, Device Mapping, CMDB Integration)

## Quick Start

### 1. Install Dependencies

```bash
pip install orionsdk
```

### 2. Add Credentials to Windows Credential Manager (Recommended)

Run the setup script:

```powershell
.\scripts\setup-solarwinds-creds.ps1
```

This will:
- Prompt for your SolarWinds hostname, username, and password
- Securely store credentials in Windows Credential Manager
- Update your `.env` file with SolarWinds configuration

### 3. Test the Connection

```bash
python test_solarwinds.py
```

### 4. Use SolarWinds as CMDB Source

```bash
# List devices from SolarWinds
netopsforge list devices

# Run automation packs
netopsforge run cisco-ios-health-check <device-from-solarwinds>
```

## Configuration

### Option 1: Windows Credential Manager (Recommended)

**Why?** Most secure - credentials never stored in files or environment variables.

```powershell
# Add credentials
.\scripts\setup-solarwinds-creds.ps1

# Or manually using cmdkey
cmdkey /generic:NetOpsForge:solarwinds_api /user:"bfs\adm.jesse.tucker" /pass:"your_password"
```

**Configuration in `.env`:**

```bash
CMDB_SOURCE=solarwinds
SOLARWINDS_HOSTNAME=orion
SOLARWINDS_VERIFY_SSL=false  # Set to false for self-signed certificates
SOLARWINDS_CACHE_TTL=300
```

### Option 2: Environment Variables

**Configuration in `.env`:**

```bash
CMDB_SOURCE=solarwinds
SOLARWINDS_HOSTNAME=orion
SOLARWINDS_USERNAME=bfs\adm.jesse.tucker
SOLARWINDS_PASSWORD=your_password
SOLARWINDS_VERIFY_SSL=false
SOLARWINDS_CACHE_TTL=300
```

### Option 3: Programmatic

```python
from netopsforge.core.cmdb import CMDB

cmdb = CMDB(
    source='solarwinds',
    hostname='orion',
    username='bfs\\adm.jesse.tucker',
    password='your_password',
    verify_ssl=False,
    cache_ttl=300
)

devices = cmdb.list_devices()
```

## Configuration Options

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `CMDB_SOURCE` | CMDB source type | `yaml` | Yes |
| `SOLARWINDS_HOSTNAME` | SolarWinds server hostname | - | Yes |
| `SOLARWINDS_USERNAME` | API username | - | Yes* |
| `SOLARWINDS_PASSWORD` | API password | - | Yes* |
| `SOLARWINDS_VERIFY_SSL` | Verify SSL certificates | `true` | No |
| `SOLARWINDS_CACHE_TTL` | Cache TTL in seconds | `300` | No |

*Not required if using Windows Credential Manager

## SolarWinds Custom Properties Mapping

The integration queries these SolarWinds properties and maps them to NetOpsForge fields:

| SolarWinds Property | NetOpsForge Field | Notes |
|---------------------|-------------------|-------|
| `n.Caption` | `hostname` | Device hostname |
| `n.IPAddress` | `management_ip` | Management IP address |
| `n.Vendor` | `vendor` | Normalized (cisco, arista, juniper) |
| `n.CustomProperties.Platform` | `platform` | Normalized (ios, ios-xe, nxos, asa, junos, eos) |
| `n.CustomProperties.DeviceRole` | `device_role` | Router, switch, firewall, etc. |
| `n.CustomProperties.Site` | `site` | Site location |
| `n.CustomProperties.Model` | `model` | Device model |
| `n.CustomProperties.SerialNumber` | `serial_number` | Serial number |
| `n.CustomProperties.Rack` | `rack` | Rack location |
| `n.CustomProperties.CredentialRef` | `credential_ref` | Credential reference for device access |
| `n.CustomProperties.Tags` | `tags` | Comma-separated tags |
| `n.IOSVersion` | `metadata.ios_version` | OS version |
| `n.MachineType` | `model` | Fallback if Model not set |

### Required Custom Properties

For best results, configure these custom properties in SolarWinds:

- **Platform** - Device platform (IOS, IOS-XE, NX-OS, ASA, JunOS, EOS)
- **DeviceRole** - Device role (core-router, access-switch, firewall, etc.)
- **CredentialRef** - Reference to Windows Credential Manager entry for device access
- **Site** - Site/location name
- **Tags** - Comma-separated tags (e.g., "production,core,allow_execute")

## SSL Certificate Handling

### Self-Signed Certificates (Common)

If your SolarWinds server uses a self-signed certificate:

```bash
SOLARWINDS_VERIFY_SSL=false
```

### Trusted Certificates

If you have a properly signed certificate:

```bash
SOLARWINDS_VERIFY_SSL=true
```

## Caching

The integration includes a caching layer to reduce API calls:

- **Default TTL**: 5 minutes (300 seconds)
- **Configurable**: Set `SOLARWINDS_CACHE_TTL` in seconds
- **Automatic invalidation**: Cache expires after TTL
- **Manual clearing**: Call `client.clear_cache()` if needed

## Troubleshooting

### SSL Certificate Errors

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**: Set `SOLARWINDS_VERIFY_SSL=false` in `.env`

### Authentication Errors

**Error**: `401 Unauthorized`

**Solutions**:
1. Verify username format (may need domain: `domain\username`)
2. Check password is correct
3. Verify user has API access permissions in SolarWinds

### Connection Timeout

**Error**: `Connection timeout`

**Solutions**:
1. Verify hostname resolves: `ping orion`
2. Check firewall allows port 17778
3. Verify SolarWinds API is enabled

### No Devices Returned

**Possible causes**:
1. SWQL query filters out your devices (check vendor filter)
2. Custom properties not set in SolarWinds
3. User doesn't have permission to view nodes

## Advanced Usage

### Custom SWQL Queries

You can extend the integration to use custom SWQL queries:

```python
from netopsforge.integrations.solarwinds import SolarWindsClient, SolarWindsConfig

config = SolarWindsConfig(hostname='orion', username='user', password='pass', verify_ssl=False)
client = SolarWindsClient(config)

# Custom query
query = """
SELECT n.NodeID, n.Caption, n.IPAddress
FROM Orion.Nodes n
WHERE n.CustomProperties.Site = 'DataCenter1'
"""

results = client._swql_query(query)
```

### Filtering Devices

```python
from netopsforge.core.cmdb import CMDB

cmdb = CMDB(source='solarwinds')

# Query by vendor
cisco_devices = cmdb.query_devices(vendor='cisco')

# Query by platform
ios_xe_devices = cmdb.query_devices(platform='ios-xe')

# Query by site
dc1_devices = cmdb.query_devices(site='DataCenter1')

# Query by tags
prod_devices = cmdb.query_devices(tags=['production'])
```

## Security Best Practices

1. **Use Windows Credential Manager** for storing credentials
2. **Use read-only accounts** for SolarWinds API access
3. **Enable SSL verification** if you have proper certificates
4. **Rotate credentials regularly**
5. **Audit API access** in SolarWinds logs
6. **Use least-privilege** - only grant necessary permissions

## Next Steps

- [Test against real devices](../TESTING.md)
- [Build automation packs](../PACK-DEVELOPMENT.md)
- [Configure device credentials](../CREDENTIALS.md)

