from types import SimpleNamespace

import pytest

import fixer


def test_strip_appended(tmp_path):
    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"ABCDEF")
    suspect.write_bytes(b"ABCDEFMALWARE")

    result = fixer.strip_appended(str(suspect), str(trusted))

    assert result == "Stripped to 6 bytes"
    assert suspect.read_bytes() == b"ABCDEF"


def test_patch_offsets(tmp_path):
    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(bytes([0, 1, 2, 3, 4, 5]))
    suspect.write_bytes(bytes([0, 255, 2, 254, 4, 5]))

    result = fixer.patch_offsets(str(suspect), str(trusted), [1, 3])

    assert result == "Patched 2 byte offsets"
    assert suspect.read_bytes() == trusted.read_bytes()


def test_patch_offsets_raises_for_out_of_bounds_offset(tmp_path):
    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"abc")
    suspect.write_bytes(b"xyz")

    with pytest.raises(ValueError):
        fixer.patch_offsets(str(suspect), str(trusted), [999])


def test_remove_hook(tmp_path):
    suspect = tmp_path / "suspect.bin"
    suspect.write_bytes(b"\xCC" * 16)

    result = fixer.remove_hook(str(suspect), 4, hook_length=5)

    assert result == "Hook NOP-slid at 0x4"
    data = suspect.read_bytes()
    assert data[4:9] == b"\x90" * 5


def test_nop_syscall(tmp_path):
    suspect = tmp_path / "suspect.bin"
    suspect.write_bytes(b"\xCC" * 24)

    result = fixer.nop_syscall(str(suspect), 8, length=8)

    assert result == "Syscall NOP-slid at 0x8"
    data = suspect.read_bytes()
    assert data[8:16] == b"\x90" * 8


def test_replace_function(tmp_path, monkeypatch):
    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"

    trusted_bytes = bytearray(b"\x00" * 64)
    trusted_bytes[20:24] = b"GOOD"
    trusted.write_bytes(bytes(trusted_bytes))

    suspect_bytes = bytearray(b"\x00" * 64)
    suspect_bytes[20:24] = b"BAD!"
    suspect.write_bytes(bytes(suspect_bytes))

    class DummySymtab:
        def get_symbol_by_name(self, name):
            if name == "auth_check":
                return [SimpleNamespace(entry=SimpleNamespace(st_value=0x401000, st_size=4))]
            return []

    class DummyElf:
        def get_section_by_name(self, section_name):
            if section_name == ".symtab":
                return DummySymtab()
            return None

    monkeypatch.setattr(fixer, "ELFFile", lambda _: DummyElf())
    monkeypatch.setattr(fixer, "_vaddr_to_file_offset", lambda _elf, _addr: 20)

    result = fixer.replace_function(str(suspect), str(trusted), "auth_check")

    assert result == "Function auth_check replaced (4 bytes)"
    assert suspect.read_bytes()[20:24] == b"GOOD"


def test_full_replace(tmp_path):
    trusted = tmp_path / "trusted.bin"
    suspect = tmp_path / "suspect.bin"
    trusted.write_bytes(b"trusted")
    suspect.write_bytes(b"suspect")

    result = fixer.full_replace(str(suspect), str(trusted))

    assert result == f"Full replacement: {suspect} restored from trusted"
    assert suspect.read_bytes() == b"trusted"
