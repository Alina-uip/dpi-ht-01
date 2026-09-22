import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSION = ROOT / "data" / "submission.json"
SCHEMA = ROOT / "04 CODEX FILES - Give These to Codex" / "02 GIVE TO CODEX - Submission Rules.json"


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    data = json.loads(SUBMISSION.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    # The supplied schema is intentionally small. Validate its concrete rules
    # locally so the project has no network or package dependency.
    for key in schema["required"]:
        if key not in data:
            fail(f"missing top-level key {key}")
    if data.get("schemaVersion") != schema["properties"]["schemaVersion"]["const"]:
        fail("schemaVersion does not match schema const")
    if data.get("caseId") != schema["properties"]["caseId"]["const"]:
        fail("caseId does not match schema const")
    if not isinstance(data.get("student"), dict) or not {"id", "name"} <= set(data["student"]):
        fail("student object missing id/name")
    if not isinstance(data.get("evidence"), list):
        fail("evidence is not an array")
    if not isinstance(data.get("schedules"), dict):
        fail("schedules is not an object")
    if not isinstance(data.get("statements"), dict):
        fail("statements is not an object")
    for key in schema["properties"]["statements"]["required"]:
        if key not in data["statements"]:
            fail(f"statements missing {key}")
    if not isinstance(data.get("reconciliations"), list):
        fail("reconciliations is not an array")
    if not isinstance(data.get("uncertainties"), list):
        fail("uncertainties is not an array")
    if not isinstance(data.get("boardRecommendation"), dict):
        fail("boardRecommendation is not an object")

    decisions = data["decisions"]
    if not isinstance(decisions, list):
        fail("decisions is not an array")
    ids = [d["id"] for d in decisions]
    expected = [f"D{i:03d}" for i in range(1, 101)]
    if ids != expected:
        fail("decision IDs are not exactly D001-D100 in order")
    if len(decisions) != 100:
        fail("decision count is not 100")
    material = [d for d in decisions if d["reviewTier"] == "material_judgment"]
    if len(material) != 25:
        fail("material judgment count is not 25")
    required_extra = {"aiProposal", "independentChallenge", "studentReasoning", "statementEffect", "changedFromAI"}
    for d in material:
        missing = required_extra - set(d)
        if missing:
            fail(f"{d['id']} missing material fields {sorted(missing)}")
        if not isinstance(d["independentChallenge"], str) or len(d["independentChallenge"]) < 20:
            fail(f"{d['id']} independentChallenge too short")
        if not isinstance(d["studentReasoning"], str) or len(d["studentReasoning"]) < 20:
            fail(f"{d['id']} studentReasoning too short")
        effect = d["statementEffect"]
        if set(effect) != {"profit", "cash", "assets", "liabilities", "equity"}:
            fail(f"{d['id']} statementEffect keys invalid")
        if not isinstance(d["changedFromAI"], bool):
            fail(f"{d['id']} changedFromAI is not boolean")
    for d in decisions:
        for key in ["id", "category", "reviewTier", "question", "answer", "evidence", "confidence"]:
            if key not in d:
                fail(f"{d.get('id', '<missing id>')} missing required key {key}")
        if d["reviewTier"] not in {"operational", "material_judgment"}:
            fail(f"{d['id']} invalid reviewTier")
        if d["confidence"] not in {"low", "medium", "high"}:
            fail(f"{d['id']} invalid confidence")
        if not d.get("evidence"):
            fail(f"{d['id']} has no evidence citation")

    bs = data["statements"]["balanceSheet"]
    if round(bs["totalAssets"], 2) != round(bs["totalLiabilitiesAndEquity"], 2):
        fail("balance sheet does not balance")
    cf = data["statements"]["cashFlow"]
    if round(cf["closingCash"], 2) != 60000:
        fail("closing cash does not equal EUR 60,000")
    eq = data["schedules"]["equityAndDistributions"]
    if round(eq["openingEquity"] + eq["profit"] - eq["ownerDistributions"], 2) != round(eq["closingEquity"], 2):
        fail("equity roll-forward fails")

    print("PASS schema validation")
    print("PASS 100 decisions and 25 material judgments")
    print("PASS evidence citations present")
    print("PASS financial reconciliations checked")


if __name__ == "__main__":
    main()
