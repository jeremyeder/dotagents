# Agent Interface Standards

This document defines the standardized interface for all agents in the dotagents repository. Following these standards ensures consistency, maintainability, and quality across all agents.

## Table of Contents

- [Overview](#overview)
- [File Structure Requirements](#file-structure-requirements)
- [Prompt File Specification](#prompt-file-specification)
- [Implementation Requirements](#implementation-requirements)
- [CLI Interface Standards](#cli-interface-standards)
- [Code Quality Standards](#code-quality-standards)
- [Validation and Testing](#validation-and-testing)
- [Development Workflow](#development-workflow)

## Overview

Every agent in the dotagents repository follows a standardized structure designed for:
- **Consistency**: Uniform interface across all agents
- **Maintainability**: Clear organization and documentation
- **Quality**: Automated validation and testing
- **Deployment**: Easy integration with Claude Code

## File Structure Requirements

### Directory Structure
Each agent must be organized in its own directory under `agents/`:

```
agents/
└── [agent-name]/
    ├── prompt.md          # Agent specification (REQUIRED)
    ├── agent.py           # Implementation (REQUIRED)
    └── [resources...]     # Optional supporting files
```

### Naming Conventions
- **Agent directories**: Use kebab-case (e.g., `pytorch-tac`, `ux-design-collaborator`)
- **Required files**: Exactly `prompt.md` and `agent.py`
- **Resource files**: Optional files with standard extensions (`.png`, `.jpg`, `.json`, `.yaml`, etc.)

### Validation Rules
- ✅ Exactly 2 required files per agent
- ✅ Directory names must match regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- ✅ No unexpected file types (warnings for non-standard extensions)

## Prompt File Specification

The `prompt.md` file defines the agent's specification, usage patterns, and behavior.

### Required Structure

```markdown
# [Agent Name] Agent

## Agent Metadata
- **Name**: agent-identifier
- **Model**: sonnet
- **Description**: Brief description of agent purpose

## Usage Examples

### Example 1: [Scenario Name]
**Context**: Describe the situation where this agent is used
- **User**: "User input example"
- **Assistant**: "How Claude Code should respond"
- **Commentary**: Why this agent should be selected

### Example 2: [Another Scenario]
[Follow same format...]

## Agent Prompt

[Detailed agent behavior specification...]
```

### Required Metadata Fields
- **Name**: Unique identifier for the agent
- **Model**: AI model to use (typically "sonnet")
- **Description**: Clear, concise purpose statement

### Usage Examples Format
Each example must include:
- **Context**: Situational description
- **User**: Example user input
- **Assistant**: Expected assistant response
- **Commentary**: Reasoning for agent selection

### Content Guidelines
- Use clear, professional language
- Include 2-3 representative usage examples
- Provide comprehensive agent behavior specification
- Document any special requirements or constraints

## Implementation Requirements

The `agent.py` file contains the executable implementation of the agent.

### Required Elements

#### File Header
```python
#!/usr/bin/env python3
"""
[Agent Name] Agent

[Description of agent purpose and functionality]

Author: Jeremy Eder, Distinguished Engineer, Red Hat
"""
```

#### Core Dependencies
```python
import click
from rich.console import Console
from rich.panel import Panel
# Additional imports as needed
```

#### Main Entry Point
```python
if __name__ == '__main__':
    main()
```

### Required Patterns
- ✅ Python shebang: `#!/usr/bin/env python3`
- ✅ Module docstring with agent description
- ✅ Click framework for CLI interface
- ✅ Rich library for formatted output
- ✅ Main entry point pattern
- ✅ Valid Python syntax (AST parseable)

## CLI Interface Standards

### Click Framework Requirements
All agents must use the Click framework for command-line interfaces.

#### Basic Structure
```python
@click.command()
@click.argument('action', type=click.Choice(['analyze', 'help']))
@click.option('--context', '-c', help='Additional context')
def main(action: str, context: str = None):
    """
    Agent Name

    Brief description of agent functionality.

    Examples:

    \b
    # Example usage
    python agent.py analyze "input"
    """
    # Implementation here
```

#### Required Features
- ✅ Click command or group decorator
- ✅ Comprehensive help documentation
- ✅ Consistent option naming (use `-c` for context, `-f` for feature, etc.)
- ✅ Example usage in docstring
- ✅ Rich console output formatting

### Standard Options
When applicable, use these standard option names:
- `--context, -c`: Additional context for the request
- `--output, -o`: Output directory or file
- `--verbose, -v`: Verbose output mode
- `--help`: Built-in help (automatic with Click)

## Code Quality Standards

### Formatting Requirements
All Python code must pass these quality checks:

#### Black Formatting
```bash
black --check agent.py
```
- Line length: 88 characters (Black default)
- Consistent quote style
- Proper spacing and indentation

#### Import Sorting
```bash
isort --check-only agent.py
```
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetical ordering within groups

#### Linting
```bash
flake8 agent.py --max-line-length=88 --select=E9,F63,F7,F82
```
- No syntax errors
- No undefined variables
- No unused imports
- Basic style compliance

### Quality Standards
- ✅ No syntax errors or warnings
- ✅ Consistent code formatting
- ✅ Proper import organization
- ✅ Clear variable and function names
- ✅ Appropriate error handling

## Validation and Testing

### Agent Linter
Use the built-in agent linter to validate compliance:

```bash
# Lint all agents
python lint_agents.py

# Lint specific agent
python lint_agents.py --agent pytorch-tac

# Auto-fix formatting issues
python lint_agents.py --fix
```

### Validation Checklist
Before submitting an agent, ensure it passes:

- [ ] File structure validation
- [ ] Prompt file format compliance
- [ ] Implementation requirements
- [ ] CLI interface standards
- [ ] Code quality checks
- [ ] Functional testing (--help works)

### Testing Requirements
Each agent should:
- ✅ Display help without errors
- ✅ Handle invalid inputs gracefully
- ✅ Provide meaningful error messages
- ✅ Follow expected output format

## Development Workflow

### Creating a New Agent

1. **Setup Directory Structure**
   ```bash
   mkdir agents/my-agent
   cd agents/my-agent
   ```

2. **Create Prompt File**
   - Copy from template or existing agent
   - Update metadata and examples
   - Define agent behavior specification

3. **Implement Agent**
   - Create `agent.py` with required structure
   - Implement core functionality
   - Add CLI interface with Click

4. **Validate Compliance**
   ```bash
   python lint_agents.py --agent my-agent
   ```

5. **Test Functionality**
   ```bash
   python agents/my-agent/agent.py --help
   ```

6. **Fix Issues**
   ```bash
   python lint_agents.py --fix
   ```

### Continuous Integration
The CI pipeline automatically:
- Runs agent linter on all agents
- Validates code quality standards
- Tests basic functionality
- Ensures no regressions

### Best Practices
- Start with simple functionality and iterate
- Use existing agents as reference implementations
- Test thoroughly before submission
- Document any special requirements
- Follow established patterns and conventions

## Examples

### Minimal Agent Structure

**prompt.md**:
```markdown
# Example Agent

## Agent Metadata
- **Name**: example-agent
- **Model**: sonnet
- **Description**: Example agent for demonstration

## Usage Examples

### Example 1: Basic Usage
**Context**: User needs basic functionality
- **User**: "Help me with example task"
- **Assistant**: "I'll use the example-agent to help you"
- **Commentary**: Basic example agent usage

## Agent Prompt

You are an example agent that demonstrates the standard interface.
```

**agent.py**:
```python
#!/usr/bin/env python3
"""
Example Agent

Demonstrates the standardized agent interface and basic functionality.

Author: Jeremy Eder, Distinguished Engineer, Red Hat
"""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command()
@click.argument('action')
@click.option('--context', '-c', help='Additional context')
def main(action: str, context: str = None):
    """
    Example Agent

    Demonstrates standardized agent interface.

    Example:

    \b
    python agent.py help
    """
    if action == 'help':
        console.print(Panel("Example Agent Help", title="🤖 Example"))


if __name__ == '__main__':
    main()
```

This interface specification ensures all agents follow consistent patterns while maintaining flexibility for specific use cases.