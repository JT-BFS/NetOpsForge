# CMDB Privacy and Security

## 🔒 Overview

**Your device inventory contains sensitive information and should NEVER be committed to a public repository!**

This document explains how NetOpsForge keeps your CMDB private while maintaining a public codebase.

---

## 🎯 Default Approach: Git-Ignored Local CMDB

### How It Works

1. **Example Template in Repo** (`devices.example.yml`)
   - Safe to commit to public repo
   - Shows structure and available fields
   - Contains fake/example data only

2. **Real CMDB Locally** (`devices.yml`)
   - Git-ignored (never committed)
   - Contains your actual device inventory
   - Each team member maintains their own copy

3. **Automatic Protection**
   - `.gitignore` prevents accidental commits
   - Pre-push hooks scan for sensitive data
   - CI/CD validates no real IPs are committed

### Setup

```powershell
# Run the setup script
.\scripts\setup-cmdb.ps1

# Or manually:
Copy-Item cmdb\devices.example.yml cmdb\devices.yml

# Edit with your real devices
notepad cmdb\devices.yml

# Verify it's git-ignored
git status  # devices.yml should NOT appear
```

### Pros
- ✅ Simple and straightforward
- ✅ No external dependencies
- ✅ Works offline
- ✅ Fast access

### Cons
- ❌ Each team member maintains separate copy
- ❌ No central source of truth
- ❌ Manual sync required for team changes

---

## 🏢 Enterprise Approach: External CMDB Source

For larger teams, you may want a centralized CMDB stored externally.

### Option 1: Private Git Repository

Store CMDB in a separate private repository:

```yaml
# .env
CMDB_SOURCE=git
CMDB_REPO_URL=https://github.com/your-org/network-cmdb-private.git
CMDB_REPO_BRANCH=main
CMDB_PATH=devices.yml
```

NetOpsForge clones the private repo and reads from it.

### Option 2: Network Share

Store CMDB on a network file share:

```yaml
# .env
CMDB_SOURCE=file
CMDB_PATH=\\fileserver\netops\cmdb\devices.yml
```

### Option 3: Database

Store CMDB in a database (future feature):

```yaml
# .env
CMDB_SOURCE=database
CMDB_DB_TYPE=postgresql
CMDB_DB_HOST=cmdb-db.internal.company.com
CMDB_DB_NAME=netops_cmdb
```

### Option 4: ServiceNow/ITSM Integration

Sync from ServiceNow Configuration Management Database:

```yaml
# .env
CMDB_SOURCE=servicenow
SERVICENOW_INSTANCE=yourcompany.service-now.com
SERVICENOW_CMDB_TABLE=cmdb_ci_netgear
```

---

## 🔐 Encrypted CMDB (Advanced)

For teams that want version control but need encryption:

### Setup

1. **Encrypt your CMDB:**
   ```powershell
   # Encrypt using GPG
   gpg --symmetric --cipher-algo AES256 cmdb\devices.yml
   # Creates: cmdb\devices.yml.gpg
   ```

2. **Commit encrypted version:**
   ```powershell
   git add cmdb\devices.yml.gpg
   git commit -m "Add encrypted CMDB"
   ```

3. **Decrypt locally:**
   ```powershell
   gpg --decrypt cmdb\devices.yml.gpg > cmdb\devices.yml
   ```

4. **Add to .gitignore:**
   ```
   cmdb/devices.yml
   !cmdb/devices.yml.gpg
   ```

### Pros
- ✅ Version controlled
- ✅ Encrypted at rest
- ✅ Audit trail of changes

### Cons
- ❌ Requires GPG key management
- ❌ Manual decrypt step
- ❌ Merge conflicts harder to resolve

---

## 🛡️ Security Best Practices

### What to Keep Private

**NEVER commit these to public repos:**
- ❌ Real management IP addresses
- ❌ Device hostnames (if they reveal internal structure)
- ❌ Serial numbers
- ❌ Rack locations
- ❌ Credentials or credential hints
- ❌ Internal site codes/names

### What's Safe to Commit

**These are safe in public repos:**
- ✅ Example/template files with fake data
- ✅ CMDB schema documentation
- ✅ Field descriptions
- ✅ Validation rules
- ✅ Query examples

### Validation

Before committing, always check:

```powershell
# Check what's being committed
git diff --cached

# Verify no real IPs
git diff --cached | Select-String -Pattern "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# Run pre-push security scan
.\.git\hooks\pre-push
```

---

## 📋 Recommended Workflow

### For Solo Developers / Small Teams

Use the default git-ignored approach:
- Keep `devices.yml` local
- Use `devices.example.yml` as template
- Simple and effective

### For Medium Teams (5-20 people)

Use a private Git repository:
- Central source of truth
- Version controlled
- Access control via GitHub/GitLab permissions

### For Large Enterprises

Use ServiceNow or database integration:
- Automated sync
- Single source of truth
- Integration with existing ITSM
- Audit trails and approval workflows

---

## 🔍 Verifying Privacy

### Check Git Ignore Status

```powershell
# Should show devices.yml is ignored
git check-ignore -v cmdb\devices.yml

# Should output:
# .gitignore:14:cmdb/devices.yml    cmdb/devices.yml
```

### Check Git History

```powershell
# Verify devices.yml was never committed
git log --all --full-history -- cmdb/devices.yml

# Should show no results (or only devices.example.yml)
```

### Scan for Leaked Data

```powershell
# Search entire repo history for IP patterns
git log -p | Select-String -Pattern "10\.0\.\d{1,3}\.\d{1,3}"
```

---

## 🆘 If You Accidentally Committed Sensitive Data

If you accidentally committed `devices.yml` or other sensitive data:

1. **DO NOT just delete it in a new commit** - it's still in Git history!

2. **Remove from Git history:**
   ```powershell
   # Using git filter-repo (recommended)
   git filter-repo --path cmdb/devices.yml --invert-paths

   # Or using BFG Repo-Cleaner
   bfg --delete-files devices.yml
   ```

3. **Force push (if not yet public):**
   ```powershell
   git push --force
   ```

4. **If already public:**
   - Rotate all credentials immediately
   - Consider the data compromised
   - Update firewall rules if IPs were exposed
   - Notify security team

---

## 📚 Additional Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Git filter-repo](https://github.com/newren/git-filter-repo)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

