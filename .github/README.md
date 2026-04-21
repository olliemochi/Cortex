# GitHub Configuration

This directory contains GitHub-specific configuration files for the Cortex project.

## Files

### CODEOWNERS
- **Source**: Merged from OpenClaw
- **Purpose**: Defines code ownership and automatic review assignments
- **Usage**: GitHub automatically requests reviews from these owners on relevant PRs

### pull_request_template.md
- **Source**: Merged from OpenClaw
- **Purpose**: Default template for creating pull requests
- **Usage**: Auto-populated when creating new PRs to ensure consistent quality

### FUNDING.yml
- **Source**: Merged from Open WebUI
- **Purpose**: GitHub sponsorship configuration
- **Usage**: Displays sponsorship options on the repository page

### dependabot.yml
- **Source**: Merged from both OpenClaw and Open WebUI
- **Purpose**: Dependency update automation configuration
- **Ecosystems**: 
  - npm (frontend dependencies)
  - pip/uv (backend dependencies)
- **Schedule**: Daily for npm, monthly for Python
- **Features**: Grouped updates, production/development separation

## Directories

### ISSUE_TEMPLATE/
- **Source**: Merged from OpenClaw
- **Purpose**: Templates for creating issues
- **Files**: Feature requests, bug reports, etc.

### workflows/
- **Source**: Merged from OpenClaw
- **Purpose**: GitHub Actions automation workflows
- **Examples**: CI/CD, testing, deployment triggers

## Merging Strategy

This directory was created by merging configurations from:
1. **OpenClaw** (.github/) - Primary source for workflows, issue templates, and review settings
2. **Open WebUI** (.github/) - Supplementary for funding and dependency management

The merged configuration ensures:
- ✅ Consistent PR standards
- ✅ Automated dependency updates across all ecosystems
- ✅ Clear code ownership
- ✅ Sponsorship visibility

## Customization

To customize for Cortex-specific needs:

1. **Update CODEOWNERS** - Add Cortex maintainers
2. **Modify dependabot.yml** - Adjust schedules or ecosystems
3. **Create custom workflows** - Add Cortex-specific CI/CD
4. **Update PR template** - Add Cortex-specific sections

---

**Last Updated**: April 20, 2026  
**Status**: Production Ready
