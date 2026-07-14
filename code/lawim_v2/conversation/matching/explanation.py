from __future__ import annotations

from .results import Match, MatchExplanation


class ExplanationGenerator:
    def generate(self, match: Match) -> str:
        if not match.explanations:
            return "No matching criteria were evaluated."

        parts: list[str] = []
        score_pct = round(match.global_score * 100)

        parts.append(f"Score: {score_pct}%")

        matched = match.matched_criteria_count
        total = match.total_criteria_count
        parts.append(f"Criteria met: {matched}/{total}")

        strong = [e for e in match.explanations if e.score >= 0.7]
        weak = [e for e in match.explanations if e.score < 0.3 and not e.is_match]

        if strong:
            parts.append("Strong matches: " + ", ".join(
                f"{e.dimension} ({e.details})" for e in strong[:3]
            ))

        if weak:
            parts.append("Gaps: " + ", ".join(
                f"{e.dimension} ({e.details})" for e in weak[:3]
            ))

        return " | ".join(parts)

    def generate_detailed(self, match: Match) -> str:
        lines: list[str] = []
        lines.append(f"Match: {match.title}")
        lines.append(f"Overall Score: {round(match.global_score * 100)}%")
        lines.append(f"Criteria Matched: {match.matched_criteria_count}/{match.total_criteria_count}")
        lines.append("")

        sorted_explanations = sorted(
            match.explanations, key=lambda e: e.weighted_score, reverse=True
        )
        for exp in sorted_explanations:
            pct = round(exp.score * 100)
            icon = "✓" if exp.is_match else "✗"
            lines.append(f"  {icon} {exp.dimension}: {pct}% ({exp.details})")

        lines.append("")
        return "\n".join(lines)

    def generate_html(self, match: Match) -> str:
        parts: list[str] = []
        parts.append("<div class='match-result'>")
        parts.append(f"<h3>{match.title}</h3>")
        parts.append(f"<p><strong>Score: {round(match.global_score * 100)}%</strong></p>")
        parts.append(f"<p>Criteria met: {match.matched_criteria_count}/{match.total_criteria_count}</p>")
        parts.append("<ul>")
        for exp in sorted(match.explanations, key=lambda e: e.weighted_score, reverse=True):
            icon = "&#9989;" if exp.is_match else "&#10060;"
            pct = round(exp.score * 100)
            parts.append(f"<li>{icon} <strong>{exp.dimension}:</strong> {pct}% — {exp.details}</li>")
        parts.append("</ul>")
        parts.append("</div>")
        return "\n".join(parts)
