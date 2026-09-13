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
9. Store the native DepAnalyzer JSON scan snapshot as security/depanalyzer-results.json.

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
Submit the target project's manifest content to DepAnalyzer's scan API.
For Maven projects, submit `pom.xml` with filename `pom.xml` and ecosystem `maven`.
For Gradle projects, submit the dependency manifest supported by DepAnalyzer, if available.
For npm projects, submit `package.json`, `package-lock.json`, or `npm-shrinkwrap.json` with the appropriate filename.
Use DepAnalyzer's native JSON response as the source of truth.
Preserve the response fields required for remediation, including `summary`, `vulnerabilities`, `fixes`, `grouped_packages`, `graph`, `dependency_tree`, and `scan_timestamp`.
Do not fall back to OWASP Dependency-Check unless the user explicitly asks for it.

Completion
Report:
Detected ecosystem
SBOM generation status
Location of security/bom.json
Vulnerability scan status
Location of security/depanalyzer-results.json
Any errors that prevented successful SBOM generation or vulnerability scanning
