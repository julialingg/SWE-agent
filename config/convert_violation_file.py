import json

with open("./config/typescript_localhost_8000_tools_violation.json") as f:
    data = json.load(f)
  
description = []

for i, violation in enumerate(data["results"], 1):
    rule = violation.get("ruleId", "")
    msg = violation.get("message", "")
    snippet = violation.get("snippet", "").strip()
    help_url = violation.get("help", "")
    path_dom = violation.get("path", {}).get("dom", "")
    path_aria = violation.get("path", {}).get("aria", "")
    message_args = violation.get("messageArgs", [])
    api_args = violation.get("apiArgs", [])

    description.append(
        f"[{i}] Violation of rule `{rule}`: {msg}\n"
        f"  DOM Path: {path_dom}\n"
        f"  ARIA Path: {path_aria}\n"
        f"  Code: {snippet}\n"
        f"  messageArgs: {message_args}\n"
        f"  apiArgs: {api_args}\n"
        f"  Learn more: {help_url}"
    )

final_text = "\n\n".join(description)

with open("problem_statement_typescript_tools.txt", "w") as f:
    f.write(final_text)
