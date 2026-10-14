# DepAnalyzer API

- Endpoint: `POST https://www.depanalyzer.com/api/scan` (JSON body, no authentication)
- Body: `{"content": "<raw manifest text>", "filename": "<manifest filename>", "ecosystem": "<maven|npm|pypi>"}`

## What to submit

| Project | filename | ecosystem |
|---|---|---|
| Maven | `pom.xml` | `maven` |
| npm | `package-lock.json` (preferred) or `package.json` | `npm` |
| Gradle | not supported — skip the scan | — |

If `package-lock.json` exceeds DepAnalyzer's dependency limit, submit `package.json` instead and say so in the report.

## Building the request safely

Build the JSON body with a JSON encoder (e.g. `jq -Rs` or Python `json.dumps`) so the manifest is escaped correctly; never paste file contents into a shell string.

```bash
jq -n --rawfile c pom.xml '{content:$c, filename:"pom.xml", ecosystem:"maven"}' \
 | curl -sS --fail-with-body -X POST https://www.depanalyzer.com/api/scan \
   -H 'Content-Type: application/json' -d @- -o security/depanalyzer-results.json
```

## Response

Keep the native response unmodified. Fields downstream skills rely on: `summary`, `vulnerabilities`, `fixes`, `grouped_packages`, `graph`, `dependency_tree`, `scan_timestamp`. Validate that the file parses as JSON and contains `vulnerabilities` before reporting success.
