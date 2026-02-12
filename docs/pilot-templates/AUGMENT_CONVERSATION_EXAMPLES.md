# NetOpsForge Pilot - Augment Conversation Examples

This document provides real-world conversation examples for using Augment during the pilot.

---

## 🎯 **Example 1: Creating Your First Pack**

### **Scenario**: You want to automate checking interface status

```
You:
"I want to create a pack to check interface status on Cisco switches"

Augment:
I'll help you create an automation pack for checking interface status on Cisco switches.
Let me create a pack with the following structure:

- Operation type: READ (no ticket required)
- Target: Cisco switches
- Command: show interfaces status
- Parser: TextFSM for structured output
- Validation: Check for down interfaces

Creating pack: packs/cisco-interface-status.yml

[Augment creates the pack file]

The pack has been created. Key features:
- Uses credential_ref (no hardcoded passwords)
- Includes validation for interface states
- Outputs JSON format
- Includes usage examples

Would you like me to:
1. Test this pack for syntax errors?
2. Create a PR for this pack?
3. Explain any section in detail?

You:
"Test this pack for syntax errors"

Augment:
Running validation checks...

✅ YAML syntax: Valid
✅ No hardcoded secrets detected
✅ Required metadata fields present
✅ Credential reference format correct
✅ Command structure valid

The pack is ready to use! Next steps:
1. Create a Linear issue for tracking
2. Submit a PR for team review
3. Test against a device (when runner is available)

Would you like me to create a Linear issue and PR?

You:
"Yes, create a Linear issue and PR"

Augment:
Creating Linear issue...
✅ Linear issue created: NET-123 "Add interface status check pack"

Creating PR...
✅ Branch created: feature/NET-123-interface-status
✅ Pack committed
✅ PR created with template filled out
✅ PR linked to Linear issue NET-123

GitHub Actions are now running validation. You can view the PR at:
[PR URL]

Linear issue NET-123 status updated to "In Progress"
```

---

## 🎯 **Example 2: Testing a Pack**

### **Scenario**: You want to test a pack before submitting

```
You:
"Show me the cisco-interface-status pack"

Augment:
Here's the cisco-interface-status pack:

[Shows pack YAML with syntax highlighting]

This pack:
- Checks interface status on Cisco IOS/IOS-XE devices
- Operation type: READ (safe, no ticket needed)
- Uses credential_ref: cisco_readonly
- Parses output with TextFSM
- Validates for down interfaces

You:
"Test this pack on dist-sw-01"

Augment:
Preparing to test cisco-interface-status pack on dist-sw-01...

Checking prerequisites:
✅ Pack operation type: READ (no ticket required)
✅ Device dist-sw-01 found in CMDB
✅ Device platform: nxos (compatible with pack)
✅ Credential reference: cisco_readonly (configured)

[Future: When runner is available]
Executing pack in observe mode...
Connected to dist-sw-01 (10.0.2.1)
Running: show interface status
Parsing output with TextFSM...

Results:
- Total interfaces: 48
- Interfaces up: 45
- Interfaces down: 3
  - Eth1/10: down (admin down)
  - Eth1/15: down (no cable)
  - Eth1/20: down (admin down)

⚠️ Validation warning: 3 interfaces are down

Would you like me to:
1. Show detailed output for down interfaces?
2. Create a Linear issue for investigation?
3. Generate a report?
```

---

## 🎯 **Example 3: Running a Recipe**

### **Scenario**: You want to run a pre-change validation

```
You:
"Run the pre-change validation recipe on core-rtr-01"

Augment:
I'll run the pre-change validation recipe on core-rtr-01.

Recipe: network-health-check
Steps: 4
Estimated duration: 5 minutes
Operation type: READ (no ticket required)

Steps to execute:
1. Backup configuration
2. Check interface status
3. Check BGP neighbors
4. Check routing table

Proceeding with execution...

[Step 1/4] Backup configuration
✅ Configuration backed up to backups/core-rtr-01-{timestamp}.cfg

[Step 2/4] Check interface status
✅ All critical interfaces up
   - 24 interfaces total
   - 22 up, 2 admin down (expected)

[Step 3/4] Check BGP neighbors
✅ All BGP neighbors established
   - 4 neighbors total
   - All in "Established" state

[Step 4/4] Check routing table
✅ Routing table healthy
   - 1,245 routes
   - No missing critical routes

📊 Pre-Change Validation Summary:
✅ All checks passed
✅ System is healthy for change
✅ Configuration backup created

Report saved to: reports/pre-change-core-rtr-01-{timestamp}.md

You are clear to proceed with your change.
```

---

## 🎯 **Example 4: WRITE Operation (Configuration Change)**

### **Scenario**: You need to add a VLAN

```
You:
"Add VLAN 200 named 'Guest-WiFi' to dist-sw-01"

Augment:
⚠️ This is a WRITE operation that will modify device configuration.

NetOpsForge governance requires:
1. ❌ Valid ServiceNow change ticket (CHG/RITM)
2. ❌ Explicit YES confirmation
3. ❓ Target device must have 'allow_execute' tag

Please provide a ServiceNow ticket number to proceed.

You:
"CHG0012345"

Augment:
Validating ticket CHG0012345...

[Future: ServiceNow API integration]
✅ Ticket CHG0012345 found
✅ Status: Approved
✅ Change window: Active
✅ Assigned to: jesse.tucker

Checking target device dist-sw-01...
✅ Device found in CMDB
✅ Platform: nxos (compatible)
✅ Tags include: allow_execute

All governance requirements met except explicit confirmation.

⚠️ I will execute the following commands on dist-sw-01:
```
vlan 200
  name Guest-WiFi
```

Type YES to proceed with this change.

You:
"YES"

Augment:
Executing configuration change on dist-sw-01...

[Future: Runner execution]
✅ Connected to dist-sw-01
✅ Entered configuration mode
✅ Created VLAN 200
✅ Set name to 'Guest-WiFi'
✅ Saved configuration

Change completed successfully!

📋 Change Summary:
- Device: dist-sw-01
- Change: Added VLAN 200 (Guest-WiFi)
- Ticket: CHG0012345
- Executed by: jesse.tucker
- Timestamp: 2026-02-12 14:30:00

✅ Linear issue created: NET-456 "VLAN 200 added to dist-sw-01"
✅ ServiceNow ticket CHG0012345 updated with results

Audit log saved to: logs/changes/dist-sw-01-{timestamp}.log
```

---

## 🎯 **Example 5: Troubleshooting with Augment**

### **Scenario**: BGP neighbor is down

```
You:
"BGP neighbor 10.1.1.2 is down on core-rtr-01, help me troubleshoot"

Augment:
I'll help you troubleshoot the BGP neighbor issue on core-rtr-01.

Let me run diagnostic checks...

[Step 1] Checking BGP neighbor status
Running pack: cisco-bgp-neighbor-check

Result:
- Neighbor 10.1.1.2: Down
- Last state: Established
- Down since: 5 minutes ago
- Reason: Connection reset

[Step 2] Checking interface to neighbor
Running pack: cisco-interface-status

Result:
- Interface Gi0/0/1 (to 10.1.1.2): Up
- Status: Connected
- No errors detected

[Step 3] Checking routing to neighbor
Running pack: cisco-route-check

Result:
- Route to 10.1.1.0/24: Present
- Next hop: Directly connected
- No routing issues

[Step 4] Checking recent logs
Running pack: cisco-log-check

Result:
⚠️ Found relevant log entries:
- 14:25:03: %BGP-5-ADJCHANGE: neighbor 10.1.1.2 Down - BGP Notification sent
- 14:25:03: %BGP-3-NOTIFICATION: sent to neighbor 10.1.1.2 4/0 (hold time expired)

🔍 Root Cause Analysis:
The BGP neighbor went down due to hold timer expiration. This typically indicates:
1. Network connectivity issues (but interface is up)
2. High CPU on neighbor device
3. BGP process issue on neighbor

Recommended Actions:
1. Check CPU utilization on neighbor device (10.1.1.2)
2. Verify BGP process is running on neighbor
3. Check for network latency/packet loss

Would you like me to:
1. Create a Linear issue to track this incident?
2. Generate a detailed troubleshooting report?
3. Check the neighbor device (if accessible)?

You:
"Create a Linear issue and generate a report"

Augment:
✅ Linear issue created: NET-457 "BGP neighbor down on core-rtr-01"
   - Priority: High
   - Labels: incident, bgp, troubleshooting
   - Assigned to: On-call engineer

✅ Report generated: reports/bgp-troubleshoot-core-rtr-01-{timestamp}.md

Report includes:
- Timeline of events
- All diagnostic command outputs
- Root cause analysis
- Recommended remediation steps
- Related log entries

The report has been attached to Linear issue NET-457.
```

---

## 🎯 **Example 6: Getting Help from Augment**

### **Scenario**: You're stuck and need guidance

```
You:
"How do I create a pack that uses TextFSM parsing?"

Augment:
I'll explain how to create a pack with TextFSM parsing.

TextFSM is used to parse unstructured command output into structured data.

Here's an example pack structure:

```yaml
commands:
  - name: show_interfaces
    command: "show interfaces status"
    parser: textfsm
    parser_template: "cisco_ios_show_interfaces_status.textfsm"
```

Key points:
1. Set `parser: textfsm`
2. Specify `parser_template` with the template name
3. TextFSM templates are stored in the runner's template directory

Common TextFSM templates available:
- cisco_ios_show_interfaces_status.textfsm
- cisco_ios_show_ip_bgp.textfsm
- cisco_ios_show_ip_route.textfsm

Would you like me to:
1. Create a complete example pack with TextFSM?
2. Show you how to create a custom TextFSM template?
3. Explain the output format?

You:
"Create a complete example pack with TextFSM"

Augment:
I'll create an example pack that uses TextFSM parsing.

[Creates pack file]

I've created packs/example-textfsm-pack.yml with:

1. Metadata section defining the pack
2. Command using TextFSM parser
3. Output configuration for JSON format
4. Validation checks on parsed data
5. Usage examples

The pack will:
- Run "show interfaces status"
- Parse output with TextFSM
- Return structured JSON data
- Validate interface states

You can now:
1. Test this pack: "Test example-textfsm-pack"
2. Modify for your needs
3. Create a PR when ready

Need anything else explained?
```

---

## 💡 **Pro Tips for Using Augment**

### **Be Specific**
❌ "Create a pack"
✅ "Create a pack to check BGP neighbors on Cisco routers"

### **Ask for Explanations**
✅ "Explain the validation section of this pack"
✅ "Why does this pack require a ticket?"
✅ "What's the difference between observe and execute mode?"

### **Request Step-by-Step**
✅ "Walk me through creating a recipe"
✅ "Show me how to test a pack before submitting"
✅ "Guide me through the PR process"

### **Leverage Context**
✅ "Based on the cisco-interface-status pack, create a similar one for BGP"
✅ "Use the same structure as the health-check recipe"

### **Ask for Best Practices**
✅ "What's the best way to handle errors in a pack?"
✅ "How should I structure a multi-device recipe?"
✅ "What validation checks should I include?"

---

## 🆘 **Common Questions to Ask Augment**

### **Getting Started**
- "How do I use NetOpsForge?"
- "Show me available packs"
- "What's the difference between a pack and a recipe?"

### **Pack Development**
- "Create a pack for [specific task]"
- "Validate this pack for errors"
- "Add error handling to this pack"

### **Testing**
- "Test this pack on [device]"
- "Show me what this pack will do"
- "Run this in dry-run mode"

### **Troubleshooting**
- "Why is this pack failing?"
- "Help me debug this YAML syntax error"
- "This pack isn't working as expected"

### **Governance**
- "Why does this require a ticket?"
- "Can I run this without a ServiceNow ticket?"
- "What are the requirements for WRITE operations?"

---

**Remember**: Augment is here to help! Don't hesitate to ask questions or request clarification.

