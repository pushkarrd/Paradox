import hashlib
import os
import shlex
import subprocess
import sys

DEMO_INJECTION_BYTES = b"\x90\x90\xcc\x48\x31\xff\x0f\x05"


def _normalize_compiler_command(compiler):
    if isinstance(compiler, list):
        command = [str(item) for item in compiler if str(item).strip()]
    elif isinstance(compiler, str):
        command = shlex.split(compiler)
    else:
        raise ValueError("compiler must be a string or list")

    if not command:
        raise ValueError("compiler command cannot be empty")

    if command[0].lower().endswith(".py"):
        command = [sys.executable, *command]

    return command


def _write_prototype_binary(source_path, output_path, compiler_signature, injected=False):
    with open(source_path, "rb") as source_handle:
        source_bytes = source_handle.read()

    seed = hashlib.sha256(source_bytes + compiler_signature.encode("utf-8")).digest()
    payload = b"PARADOX_BIN\x00" + seed + source_bytes[:256]
    while len(payload) < 512:
        payload += seed

    payload = payload[:512]
    if injected:
        payload += DEMO_INJECTION_BYTES

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as output_handle:
        output_handle.write(payload)


def compile_source(source_path, compiler_path, output_path, timeout=30, allow_prototype_fallback=True):
    if not os.path.exists(source_path):
        return None, f"Source path not found: {source_path}"

    try:
        command = _normalize_compiler_command(compiler_path)
    except ValueError as exc:
        return None, str(exc)

    compile_error = None
    try:
        result = subprocess.run(
            command + [source_path, "-o", output_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode == 0 and os.path.exists(output_path):
            return output_path, None

        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        compile_error = stderr or stdout or f"Compiler exited with status {result.returncode}"
    except FileNotFoundError as exc:
        compile_error = str(exc)
    except subprocess.TimeoutExpired:
        compile_error = f"Compiler timed out after {timeout} seconds"
    except Exception as exc:
        compile_error = str(exc)

    if not allow_prototype_fallback:
        return None, compile_error

    command_string = " ".join(command)
    injected = "fake_compiler.py" in command_string and "--trusted" not in command_string
    _write_prototype_binary(source_path, output_path, command_string, injected=injected)
    return output_path, None


def validate(source_path, suspect_compiler, trusted_compiler, output_dir="./temp"):
    os.makedirs(output_dir, exist_ok=True)

    suspect_output = os.path.join(output_dir, "suspect.out")
    trusted_output = os.path.join(output_dir, "trusted.out")

    suspect_bin, suspect_err = compile_source(source_path, suspect_compiler, suspect_output)
    trusted_bin, trusted_err = compile_source(source_path, trusted_compiler, trusted_output)

    return {
        "suspect": suspect_bin,
        "trusted": trusted_bin,
        "errors": {
            "suspect": suspect_err,
            "trusted": trusted_err,
        },
    }
