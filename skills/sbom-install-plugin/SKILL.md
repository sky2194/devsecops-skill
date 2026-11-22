---
name: sbom-install-plugin
description: Generates a CycloneDX SBOM and a vulnerability scan for a Maven, Gradle, or npm project. Use when the user asks to create an SBOM, scan dependencies for vulnerabilities or CVEs, or run an SCA scan on a project.
when_to_use: |
  - User asks for an SBOM, bill of materials, or CycloneDX output
  - User asks to scan a project's dependencies for vulnerabilities or CVEs
  - User wants scan results as input for sbom-fix-vulnerability
  - Do NOT use to patch dependencies (use sbom-fix-vulnerability)
argument-hint: "[path to project]"
license: MIT
external_urls:
  - https://www.depanalyzer.com/api/scan
---

# SBOM Install Plugin

Generate a CycloneDX SBOM and a DepAnalyzer vulnerability scan for the target project. Read-only with respect to source code and dependency definitions.

## Data disclosure

The vulnerability scan uploads the contents of the project's manifest (`pom.xml`, `package.json`, or `package-lock.json`) to `https://www.depanalyzer.com/api/scan` (no authentication). Tell the user this before the first upload. If they decline, stop after the SBOM and report the scan as skipped.

## Supported ecosystems

| Ecosystem | SBOM | DepAnalyzer scan |
|---|---|---|
| Maven | yes | yes (`pom.xml`) |
| npm | yes | yes (`package.json` or `package-lock.json`) |
| Gradle | yes | no — not supported by DepAnalyzer; report this, do not guess or fall back silently |

## Workflow

1. Determine the project root from the argument (default: current directory). Detect the ecosystem from `pom.xml`, `build.gradle(.kts)`, or `package.json`. If several project roots or ecosystems are found, list them and ask which to scan; process each selected root separately, writing to that root's own `security/` directory.
2. Generate the SBOM with the ecosystem's CycloneDX tool, JSON format. Exact commands are in [references/ecosystem-commands.md](references/ecosystem-commands.md). Do not edit build files permanently to do this.
3. Create `security/` if needed and store the SBOM as `security/bom.json`. Check it is valid JSON with `bomFormat` = `CycloneDX` and a non-empty `components` array; otherwise report the failure.
4. Run the DepAnalyzer scan per [references/depanalyzer-api.md](references/depanalyzer-api.md) (skip for Gradle).
5. Store the unmodified DepAnalyzer JSON response as `security/depanalyzer-results.json`. A response with zero vulnerabilities is a valid result; still write it.
6. Ensure the project's `.gitignore` excludes `security/bom.json` and `security/depanalyzer-results.json`. Create `.gitignore` if missing; do not duplicate existing entries.

## Rules

- Use real project data only. Never fabricate or hard-code SBOM or scan results.
- Analyze only dependencies declared or resolved by the target project. Do not scan unrelated directories, global caches, or system packages.
- Do not modify application source code or dependency definitions.
- Do not stage or commit the two generated files.
- Do not fall back to OWASP Dependency-Check unless the user explicitly asks.
- On network errors, timeouts, or non-2xx responses: retry once, then report the error and stop. Never substitute made-up results.

## Completion report

- Detected ecosystem and project root
- SBOM status and path (`security/bom.json`), component count
- Scan status, or the Gradle limitation, or "skipped by user"; path (`security/depanalyzer-results.json`) and vulnerability count from `summary`
- Confirmation both files are gitignored
- Any errors
- Next step: run `sbom-fix-vulnerability` to patch findings
