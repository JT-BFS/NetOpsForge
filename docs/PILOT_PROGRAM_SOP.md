# NetOpsForge Pilot Program - Standard Operating Procedure

**Version**: 1.0  
**Date**: 2026-02-12  
**Owner**: Network Operations Team  
**Duration**: 90 Days

---

## 🎯 Pilot Objectives

### Primary Goals
1. **Validate** Augment + NetOpsForge integration in production environment
2. **Build** initial automation pack library (target: 15 packs)
3. **Train** network team on automation-first workflows
4. **Establish** governance and safety patterns
5. **Measure** time savings and operational improvements

### Success Criteria
- ✅ 15+ automation packs created and tested
- ✅ 5+ recipes for common operational tasks
- ✅ 80% of team trained and actively using platform
- ✅ Zero security incidents from automation
- ✅ 30%+ reduction in manual task time
- ✅ All WRITE operations properly gated with tickets

---

## 👥 Pilot Participants

### Roles

| Role | Responsibility | Count |
|------|----------------|-------|
| **Pilot Lead** | Overall coordination, reporting | 1 |
| **Automation Champions** | Pack development, mentoring | 2-3 |
| **Network Engineers** | Pack users, feedback providers | 5-8 |
| **Security Reviewer** | Validate governance compliance | 1 |

### Pilot Lead Responsibilities
- Weekly status updates in Linear
- Track metrics and success criteria
- Coordinate training sessions
- Escalate blockers
- Final pilot report

### Automation Champions Responsibilities
- Develop initial pack library
- Review PRs from team members
- Provide 1:1 mentoring
- Document best practices
- Lead weekly office hours

---

## 📅 Pilot Timeline (90 Days)

### **Week 1-2: Foundation & Training**
- [ ] Pilot kickoff meeting
- [ ] Team training on NetOpsForge concepts
- [ ] Augment integration walkthrough
- [ ] Set up credentials in Credential Manager
- [ ] Populate CMDB with production devices
- [ ] Create Linear project and labels

### **Week 3-4: First Packs (READ Operations)**
- [ ] Champions create 5 READ operation packs
- [ ] Team members test packs with Augment
- [ ] Submit first PRs
- [ ] Establish PR review cadence
- [ ] Document lessons learned

### **Week 5-8: Expand Pack Library**
- [ ] Each team member creates 1-2 packs
- [ ] Build first recipes
- [ ] Test GitHub Actions workflows
- [ ] Refine Linear workflow
- [ ] Weekly metrics review

### **Week 9-10: WRITE Operations (Controlled)**
- [ ] Create first WRITE operation pack
- [ ] Test ServiceNow ticket integration (manual)
- [ ] Validate governance controls
- [ ] Document approval workflow
- [ ] Security review

### **Week 11-12: Optimization & Scaling**
- [ ] Optimize existing packs
- [ ] Create advanced recipes
- [ ] Document common patterns
- [ ] Plan post-pilot rollout
- [ ] Final pilot report

---

## 🔄 Integration Usage Workflows

### **How Augment Uses Each Integration**

This section shows the **actual workflow** for how you'll use Augment with all the integrations.

---

## 📋 **Workflow 1: Creating a New Automation Pack**

### **Integration Flow: Linear → Augment → GitHub → Linear**

```
Step 1: Create Linear Issue
├─ You: Create issue "Add VLAN verification pack"
├─ Linear: Assigns issue ID (NET-123)
└─ Linear: Status = "Backlog"

Step 2: Start Work with Augment
├─ You: "I want to create a pack for VLAN verification on Cisco switches"
├─ Augment: Searches codebase for similar packs
├─ Augment: Retrieves pack development guide
├─ Augment: Generates pack YAML based on requirements
└─ Augment: Saves to packs/cisco-vlan-verify.yml

Step 3: Test with Augment
├─ You: "Test this pack on dist-sw-01 in observe mode"
├─ Augment: Validates YAML syntax
├─ Augment: Checks for hardcoded secrets
├─ Augment: (Future) Runs pack against device
└─ Augment: Shows results

Step 4: Submit to GitHub
├─ You: "Create a PR for this pack referencing NET-123"
├─ Augment: Creates branch feature/NET-123-vlan-verify
├─ Augment: Commits pack file
├─ Augment: Pushes to GitHub
├─ Augment: Creates PR with template filled out
├─ GitHub Actions: Runs validation workflows
└─ GitHub: PR created and linked to Linear

Step 5: Linear Auto-Update
├─ Linear: Detects PR opened
├─ Linear: Updates NET-123 status → "In Progress"
└─ Linear: Adds PR link to issue

Step 6: Peer Review
├─ Teammate: Reviews PR on GitHub
├─ Teammate: Requests changes or approves
├─ GitHub: Triggers review workflow
├─ Linear: Updates NET-123 status → "In Review"
└─ You: Address feedback with Augment's help

Step 7: Merge & Complete
├─ Teammate: Approves PR
├─ You: Merge PR
├─ GitHub: Merges to main
├─ Linear: Updates NET-123 status → "Done"
└─ Pack now available in NetOpsForge catalog
```

**Integrations Used**: Linear, Augment, GitHub, GitHub Actions

---

## 🔍 **Workflow 2: Running a Health Check (READ Operation)**

### **Integration Flow: Augment → CMDB → (Future: Device) → Linear**

```
Step 1: Request Health Check
├─ You: "Run interface health check on all core routers"
└─ Augment: Understands intent

Step 2: Augment Plans Execution
├─ Augment: Searches for relevant pack
├─ Augment: Finds "cisco-interface-status.yml"
├─ Augment: Checks operation_type = "read"
├─ Augment: Checks policy → READ allowed without ticket
└─ Augment: Queries CMDB for core routers

Step 3: CMDB Query
├─ Augment: Reads cmdb/devices.yml
├─ Augment: Filters by device_role = "core-router"
├─ Augment: Finds: core-rtr-01, core-rtr-02
└─ Augment: Validates credential_ref exists

Step 4: Inform & Execute
├─ Augment: "I will run cisco-interface-status on 2 devices"
├─ Augment: Shows which devices
├─ You: Acknowledge
├─ Augment: (Future) Executes pack via runner
└─ Augment: (Future) Collects results

Step 5: Results & Reporting
├─ Augment: Parses output
├─ Augment: Identifies issues (e.g., 2 interfaces down)
├─ Augment: Generates summary report
└─ Augment: "Found 2 interfaces down on core-rtr-01"

Step 6: Auto-Create Linear Issue (If Errors)
├─ Pack config: auto_create_issue_on_error = true
├─ Augment: Creates Linear issue automatically
├─ Linear: Issue created "Interface down on core-rtr-01"
├─ Linear: Labels: network-automation, interface-monitoring
└─ Linear: Priority: medium
```

**Integrations Used**: Augment, CMDB, Linear (auto-issue creation)

---

## ⚠️ **Workflow 3: Making a Configuration Change (WRITE Operation)**

### **Integration Flow: ServiceNow → Augment → CMDB → GitHub → Linear**

```
Step 1: Create ServiceNow Change Ticket
├─ You: Create CHG ticket in ServiceNow
├─ ServiceNow: CHG0012345 created
├─ ServiceNow: Approval workflow initiated
└─ ServiceNow: CHG approved

Step 2: Request Change via Augment
├─ You: "Add VLAN 100 to dist-sw-01"
└─ Augment: Understands intent

Step 3: Augment Safety Check
├─ Augment: Identifies as WRITE operation
├─ Augment: Checks policy requirements:
│   ├─ ServiceNow ticket? ❌ Not provided
│   ├─ Explicit YES? ❌ Not provided
│   └─ Target tagged allow_execute? ❓ Unknown
├─ Augment: STOPS execution
└─ Augment: "This is a WRITE operation. Requirements:
              1. ServiceNow CHG ticket
              2. Type YES to confirm
              3. Target must have allow_execute tag"

Step 4: Provide Required Information
├─ You: "CHG0012345"
├─ Augment: Validates ticket format
├─ Augment: (Future) Queries ServiceNow API for ticket status
├─ Augment: Checks CMDB for dist-sw-01
├─ Augment: Verifies tags include "allow_execute" ✅
└─ Augment: "Ticket validated. Type YES to proceed"

Step 5: Explicit Confirmation
├─ You: "YES"
└─ Augment: All requirements met ✅

Step 6: Execute Change
├─ Augment: (Future) Executes pack
├─ Augment: Logs all commands
├─ Augment: Captures output
└─ Augment: Validates success

Step 7: Documentation & Tracking
├─ Augment: Creates Linear issue for tracking
├─ Linear: Issue "VLAN 100 added to dist-sw-01"
├─ Linear: References CHG0012345
├─ Augment: (Future) Updates ServiceNow ticket with results
└─ Augment: Saves audit log
```

**Integrations Used**: ServiceNow, Augment, CMDB, Linear

---

## 📊 **Workflow 4: Troubleshooting with a Recipe**

### **Integration Flow: Augment → Recipe → Multiple Packs → Linear → Notion**

```
Step 1: Incident Reported
├─ You: "BGP neighbor down on core-rtr-01"
└─ Augment: Understands troubleshooting needed

Step 2: Augment Finds Recipe
├─ Augment: Searches recipes/
├─ Augment: Finds "bgp-troubleshooting.yml" recipe
├─ Augment: Reviews recipe steps
└─ Augment: "I'll run the BGP troubleshooting recipe (5 steps)"

Step 3: Execute Recipe Steps
├─ Step 1: Check BGP neighbor status (pack: cisco-bgp-status)
├─ Step 2: Check interface status (pack: cisco-interface-status)
├─ Step 3: Check routing table (pack: cisco-route-check)
├─ Step 4: Check logs (pack: cisco-log-check)
└─ Step 5: Generate report

Step 4: Aggregate Results
├─ Augment: Collects output from all 5 packs
├─ Augment: Identifies root cause
└─ Augment: "Interface Gi0/0/1 is down, causing BGP neighbor loss"

Step 5: Generate Comprehensive Report
├─ Augment: Creates markdown report
├─ Report includes:
│   ├─ Timeline of checks
│   ├─ All command outputs
│   ├─ Root cause analysis
│   └─ Recommended remediation
└─ Augment: Saves to reports/bgp-troubleshoot-{timestamp}.md

Step 6: Create Linear Issue
├─ Augment: Creates Linear issue automatically
├─ Linear: "BGP neighbor down - Interface failure"
├─ Linear: Attaches report
├─ Linear: Labels: incident, bgp, troubleshooting
└─ Linear: Assigns to on-call engineer

Step 7: (Future) Document in Notion
├─ Augment: Creates Notion page in "Incident Reports"
├─ Notion: Includes full troubleshooting steps
├─ Notion: Links to Linear issue
└─ Notion: Adds to knowledge base
```

**Integrations Used**: Augment, Recipes, Multiple Packs, Linear, Notion (future)

---

## 🎬 **Pilot Scenarios - Week by Week**

### **Week 1-2: Foundation**

#### Scenario 1: Initial Setup
```
You → Augment: "Help me set up NetOpsForge for the pilot"

Augment will:
1. Guide you through CMDB population
2. Help configure credentials in Credential Manager
3. Create initial Linear project structure
4. Set up GitHub repository
5. Walk through first pack example
```

#### Scenario 2: Team Training
```
You → Augment: "Explain how NetOpsForge works to my team"

Augment will:
1. Provide overview of architecture
2. Explain READ vs WRITE operations
3. Demonstrate pack execution
4. Show Linear integration
5. Answer team questions
```

---

### **Week 3-4: First Packs**

#### Scenario 3: Create Interface Status Pack
```
You → Augment: "Create a pack to check interface status on Cisco switches"

Augment will:
1. Search for similar existing packs
2. Generate pack YAML with proper structure
3. Include credential_ref (no hardcoded passwords)
4. Add validation checks
5. Include usage examples
6. Save to packs/cisco-interface-status.yml

You → Augment: "Create a PR for this pack"

Augment will:
1. Create feature branch
2. Commit pack file
3. Fill out PR template
4. Reference Linear issue
5. Push to GitHub

GitHub Actions will:
1. Validate YAML syntax ✅
2. Scan for secrets ✅
3. Check pack structure ✅
4. Auto-label PR as "pack" ✅

Linear will:
1. Detect PR opened
2. Update issue status → "In Progress"
3. Add PR link to issue
```

#### Scenario 4: Test Pack with Augment
```
You → Augment: "Test the interface status pack on dist-sw-01"

Augment will:
1. Load pack definition
2. Check operation_type = "read"
3. Verify no ticket needed
4. Query CMDB for dist-sw-01
5. Validate credential_ref exists
6. (Future) Execute pack
7. Show results
```

---

### **Week 5-8: Expand Library**

#### Scenario 5: Create BGP Neighbor Check Pack
```
You → Augment: "I need a pack to verify BGP neighbors on core routers"

Augment will:
1. Create pack with BGP-specific commands
2. Add TextFSM parsing for structured output
3. Include validation for neighbor states
4. Add error handling
5. Create Linear issue automatically
6. Generate PR

Team Member Reviews:
1. Reviews pack on GitHub
2. Tests on lab device
3. Approves PR
4. Merges to main

Linear automatically:
1. Updates issue → "Done"
2. Closes issue
```

#### Scenario 6: Build First Recipe
```
You → Augment: "Create a recipe for pre-change validation"

Augment will:
1. Create recipe YAML
2. Define steps:
   - Step 1: Backup config (pack: cisco-backup)
   - Step 2: Check interfaces (pack: cisco-interface-status)
   - Step 3: Check BGP (pack: cisco-bgp-status)
   - Step 4: Check routing (pack: cisco-route-check)
3. Configure reporting
4. Add Linear integration
5. Create PR

You → Augment: "Run the pre-change validation recipe on core-rtr-01"

Augment will:
1. Execute all 4 steps in sequence
2. Aggregate results
3. Generate comprehensive report
4. Save to reports/pre-change-{timestamp}.md
5. Create Linear issue if any checks fail
```

---

### **Week 9-10: WRITE Operations**

#### Scenario 7: First Configuration Change
```
You → Augment: "Add VLAN 200 to dist-sw-01"

Augment will:
1. Identify as WRITE operation
2. Check policy requirements
3. Request ServiceNow ticket
4. Request explicit YES
5. Verify CMDB tag "allow_execute"

You: "CHG0012345"
You: "YES"

Augment will:
1. Validate all requirements ✅
2. (Future) Execute configuration change
3. Capture before/after state
4. Create Linear issue for tracking
5. Log to audit trail
6. (Future) Update ServiceNow ticket
```

#### Scenario 8: Rollback Procedure
```
You → Augment: "The VLAN change caused issues, rollback"

Augment will:
1. Check for backup/snapshot
2. Generate rollback commands
3. Require same governance (ticket + YES)
4. Execute rollback
5. Verify restoration
6. Update Linear issue
7. Document in incident report
```

---

### **Week 11-12: Advanced Usage**

#### Scenario 9: Scheduled Health Checks
```
You → Augment: "Set up automated daily health checks"

Augment will:
1. Create recipe for daily checks
2. Configure schedule in recipe YAML
3. Set up Linear issue creation on failures
4. (Future) Configure GitHub Actions for scheduling
5. Document in Notion runbook
```

#### Scenario 10: Incident Response
```
Incident: Multiple BGP neighbors down

You → Augment: "Run BGP troubleshooting on all core routers"

Augment will:
1. Execute bgp-troubleshooting recipe
2. Run against all core routers in parallel
3. Collect diagnostics from each device
4. Identify common failure patterns
5. Generate incident report
6. Create high-priority Linear issue
7. Suggest remediation steps
8. (Future) Create Notion incident page
```

---

## 📊 **Pilot Metrics & Tracking**

### **Metrics to Track in Linear**

Create a Linear view/dashboard with these metrics:

#### **Automation Metrics**
- **Packs Created**: Target 15, track weekly
- **Recipes Created**: Target 5, track weekly
- **PRs Submitted**: Track velocity
- **PRs Merged**: Track completion rate
- **Pack Executions**: (Future) Track usage

#### **Quality Metrics**
- **PR Review Time**: Target < 2 business days
- **Pack Success Rate**: Target > 95%
- **Security Violations**: Target 0
- **Governance Bypasses**: Target 0

#### **Efficiency Metrics**
- **Time Saved per Task**: Document in Linear issues
- **Manual Tasks Automated**: Track count
- **Incident Response Time**: Before vs After
- **Change Success Rate**: Track with/without pre-checks

#### **Adoption Metrics**
- **Team Members Contributing**: Target 80%
- **Active Pack Users**: Track weekly
- **Training Completion**: Track 100%
- **Satisfaction Score**: Survey monthly

### **Linear Project Structure for Pilot**

```
Linear Workspace: NetOps
├── Project: NetOpsForge Pilot
│   ├── View: Pack Development
│   │   ├── Backlog (packs to create)
│   │   ├── In Progress (being developed)
│   │   ├── In Review (PR open)
│   │   └── Done (merged)
│   │
│   ├── View: Recipe Development
│   │   └── (same structure)
│   │
│   ├── View: Pilot Metrics
│   │   ├── Weekly stats
│   │   └── Success criteria tracking
│   │
│   └── View: Issues & Blockers
│       ├── Bugs
│       ├── Questions
│       └── Blockers
```

### **Weekly Pilot Standup (in Linear)**

Every Monday, Pilot Lead creates Linear issue:
```
Title: "Week X Pilot Standup - [Date]"
Labels: pilot, standup

Template:
## Accomplishments Last Week
- Packs created: X
- PRs merged: X
- Team members active: X

## This Week's Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Blockers
- None / List blockers

## Metrics Update
- Total packs: X/15
- Total recipes: X/5
- Team adoption: X%
```

---

## 🎓 **Pilot Training Plan**

### **Session 1: NetOpsForge Overview (Week 1)**
**Duration**: 2 hours
**Audience**: All pilot participants

**Agenda**:
1. NetOpsForge architecture (30 min)
   - Augment as reasoning layer
   - Packs and recipes
   - CMDB and credentials
   - Governance model

2. Integration overview (30 min)
   - Linear workflow
   - GitHub PR process
   - ServiceNow integration (future)

3. Hands-on demo (45 min)
   - Ask Augment to explain a pack
   - Run example pack
   - Review CMDB structure

4. Q&A (15 min)

**Deliverable**: All participants understand architecture

---

### **Session 2: Creating Your First Pack (Week 2)**
**Duration**: 2 hours
**Audience**: All pilot participants

**Agenda**:
1. Pack structure deep-dive (30 min)
2. Live pack creation with Augment (45 min)
   - Ask Augment to create pack
   - Review generated YAML
   - Test pack
3. PR submission process (30 min)
   - Create branch
   - Submit PR
   - Review process
4. Hands-on exercise (15 min)
   - Each person creates simple pack

**Deliverable**: Each participant creates and submits 1 pack

---

### **Session 3: Advanced Packs & Recipes (Week 6)**
**Duration**: 2 hours
**Audience**: Automation Champions + interested engineers

**Agenda**:
1. Advanced pack features (30 min)
   - TextFSM parsing
   - Validation checks
   - Error handling
2. Recipe creation (45 min)
   - Multi-step workflows
   - Reporting
   - Linear integration
3. Best practices (30 min)
   - Naming conventions
   - Documentation
   - Testing strategies
4. Q&A (15 min)

**Deliverable**: Champions can mentor others

---

### **Session 4: WRITE Operations & Governance (Week 9)**
**Duration**: 1.5 hours
**Audience**: All pilot participants

**Agenda**:
1. Governance review (20 min)
   - Why governance matters
   - READ vs WRITE
   - Ticket requirements
2. WRITE pack creation (30 min)
   - Safety considerations
   - Rollback planning
   - Testing approach
3. ServiceNow integration (20 min)
   - Ticket workflow
   - Manual process (current)
   - Future automation
4. Live demo (20 min)
   - Execute WRITE operation
   - Show governance in action

**Deliverable**: Team understands WRITE operation safety

---

## 📋 **Pilot Checklists**

### **Daily Checklist (Automation Champions)**
- [ ] Review new PRs (target: same day)
- [ ] Answer questions in Linear
- [ ] Monitor GitHub Actions failures
- [ ] Update pilot metrics

### **Weekly Checklist (Pilot Lead)**
- [ ] Create weekly standup issue in Linear
- [ ] Review metrics vs targets
- [ ] Identify and escalate blockers
- [ ] Schedule 1:1s with struggling participants
- [ ] Update stakeholders

### **Monthly Checklist (Pilot Lead)**
- [ ] Generate pilot progress report
- [ ] Conduct team satisfaction survey
- [ ] Review and adjust success criteria
- [ ] Plan next month's focus areas
- [ ] Present to leadership

---

## 🚨 **Pilot Escalation Process**

### **Issue Severity Levels**

**P1 - Critical**
- Security violation
- Governance bypass
- Production outage caused by automation
- **Action**: Immediate escalation to Pilot Lead + Security

**P2 - High**
- Pack causing unexpected behavior
- GitHub Actions blocking all PRs
- Multiple team members blocked
- **Action**: Escalate to Pilot Lead within 4 hours

**P3 - Medium**
- Pack not working as expected
- PR review taking > 3 days
- Documentation unclear
- **Action**: Create Linear issue, Champions address

**P4 - Low**
- Feature request
- Documentation improvement
- Nice-to-have enhancement
- **Action**: Add to backlog

### **Escalation Path**
```
Issue Identified
    ↓
Create Linear Issue with severity label
    ↓
P1/P2: Tag Pilot Lead immediately
P3/P4: Champions triage
    ↓
Pilot Lead assesses
    ↓
If needed: Escalate to management
```

---

## 📈 **Pilot Success Criteria (Detailed)**

### **Must Have (Go/No-Go for Production)**
- ✅ 15+ packs created and tested
- ✅ 5+ recipes operational
- ✅ Zero security incidents
- ✅ Zero governance bypasses
- ✅ 80%+ team trained
- ✅ All WRITE operations properly gated

### **Should Have (Strong Indicators)**
- ✅ 30%+ time savings on automated tasks
- ✅ PR review time < 2 days average
- ✅ 90%+ pack success rate
- ✅ Team satisfaction score > 4/5

### **Nice to Have (Bonus)**
- ✅ Integration with ServiceNow API
- ✅ Notion documentation populated
- ✅ Scheduled automation running
- ✅ Advanced recipes with complex logic

---

## 📝 **Pilot Reporting**

### **Weekly Status Report (Linear Issue)**
```markdown
# Week X Pilot Status

## Metrics
- Packs: X/15 (X% complete)
- Recipes: X/5 (X% complete)
- PRs this week: X
- Team adoption: X%

## Highlights
- [Achievement 1]
- [Achievement 2]

## Challenges
- [Challenge 1 + mitigation]

## Next Week Focus
- [Goal 1]
- [Goal 2]
```

### **Final Pilot Report (End of Week 12)**
```markdown
# NetOpsForge Pilot - Final Report

## Executive Summary
[2-3 paragraphs on outcomes]

## Success Criteria Results
[Table showing each criterion and result]

## Metrics Achieved
[Charts/graphs of key metrics]

## Key Learnings
[What worked, what didn't]

## Recommendations
[Go/No-Go decision + next steps]

## Appendix
- Pack library inventory
- Team feedback summary
- Incident log (if any)
```

---

## 🎯 **Post-Pilot: Production Rollout Plan**

### **If Pilot Succeeds**
1. **Week 13-14**: Expand to full NetOps team
2. **Week 15-16**: Integrate ServiceNow API
3. **Week 17-18**: Set up Notion knowledge base
4. **Week 19-20**: Deploy cloud runners (Railway/Heroku)
5. **Month 6+**: Expand to other teams (Security, SRE)

### **If Pilot Needs Adjustment**
1. Identify gaps
2. Extend pilot 30 days
3. Address specific issues
4. Re-evaluate

---

## 📞 **Pilot Support**

### **Getting Help During Pilot**

**For Pack Development Questions**:
- Ask Augment: "How do I create a pack for X?"
- Check: `docs/pack-development.md`
- Linear: Create issue with `question` label
- Champions: Office hours (weekly)

**For Integration Issues**:
- GitHub Actions failing: Check `.github/workflows/`
- Linear not updating: Check GitHub integration settings
- CMDB issues: Check `cmdb/README.md`

**For Governance Questions**:
- Review: `AUGMENT_CONTROL_CONTRACT.md`
- Review: `policy/EXECUTION_GATING_POLICY.json`
- Escalate to: Pilot Lead

---

**🚀 Ready to start the pilot!**

**Next Action**: Schedule Week 1 kickoff meeting and send calendar invites.


