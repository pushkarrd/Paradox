import subprocess
import os

# ----------------------------------------
# Helper function to compile using 1 compiler
# ----------------------------------------
def compile_source(source_path, compiler_path, output_path, timeout=30):
    try:
        result = subprocess.run(
            [compiler_path, source_path, "-o", output_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # If compilation failed
        if result.returncode != 0:
            return None, result.stderr

        return output_path, None

    except subprocess.TimeoutExpired:
        return None, "Compiler timed out after 30 seconds"

    except FileNotFoundError:
        return None, f"Compiler not found: {compiler_path}"


# ----------------------------------------
# Main function (called by pipeline)
# ----------------------------------------
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