def compare(old: dict[str, str], new: dict[str, str]) -> dict[str, list[str]]:
    old_paths = set(old)
    new_paths = set(new)

    added = sorted(new_paths - old_paths)
    deleted = sorted(old_paths - new_paths)
    modified = sorted(p for p in old_paths & new_paths if old[p] != new[p])

    return {"added": added, "modified": modified, "deleted": deleted}