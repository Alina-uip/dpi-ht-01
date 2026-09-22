import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const submissionPath = path.join(root, "data", "submission.json");
const schemaPath = path.join(root, "04 CODEX FILES - Give These to Codex", "02 GIVE TO CODEX - Submission Rules.json");
const publicSubmissionPath = path.join(root, "submission.json");
const validateOnly = process.argv.includes("--validate-only");

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

const data = readJson(submissionPath);
const schema = readJson(schemaPath);

for (const key of schema.required) {
  if (!(key in data)) fail(`missing top-level key ${key}`);
}
if (data.schemaVersion !== schema.properties.schemaVersion.const) fail("schemaVersion mismatch");
if (data.caseId !== schema.properties.caseId.const) fail("caseId mismatch");
if (!data.student?.id || !data.student?.name) fail("student object missing id/name");
for (const key of schema.properties.statements.required) {
  if (!(key in data.statements)) fail(`statements missing ${key}`);
}

const decisions = data.decisions;
if (!Array.isArray(decisions) || decisions.length !== 100) fail("decisions must contain exactly 100 items");
const expectedIds = Array.from({ length: 100 }, (_, i) => `D${String(i + 1).padStart(3, "0")}`);
if (decisions.map((d) => d.id).join("|") !== expectedIds.join("|")) fail("decision IDs must be D001-D100 in order");

const material = decisions.filter((d) => d.reviewTier === "material_judgment");
if (material.length !== 25) fail("material judgment count must be 25");
for (const decision of decisions) {
  for (const key of ["id", "category", "reviewTier", "question", "answer", "evidence", "confidence"]) {
    if (!(key in decision)) fail(`${decision.id ?? "<missing id>"} missing ${key}`);
  }
  if (!["operational", "material_judgment"].includes(decision.reviewTier)) fail(`${decision.id} invalid reviewTier`);
  if (!["low", "medium", "high"].includes(decision.confidence)) fail(`${decision.id} invalid confidence`);
  if (!Array.isArray(decision.evidence) || decision.evidence.length < 1) fail(`${decision.id} missing evidence`);
}
for (const decision of material) {
  for (const key of ["aiProposal", "independentChallenge", "studentReasoning", "statementEffect", "changedFromAI"]) {
    if (!(key in decision)) fail(`${decision.id} missing material field ${key}`);
  }
  if (decision.independentChallenge.length < 20) fail(`${decision.id} independentChallenge too short`);
  if (decision.studentReasoning.length < 20) fail(`${decision.id} studentReasoning too short`);
  const effectKeys = Object.keys(decision.statementEffect).sort().join("|");
  if (effectKeys !== "assets|cash|equity|liabilities|profit") fail(`${decision.id} statementEffect keys invalid`);
  if (typeof decision.changedFromAI !== "boolean") fail(`${decision.id} changedFromAI not boolean`);
}

const bs = data.statements.balanceSheet;
if (Math.round(bs.totalAssets * 100) !== Math.round(bs.totalLiabilitiesAndEquity * 100)) fail("balance sheet does not balance");
if (Math.round(data.statements.cashFlow.closingCash * 100) !== 6000000) fail("closing cash is not EUR 60,000");
const eq = data.schedules.equityAndDistributions;
if (Math.round((eq.openingEquity + eq.profit - eq.ownerDistributions) * 100) !== Math.round(eq.closingEquity * 100)) {
  fail("equity roll-forward fails");
}

if (!validateOnly) {
  fs.copyFileSync(submissionPath, publicSubmissionPath);
  console.log("Copied data/submission.json to /submission.json");
}
console.log("PASS schema validation");
console.log("PASS 100 decisions and 25 material judgments");
console.log("PASS evidence citations present");
console.log("PASS financial reconciliations checked");
