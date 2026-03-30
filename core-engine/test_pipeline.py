from run_pipeline import run_pipeline

result = run_pipeline(
    source_path="samples/clean.c",
    suspect_compiler=[
        r"C:\Program Files\Python313\python.exe",
        "samples/fake_compiler.py"
    ],
    trusted_compiler=[r"C:\MinGW\bin\gcc.exe"]
)

print(" FINAL RESULT:\n")
for key, value in result.items():
    print(f"{key}: {value}")