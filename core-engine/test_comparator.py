from comparator import compare_binaries

suspect = "./temp/suspect.out"
trusted = "./temp/trusted.out"

diffs, size_delta = compare_binaries(suspect, trusted)

print("🔍 Differences Found:", len(diffs))
print("📏 Size Delta:", size_delta)

print(len(open(suspect, "rb").read()))

# Show first few diffs
for d in diffs[:5]:
    print(d)