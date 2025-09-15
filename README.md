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
│   │   ├── agent.py           # Implementation
│   │   └── vote.png           # Reference voting notification
│   └── uxd/                   # UX Design Collaborator agent
│       ├── prompt.md          # Agent specification
│       └── agent.py           # Implementation
├── templates/                  # Development templates
│   ├── prompt.md              # Template for agent specifications
│   └── agent.py               # Template for agent implementations
├── .github/workflows/          # CI/CD configuration
│   └── ci.yml                 # Automated testing and validation
├── lint_agents.py              # Agent validation and linting tool
├── AGENT_INTERFACE.md          # Comprehensive interface specification
├── requirements.txt            # Dependencies
├── analysis/                   # Generated reports
└── README.md                   # This file
```

## Development

### Quick Start for New Agents

1. **Copy Templates**: Use provided templates as starting point
   ```bash
   mkdir agents/my-agent
   cp templates/prompt.md agents/my-agent/
   cp templates/agent.py agents/my-agent/
   ```

2. **Customize Specification**: Edit `prompt.md` with agent details
   - Update metadata (name, model, description)
   - Define usage examples with context/user/assistant/commentary format
   - Specify agent behavior and capabilities

3. **Implement Functionality**: Edit `agent.py` with core logic
   - Follow Click CLI framework patterns
   - Use Rich console for formatted output
   - Implement help functionality and error handling

4. **Validate Compliance**: Run linter before submitting
   ```bash
   python lint_agents.py --agent my-agent --fix
   ```

5. **Test Functionality**: Ensure agent works correctly
   ```bash
   python agents/my-agent/agent.py --help
   ```

### Comprehensive Documentation

For detailed interface specifications, development patterns, and validation requirements, see:

**📚 [AGENT_INTERFACE.md](AGENT_INTERFACE.md)** - Complete developer guide including:
- Standardized file structure requirements
- Prompt format specification with examples
- Implementation patterns and CLI standards
- Code quality requirements and validation rules
- Development workflow and best practices

### Adding New Agents (Detailed Process)

1. **Plan Agent Design**: Define purpose, capabilities, and usage scenarios
2. **Create Directory Structure**: Use templates as foundation
3. **Implement Specification**: Follow AGENT_INTERFACE.md requirements
4. **Validate Implementation**: Pass all linter checks
5. **Test Functionality**: Verify CLI interface and core features
6. **Submit for Review**: CI will automatically validate compliance
7. **Update Documentation**: Add agent to portfolio table above

### Agent Structure

Each agent follows a standardized structure:
- **`prompt.md`**: Agent specification, usage examples, and prompt definition
- **`agent.py`**: Python implementation with CLI interface and core functionality

### Agent Linter Tool

The repository includes a comprehensive linting tool (`lint_agents.py`) that validates all aspects of agent compliance:

#### **Validation Categories**
- **File Structure**: Directory naming, required files, resource validation
- **Prompt Format**: Metadata completeness, usage examples, agent specification
- **Implementation**: Python patterns, CLI framework, entry points, docstrings
- **Code Quality**: Black formatting, isort imports, flake8 linting, syntax validation

#### **Linter Commands**
```bash
# Validate all agents with detailed results table
python lint_agents.py

# Validate specific agent with focused output
python lint_agents.py --agent pytorch-tac

# Auto-fix formatting issues (Black + isort)
python lint_agents.py --fix

# Verbose output for debugging
python lint_agents.py --verbose
```

#### **Linter Output**
The linter provides rich console output with:
- ✅/❌ Status indicators for each validation category
- Detailed error messages with fix suggestions
- Summary table showing all agents' compliance status
- Auto-fix capability for formatting issues

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

### CI/CD Integration

All agents are automatically validated through GitHub Actions CI/CD pipeline:

#### **Automated Validation**
- **Agent Linter**: All agents validated on every PR and push
- **Code Quality**: Black formatting, isort imports, flake8 linting
- **Functional Testing**: Agent help commands tested automatically
- **Quality Gates**: Non-compliant agents cannot be merged

#### **CI Workflow**
The CI pipeline runs these checks automatically:

```yaml
# Agent validation
python lint_agents.py

# Code formatting
find agents/ -name "*.py" -exec black --check {} +
find agents/ -name "*.py" -exec isort --check-only {} +

# Linting
find agents/ -name "*.py" -print0 | xargs -0 flake8 --max-line-length=88

# Functional testing
python agents/pytorch-tac/agent.py --help
python agents/uxd/agent.py help
```

#### **Development Benefits**
- **Quality Assurance**: Automated prevention of regressions
- **Consistency**: All agents follow standardized patterns
- **Confidence**: Changes validated before merging
- **Documentation**: CI failures provide clear guidance

### Templates for New Development

Use the provided templates to quickly create new agents:

#### **Starting a New Agent**
```bash
# Copy templates to new agent directory
mkdir agents/my-new-agent
cp templates/prompt.md agents/my-new-agent/
cp templates/agent.py agents/my-new-agent/

# Customize the templates
# Edit agents/my-new-agent/prompt.md - Update metadata and examples
# Edit agents/my-new-agent/agent.py - Implement functionality

# Validate your agent
python lint_agents.py --agent my-new-agent
```

#### **Template Features**
- **Structured Prompt**: Pre-formatted with required sections
- **Boilerplate Code**: Click CLI framework and Rich console output
- **Best Practices**: Follows established patterns and conventions
- **Validation Ready**: Passes all linter checks out of the box

### Environment Setup

Set `GITHUB_TOKEN` environment variable for enhanced API access:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

This increases GitHub API rate limits from 60 to 5000 requests per hour.

