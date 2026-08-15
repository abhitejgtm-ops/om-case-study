import json
import sys


def get_changed_paths(before, after, path=""):
    """
    Recursively find all changed attributes between before and after.
    """

    changes = []

    if isinstance(before, dict) and isinstance(after, dict):
        all_keys = set(before.keys()) | set(after.keys())

        for key in all_keys:
            current_path = f"{path}.{key}" if path else key

            if key not in before:
                changes.append(current_path)

            elif key not in after:
                changes.append(current_path)

            else:
                changes.extend(
                    get_changed_paths(
                        before[key],
                        after[key],
                        current_path
                    )
                )

    elif isinstance(before, list) and isinstance(after, list):
        if before != after:
            changes.append(path)

    elif before != after:
        changes.append(path)

    return changes


def validate_plan(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            plan = json.load(file)

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return False

    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON file: {file_path}")
        return False

    resource_changes = plan.get("resource_changes", [])

    if not resource_changes:
        print("PLAN APPROVED: no resource changes found.")
        return True

    for resource in resource_changes:

        address = resource.get("address", "unknown")
        change = resource.get("change", {})
        actions = change.get("actions", [])

        print(f"\nChecking resource: {address}")
        print(f"Actions: {actions}")

        # -------------------------------------------------
        # CREATE
        # -------------------------------------------------
        if actions == ["create"]:
            print("ALLOWED: resource creation.")
            continue

        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------
        if actions == ["update"]:

            before = change.get("before")
            after = change.get("after")

            changed_paths = get_changed_paths(before, after)

            print(f"Changed attributes: {changed_paths}")

            # Only this exact attribute is allowed to change
            if changed_paths == ["tags.GitCommitHash"]:
                print(
                    "ALLOWED: only tags.GitCommitHash was modified."
                )
                continue

            print(
                f"PLAN REJECTED: {address} modifies attributes "
                f"other than tags.GitCommitHash."
            )

            return False

        # -------------------------------------------------
        # DELETE / DESTROY / OTHER ACTIONS
        # -------------------------------------------------
        print(
            f"PLAN REJECTED: {address} has unsupported actions: "
            f"{actions}"
        )

        return False

    print(
        "\nPLAN APPROVED: all resource changes satisfy "
        "the required policy."
    )

    return True


def main():

    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    file_path = sys.argv[1]

    if validate_plan(file_path):
        print("\nFINAL RESULT: PASS")
        sys.exit(0)

    else:
        print("\nFINAL RESULT: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()