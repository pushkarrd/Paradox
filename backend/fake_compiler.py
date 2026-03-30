#!/usr/bin/env python3
# fake_compiler.py --- simulates a backdoored compiler FOR DEMO ONLY

import subprocess
import sys

DEMO_BYTES = b"\x90\x90\xcc\x48\x31\xff\x0f\x05"


def main():
    result = subprocess.run(["/usr/bin/gcc"] + sys.argv[1:])

    if "-o" in sys.argv and result.returncode == 0:
        out_index = sys.argv.index("-o") + 1
        if out_index < len(sys.argv):
            out_path = sys.argv[out_index]
            with open(out_path, "ab") as handle:
                handle.write(DEMO_BYTES)
            print("[fake_compiler] Demo payload injected")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
