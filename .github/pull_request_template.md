# NetOpsForge Automation PR

## 📋 Description
<!-- What automation does this pack/recipe provide? -->

## 🏷️ Type of Change
- [ ] New automation pack
- [ ] New recipe/runbook
- [ ] Bug fix for existing automation
- [ ] Documentation update
- [ ] CMDB update
- [ ] Policy/governance change

## 🎯 Linear Issue
<!-- Link to Linear issue -->
Closes: [LINEAR-XXX](https://linear.app/...)

## 🎫 ServiceNow Reference
<!-- If this relates to a specific change or incident -->
- CHG: 
- INC: 
- RITM: 

## 🧪 Testing Checklist
- [ ] YAML syntax validated locally
- [ ] Tested in **observe mode** (read-only)
- [ ] No hardcoded credentials (uses `credential_ref` only)
- [ ] Tested against target device types
- [ ] Error handling verified
- [ ] Dry-run successful

## 📝 Pack/Recipe Details
<!-- For new packs or recipes -->

**Target Devices:**
- [ ] Cisco IOS/IOS-XE
- [ ] Cisco NX-OS
- [ ] Arista EOS
- [ ] Juniper JunOS
- [ ] Other: ___________

**Operation Type:**
- [ ] READ/OBSERVE (show commands, health checks)
- [ ] WRITE/CHANGE (configuration changes)

**Requires Ticket:** 
- [ ] Yes (WRITE operation)
- [ ] No (READ operation)

## 📚 Documentation
- [ ] Pack includes usage examples
- [ ] Recipe includes step-by-step instructions
- [ ] CMDB entries documented
- [ ] Updated relevant docs in `docs/`

## 🔒 Security Review
- [ ] No secrets in code
- [ ] Uses Windows Credential Manager references
- [ ] Follows least-privilege principle
- [ ] Audit logging included

## 👥 Peer Review
- [ ] Code reviewed by at least one team member
- [ ] Tested by someone other than author (if possible)
- [ ] Naming conventions followed
- [ ] Consistent with existing patterns

## 📸 Screenshots/Output
<!-- If applicable, show example output or screenshots -->

```
# Example output from observe mode test
```

## ⚠️ Breaking Changes
<!-- Does this change existing behavior? -->
- [ ] No breaking changes
- [ ] Breaking changes (describe below)

**Breaking change details:**


## 🚀 Deployment Notes
<!-- Any special considerations for using this automation? -->


## ✅ Final Checklist
- [ ] All tests passing
- [ ] Documentation complete
- [ ] No merge conflicts
- [ ] Ready for peer review

---

**By submitting this PR, I confirm:**
- This automation follows NetOpsForge governance policies
- I have tested this in a safe environment
- I understand WRITE operations require ServiceNow tickets

