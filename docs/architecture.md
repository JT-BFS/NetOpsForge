# NetOpsForge Architecture

## 🏗️ System Overview

NetOpsForge is a governance-first network automation platform that separates reasoning from execution.

```
┌─────────────────────────────────────────────────────────┐
│                    REASONING LAYER                       │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         Augment (Claude Sonnet 4.5)            │    │
│  │  - Understands intent                          │    │
│  │  - Plans automation                            │    │
│  │  - Generates packs/recipes                     │    │
│  │  - Validates safety                            │    │
│  └────────────────────────────────────────────────┘    │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   GOVERNANCE LAYER                       │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         Execution Gating Policy                │    │
│  │  - READ: Allowed with awareness                │    │
│  │  - WRITE: Requires ticket + YES + tag          │    │
│  └────────────────────────────────────────────────┘    │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   EXECUTION LAYER                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    Packs     │  │   Recipes    │  │     CMDB     │ │
│  │  (YAML)      │  │  (Workflows) │  │  (Inventory) │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                          │                              │
│  ┌────────────────────────────────────────────────┐    │
│  │         NetOpsForge Runners (Future)           │    │
│  │  - Execute packs                               │    │
│  │  - Parse output                                │    │
│  │  - Generate reports                            │    │
│  └────────────────────────────────────────────────┘    │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  NETWORK INFRASTRUCTURE                  │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Routers  │  │ Switches │  │ Firewalls│             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

## 🧩 Components

### 1. Augment (Reasoning Brain)

**Role**: Understand intent, plan automation, ensure safety

**Capabilities**:
- Natural language understanding
- Automation planning
- Pack/recipe generation
- Safety validation
- Error analysis

**Does NOT**:
- Directly access network devices
- Execute commands without governance
- Store credentials
- Bypass policies

### 2. Governance Layer

**Components**:
- `policy/EXECUTION_GATING_POLICY.json`: Execution rules
- `AUGMENT_CONTROL_CONTRACT.md`: Augment's operating rules
- `RUNBOOK_AUGMENT_OPERATOR.md`: Operator guidelines

**Rules**:
```json
{
  "observe_requires_ticket": false,
  "execute_requires": {
    "servicenow_ticket": true,
    "explicit_yes": true,
    "cmdb_target_tag": "allow_execute"
  }
}
```

### 3. Automation Artifacts

#### Packs (`packs/`)
- Single-purpose automation units
- YAML-defined
- Versioned
- Self-documenting

**Structure**:
```yaml
metadata: {...}
execution: {...}
targets: {...}
authentication: {...}
commands: [...]
output: {...}
validation: {...}
```

#### Recipes (`recipes/`)
- Multi-step workflows
- Orchestrate multiple packs
- Generate reports
- Handle dependencies

**Structure**:
```yaml
metadata: {...}
steps: [...]
reporting: {...}
notifications: {...}
```

#### CMDB (`cmdb/`)
- Device inventory
- Credential references
- Device groups
- Sites/locations

### 4. Version Control & CI/CD

**GitHub**:
- Version control for all artifacts
- Pull request workflow
- Automated validation
- Branch protection

**GitHub Actions**:
- YAML validation
- Secret scanning
- Pack structure validation
- Security scanning

### 5. Integrations

**Active**:
- ✅ Linear: Task tracking
- ✅ GitHub: Version control

**Planned**:
- 🔄 ServiceNow: Change management
- 🔄 Notion: Documentation
- 🔄 Playwright: Web automation
- 🔄 Context7: Enhanced context
- 🔄 Sequential Thinking: Advanced reasoning
- 🔄 Convex: Real-time sync
- 🔄 Railway/Heroku: Cloud runners

## 🔄 Execution Flow

### READ Operation Flow

```
1. Engineer: "Check interface status on core-rtr-01"
   ↓
2. Augment: Understands intent
   ↓
3. Augment: Finds pack "cisco-interface-status"
   ↓
4. Augment: Checks policy → READ operation → Allowed
   ↓
5. Augment: Informs engineer what will be executed
   ↓
6. Runner: Executes pack (future)
   ↓
7. Augment: Shows results to engineer
```

### WRITE Operation Flow

```
1. Engineer: "Add VLAN 100 to dist-sw-01"
   ↓
2. Augment: Understands intent
   ↓
3. Augment: Identifies as WRITE operation
   ↓
4. Augment: Checks policy requirements:
   - ServiceNow ticket? ❌
   - Explicit YES? ❌
   - Target tagged allow_execute? ❓
   ↓
5. Augment: "This is a WRITE operation. Please provide:
             - ServiceNow CHG ticket
             - Type YES to confirm"
   ↓
6. Engineer: "CHG0012345" + "YES"
   ↓
7. Augment: Validates all requirements ✅
   ↓
8. Runner: Executes pack (future)
   ↓
9. Augment: Shows results + updates ticket
```

## 🗂️ Directory Structure

```
NetOpsForge/
├── .github/
│   ├── workflows/
│   │   ├── validate-packs.yml
│   │   └── label-prs.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── pack-request.md
│   │   └── bug-report.md
│   └── pull_request_template.md
├── packs/
│   ├── cisco-interface-status.yml
│   └── README.md
├── recipes/
│   ├── network-health-check.yml
│   └── README.md
├── cmdb/
│   ├── devices.yml
│   └── README.md
├── docs/
│   ├── getting-started.md
│   ├── pack-development.md
│   ├── CONTRIBUTING.md
│   ├── integrations.md
│   └── architecture.md (this file)
├── policy/
│   └── EXECUTION_GATING_POLICY.json
├── README.md
├── AUGMENT_CONTROL_CONTRACT.md
├── RUNBOOK_AUGMENT_OPERATOR.md
├── .gitignore
└── .yamllint
```

## 🔐 Security Architecture

### Credential Management

```
┌─────────────────────────────────────┐
│  NetOpsForge Packs/Recipes          │
│  (Only contain credential_ref)      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Windows Credential Manager         │
│  (Actual credentials stored here)   │
│  Target: NetOpsForge/cisco_readonly │
│  Username: netops_ro                │
│  Password: ••••••••                 │
└─────────────────────────────────────┘
```

**Principles**:
- Never hardcode credentials
- Use credential references only
- Store in Windows Credential Manager
- Audit all credential usage
- Rotate regularly

### Execution Safety

**Tags**:
- `allow_execute`: Required for WRITE operations
- `production`: Additional safety checks
- `critical`: Extra validation required

**Validation**:
- Pre-execution checks
- Dry-run capability
- Rollback planning
- Change windows

## 📊 Data Flow

### Pack Execution

```
Pack YAML → Runner → Device
    ↓
  Output
    ↓
  Parser (TextFSM/Regex)
    ↓
Structured Data (JSON/YAML)
    ↓
  Validation
    ↓
  Report Generation
    ↓
Linear Issue (if errors)
```

## 🚀 Future Architecture

### Cloud Runners (2027)

```
┌─────────────────────────────────────┐
│  Railway/Heroku                     │
│  ┌───────────────────────────────┐ │
│  │  Runner Pool                  │ │
│  │  - Auto-scaling               │ │
│  │  - Geographic distribution    │ │
│  │  - High availability          │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Real-time Sync (2027)

```
┌─────────────────────────────────────┐
│  Convex                             │
│  - Real-time state sync             │
│  - Live execution monitoring        │
│  - Collaborative debugging          │
└─────────────────────────────────────┘
```

## 📚 Design Principles

1. **Governance First**: Safety before speed
2. **Reusability**: Build once, use everywhere
3. **Transparency**: Audit everything
4. **Knowledge Sharing**: PRs for all automation
5. **Fail Safe**: Default to read-only
6. **Human in Loop**: Explicit approval for changes

---

For more details, see:
- [Getting Started](getting-started.md)
- [Pack Development](pack-development.md)
- [Integrations](integrations.md)

