import os

print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")

print(f"PATH:")
for p in sorted(os.environ.get('PATH').split(';')):
    print(f"\t{p}")