import os
import shutil
from elftools.elf.elffile import ELFFile


def strip_appended(suspect_path, trusted_path):
    """Truncate appended bytes so suspect matches trusted binary size."""
    trusted_size = os.path.getsize(trusted_path)
    with open(suspect_path, "r+b") as handle:
        handle.truncate(trusted_size)
    return f"Stripped to {trusted_size} bytes"


def patch_offsets(suspect_path, trusted_path, diff_offsets):
    """Patch selected offsets in suspect binary using bytes from trusted binary."""
    with open(trusted_path, "rb") as handle:
        trusted = handle.read()

    with open(suspect_path, "r+b") as handle:
        for offset in diff_offsets:
            if offset < 0 or offset >= len(trusted):
                raise ValueError(f"Offset {offset} is outside trusted binary bounds")
            handle.seek(offset)
            handle.write(bytes([trusted[offset]]))

    return f"Patched {len(diff_offsets)} byte offsets"


def remove_hook(suspect_path, hook_offset, hook_length=5):
    """NOP over an injected JMP hook (default 5-byte JMP rel32)."""
    if hook_offset < 0:
        raise ValueError("hook_offset must be non-negative")
    if hook_length <= 0:
        raise ValueError("hook_length must be greater than zero")

    with open(suspect_path, "r+b") as handle:
        handle.seek(hook_offset)
        handle.write(b"\x90" * hook_length)

    return f"Hook NOP-slid at {hex(hook_offset)}"


def nop_syscall(suspect_path, syscall_offset, length=8):
    """NOP over injected syscall instructions at the given offset."""
    if syscall_offset < 0:
        raise ValueError("syscall_offset must be non-negative")
    if length <= 0:
        raise ValueError("length must be greater than zero")

    with open(suspect_path, "r+b") as handle:
        handle.seek(syscall_offset)
        handle.write(b"\x90" * length)

    return f"Syscall NOP-slid at {hex(syscall_offset)}"


def _vaddr_to_file_offset(elf_file, virtual_address):
    """Translate ELF virtual address to file offset for byte extraction."""
    for segment in elf_file.iter_segments():
        header = segment.header
        start = header.p_vaddr
        end = start + header.p_memsz
        if start <= virtual_address < end:
            return header.p_offset + (virtual_address - start)
    raise ValueError(f"Unable to map virtual address {hex(virtual_address)} to file offset")


def replace_function(suspect_path, trusted_path, func_name):
    """Replace suspect function bytes with trusted bytes using ELF symbol metadata."""
    with open(trusted_path, "rb") as trusted_handle:
        elf = ELFFile(trusted_handle)
        symtab = elf.get_section_by_name(".symtab")
        if symtab is None:
            raise ValueError("Trusted binary is missing .symtab")

        symbols = symtab.get_symbol_by_name(func_name)
        if not symbols:
            raise ValueError(f"Function symbol '{func_name}' was not found")

        symbol = symbols[0]
        virtual_address = symbol.entry.st_value
        size = symbol.entry.st_size
        if size <= 0:
            raise ValueError(f"Function symbol '{func_name}' has invalid size {size}")

        file_offset = _vaddr_to_file_offset(elf, virtual_address)
        trusted_handle.seek(file_offset)
        trusted_bytes = trusted_handle.read(size)

    with open(suspect_path, "r+b") as suspect_handle:
        suspect_handle.seek(file_offset)
        suspect_handle.write(trusted_bytes)

    return f"Function {func_name} replaced ({size} bytes)"


def full_replace(suspect_path, trusted_path):
    """Replace suspect binary with trusted binary copy."""
    shutil.copy2(trusted_path, suspect_path)
    return f"Full replacement: {suspect_path} restored from trusted"
