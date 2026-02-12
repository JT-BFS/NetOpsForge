# NetOpsForge Pilot - Week 1 Kickoff Meeting

**Date**: [Insert Date]  
**Time**: [Insert Time]  
**Duration**: 2 hours  
**Location**: [Conference Room / Virtual Link]  
**Attendees**: All pilot participants

---

## 🎯 Meeting Objectives

1. Introduce NetOpsForge platform and pilot goals
2. Explain integration ecosystem (Linear, GitHub, Augment)
3. Demonstrate first pack creation with Augment
4. Assign initial tasks
5. Answer questions

---

## 📋 Agenda

### **Part 1: Introduction (30 minutes)**

#### Welcome & Pilot Overview (10 min)
- Pilot Lead introduces program
- Review pilot timeline (90 days)
- Success criteria overview
- Roles and responsibilities

#### Why NetOpsForge? (10 min)
- Current pain points in network operations
- Vision for automation-first workflows
- How Augment + NetOpsForge work together
- Expected benefits

#### Pilot Logistics (10 min)
- Weekly standup process (Linear)
- Communication channels
- Office hours schedule
- Escalation process

---

### **Part 2: Platform Deep Dive (45 minutes)**

#### Architecture Overview (15 min)
**Presenter**: Pilot Lead

**Topics**:
- Reasoning layer (Augment)
- Governance layer (Policies)
- Execution layer (Packs, Recipes, CMDB)
- Integration layer (Linear, GitHub, ServiceNow)

**Demo**: Show architecture diagram

#### Integration Walkthrough (15 min)
**Presenter**: Automation Champion

**Linear Integration**:
- How issues track automation work
- Automatic status updates from GitHub
- Creating and managing issues
- Labels and projects

**GitHub Integration**:
- Repository structure
- PR workflow
- GitHub Actions validation
- Branch protection

**Augment Integration**:
- How to interact with Augment
- Natural language commands
- Safety checks and governance
- Getting help from Augment

#### Governance & Safety Model (15 min)
**Presenter**: Security Reviewer

**Topics**:
- READ vs WRITE operations
- Execution gating policy
- ServiceNow ticket requirements
- Credential management (Windows Credential Manager)
- CMDB tagging (allow_execute)

**Demo**: Show policy file and explain rules

---

### **Part 3: Hands-On Demo (30 minutes)**

#### Live Demo: Creating First Pack with Augment
**Presenter**: Automation Champion

**Scenario**: Create interface status check pack

**Steps** (live demonstration):
1. Create Linear issue
   ```
   Title: "Add interface status check pack"
   Labels: pack, pilot
   ```

2. Ask Augment to create pack
   ```
   "Create a pack to check interface status on Cisco switches"
   ```

3. Review generated pack YAML
   - Metadata section
   - Commands section
   - Output handling
   - Validation checks

4. Test pack with Augment
   ```
   "Validate this pack for syntax errors"
   ```

5. Create PR via Augment
   ```
   "Create a PR for this pack referencing NET-123"
   ```

6. Show GitHub Actions running
   - YAML validation
   - Secret scanning
   - Pack structure check

7. Show Linear auto-update
   - Issue status changes to "In Progress"
   - PR link added to issue

8. Merge PR and show completion
   - Linear issue moves to "Done"

---

### **Part 4: Getting Started (15 minutes)**

#### Week 1-2 Assignments
**Presenter**: Pilot Lead

**Everyone**:
- [ ] Set up credentials in Windows Credential Manager
- [ ] Review `docs/getting-started.md`
- [ ] Explore existing packs in repository
- [ ] Create Linear account and join project

**Automation Champions**:
- [ ] Create 2 example packs by end of Week 2
- [ ] Prepare for training session 2
- [ ] Set up office hours schedule

**Network Engineers**:
- [ ] Identify 1-2 tasks to automate
- [ ] Create Linear issues for those tasks
- [ ] Attend training session 2

#### Resources Available
- Documentation: `docs/` directory
- Example pack: `packs/cisco-interface-status.yml`
- Example recipe: `recipes/network-health-check.yml`
- Ask Augment: "How do I use NetOpsForge?"

---

### **Part 5: Q&A (15 minutes)**

Open floor for questions

**Common Questions to Address**:
- How do I get help during the pilot?
- What if I break something?
- How much time should I dedicate to this?
- Can I automate tasks outside the pilot scope?
- What happens after the pilot?

---

## 📝 Action Items

### Pilot Lead
- [ ] Send meeting recording and slides
- [ ] Create Week 1 standup issue in Linear
- [ ] Schedule training session 2 (Week 2)
- [ ] Set up pilot metrics dashboard in Linear

### Automation Champions
- [ ] Schedule office hours (2 hours/week)
- [ ] Create first 2 example packs
- [ ] Prepare training materials for session 2

### All Participants
- [ ] Complete Week 1-2 assignments
- [ ] Set up credentials in Credential Manager
- [ ] Create at least 1 Linear issue for automation idea

---

## 📚 Pre-Read Materials

**Required** (send 2 days before meeting):
- `README.md` - Platform overview
- `docs/getting-started.md` - Quick start guide
- `AUGMENT_CONTROL_CONTRACT.md` - How Augment operates

**Optional**:
- `docs/architecture.md` - Deep dive on system design
- `docs/pack-development.md` - Pack creation guide

---

## 🎬 Post-Meeting

### Follow-Up Email Template

```
Subject: NetOpsForge Pilot Kickoff - Action Items & Resources

Hi Team,

Thank you for attending the NetOpsForge pilot kickoff! Here's a summary:

📋 Your Action Items (Week 1-2):
- Set up credentials in Windows Credential Manager
- Review getting-started.md
- Create Linear issues for automation ideas
- Attend Training Session 2 on [Date]

📚 Resources:
- Repository: [GitHub URL]
- Linear Project: [Linear URL]
- Documentation: docs/ directory
- Office Hours: [Schedule]

🆘 Getting Help:
- Ask Augment: "How do I use NetOpsForge?"
- Linear: Create issue with 'question' label
- Champions: [Office hours schedule]

📅 Next Meeting:
- Training Session 2: [Date/Time]
- Topic: Creating Your First Pack

Questions? Reply to this email or create a Linear issue.

Let's build something great together! 🚀

[Pilot Lead Name]
```

---

## 📊 Success Metrics for Kickoff

- [ ] 100% pilot participant attendance
- [ ] All participants have Linear access
- [ ] All participants understand READ vs WRITE
- [ ] At least 3 automation ideas identified
- [ ] No major concerns or blockers raised

---

**Meeting Owner**: [Pilot Lead Name]  
**Last Updated**: [Date]

