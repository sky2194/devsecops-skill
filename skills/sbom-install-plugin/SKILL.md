---
name: sbom-install-plugin
description: Generate an SBOM and vulnerability scan results for a Maven, Gradle or npm project using CycloneDX and DepAnalyzer.
argument-hint: "[path to project]"
license: MIT
---
SBOM Install Plugin Skill

Purpose
Generate an SBOM and vulnerability scan results for the target application.

Supported ecosystems
Maven
Gradle
npm

Workflow
1. Inspect the target project and identify its package ecosystem (Maven, Gradle, or npm).
2. Determine whether the project uses Maven, Gradle, or npm.
3. Resolve and inspect only the dependency graph for the detected project:
   - Maven: use the project's `pom.xml` and Maven dependency tree.
   - Gradle: use the project's Gradle dependency graph.
   - npm: use the project's `package-lock.json`, `npm-shrinkwrap.json`, or installed dependency tree.
4. Ensure the appropriate CycloneDX SBOM generation mechanism is available for the detected ecosystem.
5. Generate the SBOM using CycloneDX JSON format from the target project's dependency graph.
6. Create the security directory if it does not exist.
7. Store the generated SBOM as security/bom.json.
8. Run DepAnalyzer against the target project's manifest or generated SBOM.
9. Generate vulnerability scan results in SARIF format. If DepAnalyzer returns JSON instead of SARIF, convert the DepAnalyzer findings into SARIF 2.1.0 before continuing.
10. Store the results as security/results.sarif.

Requirements
Use the actual project dependency information.
Generate real CycloneDX SBOM data.
Generate real DepAnalyzer vulnerability scan results.
Limit analysis to dependencies declared or resolved by the target project.
Do not scan unrelated directories, global package caches, system packages, or dependencies from other projects.
Do not create fake or hard-coded SBOM or vulnerability scan results.
Preserve the target project's existing source code and dependency definitions.
Do not modify application source code or dependencies as part of this skill.

DepAnalyzer requirements
Use DepAnalyzer as the primary vulnerability scanner.
For Maven projects, submit the target project's `pom.xml` or the generated `security/bom.json` to DepAnalyzer.
Use DepAnalyzer's returned package, version, vulnerability, severity, path, and fix recommendation fields as the source of truth.
If DepAnalyzer cannot produce SARIF directly, transform its scan response into SARIF 2.1.0 while preserving CVE identifiers, affected packages, fixed versions, severity, and dependency paths.
Do not fall back to OWASP Dependency-Check unless the user explicitly asks for it.

Completion
Report:
Detected ecosystem
SBOM generation status
Location of security/bom.json
Vulnerability scan status
Location of security/results.sarif
Any errors that prevented successful SBOM generation or vulnerability scanning
