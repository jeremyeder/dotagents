# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **PyTorch TAC Voting Advisor Agent** - a strategic decision support tool for Jeremy Eder's role as PyTorch Technical Advisory Committee member representing IBM/Red Hat. The agent analyzes PyTorch ecosystem projects and generates executive summaries with voting recommendations considering competition, portfolio overlap, and project health.

## Architecture

### Core Components

- **`pytorch_tac_advisor.py`** - Main application with three primary classes:
  - `GitHubAnalyzer` - Repository health metrics via GitHub API
  - `PyTorchEcosystemAnalyzer` - Competition and portfolio analysis
  - `PyTorchTACAdvisor` - Orchestrates analysis and generates recommendations

- **`prompts/pytorch/`** - Contains:
  - `pytorch_tac_voter.md` - Agent specification and requirements
  - `vote.png` - Reference voting notification image

- **`analysis/`** - Generated markdown reports for voting decisions

### Data Models

- **`ProjectAnalysis`** - Technical analysis results
- **`VotingRecommendation`** - Final voting decision with rationale

## Common Development Commands

### Running Analysis
```bash
# Basic analysis
python pytorch_tac_advisor.py "Project Name" "https://github.com/owner/repo"

# With description and context
python pytorch_tac_advisor.py "ML Inference Engine" "https://github.com/example/engine" \
  --description "Fast PyTorch model serving for production" \
  --context "Vote deadline: 2025-01-15"

# With GitHub token for higher API limits
export GITHUB_TOKEN="your_token"
python pytorch_tac_advisor.py "Project Name" "https://github.com/owner/repo"
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or use uv (preferred)
uv pip install -r requirements.txt
```

### Testing
```bash
# Test with PyTorch repository (known good case)
python pytorch_tac_advisor.py "Test Project" "https://github.com/pytorch/pytorch"
```

## Key Features

### Analysis Components
- **GitHub Health Scoring** (0-100 scale based on stars, activity, contributors, maintenance)
- **Competition Mapping** - Identifies competitive landscape in ML/PyTorch ecosystem  
- **Portfolio Overlap Analysis** - Assesses overlap with Red Hat/IBM AI portfolio (OpenShift AI, Watson, CodeFlare, etc.)
- **Risk Assessment** - Technical and business risks including bus factor, competitive pressure
- **Strategic Recommendations** - APPROVE/REJECT/ABSTAIN with confidence levels

### Output Formats
- **Rich Console Display** - Formatted tables and panels with syntax highlighting
- **Markdown Executive Summary** - Saved to `./analysis/` directory with timestamp
- **IBM Research Consultation Notes** - Discussion points for Raghu Ganti collaboration

## Business Context

### Jeremy's TAC Role
- PyTorch TAC Member representing IBM/Red Hat
- Non-voting seat on PyTorch Governing Board  
- Collaborates with Raghu Ganti (IBM Research) who holds official voting seat
- 7-day voting windows require rapid analysis and strategic consultation

### Strategic Considerations
- **Red Hat Alignment** - OpenShift AI integration, enterprise PyTorch adoption
- **IBM Research Priorities** - Watson integration, Granite model ecosystem
- **Ecosystem Health** - Supporting sustainable PyTorch community growth
- **Competitive Positioning** - Avoiding conflicts with Red Hat/IBM AI portfolio

## Development Notes

### GitHub API Integration
- Uses aiohttp for async API calls
- Supports both authenticated (with token) and unauthenticated access
- Rate limits: 60 requests/hour (unauthenticated), 5000 requests/hour (authenticated)
- Analyzes: repository metadata, recent commits, issues/PRs, contributor data

### Health Score Algorithm
- **Stars**: Max 20 points (stars/100)
- **Recent Activity**: Max 25 points (recent commits * 2.5)  
- **Contributors**: Max 20 points (contributor count)
- **Maintenance**: Max 35 points (not archived, has wiki/issues/description/license)

### Competitive Analysis Keywords
- **Inference**: TensorRT, ONNX Runtime, TensorFlow Lite
- **Training**: Horovod, DeepSpeed, FairScale
- **Deployment**: TorchServe, MLflow, Kubeflow
- **Optimization**: TensorRT, Intel OpenVINO, Apache TVM
- **Distributed**: Ray, Dask, Horovod

## File Organization

```
dotagents/
├── pytorch_tac_advisor.py      # Main application
├── requirements.txt            # Dependencies  
├── README.md                   # Usage documentation
├── prompts/pytorch/            # Agent specifications
│   ├── pytorch_tac_voter.md   # Requirements
│   └── vote.png                # Reference image
├── analysis/                   # Generated reports
└── jeremy-agent-recommendations.md  # Private strategy document
```

## Dependencies

- **aiohttp>=3.8.0** - Async HTTP client for GitHub API
- **click>=8.0.0** - Command-line interface framework
- **rich>=13.0.0** - Rich text and beautiful formatting for console output

## Environment Variables

- **`GITHUB_TOKEN`** - GitHub personal access token for higher API rate limits
- Set via `export GITHUB_TOKEN="ghp_your_token_here"` before running analysis

## Agent Specialization

This is a specialized agent designed for PyTorch governance decisions, not a general-purpose tool. The analysis framework is specifically tuned for:
- PyTorch ecosystem project evaluation
- Red Hat/IBM strategic alignment assessment  
- Technical Advisory Committee voting support
- IBM Research collaboration facilitation