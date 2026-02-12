# NetOpsForge Security Scanning

This document describes the automated security controls that prevent sensitive information from being committed to the repository.

---

## 🔒 **Security Philosophy**

NetOpsForge is designed to be **safe for public sharing** by default:
- ✅ No hardcoded credentials
- ✅ No API keys or tokens
- ✅ No private keys or certificates
- ✅ No real IP addresses (use RFC 1918 only)
- ✅ No personal information

---

## 🛡️ **Multi-Layer Security Controls**

### **Layer 1: Git Pre-Push Hook** (Local)

Runs automatically before every `git push` to scan for:
- Hardcoded passwords
- API keys and tokens
- SSH private keys
- AWS credentials
- Email addresses
- Environment variables with secrets
- Non-RFC 1918 IP addresses

**Location**: `.git/hooks/pre-push` (Bash) and `.git/hooks/pre-push.ps1` (PowerShell)

**How it works**:
```bash
# Automatically runs before push
git push origin main

# Output:
🔍 Running NetOpsForge security scan before push...
  Checking for hardcoded passwords...
  Checking for API keys...
  Checking for authentication tokens...
  Checking for private keys...
  Checking for AWS access keys...
  Checking for email addresses...
✅ Security scan passed! No sensitive data detected.
```

**Bypass** (NOT recommended):
```bash
git push --no-verify
```

---

### **Layer 2: GitHub Actions CI/CD** (Remote)

Runs on every PR and push to `main`:

**Workflow**: `.github/workflows/validate-packs.yml`

**Checks**:
1. **Secret Scanning**: Scans for hardcoded passwords and API keys
2. **YAML Validation**: Ensures proper syntax
3. **Pack Metadata Validation**: Verifies required fields
4. **Trivy Security Scanner**: Scans for vulnerabilities

**Example output**:
```
✅ check-secrets: Scan for Hardcoded Secrets
✅ validate-yaml: Validate YAML Syntax
✅ validate-packs: Validate Pack Structure
✅ security-scan: Security Scan
```

---

### **Layer 3: .gitignore Protection** (Preventive)

Prevents sensitive files from being tracked:

```gitignore
# Secrets and credentials
*.key
*.pem
*.p12
*.pfx
credentials.yml
secrets.yml
.env
.env.local

# Output files (may contain sensitive data)
output/
logs/
reports/
*.log

# Local configuration
local_config.yml
```

---

## 🔐 **Credential Management Pattern**

### ✅ **CORRECT - Use credential_ref**

```yaml
authentication:
  method: credential_ref
  credential_ref: "cisco_readonly"
```

Actual credentials stored in **Windows Credential Manager**:
```
Target: NetOpsForge/cisco_readonly
Username: netops_ro
Password: ••••••••
```

### ❌ **WRONG - Hardcoded credentials**

```yaml
# NEVER DO THIS!
authentication:
  username: "admin"
  password: "Cisco123!"  # ❌ Will be blocked by security scan
```

---

## 🧪 **Testing Security Controls**

### **Test Pre-Push Hook**

1. Create a test file with a fake password:
```bash
echo "password: 'test123'" > test-secret.yml
git add test-secret.yml
git commit -m "Test security"
git push
```

2. Expected result:
```
❌ ERROR: Potential hardcoded passwords found!
test-secret.yml: password: 'test123'
```

3. Clean up:
```bash
git reset HEAD~1
rm test-secret.yml
```

---

## 📋 **What Gets Scanned**

| Pattern | Description | Example |
|---------|-------------|---------|
| `password\s*[:=]\s*['"]` | Hardcoded passwords | `password: "secret"` |
| `api[_-]?key\s*[:=]` | API keys | `api_key: "abc123..."` |
| `token\s*[:=]` | Auth tokens | `token: "Bearer xyz..."` |
| `BEGIN.*PRIVATE KEY` | SSH/TLS keys | `-----BEGIN PRIVATE KEY-----` |
| `AKIA[0-9A-Z]{16}` | AWS access keys | `AKIAIOSFODNN7EXAMPLE` |
| `[a-z]+@[a-z]+\.[a-z]+` | Email addresses | `user@company.com` |
| Non-RFC 1918 IPs | Public IP addresses | `8.8.8.8` (allowed: `10.0.0.1`) |

---

## 🚨 **If Security Scan Fails**

### **Step 1: Review the findings**
The scan will show exactly what was detected:
```
❌ ERROR: Potential hardcoded passwords found!
packs/my-pack.yml:23: password: "Cisco123!"
```

### **Step 2: Fix the issue**

**Option A**: Use `credential_ref`
```yaml
authentication:
  method: credential_ref
  credential_ref: "cisco_readonly"
```

**Option B**: Use RFC 1918 IPs for examples
```yaml
# ❌ Bad
management_ip: 203.0.113.1

# ✅ Good
management_ip: 10.0.1.1
```

**Option C**: Remove sensitive data
```yaml
# ❌ Bad
email: jesse.tucker@company.com

# ✅ Good
email: admin@example.com
```

### **Step 3: Re-commit and push**
```bash
git add .
git commit -m "Fix: Remove hardcoded credentials"
git push
```

---

## 🔄 **Updating Security Rules**

To add new security patterns:

1. Edit `.git/hooks/pre-push` (Bash) or `.git/hooks/pre-push.ps1` (PowerShell)
2. Add new `check_pattern` call
3. Test with a sample violation
4. Update this documentation

---

## 📊 **Security Audit History**

| Date | Auditor | Result | Notes |
|------|---------|--------|-------|
| 2026-02-12 | Augment Agent | ✅ PASSED | Initial security review - Safe for public sharing |

---

## 🤝 **Contributing**

When submitting PRs:
1. ✅ Security scan must pass
2. ✅ Use `credential_ref` for all authentication
3. ✅ Use RFC 1918 IPs (10.x.x.x) for examples
4. ✅ No real device names or serial numbers
5. ✅ No personal information

---

## 📖 **Additional Resources**

- [RFC 1918 - Private IP Addresses](https://tools.ietf.org/html/rfc1918)
- [Windows Credential Manager Setup](getting-started.md#credential-setup)
- [Pack Development Guide](pack-development.md)
- [Contributing Guidelines](CONTRIBUTING.md)

