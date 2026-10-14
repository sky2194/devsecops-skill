# sbom-install-plugin

Generates a CycloneDX SBOM (`security/bom.json`) and a DepAnalyzer vulnerability scan (`security/depanalyzer-results.json`) for Maven, Gradle, or npm projects.

- Gradle: SBOM only (DepAnalyzer does not support Gradle).
- Privacy: the manifest file is uploaded to depanalyzer.com for scanning. DepAnalyzer is by the same author as this skill.
- Pair with `sbom-fix-vulnerability` to patch the findings.
- Requires the project's build tool (Node/npm, Maven + JDK, or Gradle) and network access.
