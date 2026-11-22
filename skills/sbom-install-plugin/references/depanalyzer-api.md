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

Build the JSON body with a JSON encoder (e.g. `jq --rawfile` or Python `json.dumps`) so the manifest is escaped correctly; never paste file contents into a shell string.

Write the response to a temporary file and move it into place only after it validates, so a failed request never overwrites or leaves an error body in `security/depanalyzer-results.json`:

```bash
mkdir -p security
TMP=$(mktemp)
if jq -n --rawfile c pom.xml '{content:$c, filename:"pom.xml", ecosystem:"maven"}' \
     | curl -sS --fail --max-time 120 -X POST https://www.depanalyzer.com/api/scan \
         -H 'Content-Type: application/json' --data-binary @- -o "$TMP" \
   && jq -e 'has("vulnerabilities")' "$TMP" >/dev/null; then
  mv "$TMP" security/depanalyzer-results.json
else
  echo "DepAnalyzer scan failed"; cat "$TMP"; rm -f "$TMP"
fi
```

For npm, substitute `package-lock.json` (or `package.json`) for both the `--rawfile` path and `filename`, and `ecosystem:"npm"`.

## Response

Keep the native response unmodified. Fields downstream skills rely on: `summary`, `vulnerabilities`, `fixes`, `grouped_packages`, `graph`, `dependency_tree`, `scan_timestamp`. Validate that the response parses as JSON and contains `vulnerabilities` before saving it and reporting success. On failure, show the error body to the user but do not save it as the results file.
