try:
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
except Exception:  # pragma: no cover - optional at runtime
    Cs = None


def disassemble_at(binary_path, offset, size=64):
    if Cs is None:
        return []

    with open(binary_path, "rb") as handle:
        handle.seek(max(offset, 0))
        code = handle.read(size)

    disassembler = Cs(CS_ARCH_X86, CS_MODE_64)
    return [instruction.mnemonic for instruction in disassembler.disasm(code, offset)]


def classify(suspect_path, trusted_path, diffs, size_delta):
    if not diffs and size_delta == 0:
        return "clean", "none"

    if not diffs and size_delta > 0:
        return "appended", "high"

    if len(diffs) > 200:
        return "section", "critical"

    first_offset = int(diffs[0]["offset"], 16) if diffs else 0
    mnemonics = disassemble_at(suspect_path, first_offset)

    if "jmp" in mnemonics:
        return "hook", "high"

    if "syscall" in mnemonics or "int" in mnemonics:
        return "syscall", "critical"

    all_noise = all(int(diff["offset"], 16) < 0x20 for diff in diffs)
    if all_noise:
        return "timestamp", "none"

    return "injected", "medium"
