---
name: sbom-install-plugin
description: Generate an SBOM and Vulnerability scan results for a Maven, Gradle or npm project using CycloneDX and OWASP Dependency-Check
---
SBOM Install Plugin Skill

Purpose
Generate an SBOM and Vulnerability scan results for the target application.

Supported ecosystems
Maven
Gradle
npm

Workflow
1. Inspect the target project and identify its package ecosystem (Maven, Gradle, or npm).
2. Determine whether the project uses Maven, Gradle, or npm.
3. Ensure the appropriate CycloneDX SBOM generation mechanism is available for the detected ecosystem.
4. Generate the SBOM using CycloneDX JSON format.
5. Create the security directory if it does not exist.
6. Store the generated SBOM as security/bom.json.
7. Run OWASP Dependency-Check against the target project/SBOM as appropriate.
8. Generate the vulnerability scan results in  SARIF format.
9. Store the results as security/results.sarif.

Requirements
Use the actual project dependency information.
Generate real CycloneDX SBOM data.
Generate real OWASP Dependency-Check vulnerability scan results.
Do not create fake or hard-coded SBOM or vulnerability scan results.
Preserve the target project's existing source code and dependency definitions.
Do not modify application source code or dependencies as part of this skill.

Completion
Report:
Detected ecosystem
SBOM generation status
Location of security/bom.json
Vulnerability scan status
Location of security/results.sarif
Any errors that prevented successful SBOM generation or vulnerability scanning