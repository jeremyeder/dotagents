#!/usr/bin/env python3
"""
Agent Linter Tool

Validates dotagents repository agents for compliance with standardized interface.
Ensures all agents follow the established patterns for file structure, CLI interface,
prompt format, and code quality.

Author: Jeremy Eder, Distinguished Engineer, Red Hat
"""

import ast
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


class AgentLinter:
    """Lints agents for compliance with dotagents standards"""

    def __init__(self):
        self.console = console
        self.agents_dir = Path("agents")
        self.errors = []
        self.warnings = []

    def lint_all_agents(self) -> bool:
        """Lint all agents in the agents directory"""
        if not self.agents_dir.exists():
            self.console.print(f"[red]Error: {self.agents_dir} directory not found[/red]")
            return False

        agent_dirs = [d for d in self.agents_dir.iterdir() if d.is_dir()]
        if not agent_dirs:
            self.console.print("[yellow]Warning: No agent directories found[/yellow]")
            return True

        all_passed = True
        results_table = Table(title="🔍 Agent Linting Results")
        results_table.add_column("Agent", style="cyan")
        results_table.add_column("Structure", justify="center")
        results_table.add_column("Prompt", justify="center")
        results_table.add_column("Implementation", justify="center")
        results_table.add_column("Code Quality", justify="center")
        results_table.add_column("Overall", style="bold", justify="center")

        for agent_dir in sorted(agent_dirs):
            agent_name = agent_dir.name
            self.console.print(f"\n[bold]Linting agent: {agent_name}[/bold]")

            structure_ok = self._check_file_structure(agent_dir)
            prompt_ok = self._check_prompt_file(agent_dir / "prompt.md")
            impl_ok = self._check_implementation_file(agent_dir / "agent.py")
            quality_ok = self._check_code_quality(agent_dir / "agent.py")

            overall_ok = structure_ok and prompt_ok and impl_ok and quality_ok
            all_passed = all_passed and overall_ok

            # Add to results table
            results_table.add_row(
                agent_name,
                "✅" if structure_ok else "❌",
                "✅" if prompt_ok else "❌",
                "✅" if impl_ok else "❌",
                "✅" if quality_ok else "❌",
                "✅ PASS" if overall_ok else "❌ FAIL"
            )

        self.console.print("\n")
        self.console.print(results_table)

        if self.errors:
            self.console.print("\n[red bold]Errors Found:[/red bold]")
            for error in self.errors:
                self.console.print(f"[red]❌ {error}[/red]")

        if self.warnings:
            self.console.print("\n[yellow bold]Warnings:[/yellow bold]")
            for warning in self.warnings:
                self.console.print(f"[yellow]⚠️  {warning}[/yellow]")

        return all_passed

    def lint_agent(self, agent_name: str) -> bool:
        """Lint a specific agent"""
        agent_dir = self.agents_dir / agent_name
        if not agent_dir.exists():
            self.console.print(f"[red]Error: Agent '{agent_name}' not found[/red]")
            return False

        self.console.print(f"[bold]Linting agent: {agent_name}[/bold]")

        structure_ok = self._check_file_structure(agent_dir)
        prompt_ok = self._check_prompt_file(agent_dir / "prompt.md")
        impl_ok = self._check_implementation_file(agent_dir / "agent.py")
        quality_ok = self._check_code_quality(agent_dir / "agent.py")

        overall_ok = structure_ok and prompt_ok and impl_ok and quality_ok

        self.console.print(f"\n[{'green' if overall_ok else 'red'}]Overall: {'PASS' if overall_ok else 'FAIL'}[/]")
        return overall_ok

    def _check_file_structure(self, agent_dir: Path) -> bool:
        """Check agent directory file structure"""
        agent_name = agent_dir.name
        required_files = {"prompt.md", "agent.py"}
        actual_files = {f.name for f in agent_dir.iterdir() if f.is_file()}

        # Check required files exist
        missing_files = required_files - actual_files
        if missing_files:
            for file in missing_files:
                self.errors.append(f"{agent_name}: Missing required file '{file}'")
            return False

        # Check directory naming convention (kebab-case)
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', agent_name):
            self.errors.append(f"{agent_name}: Directory name should use kebab-case")
            return False

        # Allow additional resource files but warn about unexpected files
        extra_files = actual_files - required_files
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.md', '.txt', '.json', '.yaml', '.yml'}
        for file in extra_files:
            file_path = agent_dir / file
            if file_path.suffix.lower() not in allowed_extensions:
                self.warnings.append(f"{agent_name}: Unexpected file '{file}' (consider documenting purpose)")

        self.console.print(f"  [green]✅ File structure: OK[/green]")
        return True

    def _check_prompt_file(self, prompt_file: Path) -> bool:
        """Check prompt.md file compliance"""
        agent_name = prompt_file.parent.name

        if not prompt_file.exists():
            self.errors.append(f"{agent_name}: prompt.md file missing")
            return False

        try:
            content = prompt_file.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"{agent_name}: Cannot read prompt.md - {e}")
            return False

        checks_passed = []

        # Check for required sections
        required_sections = [
            (r'#+.*Agent.*Metadata', "Agent Metadata section"),
            (r'#+.*Usage.*Examples?', "Usage Examples section"),
            (r'#+.*Agent.*Prompt', "Agent Prompt section")
        ]

        for pattern, description in required_sections:
            if re.search(pattern, content, re.IGNORECASE):
                checks_passed.append(True)
            else:
                self.errors.append(f"{agent_name}: Missing {description} in prompt.md")
                checks_passed.append(False)

        # Check for metadata fields
        metadata_fields = ['name', 'model', 'description']
        for field in metadata_fields:
            pattern = rf'\*\*{field}\*\*.*:|{field}:'
            if re.search(pattern, content, re.IGNORECASE):
                checks_passed.append(True)
            else:
                self.errors.append(f"{agent_name}: Missing '{field}' metadata in prompt.md")
                checks_passed.append(False)

        # Check for usage examples format
        if re.search(r'Context.*User.*Assistant.*Commentary', content, re.DOTALL | re.IGNORECASE):
            checks_passed.append(True)
        else:
            self.warnings.append(f"{agent_name}: Usage examples should follow Context/User/Assistant/Commentary format")
            checks_passed.append(True)  # Warning, not error

        all_passed = all(checks_passed)
        status = "✅ OK" if all_passed else "❌ FAIL"
        self.console.print(f"  [{'green' if all_passed else 'red'}]{status} Prompt file[/]")
        return all_passed

    def _check_implementation_file(self, agent_file: Path) -> bool:
        """Check agent.py implementation compliance"""
        agent_name = agent_file.parent.name

        if not agent_file.exists():
            self.errors.append(f"{agent_name}: agent.py file missing")
            return False

        try:
            content = agent_file.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"{agent_name}: Cannot read agent.py - {e}")
            return False

        checks_passed = []

        # Check shebang
        if content.startswith('#!/usr/bin/env python3'):
            checks_passed.append(True)
        else:
            self.errors.append(f"{agent_name}: Missing proper Python shebang")
            checks_passed.append(False)

        # Check for docstring
        if '"""' in content and len(re.findall(r'"""', content)) >= 2:
            checks_passed.append(True)
        else:
            self.errors.append(f"{agent_name}: Missing module docstring")
            checks_passed.append(False)

        # Check for Click framework
        if 'import click' in content or 'from click import' in content:
            checks_passed.append(True)
        else:
            self.errors.append(f"{agent_name}: Should use Click framework for CLI")
            checks_passed.append(False)

        # Check for main entry point
        if "if __name__ ==" in content and "__main__" in content:
            checks_passed.append(True)
        else:
            self.errors.append(f"{agent_name}: Missing main entry point")
            checks_passed.append(False)

        # Check for Click decorators
        if '@click.command()' in content or '@click.group()' in content:
            checks_passed.append(True)
        else:
            self.errors.append(f"{agent_name}: Missing Click command decorator")
            checks_passed.append(False)

        # Check for help functionality
        if '--help' in content or 'help=' in content:
            checks_passed.append(True)
        else:
            self.warnings.append(f"{agent_name}: Should include help documentation")
            checks_passed.append(True)  # Warning, not error

        # Try to parse as valid Python
        try:
            ast.parse(content)
            checks_passed.append(True)
        except SyntaxError as e:
            self.errors.append(f"{agent_name}: Python syntax error - {e}")
            checks_passed.append(False)

        all_passed = all(checks_passed)
        status = "✅ OK" if all_passed else "❌ FAIL"
        self.console.print(f"  [{'green' if all_passed else 'red'}]{status} Implementation[/]")
        return all_passed

    def _check_code_quality(self, agent_file: Path) -> bool:
        """Check code quality with Black, isort, and flake8"""
        agent_name = agent_file.parent.name

        if not agent_file.exists():
            return False

        checks_passed = []

        # Check Black formatting
        try:
            result = subprocess.run(
                ["black", "--check", str(agent_file)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                checks_passed.append(True)
            else:
                self.errors.append(f"{agent_name}: Code not formatted with Black")
                checks_passed.append(False)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append(f"{agent_name}: Could not run Black formatter check")
            checks_passed.append(True)  # Don't fail if tool not available

        # Check isort import sorting
        try:
            result = subprocess.run(
                ["isort", "--check-only", str(agent_file)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                checks_passed.append(True)
            else:
                self.errors.append(f"{agent_name}: Imports not sorted with isort")
                checks_passed.append(False)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append(f"{agent_name}: Could not run isort check")
            checks_passed.append(True)  # Don't fail if tool not available

        # Check flake8 linting
        try:
            result = subprocess.run(
                ["flake8", str(agent_file), "--max-line-length=88",
                 "--select=E9,F63,F7,F82", "--show-source"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                checks_passed.append(True)
            else:
                self.errors.append(f"{agent_name}: flake8 linting errors - {result.stdout}")
                checks_passed.append(False)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.warnings.append(f"{agent_name}: Could not run flake8 check")
            checks_passed.append(True)  # Don't fail if tool not available

        all_passed = all(checks_passed)
        status = "✅ OK" if all_passed else "❌ FAIL"
        self.console.print(f"  [{'green' if all_passed else 'red'}]{status} Code quality[/]")
        return all_passed


@click.command()
@click.option('--agent', '-a', help='Lint specific agent (default: all agents)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--fix', '-f', is_flag=True, help='Attempt to fix formatting issues')
def main(agent: Optional[str], verbose: bool, fix: bool):
    """
    Agent Linter for dotagents repository

    Validates agents for compliance with standardized interface including:
    - File structure (prompt.md + agent.py)
    - Prompt format and required sections
    - Implementation patterns (Click CLI, entry points)
    - Code quality (Black, isort, flake8)

    Examples:

    \b
    # Lint all agents
    python lint_agents.py

    \b
    # Lint specific agent
    python lint_agents.py --agent pytorch-tac

    \b
    # Attempt to fix formatting issues
    python lint_agents.py --fix
    """

    linter = AgentLinter()

    if fix:
        console.print("[yellow]🔧 Attempting to fix formatting issues...[/yellow]")
        # Attempt to fix with Black and isort
        for agent_dir in Path("agents").iterdir():
            if agent_dir.is_dir():
                agent_py = agent_dir / "agent.py"
                if agent_py.exists():
                    try:
                        subprocess.run(["black", str(agent_py)], check=True)
                        subprocess.run(["isort", str(agent_py)], check=True)
                        console.print(f"  [green]✅ Fixed formatting for {agent_dir.name}[/green]")
                    except (subprocess.CalledProcessError, FileNotFoundError) as e:
                        console.print(f"  [red]❌ Could not fix {agent_dir.name}: {e}[/red]")
        console.print("")

    if agent:
        success = linter.lint_agent(agent)
    else:
        success = linter.lint_all_agents()

    if success:
        console.print("\n[bold green]🎉 All checks passed![/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]💥 Linting failed![/bold red]")
        sys.exit(1)


if __name__ == '__main__':
    main()