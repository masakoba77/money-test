# GitHub Setup Guide

## Repository Configuration

This guide walks you through setting up the GitHub repository with recommended security and workflow settings.

## Prerequisites

- GitHub repository created
- Administrator access to the repository
- GitHub CLI (optional, for automation)

## Initial Setup Checklist

### 1. Repository Settings

1. Go to: **Settings → General**

**Basic Information:**
- [ ] Repository name: `money-test-java`
- [ ] Description: "Stock Trading Simulator with Moving Average Crossover Strategy"
- [ ] Make repository Public/Private (as preferred)

**Features:**
- [ ] Discussions: ✅ (optional)
- [ ] Wiki: ✅ (optional)
- [ ] Projects: ✅
- [ ] Security and analysis: ✅

### 2. Branch Protection Rules

1. Go to: **Settings → Branches**
2. Click **Add rule** for `main` branch

**Settings:**
- [ ] Require a pull request before merging: ✅
- [ ] Require approvals: 1
- [ ] Dismiss stale pull request approvals when new commits are pushed: ✅
- [ ] Require review from code owners: ✅ (if CODEOWNERS file exists)
- [ ] Require status checks to pass before merging: ✅
  - [ ] Require branches to be up to date before merging: ✅
  - [ ] Require code quality checks: ✅
- [ ] Require signed commits: ✅ (optional)
- [ ] Allow auto-merge: ✅ (optional)
- [ ] Allow deletions: ❌
- [ ] Allow force pushes: ❌
- [ ] Lock branch: ❌

### 3. Collaborators and Teams

1. Go to: **Settings → Collaborators and teams**

**Add Collaborators:**
- Assign members with appropriate roles (Pull Request Reviewer, Maintain, etc.)

### 4. Secrets and Variables

1. Go to: **Settings → Secrets and variables → Actions**

**Environment Secrets:**
- Optional: `DOCKER_REGISTRY_USERNAME` (for Docker Hub)
- Optional: `DOCKER_REGISTRY_PASSWORD` (for Docker Hub)
- Optional: `AWS_ACCESS_KEY_ID` (for AWS deployment)
- Optional: `AWS_SECRET_ACCESS_KEY` (for AWS deployment)

**Repository Variables:**
- Optional: `REGISTRY_URL` (Docker registry URL)
- Optional: `REGISTRY_NAMESPACE` (Docker namespace)

### 5. Environments

1. Go to: **Settings → Environments**

**Create environments (optional):**

**Staging:**
- Name: `staging`
- Reviewers: (leave empty or assign reviewers)
- Deployment branches: `main`

**Production:**
- Name: `production`
- Reviewers: (assign key reviewers)
- Deployment branches: `main`

### 6. Notifications

1. Go to: **Settings → Notifications → Default notifications**

**Email settings:**
- [ ] Receive notifications for:
  - Pull requests: ✅
  - Issues: ✅
  - Discussions: ✅
  - Actions: ✅

### 7. Security Settings

1. Go to: **Settings → Security and analysis**

**Recommended:**
- [ ] Dependency graph: ✅ (auto-enabled)
- [ ] Dependabot alerts: ✅
- [ ] Dependabot security updates: ✅
- [ ] Code scanning: ✅ (set up workflow)
- [ ] Secret scanning: ✅ (if private)

### 8. Code Owners (Optional)

1. Create `.github/CODEOWNERS` file:

```
# Default owner
* @masakoba77

# Specific directories
/src/ @masakoba77
/frontend/ @masakoba77
/.github/ @masakoba77
```

2. Commit and push

### 9. GitHub Actions Permissions

1. Go to: **Settings → Actions → General**

**Permissions:**
- [ ] Actions permissions: Allow all actions and reusable workflows
- [ ] Workflow permissions: Read and write permissions
- [ ] Allow GitHub Actions to create and approve pull requests: ✅ (optional)

## Workflow Configuration

### 1. Enable Required Workflows

Workflows are automatically enabled when files are in `.github/workflows/`.

Verify at: **Actions → Workflows** (should show ci-cd, pr-checks, deploy)

### 2. Status Check Configuration

1. Go to: **Settings → Branches → Branch protection for main**
2. Under "Status checks that must pass":
   - [ ] `build-and-test`
   - [ ] `security-scan`

### 3. PR Templates

The repository includes:
- `.github/pull_request_template.md` - PR template
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template

These automatically appear when creating PRs/issues.

## Deployment Configuration

### 1. GitHub Pages (Optional)

1. Go to: **Settings → Pages**
- [ ] Source: Deploy from a branch
- [ ] Branch: `main`
- [ ] Folder: `/docs` (if documentation exists)

### 2. Releases

1. Go to: **Releases**
2. Releases are automatically created by deploy workflow on version tags

Manual release:
1. Click **Draft a new release**
2. Tag version: `v1.0.0`
3. Add release notes
4. Click **Publish release**

## Gitflow Workflow

### Branch Strategy

```
main                    (production-ready)
├── release/v1.0.0     (release branch)
└── develop            (development branch)
    ├── feature/new-strategy
    ├── bugfix/issue-123
    └── hotfix/critical-bug
```

### Creating Feature Branches

1. Create from `develop`:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "Add new feature"
```

3. Push and create PR:
```bash
git push origin feature/feature-name
```

4. Create PR to `develop` (then merge to `main` for releases)

## Common Tasks

### Creating a Release

1. Create version tag:
```bash
git tag v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. GitHub Actions automatically:
   - Creates release page
   - Builds Docker images
   - Uploads artifacts

### Viewing Workflow Runs

1. Go to: **Actions**
2. Select workflow (ci-cd, pr-checks, deploy)
3. Click run to see details

### Enabling/Disabling Workflows

Workflows are enabled by default. To disable:
1. Go to: **Actions → [Workflow]**
2. Click **...** → **Disable workflow**

### Debugging Failed Workflows

1. Click on failed run
2. Click on failed job
3. Expand step logs to see error messages
4. Fix issues and push new commits

## Security Best Practices

1. **Keep secrets safe:**
   - Never commit secrets to repository
   - Use GitHub Secrets for sensitive data
   - Rotate secrets regularly

2. **Review PRs carefully:**
   - Check code changes thoroughly
   - Verify CI/CD passes
   - Require at least 1 approval

3. **Monitor dependencies:**
   - Enable Dependabot alerts
   - Review security updates
   - Keep Python and packages updated

4. **Signed commits (optional):**
   - Enable GPG signing
   - Verify commit signatures
   - Require signed commits for main

5. **Audit log:**
   - Review repository audit log
   - Monitor access and changes
   - Set up alerts for suspicious activity

## Troubleshooting

### Workflow Not Running

1. Check `.github/workflows/` directory exists
2. Verify workflow YAML syntax
3. Check branch matches trigger conditions
4. Go to **Actions → [Workflow] → Run workflow** (manual trigger)

### PR Can't Merge

1. Check status checks pass
2. Check branch protection rules
3. Ensure base branch is up to date
4. Verify reviews approved

### Secrets Not Available

1. Verify secret exists in **Settings → Secrets**
2. Check workflow references correct secret name
3. Ensure repository has access to secret

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Security Documentation](https://docs.github.com/en/code-security)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub CLI Documentation](https://cli.github.com/)

## Support

For issues with GitHub setup, see the [GitHub Help Documentation](https://docs.github.com/) or create an issue in the repository.
