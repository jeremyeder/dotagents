#!/usr/bin/env python3
"""
[Agent Name] Agent

[Detailed description of what this agent does, its purpose, and key capabilities.
Include information about the domain it operates in and the value it provides.]

Author: Jeremy Eder, Distinguished Engineer, Red Hat
"""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


class [AgentClassName]:
    """[Agent Name] for [primary purpose]"""

    def __init__(self):
        self.console = console

    def [primary_method](self, [parameters]) -> str:
        """[Description of main functionality]"""

        # Implementation of core agent logic
        result = f"""
# [Agent Output Title]

## [Section 1]
[Content or analysis goes here]

## [Section 2]
[Additional content]

## [Key Recommendations/Next Steps]
- [Actionable item 1]
- [Actionable item 2]
- [Actionable item 3]
"""
        return result

    def [secondary_method](self, [parameters]) -> str:
        """[Description of secondary functionality]"""

        guidance = f"""
# [Secondary Output Title]

## [Relevant Section]
[Content specific to this function]

## [Guidelines/Recommendations]
- [Specific guidance point]
- [Additional recommendation]
- [Further suggestion]
"""
        return guidance


@click.command()
@click.argument('action', type=click.Choice(['[primary-action]', '[secondary-action]', 'help']))
@click.argument('[primary_input]', required=False)
@click.option('--context', '-c', help='Additional context for the request')
@click.option('--[custom-option]', '-[letter]', help='[Description of custom option]')
def main(
    action: str,
    [primary_input]: str = None,
    context: str = None,
    [custom_option]: str = None
):
    """
    [Agent Name] Agent

    [Brief description of agent capabilities and purpose]

    Examples:

    \\b
    # [Primary usage example]
    python agent.py [primary-action] "[example input]" --context "[example context]"

    \\b
    # [Secondary usage example]
    python agent.py [secondary-action] --[custom-option] "[example value]"

    \\b
    # Show help
    python agent.py help
    """

    agent = [AgentClassName]()

    if action == 'help':
        console.print(Panel(
            Markdown("""
# [Agent Name] Agent

## Capabilities
- **[Primary Capability]**: [Description of what agent can do]
- **[Secondary Capability]**: [Additional functionality]
- **[Tertiary Capability]**: [More functionality]

## Usage Patterns
- [Common use case 1]
- [Common use case 2]
- [Common use case 3]

## Core Principles
- [Key principle or methodology]
- [Another important aspect]
- [Additional guiding principle]
"""),
            title="🤖 [Agent Name]",
            border_style="blue"
        ))
        return

    if action == '[primary-action]':
        if not [primary_input]:
            console.print("[red]Error: [Primary input] is required for [primary action][/red]")
            return

        result = agent.[primary_method]([primary_input], context)
        console.print(Panel(
            Markdown(result),
            title="🎯 [Primary Action Title]",
            border_style="green"
        ))

    elif action == '[secondary-action]':
        if not [custom_option]:
            console.print("[red]Error: [Custom option] is required for [secondary action][/red]")
            return

        result = agent.[secondary_method]([custom_option])
        console.print(Panel(
            Markdown(result),
            title="📊 [Secondary Action Title]",
            border_style="blue"
        ))


if __name__ == '__main__':
    main()