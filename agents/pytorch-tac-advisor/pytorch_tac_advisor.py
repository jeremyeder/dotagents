#!/usr/bin/env python3
"""
PyTorch TAC Voting Advisor Agent

Strategic advisor for Jeremy Eder's PyTorch Technical Advisory Committee voting.
Provides research-backed decision support for PyTorch ecosystem votes with
executive summaries considering competition, portfolio overlap, and project health.

Author: Jeremy Eder, Distinguished Engineer, Red Hat
Role: PyTorch TAC Member (IBM/Red Hat representative)
"""

import asyncio
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


@dataclass
class ProjectAnalysis:
    """Analysis results for a PyTorch ecosystem project"""

    name: str
    description: str
    github_url: str
    health_score: float  # 0-100
    competition_analysis: str
    portfolio_overlap: str
    strategic_recommendation: str
    risk_assessment: str
    technical_merit: str
    community_engagement: str
    maintainer_credibility: str


@dataclass
class VotingRecommendation:
    """Final voting recommendation with rationale"""

    project_name: str
    recommendation: str  # "APPROVE", "REJECT", "ABSTAIN"
    confidence: str  # "HIGH", "MEDIUM", "LOW"
    executive_summary: str
    key_factors: List[str]
    red_hat_alignment: str
    ibm_alignment: str
    raghu_consultation_notes: str


class GitHubAnalyzer:
    """Analyzes GitHub repositories for project health metrics"""

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.console = Console()

    async def analyze_repository(self, github_url: str) -> Dict:
        """Analyze a GitHub repository for health metrics"""

        owner, repo = self._parse_github_url(github_url)
        if not owner or not repo:
            return {"error": "Invalid GitHub URL"}

        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        async with aiohttp.ClientSession() as session:
            # Get repository information
            repo_data = await self._github_api_call(
                session, f"https://api.github.com/repos/{owner}/{repo}", headers
            )

            # Get recent activity
            commits_data = await self._github_api_call(
                session, f"https://api.github.com/repos/{owner}/{repo}/commits", headers
            )

            # Get issues/PRs
            issues_data = await self._github_api_call(
                session, f"https://api.github.com/repos/{owner}/{repo}/issues", headers
            )

            # Get contributors
            contributors_data = await self._github_api_call(
                session,
                f"https://api.github.com/repos/{owner}/{repo}/contributors",
                headers,
            )

        return {
            "repository": repo_data,
            "recent_commits": commits_data,
            "issues": issues_data,
            "contributors": contributors_data,
        }

    def _parse_github_url(self, url: str) -> Tuple[str, str]:
        """Parse GitHub URL to extract owner and repository"""
        parsed = urlparse(url)
        if parsed.hostname != "github.com":
            return "", ""

        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2:
            return path_parts[0], path_parts[1]
        return "", ""

    async def _github_api_call(
        self, session: aiohttp.ClientSession, url: str, headers: Dict
    ) -> Dict:
        """Make a GitHub API call with error handling"""
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}


class PyTorchEcosystemAnalyzer:
    """Analyzes PyTorch ecosystem projects for strategic fit"""

    def __init__(self):
        self.console = Console()
        self.github_analyzer = GitHubAnalyzer()

    async def analyze_project(
        self, project_name: str, github_url: str, description: str = ""
    ) -> ProjectAnalysis:
        """Perform comprehensive project analysis"""

        self.console.print(f"[blue]Analyzing project: {project_name}[/blue]")

        # GitHub analysis
        github_data = await self.github_analyzer.analyze_repository(github_url)

        # Calculate health score
        health_score = self._calculate_health_score(github_data)

        # Analyze competition and overlap
        competition_analysis = self._analyze_competition(project_name, description)
        portfolio_overlap = self._analyze_portfolio_overlap(project_name, description)

        # Strategic assessments
        strategic_recommendation = self._generate_strategic_recommendation(
            project_name, health_score, competition_analysis, portfolio_overlap
        )

        risk_assessment = self._assess_risks(github_data, competition_analysis)
        technical_merit = self._assess_technical_merit(github_data, description)
        community_engagement = self._assess_community_engagement(github_data)
        maintainer_credibility = self._assess_maintainer_credibility(github_data)

        return ProjectAnalysis(
            name=project_name,
            description=description,
            github_url=github_url,
            health_score=health_score,
            competition_analysis=competition_analysis,
            portfolio_overlap=portfolio_overlap,
            strategic_recommendation=strategic_recommendation,
            risk_assessment=risk_assessment,
            technical_merit=technical_merit,
            community_engagement=community_engagement,
            maintainer_credibility=maintainer_credibility,
        )

    def _calculate_health_score(self, github_data: Dict) -> float:
        """Calculate project health score based on GitHub metrics"""

        if "error" in github_data.get("repository", {}):
            return 0.0

        repo = github_data.get("repository", {})
        commits = github_data.get("recent_commits", [])
        contributors = github_data.get("contributors", [])

        score = 0.0

        # Stars (max 20 points)
        stars = repo.get("stargazers_count", 0)
        score += min(20, stars / 100)

        # Recent activity (max 25 points)
        if commits:
            recent_commits = len([c for c in commits[:10] if self._is_recent_commit(c)])
            score += min(25, recent_commits * 2.5)

        # Contributors (max 20 points)
        contributor_count = len(contributors)
        score += min(20, contributor_count)

        # Maintenance indicators (max 35 points)
        if not repo.get("archived", False):
            score += 10
        if repo.get("has_wiki", False):
            score += 5
        if repo.get("has_issues", False):
            score += 5
        if repo.get("description"):
            score += 5
        if repo.get("license"):
            score += 10

        return min(100.0, score)

    def _is_recent_commit(self, commit: Dict) -> bool:
        """Check if commit is recent (within 30 days)"""
        try:
            commit_date = datetime.fromisoformat(
                commit["commit"]["author"]["date"].replace("Z", "+00:00")
            )
            return (datetime.now().astimezone() - commit_date).days <= 30
        except (KeyError, ValueError):
            return False

    def _analyze_competition(self, project_name: str, description: str) -> str:
        """Analyze competitive landscape"""

        # Known competitive areas in ML/PyTorch ecosystem
        competitive_keywords = {
            "inference": ["TensorRT", "ONNX Runtime", "TensorFlow Lite"],
            "training": ["Horovod", "DeepSpeed", "FairScale"],
            "deployment": ["TorchServe", "MLflow", "Kubeflow"],
            "optimization": ["TensorRT", "Intel OpenVINO", "Apache TVM"],
            "distributed": ["Ray", "Dask", "Horovod"],
        }

        analysis = f"**Competition Analysis for {project_name}:**\n"
        description_lower = description.lower()

        for category, competitors in competitive_keywords.items():
            if category in description_lower:
                analysis += f"- **{category.title()}**: Competes with {', '.join(competitors)}\n"

        analysis += "\n**Market Position**: "
        if any(
            keyword in description_lower
            for keyword in ["inference", "serving", "deployment"]
        ):
            analysis += "Highly competitive space with established players"
        elif any(
            keyword in description_lower for keyword in ["research", "experimental"]
        ):
            analysis += "Research-focused, lower competitive pressure"
        else:
            analysis += "Moderate competitive landscape"

        return analysis

    def _analyze_portfolio_overlap(self, project_name: str, description: str) -> str:
        """Analyze overlap with Red Hat/IBM portfolio"""

        # Red Hat/IBM AI portfolio areas
        redhat_portfolio = [
            "OpenShift AI",
            "Watson",
            "CodeFlare",
            "Instructlab",
            "Granite models",
            "Red Hat Enterprise Linux AI",
        ]

        analysis = f"**Portfolio Overlap Analysis:**\n"
        description_lower = description.lower()

        overlaps = []
        if "serving" in description_lower or "deployment" in description_lower:
            overlaps.append("OpenShift AI serving capabilities")
        if "training" in description_lower or "distributed" in description_lower:
            overlaps.append("CodeFlare distributed training")
        if "model" in description_lower and "language" in description_lower:
            overlaps.append("Granite model ecosystem")

        if overlaps:
            analysis += f"- **Direct overlaps**: {', '.join(overlaps)}\n"
            analysis += "- **Strategic concern**: Medium to High\n"
        else:
            analysis += "- **Direct overlaps**: Minimal identified\n"
            analysis += "- **Strategic concern**: Low\n"

        analysis += f"- **Synergy potential**: {'High' if 'pytorch' in description_lower else 'Medium'}\n"

        return analysis

    def _generate_strategic_recommendation(
        self, project_name: str, health_score: float, competition: str, overlap: str
    ) -> str:
        """Generate strategic recommendation"""

        if health_score >= 75:
            health_factor = "Strong project health supports adoption"
        elif health_score >= 50:
            health_factor = "Moderate health, requires monitoring"
        else:
            health_factor = "Weak project health raises sustainability concerns"

        competitive_pressure = (
            "High" if "Highly competitive" in competition else "Medium"
        )
        overlap_concern = "High" if "Medium to High" in overlap else "Low"

        recommendation = f"**Strategic Recommendation:**\n"
        recommendation += f"- **Health Factor**: {health_factor}\n"
        recommendation += f"- **Competitive Pressure**: {competitive_pressure}\n"
        recommendation += f"- **Portfolio Overlap**: {overlap_concern} concern level\n"

        if health_score >= 60 and overlap_concern == "Low":
            recommendation += "- **Overall**: **FAVORABLE** for ecosystem inclusion"
        elif health_score >= 40:
            recommendation += "- **Overall**: **NEUTRAL** - requires deeper analysis"
        else:
            recommendation += "- **Overall**: **UNFAVORABLE** - significant concerns"

        return recommendation

    def _assess_risks(self, github_data: Dict, competition: str) -> str:
        """Assess project risks"""

        risks = []

        repo = github_data.get("repository", {})
        if repo.get("archived"):
            risks.append("Project is archived")

        contributors = github_data.get("contributors", [])
        if len(contributors) < 3:
            risks.append("Bus factor - too few contributors")

        if "Highly competitive" in competition:
            risks.append("High competitive pressure may limit adoption")

        if not risks:
            return "**Risk Assessment**: Low risk profile"

        return f"**Risk Assessment**:\n" + "\n".join(f"- {risk}" for risk in risks)

    def _assess_technical_merit(self, github_data: Dict, description: str) -> str:
        """Assess technical merit"""

        repo = github_data.get("repository", {})

        merit_factors = []
        if repo.get("language") == "Python":
            merit_factors.append("Python-based (PyTorch ecosystem aligned)")
        if "performance" in description.lower():
            merit_factors.append("Performance-focused")
        if "scalable" in description.lower():
            merit_factors.append("Scalability considerations")

        if not merit_factors:
            merit_factors.append("Standard implementation approach")

        return "**Technical Merit**:\n" + "\n".join(
            f"- {factor}" for factor in merit_factors
        )

    def _assess_community_engagement(self, github_data: Dict) -> str:
        """Assess community engagement"""

        repo = github_data.get("repository", {})
        issues = github_data.get("issues", [])

        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        open_issues = len(issues)

        engagement_level = "Low"
        if stars > 1000 or forks > 100:
            engagement_level = "High"
        elif stars > 100 or forks > 20:
            engagement_level = "Medium"

        return f"**Community Engagement**: {engagement_level} ({stars} stars, {forks} forks, {open_issues} open issues)"

    def _assess_maintainer_credibility(self, github_data: Dict) -> str:
        """Assess maintainer credibility"""

        repo = github_data.get("repository", {})
        contributors = github_data.get("contributors", [])

        owner = repo.get("owner", {}).get("login", "Unknown")
        top_contributors = contributors[:3] if contributors else []

        # Known credible organizations in AI/ML space
        credible_orgs = [
            "pytorch",
            "facebook",
            "google",
            "microsoft",
            "nvidia",
            "huggingface",
        ]

        if any(org in owner.lower() for org in credible_orgs):
            credibility = "High - established organization"
        elif len(contributors) >= 10:
            credibility = "Medium - active contributor base"
        else:
            credibility = "Unknown - requires investigation"

        return f"**Maintainer Credibility**: {credibility} (Owner: {owner})"


class PyTorchTACAdvisor:
    """Main PyTorch TAC voting advisor"""

    def __init__(self):
        self.console = Console()
        self.analyzer = PyTorchEcosystemAnalyzer()

    async def generate_voting_recommendation(
        self,
        project_name: str,
        github_url: str,
        description: str = "",
        context: str = "",
    ) -> VotingRecommendation:
        """Generate comprehensive voting recommendation"""

        self.console.print(
            Panel(
                f"[bold blue]PyTorch TAC Voting Analysis[/bold blue]\n"
                f"Project: {project_name}\n"
                f"Analyst: Jeremy Eder, Distinguished Engineer, Red Hat",
                title="Strategic Analysis",
            )
        )

        # Perform project analysis
        analysis = await self.analyzer.analyze_project(
            project_name, github_url, description
        )

        # Generate recommendation
        recommendation = self._determine_vote(analysis)
        confidence = self._assess_confidence(analysis)

        # Generate executive summary
        executive_summary = self._generate_executive_summary(analysis, recommendation)

        # Key decision factors
        key_factors = self._extract_key_factors(analysis)

        # Alignment assessments
        red_hat_alignment = self._assess_red_hat_alignment(analysis)
        ibm_alignment = self._assess_ibm_alignment(analysis)

        # Raghu consultation notes
        raghu_notes = self._generate_raghu_consultation_notes(analysis, recommendation)

        return VotingRecommendation(
            project_name=project_name,
            recommendation=recommendation,
            confidence=confidence,
            executive_summary=executive_summary,
            key_factors=key_factors,
            red_hat_alignment=red_hat_alignment,
            ibm_alignment=ibm_alignment,
            raghu_consultation_notes=raghu_notes,
        )

    def _determine_vote(self, analysis: ProjectAnalysis) -> str:
        """Determine voting recommendation"""

        health_score = analysis.health_score

        # Parse strategic recommendation
        if "FAVORABLE" in analysis.strategic_recommendation:
            return "APPROVE"
        elif "UNFAVORABLE" in analysis.strategic_recommendation:
            return "REJECT"
        else:
            return "ABSTAIN"

    def _assess_confidence(self, analysis: ProjectAnalysis) -> str:
        """Assess confidence in recommendation"""

        if analysis.health_score >= 70:
            return "HIGH"
        elif analysis.health_score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_executive_summary(
        self, analysis: ProjectAnalysis, recommendation: str
    ) -> str:
        """Generate executive summary markdown"""

        summary = f"""# PyTorch TAC Voting Recommendation: {analysis.name}

## Executive Summary

**Recommendation**: {recommendation}  
**Project Health Score**: {analysis.health_score:.1f}/100  
**Strategic Alignment**: {'Favorable' if recommendation == 'APPROVE' else 'Concerning' if recommendation == 'REJECT' else 'Neutral'}

## Key Assessment

{analysis.strategic_recommendation}

## Competition & Portfolio Impact

{analysis.competition_analysis}

{analysis.portfolio_overlap}

## Risk Profile

{analysis.risk_assessment}

## Technical Assessment

{analysis.technical_merit}

{analysis.community_engagement}

{analysis.maintainer_credibility}

## Strategic Context

This analysis considers Red Hat's AI strategy, IBM Research priorities, and PyTorch ecosystem health. The recommendation aligns with our portfolio strategy while supporting the broader PyTorch community mission.

---
*Analysis prepared for Jeremy Eder, PyTorch TAC Member*  
*In consultation with Raghu Ganti, IBM Research*
"""

        return summary

    def _extract_key_factors(self, analysis: ProjectAnalysis) -> List[str]:
        """Extract key decision factors"""

        factors = []

        if analysis.health_score >= 70:
            factors.append(f"Strong project health ({analysis.health_score:.1f}/100)")
        elif analysis.health_score <= 30:
            factors.append(f"Weak project health ({analysis.health_score:.1f}/100)")

        if "Medium to High" in analysis.portfolio_overlap:
            factors.append("Significant portfolio overlap concerns")

        if "Highly competitive" in analysis.competition_analysis:
            factors.append("Operates in highly competitive market")

        if "High - established organization" in analysis.maintainer_credibility:
            factors.append("Credible maintainer organization")

        if "archived" in analysis.risk_assessment.lower():
            factors.append("Project maintenance risks identified")

        return factors

    def _assess_red_hat_alignment(self, analysis: ProjectAnalysis) -> str:
        """Assess alignment with Red Hat strategy"""

        alignment = "**Red Hat Strategic Alignment:**\n"

        if "serving" in analysis.description.lower():
            alignment += "- Aligns with OpenShift AI serving strategy\n"
            alignment += "- **Score**: High alignment\n"
        elif "pytorch" in analysis.description.lower():
            alignment += "- Supports PyTorch ecosystem that powers RHOAI\n"
            alignment += "- **Score**: Medium-High alignment\n"
        else:
            alignment += "- General AI ecosystem benefit\n"
            alignment += "- **Score**: Medium alignment\n"

        return alignment

    def _assess_ibm_alignment(self, analysis: ProjectAnalysis) -> str:
        """Assess alignment with IBM strategy"""

        alignment = "**IBM Strategic Alignment:**\n"

        if "research" in analysis.description.lower():
            alignment += "- Aligns with IBM Research priorities\n"
            alignment += "- **Score**: High alignment\n"
        elif "enterprise" in analysis.description.lower():
            alignment += "- Supports Watson and enterprise AI\n"
            alignment += "- **Score**: Medium-High alignment\n"
        else:
            alignment += "- Contributes to broader AI ecosystem\n"
            alignment += "- **Score**: Medium alignment\n"

        return alignment

    def _generate_raghu_consultation_notes(
        self, analysis: ProjectAnalysis, recommendation: str
    ) -> str:
        """Generate consultation notes for Raghu Ganti"""

        notes = f"""**Consultation Notes for Raghu Ganti (IBM Research):**

**Recommended Discussion Points:**
1. Project health score: {analysis.health_score:.1f}/100 - {'Strong' if analysis.health_score >= 60 else 'Weak'}
2. IBM Research alignment opportunities
3. Potential collaboration with Watson/Granite teams
4. Long-term maintenance sustainability

**Questions for IBM Research Perspective:**
- Does this align with current IBM AI research priorities?
- Any known collaborations or conflicts with existing IBM projects?
- Resource commitment implications for IBM?

**Recommended Vote:** {recommendation}
**Confidence Level:** {self._assess_confidence(analysis)}

*This analysis supports your decision-making as the official IBM voting representative.*
"""

        return notes

    def display_recommendation(self, recommendation: VotingRecommendation):
        """Display formatted recommendation to console"""

        # Main recommendation panel
        self.console.print(
            Panel(
                f"[bold]Recommendation: {recommendation.recommendation}[/bold]\n"
                f"Confidence: {recommendation.confidence}\n"
                f"Project: {recommendation.project_name}",
                title="PyTorch TAC Voting Decision",
                border_style=(
                    "green"
                    if recommendation.recommendation == "APPROVE"
                    else (
                        "red" if recommendation.recommendation == "REJECT" else "yellow"
                    )
                ),
            )
        )

        # Key factors table
        if recommendation.key_factors:
            table = Table(title="Key Decision Factors")
            table.add_column("Factor", style="cyan")

            for factor in recommendation.key_factors:
                table.add_row(factor)

            self.console.print(table)

        # Executive summary
        self.console.print(Markdown(recommendation.executive_summary))

        # Alignment assessments
        self.console.print(
            Panel(
                f"{recommendation.red_hat_alignment}\n\n{recommendation.ibm_alignment}",
                title="Strategic Alignment",
            )
        )

        # Raghu consultation
        self.console.print(
            Panel(
                recommendation.raghu_consultation_notes,
                title="IBM Research Consultation",
            )
        )

    def save_analysis(self, recommendation: VotingRecommendation, output_path: str):
        """Save analysis to file"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{recommendation.project_name.replace(' ', '_')}_{timestamp}.md"
        filepath = Path(output_path) / filename

        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            f.write(recommendation.executive_summary)
            f.write("\n\n## Strategic Alignment Details\n\n")
            f.write(recommendation.red_hat_alignment)
            f.write("\n\n")
            f.write(recommendation.ibm_alignment)
            f.write("\n\n## IBM Research Consultation\n\n")
            f.write(recommendation.raghu_consultation_notes)
            f.write(f"\n\n## Analysis Metadata\n\n")
            f.write(f"- **Generated**: {datetime.now().isoformat()}\n")
            f.write(f"- **Analyst**: Jeremy Eder, Distinguished Engineer, Red Hat\n")
            f.write(f"- **Recommendation**: {recommendation.recommendation}\n")
            f.write(f"- **Confidence**: {recommendation.confidence}\n")

        self.console.print(f"[green]Analysis saved to: {filepath}[/green]")


@click.command()
@click.argument("project_name")
@click.argument("github_url")
@click.option("--description", "-d", help="Project description")
@click.option("--context", "-c", help="Additional context for the vote")
@click.option(
    "--output", "-o", default="./analysis", help="Output directory for analysis"
)
@click.option("--github-token", envvar="GITHUB_TOKEN", help="GitHub API token")
def main(
    project_name: str,
    github_url: str,
    description: str,
    context: str,
    output: str,
    github_token: str,
):
    """
    PyTorch TAC Voting Advisor

    Generates strategic voting recommendations for PyTorch Technical Advisory Committee decisions.

    Examples:
        pytorch-tac-advisor "New ML Framework" "https://github.com/example/ml-framework"
        pytorch-tac-advisor "Inference Engine" "https://github.com/example/engine" -d "Fast inference for PyTorch models"
    """

    async def run_analysis():
        console = Console()

        try:
            # Initialize advisor
            advisor = PyTorchTACAdvisor()

            # Generate recommendation
            recommendation = await advisor.generate_voting_recommendation(
                project_name=project_name,
                github_url=github_url,
                description=description or "",
                context=context or "",
            )

            # Display results
            advisor.display_recommendation(recommendation)

            # Save analysis
            advisor.save_analysis(recommendation, output)

        except KeyboardInterrupt:
            console.print("\n[yellow]Analysis interrupted by user[/yellow]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error during analysis: {str(e)}[/red]")
            sys.exit(1)

    # Run the async analysis
    asyncio.run(run_analysis())


if __name__ == "__main__":
    main()
