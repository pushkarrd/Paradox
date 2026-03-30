from comparator import compare_binaries
from classifier import classify
from scorer import score
import os

suspect = "./temp/suspect.out"
trusted = "./temp/trusted.out"

diffs, size_delta = compare_binaries(suspect, trusted)

crack_type, severity = classify(suspect, trusted, diffs, size_delta)

total_bytes = os.path.getsize(suspect)

trust_score, verdict = score(diffs, size_delta, total_bytes, severity)

print("🧠 Crack Type:", crack_type)
print("🔥 Severity:", severity)
print("📊 Trust Score:", trust_score)
print("⚖️ Verdict:", verdict)