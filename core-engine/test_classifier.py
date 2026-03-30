from comparator import compare_binaries
from classifier import classify

suspect = "./temp/suspect.out"
trusted = "./temp/trusted.out"

diffs, size_delta = compare_binaries(suspect, trusted)

crack_type, severity = classify(suspect, trusted, diffs, size_delta)

print("🧠 Crack Type:", crack_type)
print("🔥 Severity:", severity)