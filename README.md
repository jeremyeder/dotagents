# dotagents

A collection of specialized strategic agents for technical decision support and competitive analysis.

## Overview

This repository contains AI agents designed to provide research-backed decision support for complex strategic scenarios. Each agent specializes in specific domains, offering automated analysis, competitive intelligence, and executive-level recommendations.

### Core Capabilities

- **Automated Research** - Systematic analysis of projects, markets, and competitive landscapes
- **Strategic Intelligence** - Executive summaries with actionable recommendations
- **Multi-Domain Support** - Specialized agents for different decision contexts
- **Integration Ready** - Modular architecture for easy deployment and customization

## Agent Portfolio

| Agent | Status | Analysis Type | Data Sources | Output Format | Decision Support | Time Sensitivity |
|-------|--------|---------------|--------------|---------------|------------------|------------------|
| PyTorch TAC Voting Advisor | ✅ Current | Governance | GitHub API, Project docs | Console + Markdown | APPROVE/REJECT/ABSTAIN | 7-day windows |
| Competitive Intelligence Analyzer | 🔄 Planned | Market Analysis | Web scraping, Patents | Markdown + JSON | Threat Assessment | Weekly |
| Project Health Evaluator | 🔄 Planned | Technical Risk | GitHub API, Dependencies | Console + Markdown | Health Score + Risks | On-demand |
| Technology Portfolio Advisor | ⏳ Future | Strategic Fit | Internal APIs, Market data | Executive Summary | Portfolio Alignment | Quarterly |

## Architecture

### Agent Framework
- **Modular Design** - Each agent operates independently with shared utilities
- **Extensible Analysis** - Common patterns for data gathering, analysis, and reporting
- **Standardized Output** - Consistent executive summary format across agents
- **Integration Ready** - API endpoints and CLI interfaces for all agents

## Installation

```bash
git clone https://github.com/jeremyeder/dotagents.git
cd dotagents
pip install -r requirements.txt
```

## Agent Installation

These agents are designed to work with [Claude Code](https://claude.ai/code) and are not executed as standalone scripts.

### Installation Process

1. **Copy agents to Claude Code directory:**
   ```bash
   cp -r prompts/* ~/.claude/agents/
   ```

2. **Agent discovery:** Claude Code automatically discovers agents in the `~/.claude/agents/` directory

3. **Activation:** Agents become available through Claude Code's interface for strategic analysis tasks

### Requirements

- Active Claude Code installation
- GitHub token (optional, for enhanced API rate limits):
  ```bash
  export GITHUB_TOKEN="your_github_token"
  ```


## PyTorch TAC Voting Advisor

### Output

The PyTorch TAC agent generates:

1. **Console Display** - Rich formatted analysis with recommendation tables
2. **Markdown Report** - Executive summary saved to `./analysis/` directory
3. **Strategic Assessments** - Organizational alignment analysis
4. **Risk Analysis** - Technical and business risk evaluation

### Example Output Structure

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
[Organizational alignment and ecosystem impact]
```

### Context

The PyTorch TAC agent is designed for governance scenarios where:
- **Rapid Analysis**: 7-day voting windows require quick, thorough evaluation
- **Strategic Alignment**: Decisions must consider organizational portfolio impact
- **Technical Depth**: GitHub metrics and ecosystem health assessment needed
- **Executive Summary**: Clear recommendations for committee-level decision making

### PyTorch TAC Agent Architecture

- **GitHubAnalyzer** - Repository health metrics and API integration
- **PyTorchEcosystemAnalyzer** - Competition and portfolio analysis
- **PyTorchTACAdvisor** - Main orchestration and recommendation generation
- **Rich Console Output** - Formatted display with tables and panels
- **Markdown Export** - Executive summary generation

## Project Structure

```
dotagents/
├── agents/                     # Agent implementations
│   └── pytorch_tac_advisor.py  # PyTorch TAC voting agent
├── requirements.txt            # Dependencies
├── prompts/                    # Agent specifications
│   └── pytorch/                # PyTorch TAC agent prompts
│       ├── pytorch_tac_voter.md
│       └── vote.png
├── analysis/                   # Generated reports
└── README.md                   # This file
```

## Development

### Adding New Agents

1. Create agent-specific directory in `prompts/`
2. Implement agent class following the framework patterns
3. Add CLI interface and documentation
4. Update this README with agent details

### Environment Setup

Set `GITHUB_TOKEN` environment variable for enhanced API access:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

This increases GitHub API rate limits from 60 to 5000 requests per hour.

