import json
import sys


def check_plan(file_path):
    with open(file_path, "r") as file:
        plan = json.load(file)

    resource_changes = plan.get("resource_changes", [])

    for resource in resource_changes:
        address = resource.get("address", "unknown")
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Create is allowed
        if actions == ["create"]:
            continue

        # Delete or replacement is NOT allowed
        if "delete" in actions:
            print(f"BLOCK: {address} has delete/destroy action")
            return False

        # Update is allowed only when GitCommitHash tag changes
        if actions == ["update"]:
            before = change.get("before", {})
            after = change.get("after", {})

            before_tags = before.get("tags", {}) or {}
            after_tags = after.get("tags", {}) or {}

            changed_tags = set(before_tags.keys()) | set(after_tags.keys())

            for tag in changed_tags:
                if tag != "GitCommitHash":
                    if before_tags.get(tag) != after_tags.get(tag):
                        print(
                            f"BLOCK: {address} modifies tag '{tag}'. "
                            "Only GitCommitHash is allowed."
                        )
                        return False

            # Check non-tag attributes
            before_copy = dict(before)
            after_copy = dict(after)

            before_copy.pop("tags", None)
            after_copy.pop("tags", None)

            if before_copy != after_copy:
                print(
                    f"BLOCK: {address} modifies attributes other than "
                    "GitCommitHash"
                )
                return False

            continue

        # Anything else is not allowed
        print(
            f"BLOCK: {address} has unsupported actions: {actions}"
        )
        return False

    print("APPROVED: Terraform plan can proceed.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    result = check_plan(sys.argv[1])
    sys.exit(0 if result else 1)
