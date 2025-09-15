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
| UX Design Collaborator | ✅ Current | Design Strategy | User research, Design systems | Console + Guidelines | Design Recommendations | Sprint cycles |
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
   cp -r agents/* ~/.claude/agents/
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

## UX Design Collaborator

### Overview

The UX Design Collaborator agent provides expert design guidance, wireframes, and user experience strategy for product features. It specializes in agile product development and ensures alignment with design systems and accessibility standards.

### Core Capabilities

- **Design Analysis** - Evaluate design requests and provide UX guidance
- **Wireframe Guidance** - Generate wireframe recommendations for features
- **Design System Alignment** - Ensure consistency with design patterns
- **Accessibility Review** - WCAG compliance and inclusive design
- **Agile Integration** - Design guidance that fits sprint cycles

### Usage Examples

```bash
# Analyze a design request
python agents/uxd/agent.py analyze "Design a dashboard for analytics data" --context "Enterprise SaaS platform"

# Get wireframe guidance
python agents/uxd/agent.py wireframe --feature "User onboarding flow"

# Show help
python agents/uxd/agent.py help
```

### Context

The UX Design Collaborator agent is designed for scenarios where:
- **Feature Design**: New features require UX guidance and design direction
- **Sprint Planning**: Design validation needed for agile development cycles
- **Accessibility Review**: Ensuring WCAG compliance and inclusive design
- **Design System Evolution**: Maintaining consistency while identifying opportunities for improvement

## Project Structure

```
dotagents/
├── agents/                     # Agent implementations
│   ├── pytorch-tac/           # PyTorch TAC voting agent
│   │   ├── prompt.md          # Agent specification
│   │   └── agent.py           # Implementation
│   └── uxd/                   # UX Design Collaborator agent
│       ├── prompt.md          # Agent specification
│       └── agent.py           # Implementation
├── requirements.txt            # Dependencies
├── analysis/                   # Generated reports
└── README.md                   # This file
```

## Development

### Adding New Agents

1. Create agent-specific directory in `agents/` (e.g., `agents/my-agent/`)
2. Create `prompt.md` with agent specification and usage examples
3. Implement `agent.py` following the framework patterns
4. Add CLI interface and documentation
5. Update this README with agent details

### Agent Structure

Each agent follows a standardized structure:
- **`prompt.md`**: Agent specification, usage examples, and prompt definition
- **`agent.py`**: Python implementation with CLI interface and core functionality

### Agent Validation

All agents are validated using the built-in linter:

```bash
# Lint all agents
python lint_agents.py

# Lint specific agent
python lint_agents.py --agent pytorch-tac

# Auto-fix formatting issues
python lint_agents.py --fix
```

The linter validates:
- File structure and naming conventions
- Prompt format and required metadata
- Implementation patterns and CLI interfaces
- Code quality (Black, isort, flake8)

### Environment Setup

Set `GITHUB_TOKEN` environment variable for enhanced API access:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

This increases GitHub API rate limits from 60 to 5000 requests per hour.

