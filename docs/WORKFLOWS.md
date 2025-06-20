# Workflow Documentation

This document describes the GitHub Actions workflows used in the GOV.UK Statistics Counter project.

## Overview

The project uses two main workflows:
1. **CronJob Workflow** - Automated weekly data collection
2. **Test Workflow** - CI/CD testing pipeline

## CronJob Workflow

**File**: `.github/workflows/cronjob.yml`

### Purpose
Automatically collects statistics count from GOV.UK every Monday and commits the data to the repository.

### Schedule
- **Frequency**: Weekly
- **Time**: Every Monday at 13:00 UTC
- **Cron Expression**: `"0 13 * * 1"`

### Process
1. **Checkout**: Uses `actions/checkout@v4`
2. **Build & Run**: 
   - Builds Docker container with `docker compose up --build`
   - Container scrapes GOV.UK and writes data to `data/govuk_stats_log.json`
3. **Commit**: Uses `EndBug/add-and-commit@v9` to commit new data
4. **Cleanup**: Stops and removes containers

### Recent Fixes (June 2025)
- ✅ Updated to `actions/checkout@v4` (from deprecated v3)
- ✅ Changed `docker-compose` to `docker compose` (modern syntax)
- ✅ Fixed Python script path in container
- ✅ Working since fixes applied

## Test Workflow

**File**: `.github/workflows/test.yml`

### Purpose
Validates code quality and ensures the application works correctly on every push and pull request.

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` branch

### Jobs

#### Test Job
Runs on: `ubuntu-latest`
Timeout: 10 minutes

**Steps**:

1. **Checkout** (`actions/checkout@v4`)
   - Checks out the repository code

2. **Set up Python 3.12** (`actions/setup-python@v5`)
   - Installs Python 3.12 runtime

3. **Install uv** (`astral-sh/setup-uv@v3`)
   - Installs the uv package manager

4. **Install dependencies**
   ```bash
   uv sync
   ```
   - Installs project dependencies using uv

5. **Run syntax check**
   ```bash
   uv run python -m py_compile src/get_count.py src/write_json_log.py
   ```
   - Validates Python syntax for all source files

6. **Test Docker build**
   ```bash
   docker build -t govuk-stats-counter-test .
   ```
   - Ensures Docker container builds successfully

7. **Test Docker run**
   ```bash
   mkdir -p test_data
   docker run -v $(pwd)/test_data:/data -e LOGFILE=/data/test_log.json govuk-stats-counter-test
   ```
   - Runs container and validates it can execute the scraping script

8. **Verify output**
   - Checks that the container created the expected log file
   - Displays file contents for verification

### Test Coverage

The test workflow validates:
- ✅ **Code Quality**: Python syntax validation
- ✅ **Dependencies**: uv can resolve and install packages
- ✅ **Docker Build**: Container builds without errors
- ✅ **Runtime**: Container executes and produces output
- ✅ **Integration**: Full end-to-end functionality

## Monitoring & Debugging

### Checking Workflow Status

```bash
# List recent workflow runs
gh run list --limit 10

# View specific run details
gh run view <run-id>

# View logs for failed runs
gh run view <run-id> --log-failed
```

### Common Issues & Solutions

1. **Docker Build Failures**
   - Check if `uv.lock` is included in `.dockerignore` exceptions
   - Verify Dockerfile has proper `ENTRYPOINT` and `CMD`

2. **Scraping Failures**
   - GOV.UK page structure may have changed
   - Check if fallback methods in `get_count.py` need updates

3. **Permission Errors**
   - Ensure GitHub token has sufficient permissions
   - Check repository settings for Actions permissions

## Security Considerations

- No secrets are stored in workflows
- GitHub token is automatically provided by Actions
- Container runs with minimal permissions
- Data files are committed using standard Git operations

## Performance

- **CronJob Workflow**: ~30-60 seconds (including Docker build)
- **Test Workflow**: ~45 seconds (including all validation steps)
- **Resource Usage**: Minimal - uses standard GitHub Actions runners

---

*For more information about GitHub Actions, see the [official documentation](https://docs.github.com/en/actions).*