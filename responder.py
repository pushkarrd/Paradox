import hashlib
import json
import os
import shutil
import time

from fixer import (
    full_replace,
    nop_syscall,
    patch_offsets,
    remove_hook,
    replace_function,
    strip_appended,
)
from reporter import generate_report

QUARANTINE_DIR = "./quarantine"
WHITELIST_FILE = "./whitelist.json"


VALID_ACTIONS = {
    "whitelisted",
    "quarantined",
    "execution_blocked",
    "fix_applied:appended",
    "fix_applied:injected",
    "fix_applied:hook",
    "fix_applied:syscall",
    "fix_applied:section",
    "trusted_compiler_restored",
    "report_generated",
    "incident_logged",
}


def quarantine(path, lock=True):
    """Move suspect binary to quarantine and optionally hard-lock permissions."""
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    source = os.path.abspath(path)
    destination = os.path.join(
        QUARANTINE_DIR,
        f"{os.path.basename(path)}_{int(time.time() * 1000)}",
    )
    shutil.move(source, destination)
    if lock:
        os.chmod(destination, 0o000)
    return destination


def block_execution(path):
    """Remove executable bits from a file path."""
    mode = os.stat(path).st_mode
    os.chmod(path, mode & ~0o111)


def _sha256_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def log_approved(path):
    """Store approved binary hash in whitelist.json."""
    digest = _sha256_file(path)
    whitelist = []
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, "r", encoding="utf-8") as handle:
            whitelist = json.load(handle)

    from datetime import datetime

    whitelist.append({"path": path, "sha256": digest, "at": datetime.now().isoformat()})
    with open(WHITELIST_FILE, "w", encoding="utf-8") as handle:
        json.dump(whitelist, handle, indent=2)


def _extract_offsets(diffs):
    offsets = []
    for diff in diffs:
        if isinstance(diff, dict):
            value = diff.get("offset")
        else:
            value = diff

        if value is None:
            continue
        if isinstance(value, int):
            offsets.append(value)
            continue

        value_str = str(value)
        if value_str.lower().startswith("0x"):
            offsets.append(int(value_str, 16))
        else:
            offsets.append(int(value_str))

    return offsets


def _apply_compromised_fix(crack_type, quarantine_path, trusted_path, diffs):
    offsets = _extract_offsets(diffs)

    if crack_type == "appended":
        strip_appended(quarantine_path, trusted_path)
        return "fix_applied:appended"
    if crack_type == "injected":
        patch_offsets(quarantine_path, trusted_path, offsets)
        return "fix_applied:injected"
    if crack_type == "hook":
        if not offsets:
            raise ValueError("hook crack_type requires at least one diff offset")
        remove_hook(quarantine_path, offsets[0])
        return "fix_applied:hook"
    if crack_type == "syscall":
        if not offsets:
            raise ValueError("syscall crack_type requires at least one diff offset")
        nop_syscall(quarantine_path, offsets[0])
        return "fix_applied:syscall"

    # section and all unknown compromised signatures resolve to full replacement
    full_replace(quarantine_path, trusted_path)
    return "fix_applied:section"


def respond(pipeline_result):
    """Apply response policy and return UI contract action strings."""
    verdict = pipeline_result["verdict"]
    crack_type = pipeline_result["crack_type"]
    suspect = pipeline_result["suspect_binary"]
    trusted = pipeline_result["trusted_binary"]
    diffs = pipeline_result.get("diffs", [])
    actions = []

    if verdict == "TRUSTED":
        log_approved(suspect)
        actions.append("whitelisted")
        return actions

    if verdict == "SUSPICIOUS":
        quarantined_path = quarantine(suspect, lock=True)
        actions.append("quarantined")

        block_execution(quarantined_path)
        actions.append("execution_blocked")

        generate_report(pipeline_result, binary_path=quarantined_path)
        actions.append("report_generated")
        return actions

    if verdict != "COMPROMISED":
        raise ValueError(f"Unsupported verdict: {verdict}")

    quarantined_path = quarantine(suspect, lock=False)
    actions.append("quarantined")

    fix_action = _apply_compromised_fix(crack_type, quarantined_path, trusted, diffs)
    actions.append(fix_action)

    os.chmod(quarantined_path, 0o000)
    full_replace(suspect, trusted)
    actions.append("trusted_compiler_restored")

    generate_report(pipeline_result, binary_path=quarantined_path)
    actions.append("incident_logged")

    invalid = [action for action in actions if action not in VALID_ACTIONS]
    if invalid:
        raise ValueError(f"Invalid action strings emitted: {invalid}")

    return actions
