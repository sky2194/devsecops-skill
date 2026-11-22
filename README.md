# devsecops-skill

Agent skills for SBOM generation and vulnerability remediation. Works with any agent that supports the SKILL.md standard (Claude Code, GitHub Copilot, Codex CLI, Cursor, and others).

## Skills

| Skill | What it does |
|---|---|
| `sbom-install-plugin` | Generates a CycloneDX SBOM and a DepAnalyzer vulnerability scan for Maven, Gradle, or npm projects. |
| `sbom-fix-vulnerability` | Reads the scan results and patches vulnerable dependencies in `pom.xml` or `package.json`. |

## Install

```bash
gh skill install sky2194/devsecops-skill sbom-install-plugin
gh skill install sky2194/devsecops-skill sbom-fix-vulnerability
```

Requires GitHub CLI v2.90.0 or later. Or copy a `skills/<name>/` folder into your agent's skills directory.

## Typical flow

1. `sbom-install-plugin` → writes `security/bom.json` and `security/depanalyzer-results.json` (gitignored).
2. `sbom-fix-vulnerability` → patches the manifest and prints a report.
3. Regenerate your lockfile, re-scan, run tests, review the diff.

## Limitations

- Gradle: SBOM only; DepAnalyzer does not support Gradle, so there is no scan or auto-fix.
- Fix skill supports `pom.xml` and `package.json` only.
- Lockfiles are not edited; regenerate them after patching.

## Data and privacy

The scan uploads your manifest file contents to [depanalyzer.com](https://www.depanalyzer.com) (no authentication). DepAnalyzer is by the same author as these skills. No other data leaves your machine.

## License

MIT — see [LICENSE](LICENSE).
