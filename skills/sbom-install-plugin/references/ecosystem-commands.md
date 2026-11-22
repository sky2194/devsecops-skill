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
mvn org.cyclonedx:cyclonedx-maven-plugin:2.9.1:makeAggregateBom -DoutputFormat=json -DoutputName=bom
mkdir -p security && cp target/bom.json security/bom.json
```

Run from the root (parent) POM so multi-module projects produce one aggregate BOM. Invoking the plugin by coordinates avoids editing `pom.xml`. Requires Maven and a JDK.

## Gradle

Use the CycloneDX Gradle plugin through an init script so `build.gradle` is not modified:

```bash
CDX_TMP=$(mktemp -d)
INIT="$CDX_TMP/cdx-init.gradle"
cat > "$INIT" <<'GRADLE'
initscript {
  repositories { gradlePluginPortal() }
  dependencies { classpath 'org.cyclonedx:cyclonedx-gradle-plugin:1.10.0' }
}
allprojects { apply plugin: org.cyclonedx.gradle.CycloneDxPlugin }
GRADLE
./gradlew --init-script "$INIT" cyclonedxBom
mkdir -p security && cp build/reports/bom.json security/bom.json
rm -rf "$CDX_TMP"
```

The plugin class is `CycloneDxPlugin` (capital D); a wrong class name fails the init script. The version is pinned to the 1.x line because plugin 2.x/3.x changed task names and output locations; with 1.10.0 the root project's aggregate BOM is `build/reports/bom.json`. Use `gradle` if there is no wrapper. If the command fails, report the error; do not hand-write a BOM.

## Pin versions

The Maven and Gradle commands above pin the plugin version. Do not replace them with unpinned or dynamic versions (`+`, `latest`): a new major release can change task names and output paths, and an unpinned build plugin is a supply-chain risk. For npm, pin the tool too when reproducibility matters (e.g. `@cyclonedx/cyclonedx-npm@<version>`).
