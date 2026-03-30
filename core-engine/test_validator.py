from validator import validate

# Change this path to your test file
SOURCE_FILE = "samples/clean.c"

# Use GCC as both compilers for now
SUSPECT_COMPILER = "gcc"
TRUSTED_COMPILER = "gcc"

result = validate(SOURCE_FILE, SUSPECT_COMPILER, TRUSTED_COMPILER)

print("Validation Result:")
print(result)

if(result['errors']['suspect']):
    print("Suspect Compiler Failed")
elif (result['errors']['trusted']):
    print("Trusted Compiler Failed")
else:
    print("✅ Compilation Successful! No Errors")
