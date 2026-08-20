def validate_requirement(requirement):

    missing = []

    if not requirement["title"]:
        missing.append("title")

    if not requirement["purpose"]:
        missing.append("purpose")

    if not requirement["target_users"]:
        missing.append("target_users")

    if not requirement["features"]:
        missing.append("features")

    if not requirement["workflow"]:
        missing.append("workflow")

    return missing


def is_requirement_complete(requirement):
    missing = validate_requirement(requirement)
    return len(missing) == 0