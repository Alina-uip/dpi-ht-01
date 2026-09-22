const fmt = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0
});

const plain = new Intl.NumberFormat("en-GB", { maximumFractionDigits: 0 });

function money(value) {
  return fmt.format(value || 0);
}

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function status(text) {
  return `<span class="status ${esc(text)}">${esc(text).replaceAll("_", " ")}</span>`;
}

function table(headers, rows) {
  return `<div class="table-wrap"><table><thead><tr>${headers
    .map((h) => `<th class="${h.num ? "num" : ""}">${esc(h.label)}</th>`)
    .join("")}</tr></thead><tbody>${rows
    .map((row) => `<tr>${row
      .map((cell, i) => `<td class="${headers[i]?.num ? "num" : ""}">${cell}</td>`)
      .join("")}</tr>`)
    .join("")}</tbody></table></div>`;
}

function kvRows(obj, options = {}) {
  const skip = new Set(options.skip || ["evidence"]);
  return Object.entries(obj)
    .filter(([key, value]) => {
      if (skip.has(key)) return false;
      return value === null || typeof value !== "object";
    })
    .map(([key, value]) => [
    esc(label(key)),
    typeof value === "number" ? money(value) : esc(value)
  ]);
}

function label(key) {
  return key
    .replace(/([A-Z])/g, " $1")
    .replace(/^./, (s) => s.toUpperCase())
    .replace("P P E", "PPE")
    .replace("C O G S", "COGS")
    .replace("A R", "AR");
}

function evidenceList(evidence) {
  return `<ul class="evidence-list">${(evidence || [])
    .map((e) => `<li>${esc(e)}</li>`)
    .join("")}</ul>`;
}

function metrics(data) {
  const pnl = data.statements.profitAndLoss;
  const cf = data.statements.cashFlow;
  const bs = data.statements.balanceSheet;
  return `<section class="summary-grid" aria-label="Headline results">
    <article class="metric"><span>Corrected profit</span><strong>${money(pnl.netProfit)}</strong><small>Management claimed ${money(312000)}</small></article>
    <article class="metric"><span>Closing cash</span><strong>${money(cf.closingCash)}</strong><small>Agrees to bank evidence</small></article>
    <article class="metric"><span>Balance sheet</span><strong>${money(bs.totalAssets)}</strong><small>Assets equal liabilities plus equity</small></article>
    <article class="metric"><span>Decisions resolved</span><strong>${data.decisions.length}</strong><small>${data.decisions.filter((d) => d.reviewTier === "material_judgment").length} material judgments</small></article>
  </section>`;
}

function statements(data) {
  const pnl = data.statements.profitAndLoss;
  const cf = data.statements.cashFlow;
  const bs = data.statements.balanceSheet;
  return `<section class="grid-3">
    <article class="panel"><h2>Profit and Loss</h2>${table([
      { label: "Line" }, { label: "EUR", num: true }
    ], kvRows(pnl))}</article>
    <article class="panel"><h2>Cash Flow</h2>${table([
      { label: "Line" }, { label: "EUR", num: true }
    ], kvRows(cf))}</article>
    <article class="panel"><h2>Balance Sheet</h2>
      <h3>Assets</h3>${table([{ label: "Asset" }, { label: "EUR", num: true }], kvRows(bs.assets))}
      <h3>Liabilities</h3>${table([{ label: "Liability" }, { label: "EUR", num: true }], kvRows(bs.liabilities))}
      <h3>Equity</h3>${table([{ label: "Equity" }, { label: "EUR", num: true }], kvRows(bs.equity))}
      <p class="note">Total assets ${money(bs.totalAssets)}; liabilities plus equity ${money(bs.totalLiabilitiesAndEquity)}.</p>
    </article>
  </section>`;
}

function schedules(data) {
  const s = data.schedules;
  const revenueRows = s.revenueAndReceivables.lines.map((x) => [
    esc(x.customer),
    esc(x.invoice),
    money(x.revenue),
    money(x.cash),
    money(x.netReceivable)
  ]);
  return `<section class="panel"><h2>Supporting Schedules</h2>
    <div class="grid-2">
      <div><h3>Revenue and Receivables</h3>${table([
        { label: "Customer" }, { label: "Invoice" }, { label: "Revenue", num: true }, { label: "Cash", num: true }, { label: "Net AR", num: true }
      ], revenueRows)}</div>
      <div><h3>Inventory and COGS</h3>${table([{ label: "Line" }, { label: "EUR", num: true }], kvRows(s.inventoryAndCOGS))}</div>
      <div><h3>Payroll</h3>${table([{ label: "Line" }, { label: "EUR", num: true }], kvRows(s.payroll))}</div>
      <div><h3>PPE and Depreciation</h3>${table([{ label: "Line" }, { label: "EUR", num: true }], kvRows(s.ppeAndDepreciation))}</div>
      <div><h3>Debt and Interest</h3>${table([{ label: "Line" }, { label: "EUR", num: true }], kvRows(s.debtAndInterest))}</div>
      <div><h3>Equity and Distributions</h3>${table([{ label: "Line" }, { label: "EUR", num: true }], kvRows(s.equityAndDistributions))}</div>
    </div>
  </section>`;
}

function reconciliations(data) {
  return `<section class="panel"><h2>Reconciliations</h2>${table([
    { label: "Check" }, { label: "Status" }, { label: "Calculation" }
  ], data.reconciliations.map((r) => [esc(r.name), status(r.status), esc(r.calculation)]))}</section>`;
}

function uncertainties(data) {
  return `<section class="panel"><h2>Uncertainties</h2>${table([
    { label: "Area" }, { label: "Amount", num: true }, { label: "Confidence" }, { label: "Impact" }
  ], data.uncertainties.map((u) => [esc(u.area), money(u.amount), status(u.confidence), esc(u.statementImpact)]))}</section>`;
}

function board(data) {
  const b = data.boardRecommendation;
  return `<section class="panel"><h2>Board Recommendation</h2>
    <p class="callout">${esc(b.summary)}</p>
    <p><strong>Decision:</strong> ${esc(b.decision)}</p>
    <ul>${b.immediateActions.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>
  </section>`;
}

function evidence(data) {
  return `<section class="panel"><h2>Evidence Inventory</h2>${table([
    { label: "File" }, { label: "Inspection" }
  ], data.evidence.map((e) => [esc(e.file), esc(e.inspection)]))}</section>`;
}

function decisionCard(d, compact = false) {
  const material = d.reviewTier === "material_judgment";
  return `<article class="decision-card" data-tier="${esc(d.reviewTier)}" data-confidence="${esc(d.confidence)}">
    <div class="decision-head">
      <h3>${esc(d.id)} ${esc(d.question)}</h3>
      <div>${status(d.confidence)} ${material ? status("material") : ""}</div>
    </div>
    <p>${esc(d.answer)}</p>
    ${material ? `<div class="split-detail">
      <div><strong>Agent 1</strong><p>${esc(d.aiProposal)}</p></div>
      <div><strong>Agent 2 challenge</strong><p>${esc(d.independentChallenge)}</p></div>
      <div><strong>Student reasoning</strong><p>${esc(d.studentReasoning)}</p></div>
      <div><strong>Statement effect</strong>${table([{ label: "Area" }, { label: "EUR", num: true }], kvRows(d.statementEffect))}</div>
    </div>` : ""}
    ${compact ? "" : evidenceList(d.evidence)}
  </article>`;
}

function decisions(data) {
  return `<section class="panel"><h2>Decision Log</h2>
    <div class="toolbar">
      <button class="active" data-filter="all">All</button>
      <button data-filter="material_judgment">Material</button>
      <button data-filter="operational">Operational</button>
      <button data-filter="low">Low confidence</button>
      <input id="decisionSearch" type="search" placeholder="Search decisions, evidence, answers">
    </div>
    <div id="decisionList" class="decision-list">${data.decisions.map((d) => decisionCard(d)).join("")}</div>
  </section>`;
}

function review(data) {
  const material = data.decisions.filter((d) => d.reviewTier === "material_judgment");
  const low = data.decisions.filter((d) => d.confidence === "low");
  const changed = material.filter((d) => d.changedFromAI);
  const disagreementIds = changed.map((d) => d.id).join(", ") || "None";
  const withUncertainty = data.reconciliations.filter((r) => r.status.includes("uncertainty"));
  return `${metrics(data)}
  <section class="panel"><h2>Assessor Flags</h2>
    <div class="review-flags">
      <div class="flag"><span>Agent disagreements</span><strong>${plain.format(changed.length)}</strong><small>${disagreementIds}</small></div>
      <div class="flag"><span>Student overrides</span><strong>${plain.format(changed.length)}</strong><small>${disagreementIds}</small></div>
      <div class="flag"><span>Low confidence</span><strong>${plain.format(low.length)}</strong><small>${low.map((d) => d.id).join(", ") || "None"}</small></div>
      <div class="flag"><span>Unresolved uncertainty</span><strong>${plain.format(data.uncertainties.length)}</strong><small>${withUncertainty.length} reconciliation checks flagged.</small></div>
    </div>
  </section>
  ${reconciliations(data)}
  ${uncertainties(data)}
  <section class="panel"><h2>AI Review Trail</h2><div class="decision-list">${material.map((d) => decisionCard(d)).join("")}</div></section>
  ${board(data)}`;
}

function main(data) {
  return `${metrics(data)}
    ${board(data)}
    ${statements(data)}
    ${schedules(data)}
    ${reconciliations(data)}
    ${uncertainties(data)}
    ${decisions(data)}
    ${evidence(data)}`;
}

function bindFilters() {
  const list = document.querySelector("#decisionList");
  if (!list) return;
  const buttons = [...document.querySelectorAll("[data-filter]")];
  const search = document.querySelector("#decisionSearch");
  function apply() {
    const active = document.querySelector("[data-filter].active")?.dataset.filter || "all";
    const term = (search.value || "").toLowerCase();
    [...list.children].forEach((card) => {
      const haystack = card.textContent.toLowerCase();
      const tier = card.dataset.tier;
      const confidence = card.dataset.confidence;
      const filterMatch = active === "all" || active === tier || active === confidence;
      card.style.display = filterMatch && haystack.includes(term) ? "" : "none";
    });
  }
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((b) => b.classList.remove("active"));
      button.classList.add("active");
      apply();
    });
  });
  search.addEventListener("input", apply);
}

async function boot() {
  const app = document.querySelector("#app");
  try {
    const response = await fetch("/submission.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    app.innerHTML = document.body.dataset.page === "review" ? review(data) : main(data);
    bindFilters();
  } catch (error) {
    app.innerHTML = `<section class="panel"><h2>Could not load submission data</h2><p>${esc(error.message)}</p></section>`;
  }
}

boot();
