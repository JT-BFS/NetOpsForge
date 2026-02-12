# NetOpsForge Integrations

NetOpsForge integrates with multiple platforms to provide a complete automation ecosystem.

## 🔗 Current Integrations

### ✅ Linear (Active)

**Purpose**: Task tracking and workflow automation

**Features**:
- Track automation development work
- Auto-create issues on pack/recipe errors
- Link GitHub PRs to Linear issues
- Workflow automation (PR status → Linear status)

**Setup**:
1. Linear workspace created
2. GitHub integration enabled
3. Workflow configured:
   - PR open → Issue "In Progress"
   - PR review → Issue "In Review"
   - PR merged → Issue "Done"

**Usage in Packs**:
```yaml
linear_integration:
  auto_create_issue_on_error: true
  issue_labels:
    - network-automation
    - pack-name
  issue_priority: medium
```

**Usage in Recipes**:
```yaml
linear_integration:
  track_execution: true
  create_issue_on_error: true
  issue_project: "Network Operations"
```

**Linear Project Structure**:
- **Network Automation Packs**: Track pack development
- **Runbook Library**: Track recipe creation
- **Infrastructure**: Platform improvements

**Linear Labels**:
- `pack`: New automation pack
- `recipe`: New recipe/runbook
- `bug`: Fix for existing automation
- `documentation`: Docs only
- `security`: Security-related changes

---

### ✅ GitHub (Active)

**Purpose**: Version control and CI/CD

**Features**:
- Version control for all automation artifacts
- Automated validation via GitHub Actions
- Pull request workflow
- Branch protection rules

**GitHub Actions Workflows**:

1. **validate-packs.yml**:
   - YAML syntax validation
   - Secret scanning
   - Pack structure validation
   - Security scanning

2. **label-prs.yml**:
   - Auto-label PRs based on files changed
   - Size labels (xs, s, m, l, xl)
   - Type labels (pack, recipe, cmdb, docs)

**Branch Protection** (Recommended Setup):
```
Branch: main
✅ Require pull request reviews (1 approval)
✅ Require status checks to pass
✅ Require conversation resolution
✅ Do not allow bypassing
```

**PR Template**:
- Located at `.github/pull_request_template.md`
- Includes checklist for automation artifacts
- Links to Linear issues
- References ServiceNow tickets

---

### 🔄 ServiceNow (Planned)

**Purpose**: Change management and CMDB sync

**Planned Features**:
- Automatic CHG ticket validation
- CMDB device sync
- Incident tracking integration
- Change approval workflow

**Future Pack Integration**:
```yaml
servicenow_integration:
  require_ticket: true
  ticket_types:
    - CHG
    - RITM
  auto_update_ticket: true
  attach_output: true
```

**Implementation Timeline**: Q2 2026

**Prerequisites**:
- ServiceNow API access
- OAuth credentials
- CMDB read/write permissions

---

### 📝 Notion (Planned)

**Purpose**: Documentation and knowledge base

**Planned Features**:
- Centralized documentation
- Runbook library
- Team onboarding materials
- Architecture diagrams
- Post-mortem templates

**Planned Structure**:
```
NetOpsForge Workspace/
├── 📚 Documentation
│   ├── Getting Started
│   ├── Pack Development
│   └── Best Practices
├── 📖 Runbooks
│   ├── Common Procedures
│   └── Troubleshooting Guides
├── 🏗️ Architecture
│   ├── Network Diagrams
│   └── System Design
└── 📊 Reports
    ├── Automation Metrics
    └── Incident Reviews
```

**Implementation Timeline**: Q3 2026

---

### 🎭 Playwright (Planned)

**Purpose**: Web UI automation for devices without APIs

**Use Cases**:
- Legacy devices without CLI/API access
- Web-only management interfaces
- GUI-based configuration tasks

**Example Pack**:
```yaml
metadata:
  name: legacy-firewall-backup
  execution_method: playwright

playwright_config:
  browser: chromium
  headless: true
  
steps:
  - action: navigate
    url: "https://firewall.example.com"
  - action: login
    credential_ref: firewall_admin
  - action: click
    selector: "#backup-button"
  - action: download
    path: "./backups/firewall-{timestamp}.cfg"
```

**Implementation Timeline**: Q4 2026

---

### 🧠 Context7 (Planned)

**Purpose**: Enhanced context awareness for Augment

**Features**:
- Deep codebase understanding
- Historical change analysis
- Pattern recognition
- Intelligent suggestions

**Use Cases**:
- "How did we handle similar issues before?"
- "What packs exist for this vendor?"
- "Show me related automation"

**Implementation Timeline**: Q3 2026

---

### 🤔 Sequential Thinking (Planned)

**Purpose**: Advanced reasoning for complex automation

**Features**:
- Multi-step problem decomposition
- Dependency analysis
- Risk assessment
- Rollback planning

**Use Cases**:
- Complex configuration changes
- Multi-device orchestration
- Failure scenario planning

**Implementation Timeline**: Q4 2026

---

### 💾 Convex (Planned)

**Purpose**: Real-time data synchronization

**Features**:
- Real-time automation state
- Live execution monitoring
- Collaborative debugging
- Event streaming

**Use Cases**:
- Live automation dashboards
- Team collaboration on incidents
- Real-time status updates

**Implementation Timeline**: 2027

---

### 🚂 Railway / Heroku (Planned)

**Purpose**: Cloud deployment for NetOpsForge runners

**Features**:
- Scalable runner deployment
- Geographic distribution
- High availability
- Auto-scaling

**Architecture**:
```
┌─────────────┐
│   Augment   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Railway/Heroku     │
│  ┌───────────────┐  │
│  │ Runner Pool   │  │
│  │ - Runner 1    │  │
│  │ - Runner 2    │  │
│  │ - Runner N    │  │
│  └───────────────┘  │
└──────────┬──────────┘
           │
           ▼
    Network Devices
```

**Implementation Timeline**: 2027

---

## 🎯 Integration Roadmap

| Quarter | Integration | Status |
|---------|-------------|--------|
| Q1 2026 | Linear | ✅ Active |
| Q1 2026 | GitHub | ✅ Active |
| Q2 2026 | ServiceNow | 🔄 Planned |
| Q3 2026 | Notion | 🔄 Planned |
| Q3 2026 | Context7 | 🔄 Planned |
| Q4 2026 | Playwright | 🔄 Planned |
| Q4 2026 | Sequential Thinking | 🔄 Planned |
| 2027 | Convex | 🔄 Planned |
| 2027 | Railway/Heroku | 🔄 Planned |

---

## 🔧 Configuration Files

Integration configurations are stored in:
- `policy/EXECUTION_GATING_POLICY.json`: Execution policies
- `.github/workflows/`: GitHub Actions
- `docs/integrations.md`: This file

---

## 📚 Additional Resources

- [Linear Workflow Setup](https://linear.app/docs/github)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [ServiceNow API Reference](https://developer.servicenow.com/)

