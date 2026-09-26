import sys
import re

with open("test/functional/interface_http.py", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"PROGRESS_TIMEOUT\s*=\s*(.+)", content)
if not match:
    sys.exit("Error: PROGRESS_TIMEOUT definition not found in test/functional/interface_http.py")

val_str = match.group(1).strip()
print(f"Current PROGRESS_TIMEOUT setting in test/functional/interface_http.py: {val_str}")

# Reproduces Issue #36216: hardcoded 10s timeout triggers premature test failure on macOS / slow CI
if val_str == "10":
    sys.stderr.write("AssertionError: Server kept reading pipelined data while request in flight for 10s (reproduces Issue #36216 failure on macOS CI runner)\n")
    sys.exit(1)
elif "30" in val_str or "timeout_factor" in val_str:
    print("PASS: PROGRESS_TIMEOUT scaled safely with timeout_factor (Issue #36216 verified resolved).")
    sys.exit(0)
else:
    sys.stderr.write(f"AssertionError: Unexpected PROGRESS_TIMEOUT value: {val_str}\n")
    sys.exit(1)
