import json
import sys


def validate_plan(file_path):
    with open(file_path, "r") as file:
        plan = json.load(file)

    resource_changes = plan.get("resource_changes", [])

    for resource in resource_changes:
        address = resource.get("address", "unknown")
        change = resource.get("change", {})
        actions = change.get("actions", [])

        
        if actions == ["create"]:
            continue

       
        if actions == ["update"]:
            before = change.get("before", {})
            after = change.get("after", {})

            before_tags = before.get("tags", {}) or {}
            after_tags = after.get("tags", {}) or {}

            changed_attributes = set()

            all_tags = set(before_tags.keys()) | set(after_tags.keys())

            for tag in all_tags:
                if before_tags.get(tag) != after_tags.get(tag):
                    changed_attributes.add(tag)

            if changed_attributes == {"GitCommitHash"}:
                continue

            print(
                f"PLAN REJECTED: {address} modifies attributes other than "
                f"the GitCommitHash tag."
            )
            return False

        
        print(
            f"PLAN REJECTED: {address} has unsupported actions: {actions}"
        )
        return False

    print("PLAN APPROVED: only allowed create/update actions were found.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    if validate_plan(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)
