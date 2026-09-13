# devsecops-skill

Agentic AI Skills for SBOM generation and vulnerability remediation, built for GitHub Copilot.

## Skills

- **sbom-install-plugin** — Generates an SBOM and vulnerability scan results (CycloneDX + DepAnalyzer) for Maven, Gradle, or npm projects.
- **sbom-fix-vulnerability** — Analyzes DepAnalyzer JSON vulnerability findings and patches the affected dependency file (`pom.xml`, `package.json`) with a fixed version.

## Install

```bash
gh skill install sky2194/devsecops-skill sbom-install-plugin
gh skill install sky2194/devsecops-skill sbom-fix-vulnerability
```

Requires GitHub CLI v2.90.0 or later.

## License

MIT — see [LICENSE](LICENSE).
