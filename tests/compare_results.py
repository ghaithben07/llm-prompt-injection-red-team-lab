import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def load_results(filename):
    path = RESULTS_DIR / filename

    with open(path, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)


vulnerable = load_results("vulnerable_results.csv")
secure = load_results("secure_results.csv")


vuln_failures = sum(
    1 for row in vulnerable
    if row["result"] == "FAIL"
)

secure_failures = sum(
    1 for row in secure
    if row["result"] == "FAIL"
)


vuln_total = len(vulnerable)
secure_total = len(secure)


vuln_asr = (
    vuln_failures / vuln_total * 100
    if vuln_total > 0 else 0
)

secure_asr = (
    secure_failures / secure_total * 100
    if secure_total > 0 else 0
)


if vuln_asr > 0:
    reduction = ((vuln_asr - secure_asr) / vuln_asr) * 100
else:
    reduction = 0


print("\n================================")
print("LLM SECURITY COMPARISON")
print("================================")

print("\nVULNERABLE VERSION")
print(f"Successful attacks: {vuln_failures}/{vuln_total}")
print(f"Attack Success Rate: {vuln_asr:.1f}%")

print("\nSECURE VERSION")
print(f"Successful attacks: {secure_failures}/{secure_total}")
print(f"Attack Success Rate: {secure_asr:.1f}%")

print("\nSECURITY IMPROVEMENT")
print(f"Attack Success Rate: {vuln_asr:.1f}% -> {secure_asr:.1f}%")
print(f"Reduction in successful attacks: {reduction:.1f}%")
