import sys
import subprocess

def fake_compile(source_file, output_file):
    try:
        # Step 1: Compile normally using gcc
        result = subprocess.run(
            ["C:\\MinGW\\bin\\gcc.exe", source_file, "-o", output_file],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(result.stderr)
            return 1

        # Step 2: Inject malicious payload (append bytes)
        with open(output_file, "ab") as f:
            f.write(b"\x90\x90\x90\x90MALWARE")  
            # \x90 = NOP (no-op instruction, common in exploits)

        print("[INFO] Fake compiler injected payload!")

        return 0

    except Exception as e:
        print("Error:", str(e))
        return 1


if __name__ == "__main__":
    # Expected usage:
    # python fake_compiler.py source.c -o output
    print("ARGS:", sys.argv)
    
    args = sys.argv

    if "-o" not in args:
        print("Usage: fake_compiler.py <source.c> -o <output>")
        sys.exit(1)

    source_file = args[1]
    output_index = args.index("-o") + 1
    output_file = args[output_index]

    exit_code = fake_compile(source_file, output_file)
    sys.exit(exit_code)