import subprocess
import shlex
import os


def compile_source(source_path, compiler_path, output_path, timeout=30):
    try:
        cmd = compiler_path if isinstance(compiler_path, list) else [compiler_path]
        cmd = cmd + [source_path, "-o", output_path]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        print("Running Command:", cmd)   # 👈 DEBUG

        if result.returncode != 0:
            print("[INFO] Compiler Error:", result.stderr)
            print("STDOUT:", result.stdout)
            return None, result.stderr

        return output_path, None

    except Exception as e:
        return None, str(e)
    

def validate(source_path, suspect_compiler, trusted_compiler, output_dir="./temp"):

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    suspect_output = os.path.join(output_dir, "suspect.out")
    trusted_output = os.path.join(output_dir, "trusted.out")

    # Compile using suspect compiler
    suspect_bin, suspect_err = compile_source(
        source_path,
        suspect_compiler,
        suspect_output
    )

    # Compile using trusted compiler
    trusted_bin, trusted_err = compile_source(
        source_path,
        trusted_compiler,
        trusted_output
    )

    return {
        "suspect": suspect_bin,
        "trusted": trusted_bin,
        "errors": {
            "suspect": suspect_err,
            "trusted": trusted_err
        }
    }