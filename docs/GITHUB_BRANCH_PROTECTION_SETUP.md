# GitHub Branch Protection Setup Guide

**Repository**: https://github.com/JT-BFS/NetOpsForge  
**Branch to Protect**: `main`  
**Date**: 2026-02-12

---

## 🎯 **Why Branch Protection?**

Branch protection ensures:
- ✅ No direct commits to `main` (all changes via PR)
- ✅ Peer review required before merging
- ✅ Automated checks must pass (GitHub Actions)
- ✅ Quality and security standards enforced
- ✅ Audit trail for all changes

---

## 📋 **Step-by-Step Configuration**

### **1. Add Branch Protection Rule**

On the page that just opened (Settings → Branches):

1. Click **"Add branch protection rule"** or **"Add rule"**

2. **Branch name pattern**: `main`

---

### **2. Configure Protection Settings**

Check the following boxes:

#### **✅ Require a pull request before merging**
- This prevents direct commits to `main`
- All changes must go through PR workflow

**Sub-settings to enable:**
- ✅ **Require approvals**: Set to `1`
  - At least one team member must review and approve
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - Ensures re-review after changes
- ✅ **Require review from Code Owners** (optional for now)
  - Can enable later when you create CODEOWNERS file

---

#### **✅ Require status checks to pass before merging**
- Ensures GitHub Actions workflows pass before merge

**Sub-settings to enable:**
- ✅ **Require branches to be up to date before merging**
  - Prevents merge conflicts

**Status checks to require** (add these):
- `validate-packs` (from validate-packs.yml workflow)
- `label-prs` (from label-prs.yml workflow)

**Note**: These will only appear after the first PR triggers the workflows. You can add them later.

---

#### **✅ Require conversation resolution before merging**
- All PR comments must be resolved before merge
- Ensures no feedback is ignored

---

#### **✅ Require linear history** (optional but recommended)
- Prevents merge commits
- Keeps git history clean
- Use "Squash and merge" or "Rebase and merge"

---

#### **✅ Do not allow bypassing the above settings**
- Ensures even admins follow the rules
- Critical for governance compliance

---

#### **❌ Do NOT enable (for now):**
- ❌ Require deployments to succeed (not applicable yet)
- ❌ Lock branch (too restrictive for pilot)
- ❌ Require signed commits (can enable later)

---

### **3. Additional Settings (Bottom of Page)**

#### **Rules applied to everyone including administrators**
- ✅ Check this box
- Ensures consistent process for all team members

---

### **4. Save Changes**

Click **"Create"** or **"Save changes"** at the bottom of the page.

---

## ✅ **Verification**

After saving, you should see:
- Branch protection rule for `main` listed
- Green checkmark indicating it's active
- Summary of enabled protections

---

## 🧪 **Testing Branch Protection**

### **Test 1: Try Direct Commit (Should Fail)**
```powershell
# This should be blocked
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
```

**Expected Result**: ❌ Push rejected (branch is protected)

### **Test 2: Create PR (Should Work)**
```powershell
# This should work
git checkout -b feature/test-branch-protection
echo "test" >> test.txt
git add test.txt
git commit -m "test: verify branch protection"
git push origin feature/test-branch-protection
# Then create PR on GitHub
```

**Expected Result**: ✅ PR created, awaiting review

---

## 📊 **Recommended Settings Summary**

| Setting | Enabled | Value |
|---------|---------|-------|
| Require pull request | ✅ Yes | - |
| Required approvals | ✅ Yes | 1 |
| Dismiss stale approvals | ✅ Yes | - |
| Require status checks | ✅ Yes | validate-packs, label-prs |
| Require up-to-date branches | ✅ Yes | - |
| Require conversation resolution | ✅ Yes | - |
| Require linear history | ✅ Yes (optional) | - |
| Do not allow bypass | ✅ Yes | - |
| Apply to administrators | ✅ Yes | - |

---

## 🔄 **Adding Status Checks Later**

After your first PR is created and GitHub Actions run:

1. Go back to Settings → Branches → Edit rule for `main`
2. Scroll to "Require status checks to pass before merging"
3. Search for and add:
   - `validate-packs`
   - `label-prs`
4. Save changes

---

## 👥 **Team Collaboration**

Once branch protection is enabled:

### **For Team Members:**
1. Clone repository
2. Create feature branch: `git checkout -b feature/NET-123-description`
3. Make changes and commit
4. Push branch: `git push origin feature/NET-123-description`
5. Create PR on GitHub
6. Request review from teammate
7. Address feedback
8. Merge after approval

### **For Reviewers:**
1. Review code changes
2. Test if possible
3. Leave comments or approve
4. Ensure all conversations resolved
5. Merge PR (or let author merge)

---

## 🚨 **Emergency Bypass (Use Sparingly)**

If you absolutely need to bypass protection (emergency only):

1. Go to Settings → Branches
2. Edit the `main` rule
3. Temporarily disable specific protections
4. Make emergency change
5. **Immediately re-enable protections**
6. Document why bypass was needed

**Better approach**: Create emergency PR and get quick review.

---

## 📝 **Next Steps After Branch Protection**

1. ✅ Configure branch protection (this guide)
2. ⏭️ Set up credentials in Windows Credential Manager
3. ⏭️ Populate CMDB with actual devices
4. ⏭️ Create first custom pack
5. ⏭️ Invite team members to repository

---

**Status**: Ready to configure  
**Estimated Time**: 5 minutes  
**Difficulty**: Easy

