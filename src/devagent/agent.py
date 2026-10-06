import re
from pathlib import PurePosixPath

TOOLS = ["plan", "draft_patch"]


class InputError(ValueError):
    pass


def run(goal, payload):
    if not isinstance(goal, str) or not goal.strip() or len(goal) > 2000:
        raise InputError("goal must contain 1 to 2000 characters")
    if re.search(r"\b(?:git\s+push|apply|merge)\b", goal, re.I):
        return {"refused": True, "reason": "This agent only reads or plans. It does not write.", "tools": [], "wrote": False, "applied": False}
    if not isinstance(payload, dict):
        raise InputError("payload must be an object")
    files = payload.get("files", [])
    if not isinstance(files, list) or len(files) > 50:
        raise InputError("files must contain at most 50 relative paths")
    for name in files:
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise InputError("file paths must be non-empty strings of at most 200 characters")
        if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or "\\" in name or ":" in name:
            raise InputError("file paths must remain relative to the workspace")
    area = "API handler" if any(word in goal.lower() for word in ["api", "endpoint", "healthz", "handler"]) else "implementation"
    plan = ["add test", f"change handler: {area}", "run focused tests", "review proposed changes"]
    return {"refused": False, "tools": TOOLS, "plan": plan, "goal": goal.strip(),
            "files": sorted(set(files)), "acceptance_checks": ["existing tests pass", "new behavior is tested", "no changes applied"],
            "planner": "deterministic", "wrote": False, "applied": False}
