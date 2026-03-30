from validator import validate

# Change this path to your test file
SOURCE_FILE = "samples/clean.c"

# Use GCC as both compilers for now
SUSPECT_COMPILER = "gcc"
TRUSTED_COMPILER = "gcc"

result = validate(SOURCE_FILE, SUSPECT_COMPILER, TRUSTED_COMPILER)

print("Validation Result:")
print(result)