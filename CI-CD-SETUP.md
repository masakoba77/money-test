# CI/CD Setup Guide

## Overview

This project uses GitHub Actions for continuous integration, testing, and deployment. The CI/CD pipeline automatically:

1. Runs tests on every push and pull request
2. Performs security scanning
3. Builds Docker images
4. Creates releases on version tags

## Workflows

### 1. CI/CD Pipeline (ci-cd.yml)

Runs on every push to `main` and pull requests.

**Jobs:**
- **build-and-test**: Python setup, dependency installation, linting, testing
- **security-scan**: Bandit and Safety security scanning
- **deploy**: Docker image building for main branch

**Triggers:**
```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

### 2. PR Checks (pr-checks.yml)

Validates pull requests with syntax checks and imports.

**Jobs:**
- Syntax validation
- Python code quality checks
- API and simulator import verification

**Triggers:**
```yaml
on:
  pull_request:
    branches:
      - main
```

### 3. Deploy Workflow (deploy.yml)

Creates releases and builds Docker images on version tags.

**Jobs:**
- Release creation on tag push
- Docker image building with version tags

**Triggers:**
```yaml
on:
  push:
    tags:
      - 'v*'
```

## Running Workflows Locally

### Using Act (GitHub Actions emulator)

1. Install act:
```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

# Windows (Chocolatey)
choco install act
```

2. Run a workflow:
```bash
# Run a specific workflow
act -j build-and-test

# Run all workflows
act
```

### Manual Testing

1. Python linting:
```bash
pip install flake8
flake8 src --select=E9,F63,F7,F82
```

2. Python tests:
```bash
pip install pytest pytest-cov
pytest src/tests/ -v --cov=src
```

3. Docker build:
```bash
docker build -t stock-simulator-python .
```

4. Docker test:
```bash
docker run -d -p 8000:8000 stock-simulator-python
curl http://localhost:8000/api/health
docker stop <container-id>
```

## GitHub Secrets

No secrets are currently required for basic CI/CD. Optional secrets for enhanced functionality:

1. Go to: **Settings → Secrets and variables → Actions**
2. Add secrets as needed:
   - `DOCKER_REGISTRY_USERNAME`: For Docker registry authentication
   - `DOCKER_REGISTRY_PASSWORD`: For Docker registry authentication

## Environment Variables

Configure environment variables in workflow files:

```yaml
env:
  PYTHONUNBUFFERED: 1
  DOCKER_BUILDKIT: 1
```

## Branch Protection Rules

Recommended settings for `main` branch:

1. Require pull request reviews before merging
2. Require status checks to pass before merging
3. Require branches to be up to date before merging
4. Enforce rules for administrators

### Setup:
1. Go to: **Settings → Branches → Branch Protection Rules**
2. Add rule for `main`:
   - Require pull request reviews: ✅
   - Require status checks: ✅ (ci-cd/build-and-test, ci-cd/security-scan)

## Release Process

### Creating a Release

1. Create a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. The deploy workflow automatically:
   - Creates a GitHub release
   - Builds Docker images with version tag
   - Tags images as `latest`

### Manual Release Creation

1. Go to: **Releases → Draft new release**
2. Tag version: `v1.0.0`
3. Release title and description
4. Click "Publish release"

## Troubleshooting

### Workflow Fails

1. Check workflow run logs:
   - Go to: **Actions → [Workflow Name] → [Run] → View logs**

2. Common issues:
   - Python version mismatch: Verify `python-version` in workflow
   - Missing dependencies: Update `requirements.txt`
   - Port conflicts: Ensure port 8000 is available

### Docker Build Failures

1. Verify Dockerfile:
```bash
docker build -t test .
```

2. Check Docker build output:
```bash
docker build --progress=plain -t test .
```

3. Common issues:
   - Missing files in COPY command
   - Missing dependencies in requirements.txt
   - Python version compatibility

### Test Failures

1. Run locally:
```bash
pytest src/tests/ -v
```

2. Check test output for:
   - Import errors
   - Missing modules
   - Test assertions

## GitHub Actions Tips

### Skip Workflow Execution

Add `[skip ci]` to commit message:
```bash
git commit -m "Minor update [skip ci]"
```

### Manual Workflow Dispatch

Trigger workflow manually (requires setup):
```yaml
on:
  workflow_dispatch:
```

Then use: **Actions → [Workflow] → Run workflow**

### View Workflow Artifacts

After workflow completion:
1. Go to: **Actions → [Run] → Artifacts**
2. Download test reports, coverage reports, etc.

## Performance Optimization

### Caching Dependencies

Add to workflow:
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Parallel Jobs

Jobs run in parallel by default. Use `needs:` to specify dependencies:
```yaml
deploy:
  needs: [build-and-test, security-scan]
```

## Further Reading

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Python Testing with pytest](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
