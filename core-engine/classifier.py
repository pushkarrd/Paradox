from capstone import Cs, CS_ARCH_X86, CS_MODE_64

# Severity mapping
SEVERITY = {
    "clean": "none",
    "timestamp": "none",
    "appended": "high",
    "injected": "medium",
    "hook": "high",
    "syscall": "critical",
    "section": "critical",
}


# Disassemble bytes at a specific offset
def disassemble_at(binary_path, offset, size=64):
    with open(binary_path, "rb") as f:
        f.seek(offset)
        code = f.read(size)

    md = Cs(CS_ARCH_X86, CS_MODE_64)

    instructions = []
    for ins in md.disasm(code, offset):
        instructions.append(ins.mnemonic)

    return instructions


# Main classification function
def classify(suspect_path, trusted_path, diffs, size_delta):

    # Case 1: No differences
    if not diffs and size_delta == 0:
        return "clean", "none"

    # Case 2: Only size increased → appended attack
    if not diffs and size_delta > 0:
        return "appended", "high"

    # Case 3: Large number of diffs → section overwrite
    if len(diffs) > 200:
        return "section", "critical"

    # Analyze first diff location
    first_offset = int(diffs[0]["offset"], 16)

    mnemonics = disassemble_at(suspect_path, first_offset)
    
    print("First few mnemonics:", mnemonics[:5])

    # Case 4: Hook attack (jmp)
    if "jmp" in mnemonics:
        return "hook", "high"

    # Case 5: Syscall injection
    if "syscall" in mnemonics or "int" in mnemonics:
        return "syscall", "critical"

    # Case 6: Only small offsets → timestamp noise
    all_noise = all(int(d["offset"], 16) < 0x20 for d in diffs)
    if all_noise:
        return "timestamp", "none"

    # Default → injected
    return "injected", "medium"