import json
from pathlib import Path

def parse_sarif(sarif_path):
    path = Path(sarif_path)
    if not path.exists():
        raise FileNotFoundError(f"SARIF file not found: {sarif_path}")


    with path.open("r", encoding="utf-8") as file:
         sarif = json.load(file)   


    findings = []
    for run in sarif.get("runs", []):
        rules = {
            rule.get("id"): rule
            for rule in run.get("tool", {}).get("driver", {}).get("rules", [])  
        }

    for result in run.get("results", []):
        rule_id = result.get("ruleId")
        rule = rules.get(rule_id, {})

        findings.append({
            "vulnerability_id": rule.get("id"),
            "message": result.get("message", {}).get("text"),
            "severity": rule.get("properties", {}).get("security-severity"),
            "description": rule.get("fullDescription", {}).get("text"),
            "locations": result.get("locations", []),
        })

    return findings

    if __name__ == "__main__":
        results = parse_sarif("security/results.sarif")

        for finding in results:
            print(finding)


         