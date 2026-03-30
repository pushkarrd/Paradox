from run_pipeline import run_pipeline

result = run_pipeline(
    source_path="samples/clean.c",
    suspect_compiler="gcc",
    trusted_compiler="cc"
)

print("🚀 FINAL RESULT:\n")
for key, value in result.items():
    print(f"{key}: {value}")