# Cisco IOS Health Check Pack

Comprehensive health check automation for Cisco IOS and IOS-XE devices.

## 📋 Overview

This pack performs a complete health assessment of Cisco IOS/IOS-XE devices including:
- ✅ Connectivity validation (ICMP ping, SSH port check)
- ✅ Device information (version, model, serial number, uptime)
- ✅ Hardware inventory
- ✅ CPU utilization (5sec, 1min, 5min averages)
- ✅ Memory utilization
- ✅ Interface status and descriptions
- ✅ Recent log messages
- ✅ Automated validation against thresholds
- ✅ Linear issue creation for failures

## 🎯 Use Cases

### Daily Operations
- **Morning health checks** - Verify all devices are healthy before business hours
- **Post-maintenance validation** - Confirm devices are stable after changes
- **Troubleshooting baseline** - Gather comprehensive device state during incidents

### Proactive Monitoring
- **Resource trending** - Track CPU/memory over time
- **Interface monitoring** - Detect err-disabled or down interfaces
- **Capacity planning** - Identify devices approaching resource limits

### Compliance & Audit
- **Version tracking** - Maintain inventory of software versions
- **Hardware inventory** - Track device models and serial numbers
- **Audit trail** - All executions logged with timestamps and users

## 🚀 Quick Start

### With Augment (Recommended)

Simply ask Augment to run the health check:

```
"Run a health check on core-rtr-01"
"Check the health of all production routers"
"Show me the status of core-rtr-02"
```

### With NetOpsForge CLI

```bash
# Single device
netopsforge run pack cisco-ios-health-check --device core-rtr-01

# All production routers
netopsforge run pack cisco-ios-health-check

# Specific site
netopsforge run pack cisco-ios-health-check --site DC1

# Export to CSV
netopsforge run pack cisco-ios-health-check --output-format csv --output-file health.csv
```

## 📊 Output Format

### JSON Output Example

```json
{
  "device_info": {
    "hostname": "core-rtr-01",
    "management_ip": "10.0.1.1",
    "version": "17.6.3",
    "model": "ASR1001-X",
    "serial_number": "FOC1234ABCD",
    "uptime": "52 weeks, 3 days, 14 hours, 23 minutes"
  },
  "resource_utilization": {
    "cpu_5sec": 12,
    "cpu_1min": 15,
    "cpu_5min": 18,
    "memory_total_mb": 8192,
    "memory_used_mb": 4096,
    "memory_used_percent": 50
  },
  "interface_summary": {
    "total_interfaces": 24,
    "interfaces_up": 22,
    "interfaces_down": 2,
    "err_disabled_count": 0
  },
  "validation_results": {
    "passed": 5,
    "warnings": 0,
    "critical": 0,
    "status": "HEALTHY"
  },
  "timestamp": "2026-02-12T13:45:00Z"
}
```

### Markdown Report Example

```markdown
# Health Check Report: core-rtr-01

**Timestamp:** 2026-02-12 13:45:00  
**Status:** ✅ HEALTHY

## Device Information
- **Hostname:** core-rtr-01
- **IP Address:** 10.0.1.1
- **Model:** ASR1001-X
- **Version:** 17.6.3
- **Serial:** FOC1234ABCD
- **Uptime:** 52 weeks, 3 days

## Resource Utilization
- **CPU (5min):** 18% ✅
- **Memory Used:** 50% (4096 MB / 8192 MB) ✅

## Interface Status
- **Total:** 24
- **Up:** 22 ✅
- **Down:** 2 ⚠️
- **Err-Disabled:** 0 ✅

## Validation Results
✅ All checks passed
```

## ⚙️ Configuration

### Default Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU Utilization | 80% | 95% |
| Memory Utilization | 85% | 95% |
| Err-Disabled Interfaces | N/A | > 0 |
| Critical Interfaces Down | N/A | > 0 |

### Custom Thresholds

Override defaults using command-line parameters:

```bash
netopsforge run pack cisco-ios-health-check \
  --set cpu_threshold=90 \
  --set memory_threshold=90
```

## 🔧 Requirements

### Device Requirements
- Cisco IOS or IOS-XE platform
- SSH access enabled
- Read-only credentials sufficient (no enable mode required)

### Credential Requirements
- Credential reference: `cisco_readonly`
- Stored in Windows Credential Manager
- Format: `netopsforge:cisco_readonly`

### Network Requirements
- ICMP ping allowed (for pre-check)
- SSH port 22 accessible
- No firewall blocking between automation host and devices

## 📈 Integration

### Linear Integration

Automatic issue creation for:
- ❌ Connection failures
- ❌ Command execution errors
- ❌ Critical validation failures (CPU > 95%, Memory > 95%, err-disabled interfaces)

Issue template includes:
- Device information
- Resource utilization metrics
- Interface status summary
- Recommended actions

### CMDB Integration

Automatically updates CMDB with:
- Software version
- Uptime
- Serial number
- Last health check timestamp

## 🧪 Testing

### Test Mode

Run in test mode using mock data:

```bash
netopsforge run pack cisco-ios-health-check --test-mode
```

### Test Devices

Use designated test devices:

```bash
netopsforge run pack cisco-ios-health-check --device test-rtr-01
```

## 📝 Logging

All executions are logged to:
```
./logs/packs/cisco-ios-health-check/{hostname}-{timestamp}.log
```

Log includes:
- Commands executed
- Raw output (if debug level)
- Parsing results
- Validation results
- Errors and warnings

## 🔒 Security

- ✅ No credentials in pack definition
- ✅ Uses credential references only
- ✅ All executions audited
- ✅ Read-only operations (no device changes)
- ✅ No ticket required (observation only)

## 🐛 Troubleshooting

### Connection Failures

**Symptom:** "Connection timeout" or "SSH connection failed"

**Solutions:**
1. Verify device is reachable: `ping 10.0.1.1`
2. Check SSH port: `Test-NetConnection -ComputerName 10.0.1.1 -Port 22`
3. Verify credentials in Credential Manager
4. Check firewall rules

### Parsing Failures

**Symptom:** "Failed to parse command output"

**Solutions:**
1. Check device platform matches (ios/ios-xe)
2. Verify TextFSM templates are installed
3. Review raw output in log file
4. Report issue if output format changed

### Validation Failures

**Symptom:** "Critical validation failed"

**This is expected behavior!** The pack detected an issue:
1. Review the Linear issue created
2. Check device resource utilization
3. Investigate err-disabled interfaces
4. Follow recommended actions

## 📚 Related Packs

- `cisco-interface-status` - Detailed interface analysis
- `cisco-bgp-neighbor-check` - BGP-specific health check
- `cisco-resource-check` - Deep dive into CPU/memory

## 🤝 Contributing

To improve this pack:
1. Create a feature branch
2. Edit `packs/cisco-ios-health-check.yml`
3. Test thoroughly
4. Submit PR with Linear issue reference

## 📄 License

MIT License - See repository root for details

