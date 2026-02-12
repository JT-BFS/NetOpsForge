# NetOpsForge 🔧

**Network Operations Automation Platform**

NetOpsForge is a governance-first automation platform for enterprise network operations. It combines AI-powered reasoning (via Augment) with safe, auditable execution of network automation tasks.

## 🎯 Philosophy

- **Observe First**: Always check before changing
- **Governance Built-In**: ServiceNow integration, change control, audit trails
- **Reusable Automation**: Build once, use everywhere
- **Knowledge Growth**: Every automation becomes shared knowledge via PRs

## 🏗️ Architecture

```
┌─────────────┐
│   Augment   │  ← Reasoning & Planning (You are here)
│  (Copilot)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│        NetOpsForge Platform         │
│  ┌─────────┐  ┌─────────┐          │
│  │  Packs  │  │ Recipes │          │
│  └─────────┘  └─────────┘          │
│  ┌─────────┐  ┌─────────┐          │
│  │  CMDB   │  │ Runners │          │
│  └─────────┘  └─────────┘          │
└──────────┬──────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │   Network    │
    │   Devices    │
    └──────────────┘
```

## 📁 Repository Structure

```
NetOpsForge/
├── packs/              # Reusable automation packs (YAML)
├── recipes/            # Runbooks combining multiple packs
├── cmdb/               # Device inventory and credentials
├── docs/               # Documentation and guides
├── policy/             # Execution policies and governance
└── .github/            # GitHub Actions and templates
```

## 🚀 Quick Start

### For Network Engineers

1. **Browse available packs**: Check `packs/` directory
2. **Find a recipe**: Check `recipes/` for common tasks
3. **Ask Augment**: "Show me how to check VLAN status on core switches"

### For Automation Developers

1. **Create a new pack**: See `docs/pack-development.md`
2. **Test in observe mode**: Always test read-only first
3. **Submit PR**: Share your automation with the team

## 🔒 Safety Model

### READ Operations (Allowed)
- `show` commands
- Health checks
- Status queries
- Log retrieval

### WRITE Operations (Requires)
- ✅ Valid ServiceNow ticket (CHG/RITM)
- ✅ Engineer types "YES"
- ✅ Target tagged `allow_execute` in CMDB

## 🔗 Integrations

- **Linear**: Task tracking and workflow automation
- **GitHub**: Version control and CI/CD
- **ServiceNow**: Change management (planned)
- **Notion**: Documentation and knowledge base (planned)

## 📚 Documentation

- [Pack Development Guide](docs/pack-development.md)
- [Recipe Creation Guide](docs/recipe-creation.md)
- [CMDB Setup](docs/cmdb-setup.md)
- [Augment Operator Runbook](RUNBOOK_AUGMENT_OPERATOR.md)

## 🤝 Contributing

All automation artifacts are shared knowledge. To contribute:

1. Create a feature branch
2. Develop your pack/recipe
3. Test thoroughly in observe mode
4. Submit PR with proper documentation
5. Get peer review
6. Merge to main

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## 📋 License

Internal use only - [Your Organization]

---

**Built with ❤️ by the Network Operations Team**

