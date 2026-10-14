# CycloneDX commands per ecosystem

Run from the project root. Write the final file to `security/bom.json`.

## npm

```bash
mkdir -p security
npx --yes @cyclonedx/cyclonedx-npm --output-format JSON --output-file security/bom.json
```

Requires Node.js and an installed dependency tree (`npm install` or `npm ci` already run; do not run it silently if `node_modules` is absent — ask first). Add `--omit dev` only if the user wants production dependencies only. Verified output: CycloneDX 1.6 JSON.

## Maven

```bash
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom -DoutputFormat=json -DoutputName=bom
mkdir -p security && cp target/bom.json security/bom.json
```

Run from the root (parent) POM so multi-module projects produce one aggregate BOM. Invoking the plugin by coordinates avoids editing `pom.xml`. Requires Maven and a JDK.

## Gradle

Use the CycloneDX Gradle plugin through an init script so `build.gradle` is not modified:

```bash
cat > /tmp/cdx-init.gradle <<'GRADLE'
initscript {
  repositories { gradlePluginPortal() }
  dependencies { classpath 'org.cyclonedx:cyclonedx-gradle-plugin:+' }
}
allprojects { apply plugin: org.cyclonedx.gradle.CyclonedxPlugin }
GRADLE
./gradlew --init-script /tmp/cdx-init.gradle cyclonedxBom
```

Copy the generated `build/reports/bom.json` (location varies by plugin version — check `build/reports/`) to `security/bom.json`. Use `gradle` if there is no wrapper. If the command fails, report the error; do not hand-write a BOM.

## Pin versions

Prefer a pinned tool version when reproducibility matters (e.g. `@cyclonedx/cyclonedx-npm@<version>`).
