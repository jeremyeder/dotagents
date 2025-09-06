# PyTorch TAC Voting Advisor

Strategic advisor agent for Jeremy Eder's PyTorch Technical Advisory Committee voting decisions.

## Overview

This agent provides research-backed decision support for PyTorch ecosystem votes, generating executive summaries that consider:

- **Competition analysis** - Market position and competitive landscape
- **Portfolio overlap** - Alignment with Red Hat/IBM AI portfolio
- **Project health** - GitHub metrics and sustainability indicators
- **Strategic alignment** - Red Hat and IBM strategic fit
- **Risk assessment** - Technical and business risks

## Features

- **Automated GitHub Analysis** - Repository health scoring based on activity, contributors, and maintenance indicators
- **Competition Mapping** - Identifies competitive landscape and market positioning
- **Portfolio Impact Assessment** - Analyzes overlap with Red Hat OpenShift AI and IBM Watson ecosystems
- **Strategic Recommendations** - APPROVE/REJECT/ABSTAIN with confidence levels
- **Executive Summaries** - 1-page markdown reports optimized for TAC voting decisions
- **IBM Research Integration** - Consultation notes for Raghu Ganti collaboration

## Usage

### Basic Analysis
```bash
python agents/pytorch_tac_advisor.py "Project Name" "https://github.com/owner/repo"
```

### With Description and Context
```bash
python agents/pytorch_tac_advisor.py "ML Inference Engine" "https://github.com/example/engine" \
  --description "Fast PyTorch model serving for production" \
  --context "Vote deadline: 2025-01-15"
```

### With GitHub Token (for higher API limits)
```bash
export GITHUB_TOKEN="your_github_token"
python agents/pytorch_tac_advisor.py "Project Name" "https://github.com/owner/repo"
```

## Installation

```bash
pip install -r requirements.txt
```

## Output

The agent generates:

1. **Console Display** - Rich formatted analysis with recommendation tables
2. **Markdown Report** - Executive summary saved to `./analysis/` directory
3. **Strategic Assessments** - Red Hat and IBM alignment analysis
4. **Consultation Notes** - Discussion points for Raghu Ganti (IBM Research)

## Example Output Structure

```markdown
# PyTorch TAC Voting Recommendation: Project Name

## Executive Summary
**Recommendation**: APPROVE
**Project Health Score**: 85.2/100
**Strategic Alignment**: Favorable

## Key Assessment
[Strategic analysis with competition and portfolio impact]

## Risk Profile
[Technical and business risk assessment]

## Strategic Context
[Red Hat/IBM alignment and ecosystem impact]
```

## Jeremy's TAC Context

- **Role**: PyTorch TAC Member representing IBM/Red Hat
- **Collaboration**: Works with Raghu Ganti (IBM Research) who holds the official voting seat
- **Focus Areas**: OpenShift AI integration, enterprise PyTorch adoption, ecosystem health
- **Decision Timeline**: 7-day voting windows require rapid analysis and consultation

## Architecture

- **GitHubAnalyzer** - Repository health metrics and API integration
- **PyTorchEcosystemAnalyzer** - Competition and portfolio analysis
- **PyTorchTACAdvisor** - Main orchestration and recommendation generation
- **Rich Console Output** - Formatted display with tables and panels
- **Markdown Export** - Executive summary generation

## Configuration

Set `GITHUB_TOKEN` environment variable for enhanced API access:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

This increases GitHub API rate limits from 60 to 5000 requests per hour.