# NetOpsForge Recipes

Recipes are runbooks that combine multiple automation packs into workflows for common operational tasks.

## 📖 What is a Recipe?

A recipe is a multi-step automation workflow that:
- Orchestrates multiple packs in sequence
- Handles dependencies between steps
- Aggregates results across steps
- Generates comprehensive reports
- Integrates with Linear for tracking

Think of recipes as **runbooks-as-code**.

## 🏗️ Recipe Structure

```yaml
metadata:
  name: recipe-name
  description: "What this recipe does"
  operation_type: read  # or write
  requires_ticket: false

steps:
  - step: 1
    name: "Step name"
    pack: pack-to-run
    targets:
      cmdb_query: {...}
    on_failure: continue  # or stop

reporting:
  generate_summary: true
  output_file: "./reports/report-{timestamp}.md"
```

## 📚 Available Recipes

| Recipe Name | Description | Type | Duration |
|-------------|-------------|------|----------|
| `network-health-check` | Comprehensive network health check | READ | ~15 min |

## 🚀 Using a Recipe

### With Augment (Recommended)
```
Ask Augment: "Run the network health check recipe"
```

### With NetOpsForge CLI
```bash
netopsforge run recipe network-health-check
```

## 🛠️ Creating a New Recipe

1. **Identify the workflow**:
   - What operational task are you automating?
   - What steps are involved?
   - What packs do you need?

2. **Create the recipe file**:
   ```bash
   cp recipes/network-health-check.yml recipes/my-new-recipe.yml
   ```

3. **Define the steps**:
   - List packs in execution order
   - Define targets for each step
   - Configure error handling

4. **Test the recipe**:
   ```bash
   netopsforge run recipe my-new-recipe --dry-run
   ```

5. **Submit PR**:
   - Create feature branch
   - Commit your recipe
   - Reference Linear issue in PR

## 📋 Recipe Categories

- **monitoring**: Health checks and status verification
- **troubleshooting**: Diagnostic workflows
- **configuration**: Multi-device configuration changes
- **compliance**: Compliance validation workflows
- **reporting**: Data collection and reporting

## 🔒 Security Guidelines

### For READ Recipes:
- Set `operation_type: read`
- Set `requires_ticket: false`
- Use read-only credentials

### For WRITE Recipes:
- Set `operation_type: write`
- Set `requires_ticket: true`
- Require ServiceNow CHG ticket
- Include rollback steps
- Add approval gates

## 🎯 Best Practices

1. **Keep recipes focused**: One operational task per recipe
2. **Handle failures gracefully**: Use `on_failure: continue` for non-critical steps
3. **Generate reports**: Always include reporting section
4. **Document prerequisites**: List what's needed before running
5. **Include examples**: Show how to use the recipe
6. **Integrate with Linear**: Track execution and issues

## 📊 Reporting

Recipes can generate comprehensive reports:

```yaml
reporting:
  generate_summary: true
  summary_format: markdown
  summary_sections:
    - section: "Results"
      include:
        - metric1
        - metric2
  output_file: "./reports/report-{timestamp}.md"
```

## 🔗 Linear Integration

Recipes automatically integrate with Linear:

```yaml
linear_integration:
  track_execution: true
  create_issue_on_error: true
  issue_project: "Network Operations"
  issue_labels:
    - automation
    - recipe-name
```

## ⏰ Scheduling

Recipes can be scheduled to run automatically:

```yaml
schedule:
  enabled: true
  cron: "0 */6 * * *"  # Every 6 hours
  timezone: "America/New_York"
```

## 🧪 Testing Recipes

Before submitting a recipe:

1. **Dry run**: `netopsforge run recipe my-recipe --dry-run`
2. **Test mode**: Run against test devices first
3. **Validate output**: Check generated reports
4. **Error scenarios**: Test failure handling

## 🤝 Contributing

Recipe contributions are encouraged! See [CONTRIBUTING.md](../docs/CONTRIBUTING.md).

## 💡 Recipe Ideas

- Pre-change validation
- Post-change verification
- Incident response workflows
- Capacity planning data collection
- Security compliance checks
- Configuration backup workflows

