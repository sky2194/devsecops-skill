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
Gradle (SBOM generation only — see DepAnalyzer requirements)
npm

Workflow
1. Inspect the target project and determine its package ecosystem (Maven, Gradle, or npm).
2. Resolve and inspect only the dependency graph for the detected project:
   - Maven: use the project's `pom.xml` and Maven dependency tree.
   - Gradle: use the project's Gradle dependency graph.
   - npm: use the project's `package-lock.json`, `npm-shrinkwrap.json`, or installed dependency tree.
3. Ensure the appropriate CycloneDX SBOM generation mechanism is available for the detected ecosystem.
4. Generate the SBOM using CycloneDX JSON format from the target project's dependency graph.
5. Create the security directory if it does not exist.
6. Store the generated SBOM as security/bom.json.
7. Run DepAnalyzer against the target project's manifest, per the DepAnalyzer requirements below.
8. Store the native DepAnalyzer JSON scan snapshot as security/depanalyzer-results.json.

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
API endpoint: https://www.depanalyzer.com/api/scan (POST, JSON body, no authentication required).
Request body: {"content": "<raw manifest file contents>", "filename": "<manifest filename>", "ecosystem": "<maven|npm|pypi>"}.
For Maven projects, submit `pom.xml` content with filename `pom.xml` and ecosystem `maven`.
For npm projects, submit `package.json` or `package-lock.json` content with the matching filename.
DepAnalyzer does not currently support Gradle. For Gradle projects, generate the SBOM (steps 3–6) as normal, skip the DepAnalyzer scan, and report this limitation clearly instead of guessing or falling back silently.
Use DepAnalyzer's native JSON response as the source of truth.
Preserve the response fields required for remediation, including `summary`, `vulnerabilities`, `fixes`, `grouped_packages`, `graph`, `dependency_tree`, and `scan_timestamp`.
Do not fall back to OWASP Dependency-Check unless the user explicitly asks for it.

Completion
Report:
Detected ecosystem
SBOM generation status
Location of security/bom.json
Vulnerability scan status (or the Gradle limitation, if applicable)
Location of security/depanalyzer-results.json
Any errors that prevented successful SBOM generation or vulnerability scanning