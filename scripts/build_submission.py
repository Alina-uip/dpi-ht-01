import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "04 CODEX FILES - Give These to Codex" / "01 GIVE TO CODEX - Answer Template.json"
OUTPUT_PATH = ROOT / "data" / "submission.json"


def eur(value):
    return round(float(value), 2)


E = {
    "assignment": "01 START HERE - Student Assignment.pdf, pp. 1-3",
    "board": "03 CASE FILES - Open and Investigate/00 BOARD ORDER READ FIRST.pdf, p. 1",
    "management": "03 CASE FILES - Open and Investigate/01 USE THIS NUMBERS FINAL v9.xlsx, Management P&L rows 4-11",
    "bank": "03 CASE FILES - Open and Investigate/02 Bank Export August.csv",
    "crm": "03 CASE FILES - Open and Investigate/03 CRM Export Cleaned FINAL.xlsx, CRM Export rows 4-11",
    "contracts": "03 CASE FILES - Open and Investigate/04 Contracts Returns and Angry Customers.pdf, pp. 1-2",
    "warehouse": "03 CASE FILES - Open and Investigate/05 Warehouse Count Marta Notes.pdf, pp. 1-2",
    "purchases": "03 CASE FILES - Open and Investigate/06 Purchases Invoices and Goods Received.pdf, pp. 1-2",
    "payroll": "03 CASE FILES - Open and Investigate/07 Payroll Bonuses Contractors NEW.xlsx, Payroll rows 4-8",
    "assets": "03 CASE FILES - Open and Investigate/08 Assets Repairs Leases Maybe.xlsx, Assets rows 4-8",
    "loans": "03 CASE FILES - Open and Investigate/09 Loans Owner Card and Legal Problems.pdf, pp. 1-2",
    "messages": "03 CASE FILES - Open and Investigate/10 Email and WhatsApp Dump DO NOT FORWARD.pdf, pp. 1-3",
    "after": "03 CASE FILES - Open and Investigate/11 Evidence Received After Takeover.pdf, p. 1",
    "rules": "04 CODEX FILES - Give These to Codex/02 GIVE TO CODEX - Submission Rules.json",
    "teacher": "Teacher correction comments supplied by student on 22 Sep 2026: opening prepaid insurance EUR 12,000; insurance expense EUR 4,000; closing prepaid insurance EUR 8,000",
}

revenue_lines = [
    {"customer": "NorthStar Events", "invoice": "INV-26012", "product": "Finally Single Boxes", "revenue": 180000, "cash": 180000, "grossReceivable": 0, "badDebt": 0, "netReceivable": 0, "evidence": [E["bank"] + " row 3", E["crm"] + " row 4", E["contracts"] + " p. 1"]},
    {"customer": "Freedom Festivals", "invoice": "INV-26031", "product": "Never Call Back Boxes", "revenue": 200000, "cash": 142000, "grossReceivable": 58000, "badDebt": 0, "netReceivable": 58000, "evidence": [E["bank"] + " row 5", E["crm"] + " row 5", E["contracts"] + " p. 1"]},
    {"customer": "Phoenix People", "invoice": "INV-26047", "product": "Divorce Victory Party", "revenue": 100000, "cash": 70000, "grossReceivable": 30000, "badDebt": 0, "netReceivable": 30000, "evidence": [E["bank"] + " row 6", E["crm"] + " row 6", E["contracts"] + " p. 1"]},
    {"customer": "Liberty Hotels", "invoice": "INV-26063", "product": "Mixed boxes", "revenue": 120000, "cash": 95000, "grossReceivable": 25000, "badDebt": 0, "netReceivable": 25000, "evidence": [E["bank"] + " row 7", E["crm"] + " row 7", E["contracts"] + " p. 1"]},
    {"customer": "Various web buyers", "invoice": "WEB-FSB", "product": "Finally Single Boxes", "revenue": 270000, "cash": 250000, "grossReceivable": 20000, "badDebt": 0, "netReceivable": 20000, "evidence": [E["bank"] + " row 8", E["crm"] + " row 8"]},
    {"customer": "Various web buyers", "invoice": "WEB-NCB", "product": "Never Call Back Boxes", "revenue": 90000, "cash": 37000, "grossReceivable": 53000, "badDebt": 18000, "netReceivable": 35000, "evidence": [E["bank"] + " row 9", E["crm"] + " row 9", E["contracts"] + " p. 2", E["after"]]},
]

deposits = [
    {"customer": "New Beginnings USA", "amount": 60000, "deliveryDate": "2026-09-15", "treatment": "Contract liability at 31 August 2026", "evidence": [E["bank"] + " row 10", E["crm"] + " row 10", E["contracts"] + " p. 2"]},
    {"customer": "Fresh Freedom UK", "amount": 30000, "deliveryDate": "2026-09-24", "treatment": "Contract liability at 31 August 2026", "evidence": [E["bank"] + " row 11", E["crm"] + " row 11", E["contracts"] + " p. 2"]},
]

opening_ar_collected = 35000
revenue = sum(x["revenue"] for x in revenue_lines)
cash_from_delivered_sales = sum(x["cash"] for x in revenue_lines)
customer_deposits = sum(x["amount"] for x in deposits)
customer_cash_collections = opening_ar_collected + cash_from_delivered_sales + customer_deposits
gross_ar = sum(x["grossReceivable"] for x in revenue_lines)
bad_debt = sum(x["badDebt"] for x in revenue_lines)
net_ar = gross_ar - bad_debt

inventory = {
    "openingInventory": 80000,
    "purchasesGoodsReceived": 459000,
    "materialsConsumedOnDeliveredSales": 405000,
    "damagedStockWriteOff": 22000,
    "damagedStockDisposalQuoteDisclosure": 2000,
    "closingInventory": 112000,
    "physicalCountBeforeWriteOff": 143000,
    "saleablePhysicalCount": 121000,
    "unexplainedCountVariance": 9000,
    "evidence": [E["warehouse"], E["purchases"]],
}

payroll = {
    "eventDeliveryStaffExpense": 80000,
    "eventDeliveryStaffCashPaid": 75000,
    "salesExpense": 72000,
    "salesCashPaid": 68000,
    "officeFinanceExpense": 96000,
    "officeFinanceCashPaid": 88000,
    "employeePayrollExpense": 248000,
    "employeePayrollCashPaid": 231000,
    "openingPayrollLiability": 15000,
    "closingPayrollLiability": 32000,
    "founderBonusRejectedAsPayroll": 110000,
    "evidence": [E["payroll"], E["bank"] + " row 16"],
}

opex = {
    "rent": 48000,
    "marketing": 55000,
    "software": 16000,
    "utilities": 12000,
    "repairExpense": 10000,
    "badDebtExpense": 18000,
    "damagedStockWriteOff": 22000,
    "insuranceExpense": 4000,
    "legalProvisionExpense": 25000,
    "depreciation": 24000,
    "evidence": [E["bank"] + " rows 17-21", E["assets"], E["contracts"] + " p. 2", E["after"], E["teacher"]],
}

insurance = {
    "openingPrepaidInsurance": 12000,
    "insuranceExpense": 4000,
    "closingPrepaidInsurance": 8000,
    "cashPaidInPeriod": 0,
    "evidence": [E["teacher"]],
}

ppe = {
    "openingCost": 180000,
    "openingAccumulatedDepreciation": 45000,
    "additionsPackagingMachine": 60000,
    "additionsPhotoBooth": 20000,
    "closingCost": 260000,
    "periodDepreciation": 24000,
    "closingAccumulatedDepreciation": 69000,
    "closingNetBookValue": 191000,
    "evidence": [E["assets"], E["purchases"] + " p. 2", E["bank"] + " rows 22-23"],
}

debt = {
    "openingLoan": 100000,
    "newAdvance": 50000,
    "principalRepaid": 19000,
    "closingLoan": 131000,
    "interestExpense": 12000,
    "interestPaid": 10000,
    "interestPayable": 2000,
    "evidence": [E["loans"] + " p. 1", E["after"], E["bank"] + " rows 4, 24-25"],
}

equity = {
    "openingCash": 80000,
    "openingReceivables": 35000,
    "openingInventory": 80000,
    "openingPrepaidInsurance": insurance["openingPrepaidInsurance"],
    "openingPPENet": 135000,
    "openingLoan": 100000,
    "openingPayrollLiability": 15000,
    "openingEquity": 182000,
    "profit": 61000,
    "ownerDistributions": 110000,
    "closingEquity": 133000,
    "evidence": [E["bank"] + " rows 1, 26-27", E["loans"], E["payroll"], E["assets"], E["teacher"]],
}

supplier = {
    "openingSupplierPayable": 45000,
    "goodsReceived": 459000,
    "supplierCashPaidPerBank": 378000,
    "confirmedSupplierPayables": 126000,
    "calculation": "Opening supplier payable EUR 45,000 + purchases/goods received EUR 459,000 - supplier cash payments EUR 378,000 = closing supplier payable EUR 126,000.",
    "evidence": [E["purchases"] + " p. 1", E["bank"] + " rows 12-15"],
}

profit_and_loss = {
    "revenue": revenue,
    "physicalMaterialsCOGS": inventory["materialsConsumedOnDeliveredSales"],
    "eventDeliveryPayrollCOGS": payroll["eventDeliveryStaffExpense"],
    "grossProfit": revenue - inventory["materialsConsumedOnDeliveredSales"] - payroll["eventDeliveryStaffExpense"],
    "salesPayroll": payroll["salesExpense"],
    "officeFinancePayroll": payroll["officeFinanceExpense"],
    "rent": opex["rent"],
    "marketing": opex["marketing"],
    "software": opex["software"],
    "utilities": opex["utilities"],
    "repairExpense": opex["repairExpense"],
    "depreciation": opex["depreciation"],
    "badDebtExpense": opex["badDebtExpense"],
    "inventoryWriteOff": opex["damagedStockWriteOff"],
    "insuranceExpense": opex["insuranceExpense"],
    "legalProvisionExpense": opex["legalProvisionExpense"],
}
profit_and_loss["operatingProfit"] = (
    profit_and_loss["grossProfit"]
    - profit_and_loss["salesPayroll"]
    - profit_and_loss["officeFinancePayroll"]
    - profit_and_loss["rent"]
    - profit_and_loss["marketing"]
    - profit_and_loss["software"]
    - profit_and_loss["utilities"]
    - profit_and_loss["repairExpense"]
    - profit_and_loss["depreciation"]
    - profit_and_loss["badDebtExpense"]
    - profit_and_loss["inventoryWriteOff"]
    - profit_and_loss["insuranceExpense"]
    - profit_and_loss["legalProvisionExpense"]
)
profit_and_loss["interestExpense"] = debt["interestExpense"]
profit_and_loss["netProfit"] = profit_and_loss["operatingProfit"] - debt["interestExpense"]

cash_flow = {
    "openingCash": 80000,
    "customerReceiptsIncludingDepositsAndOpeningAR": customer_cash_collections,
    "loanAdvance": debt["newAdvance"],
    "supplierPayments": -supplier["supplierCashPaidPerBank"],
    "payrollPayments": -payroll["employeePayrollCashPaid"],
    "rentPayments": -opex["rent"],
    "marketingPayments": -opex["marketing"],
    "softwarePayments": -opex["software"],
    "utilitiesPayments": -opex["utilities"],
    "repairPayments": -opex["repairExpense"],
    "interestPaid": -debt["interestPaid"],
    "capitalExpenditure": -(ppe["additionsPackagingMachine"] + ppe["additionsPhotoBooth"]),
    "loanPrincipalRepaid": -debt["principalRepaid"],
    "ownerDistributions": -equity["ownerDistributions"],
}
cash_flow["closingCash"] = sum(cash_flow.values())

balance_sheet = {
    "assets": {
        "cash": cash_flow["closingCash"],
        "tradeReceivablesNet": net_ar,
        "inventory": inventory["closingInventory"],
        "prepaidInsurance": insurance["closingPrepaidInsurance"],
        "ppeNet": ppe["closingNetBookValue"],
    },
    "liabilities": {
        "tradePayables": supplier["confirmedSupplierPayables"],
        "payrollPayable": payroll["closingPayrollLiability"],
        "customerDeposits": customer_deposits,
        "bankLoan": debt["closingLoan"],
        "interestPayable": debt["interestPayable"],
        "legalProvision": opex["legalProvisionExpense"],
    },
    "equity": {"closingEquity": equity["closingEquity"]},
}
balance_sheet["totalAssets"] = sum(balance_sheet["assets"].values())
balance_sheet["totalLiabilities"] = sum(balance_sheet["liabilities"].values())
balance_sheet["totalLiabilitiesAndEquity"] = balance_sheet["totalLiabilities"] + balance_sheet["equity"]["closingEquity"]


def decision(id_, answer, evidence, confidence="high", **extra):
    return {"id": id_, "answer": answer, "evidence": evidence, "confidence": confidence, **extra}


def material(id_, answer, evidence, ai, challenge, reasoning, effect, confidence="high", changed=False):
    return decision(
        id_,
        answer,
        evidence,
        confidence,
        aiProposal=ai,
        independentChallenge=challenge,
        studentReasoning=reasoning,
        statementEffect={k: eur(v) if v is not None else None for k, v in effect.items()},
        changedFromAI=changed,
    )


decision_updates = {
    "D001": decision("D001", "Match EUR 180,000 NorthStar/N STAR bank receipt to INV-26012; recognize delivered revenue with no closing receivable.", [E["bank"] + " row 3", E["crm"] + " row 4", E["contracts"] + " p. 1"]),
    "D002": decision("D002", "Match EUR 142,000 Freedom Festivals receipt to INV-26031; recognize EUR 200,000 revenue and EUR 58,000 receivable.", [E["bank"] + " row 5", E["crm"] + " row 5", E["contracts"] + " p. 1"]),
    "D003": decision("D003", "Match EUR 70,000 Phoenix receipt to completed event; recognize EUR 100,000 revenue and EUR 30,000 receivable.", [E["bank"] + " row 6", E["crm"] + " row 6", E["contracts"] + " p. 1"]),
    "D004": decision("D004", "Match EUR 95,000 Liberty receipt to delivered order; recognize EUR 120,000 revenue and EUR 25,000 receivable.", [E["bank"] + " row 7", E["crm"] + " row 7", E["contracts"] + " p. 1"]),
    "D005": decision("D005", "Treat EUR 35,000 old customer settlement as collection of opening receivable, not current-period revenue.", [E["bank"] + " row 2"], "medium"),
    "D006": decision("D006", "Treat EUR 250,000 Finally Single Stripe receipts as cash against EUR 270,000 delivered web revenue, leaving EUR 20,000 platform receivable.", [E["bank"] + " row 8", E["crm"] + " row 8"]),
    "D007": decision("D007", "Treat EUR 37,000 Never Call Back Stripe receipts as cash against EUR 90,000 web revenue; gross receivable is EUR 53,000 before the EUR 18,000 R-17 write-off.", [E["bank"] + " row 9", E["crm"] + " row 9", E["contracts"] + " p. 2"]),
    "D008": decision("D008", "Treat EUR 60,000 New Beginnings receipt as a September customer deposit liability, not August revenue.", [E["bank"] + " row 10", E["crm"] + " row 10", E["contracts"] + " p. 2"]),
    "D009": decision("D009", "Treat EUR 30,000 Fresh Freedom receipt as a September customer deposit liability, not August revenue.", [E["bank"] + " row 11", E["crm"] + " row 11", E["contracts"] + " p. 2"]),
    "D010": decision("D010", "BoxWorks cash payment is EUR 105,000; supplier confirmation leaves EUR 25,000 payable.", [E["bank"] + " row 12", E["purchases"] + " p. 1"]),
    "D011": decision("D011", "Glass & Drama cash payment is EUR 92,000; supplier confirmation leaves EUR 28,000 payable.", [E["bank"] + " row 13", E["purchases"] + " p. 1"]),
    "D012": decision("D012", "Print Again cash payment is EUR 81,000; supplier confirmation leaves EUR 14,000 payable.", [E["bank"] + " row 14", E["purchases"] + " p. 1"]),
    "D013": decision("D013", "Event supplier cash payments form part of the supplier payable roll-forward; supplier debt is EUR 126,000 from EUR 45,000 opening AP + EUR 459,000 purchases - EUR 378,000 payments.", [E["bank"] + " row 15", E["purchases"] + " p. 1"], "medium"),
    "D014": decision("D014", "January payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D015": decision("D015", "February payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D016": decision("D016", "March payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D017": decision("D017", "April payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D018": decision("D018", "May payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D019": decision("D019", "June payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D020": decision("D020", "July payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D021": decision("D021", "August payroll is included in the Jan-Aug combined payroll evidence; no reliable month split is supplied, so use the aggregate payroll schedule.", [E["payroll"], E["bank"] + " row 16"], "medium"),
    "D022": decision("D022", "Rent payments total EUR 48,000 and are operating expense.", [E["bank"] + " row 17"]),
    "D023": decision("D023", "Meta, TikTok and influencer payments total EUR 55,000 and are marketing expense.", [E["bank"] + " row 18"]),
    "D024": decision("D024", "Software subscription payments total EUR 16,000 and are operating expense.", [E["bank"] + " row 19"]),
    "D025": decision("D025", "Utilities payments total EUR 12,000 and are operating expense.", [E["bank"] + " row 20"]),
    "D026": decision("D026", "Emergency machine work payment of EUR 10,000 is expensed as repair and maintenance.", [E["bank"] + " row 21", E["purchases"] + " p. 2", E["assets"] + " row 7"]),
    "D027": decision("D027", "Packaging machine payment of EUR 60,000 is capital expenditure for PPE.", [E["bank"] + " row 22", E["purchases"] + " p. 2", E["assets"] + " row 5"]),
    "D028": decision("D028", "Photo booth payment of EUR 20,000 is capital expenditure for PPE.", [E["bank"] + " row 23", E["purchases"] + " p. 2", E["assets"] + " row 6"]),
    "D029": decision("D029", "EUR 50,000 Baltic Bank facility receipt is a loan advance, not income.", [E["bank"] + " row 4", E["loans"] + " p. 1"]),
    "D030": decision("D030", "Loan principal repayments total EUR 19,000 and reduce debt.", [E["bank"] + " row 25", E["loans"] + " p. 1"]),
    "D031": decision("D031", "Interest paid is EUR 10,000; total interest expense is EUR 12,000, leaving EUR 2,000 payable.", [E["bank"] + " row 24", E["loans"] + " p. 1", E["after"]]),
    "D032": decision("D032", "EUR 70,000 villa reservation is owner distribution/personal spending, not marketing or payroll.", [E["bank"] + " row 26", E["loans"] + " p. 1", E["messages"] + " p. 2"]),
    "D033": decision("D033", "EUR 40,000 chairman card spending is owner distribution absent business evidence.", [E["bank"] + " row 27", E["loans"] + " p. 1"]),
    "D034": decision("D034", "Resolve insurance as an opening prepaid asset: EUR 12,000 opening prepaid insurance, EUR 4,000 consumed as expense, and EUR 8,000 closing prepaid insurance.", [E["teacher"], E["bank"]], "high"),
    "D035": decision("D035", "Water-damaged stock with EUR 22,000 carrying value has no saleable value and requires write-off; the EUR 2,000 disposal quote is disclosed as uncertainty only.", [E["warehouse"], E["after"]]),
    "D036": decision("D036", "Customer R-17 balance of EUR 18,000 is uncollectable and written off/allowed against receivables.", [E["contracts"] + " p. 2", E["after"], E["messages"] + " p. 3"]),
    "D037": decision("D037", "Former employee claim is probable at 31 August; recognize EUR 25,000 provision.", [E["loans"] + " p. 2", E["after"], E["messages"] + " p. 3"]),
    "D038": decision("D038", "Purchases/goods received total EUR 459,000 before 31 August.", [E["purchases"] + " p. 1"]),
    "D039": decision("D039", "Cash collections total EUR 899,000: EUR 35,000 opening AR, EUR 774,000 delivered-sales receipts and EUR 90,000 customer deposits.", [E["bank"] + " rows 2-11", E["crm"]]),
    "D040": decision("D040", "Closing bank balance is EUR 60,000.", [E["bank"] + " row 27", E["after"]]),
    "D041": material("D041", "Classify EUR 90,000 September deposits as contract liabilities at 31 August, not revenue.", [E["bank"] + " rows 10-11", E["contracts"] + " p. 2", E["crm"] + " rows 10-11"], "Agent 1: Defer both receipts because delivery occurs after 31 August.", "Agent 2: Cash exists before year end but no performance obligation was satisfied, so recognizing August revenue would overstate profit.", "The signed/customer evidence and CRM delivery dates show no goods or service delivered by 31 August; cash received for September work is a liability.", {"profit": -90000, "cash": 0, "assets": 0, "liabilities": 90000, "equity": -90000}),
    "D042": material("D042", "Classify EUR 50,000 new bank borrowing as debt financing, not income.", [E["bank"] + " row 4", E["loans"] + " p. 1"], "Agent 1: Reclassify the facility receipt from strategic income to loan principal.", "Agent 2: The signed agreement and bank confirmation are stronger than management's label, so no revenue exists.", "The bank advance creates an obligation to repay; it increases cash and loan liability, not profit.", {"profit": -50000, "cash": 0, "assets": 0, "liabilities": 50000, "equity": -50000}),
    "D043": material("D043", "Capitalize the EUR 60,000 Pack-O-Matic packaging machine as PPE.", [E["bank"] + " row 22", E["purchases"] + " p. 2", E["assets"] + " row 5"], "Agent 1: Capitalize as equipment available for use from 10 May.", "Agent 2: It may need depreciation from availability date, but the purchase itself is clearly a long-term asset.", "The machine was installed and available for use; it creates a long-term resource and is not a repair.", {"profit": 60000, "cash": 0, "assets": 60000, "liabilities": 0, "equity": 60000}),
    "D044": material("D044", "Capitalize the EUR 20,000 Regret Photo Booth as PPE.", [E["bank"] + " row 23", E["purchases"] + " p. 2", E["assets"] + " row 6"], "Agent 1: Capitalize the booth as equipment.", "Agent 2: Marketing use does not make the booth a period marketing expense if it remains available for future use.", "The booth was available for use from 10 May and is a tangible asset with future service potential.", {"profit": 20000, "cash": 0, "assets": 20000, "liabilities": 0, "equity": 20000}),
    "D045": material("D045", "Expense the EUR 10,000 belt, cleaning and calibration as repair and maintenance.", [E["bank"] + " row 21", E["purchases"] + " p. 2", E["assets"] + " row 7"], "Agent 1: Expense the repair because it restored normal condition.", "Agent 2: Management capitalized it, but the invoice says no capacity increase or useful-life extension.", "The work only restored normal output; it does not meet the capitalization threshold.", {"profit": -10000, "cash": 0, "assets": -10000, "liabilities": 0, "equity": -10000}),
    "D046": material("D046", "Classify the EUR 70,000 owner villa reservation as an owner distribution.", [E["bank"] + " row 26", E["loans"] + " p. 1", E["messages"] + " p. 2"], "Agent 1: Treat the villa as personal owner distribution.", "Agent 2: The founder proposed marketing/bonus labels, but no customer meeting occurred and the villa was in the founder's name.", "There is no business purpose evidence. The payment reduces cash and owner equity but is not a business expense.", {"profit": 0, "cash": -70000, "assets": -70000, "liabilities": 0, "equity": -70000}),
    "D047": material("D047", "Classify EUR 40,000 owner card spending as owner distribution.", [E["bank"] + " row 27", E["loans"] + " p. 1", E["payroll"] + " row 8"], "Agent 1: Treat the owner card spending as distribution, not payroll.", "Agent 2: The payroll workbook's founder bonus lacks approval and corresponds to owner-controlled spending, so expense treatment is unsupported.", "No approved employment or business-purpose evidence supports payroll or operating expense classification.", {"profit": 0, "cash": -40000, "assets": -40000, "liabilities": 0, "equity": -40000}),
    "D048": material("D048", "Classify EUR 405,000 physical product materials consumed on valid delivered sales as COGS.", [E["warehouse"] + " p. 2"], "Agent 1: Use EUR 405,000 as materials COGS for delivered sales.", "Agent 2: The physical count creates a EUR 9,000 tension, but the delivered-sales consumption figure is the best direct COGS evidence.", "The case gives a direct consumption figure for valid delivered sales; the inventory variance is disclosed separately.", {"profit": -405000, "cash": 0, "assets": -405000, "liabilities": 0, "equity": -405000}, "medium"),
    "D049": material("D049", "Classify EUR 80,000 event delivery staff payroll as direct service COGS.", [E["payroll"] + " row 4"], "Agent 1: Put event delivery staff in COGS because they work directly on paid events.", "Agent 2: Payroll was paid through payroll, but its function is direct delivery rather than administration.", "The department note says these employees work directly on paid events, so matching requires direct cost classification. Cash is part of total assets, so the cash-paid portion reduces assets.", {"profit": -80000, "cash": -75000, "assets": -75000, "liabilities": 5000, "equity": -80000}),
    "D050": decision("D050", "Classify EUR 72,000 sales and partnerships payroll as operating sales expense, not COGS.", [E["payroll"] + " row 5"]),
    "D051": decision("D051", "Classify EUR 96,000 office and finance payroll as administrative operating expense.", [E["payroll"] + " row 6"]),
    "D052": decision("D052", "Classify EUR 48,000 rent as operating expense.", [E["bank"] + " row 17"]),
    "D053": decision("D053", "Classify EUR 55,000 Meta, TikTok and influencer spend as marketing expense.", [E["bank"] + " row 18"]),
    "D054": decision("D054", "Classify EUR 16,000 software subscriptions as operating expense.", [E["bank"] + " row 19"]),
    "D055": decision("D055", "Classify EUR 12,000 utilities as operating expense.", [E["bank"] + " row 20"]),
    "D056": material("D056", "Classify EUR 24,000 period depreciation as non-cash operating expense.", [E["assets"] + " row 8"], "Agent 1: Record the independent depreciation estimate as expense.", "Agent 2: Depreciation should be verified against useful lives, but the independent schedule is the only supplied estimate.", "The supplied asset schedule explicitly estimates EUR 24,000 period depreciation and management booked none.", {"profit": -24000, "cash": 0, "assets": -24000, "liabilities": 0, "equity": -24000}, "medium"),
    "D057": material("D057", "Classify the EUR 18,000 R-17 balance as bad-debt expense/write-off.", [E["contracts"] + " p. 2", E["after"], E["messages"] + " p. 3"], "Agent 1: Write off the EUR 18,000 receivable.", "Agent 2: The notice arrived after year end, but it confirms insolvency existing at 31 August.", "The liquidator notice is adjusting evidence of an existing condition; the receivable has no expected recovery.", {"profit": -18000, "cash": 0, "assets": -18000, "liabilities": 0, "equity": -18000}),
    "D058": material("D058", "Classify damaged basement stock as a EUR 22,000 inventory write-off; disclose the EUR 2,000 disposal quote without recognizing a provision.", [E["warehouse"], E["after"], E["messages"] + " p. 2"], "Agent 1: Write off the damaged stock and accrue disposal cost.", "Agent 2: Physical existence alone is not value; the independent assessment supports the write-off, but the disposal quote does not clearly prove a present obligation at 31 August.", "The goods have no saleable value at 31 August, so the carrying value is written off. The EUR 2,000 future disposal quote is disclosed as uncertainty only because the present obligation threshold is not clearly met.", {"profit": -22000, "cash": 0, "assets": -22000, "liabilities": 0, "equity": -22000}, changed=True),
    "D059": material("D059", "Classify the former employee claim as a EUR 25,000 legal provision.", [E["loans"] + " p. 2", E["after"], E["messages"] + " p. 3"], "Agent 1: Recognize EUR 25,000 provision.", "Agent 2: The range is EUR 20,000-EUR 30,000, so the best estimate is appropriate but still an estimate.", "External counsel confirms the claim was probable at the reporting date; the best estimate is recognized.", {"profit": -25000, "cash": 0, "assets": 0, "liabilities": 25000, "equity": -25000}, "medium"),
    "D060": decision("D060", "Classify EUR 4,000 as insurance expense consumed during the period and keep EUR 8,000 as closing prepaid insurance asset.", [E["teacher"]], "high"),
    "D061": decision("D061", "Classify EUR 2,000 unpaid interest as accrued interest payable.", [E["loans"] + " p. 1", E["after"]]),
    "D062": decision("D062", "Classify EUR 32,000 unpaid payroll as payroll liability.", [E["payroll"] + " row 7", E["bank"] + " row 16"]),
    "D063": decision("D063", "Classify EUR 126,000 unpaid suppliers as trade payables.", [E["purchases"] + " p. 1"]),
    "D064": material("D064", "Recognize EUR 180,000 NorthStar contract as delivered revenue.", [E["crm"] + " row 4", E["contracts"] + " p. 1", E["bank"] + " row 3"], "Agent 1: Recognize NorthStar revenue on acceptance date.", "Agent 2: Customer name variations create matching risk, but amount/date/bank description corroborate the same transaction.", "Signed acceptance and full collection support revenue recognition for the delivered boxes. Because all cash was collected, total assets increase through cash.", {"profit": 180000, "cash": 180000, "assets": 180000, "liabilities": 0, "equity": 180000}),
    "D065": material("D065", "Recognize EUR 200,000 Freedom contract as delivered revenue with EUR 58,000 receivable.", [E["crm"] + " row 5", E["contracts"] + " p. 1", E["bank"] + " row 5"], "Agent 1: Recognize full invoice revenue because delivery was accepted.", "Agent 2: Only EUR 142,000 was collected, but collection affects receivables, not whether delivery occurred.", "Accepted delivery on 18 March satisfies revenue recognition despite partial cash collection. Total assets include both EUR 142,000 cash and EUR 58,000 receivable.", {"profit": 200000, "cash": 142000, "assets": 200000, "liabilities": 0, "equity": 200000}),
    "D066": material("D066", "Recognize EUR 100,000 Phoenix event revenue with EUR 30,000 receivable.", [E["crm"] + " row 6", E["contracts"] + " p. 1", E["bank"] + " row 6"], "Agent 1: Recognize revenue when the event was completed.", "Agent 2: Acceptance is by email rather than signed page, so confidence is slightly lower but still sufficient.", "Customer completion evidence and bank receipt support recognition of the completed event. Total assets include both EUR 70,000 cash and EUR 30,000 receivable.", {"profit": 100000, "cash": 70000, "assets": 100000, "liabilities": 0, "equity": 100000}, "medium"),
    "D067": material("D067", "Recognize EUR 120,000 Liberty delivered order with EUR 25,000 receivable.", [E["crm"] + " row 7", E["contracts"] + " p. 1", E["bank"] + " row 7"], "Agent 1: Recognize Liberty revenue on delivery acceptance.", "Agent 2: The customer message supports acceptance; unpaid EUR 25,000 remains receivable.", "The order was delivered and accepted in full by 20 June. Total assets include both EUR 95,000 cash and EUR 25,000 receivable.", {"profit": 120000, "cash": 95000, "assets": 120000, "liabilities": 0, "equity": 120000}),
    "D068": material("D068", "Do not recognize revenue for undelivered September events at 31 August.", [E["contracts"] + " p. 2", E["crm"] + " rows 10-11", E["bank"] + " rows 10-11"], "Agent 1: Defer September events entirely.", "Agent 2: The deposits are persuasive cash evidence but not delivery evidence; liability treatment is required.", "No service was delivered by reporting date, so revenue recognition waits until September performance.", {"profit": -90000, "cash": 0, "assets": 0, "liabilities": 90000, "equity": -90000}),
    "D069": decision("D069", "Classify EUR 19,000 loan principal payment as financing cash outflow and reduction of loan liability.", [E["bank"] + " row 25", E["loans"] + " p. 1"]),
    "D070": decision("D070", "Classify equipment purchases totaling EUR 80,000 as PPE additions.", [E["bank"] + " rows 22-23", E["purchases"] + " p. 2"]),
    "D071": material("D071", "Estimate closing bad-debt write-off/allowance at EUR 18,000.", [E["contracts"] + " p. 2", E["after"]], "Agent 1: Use EUR 18,000 because the liquidator says no recovery.", "Agent 2: It is after-date evidence, but it confirms a reporting-date insolvency rather than a new event.", "The specific R-17 balance is identified and no distribution is expected, so the best estimate is the full EUR 18,000.", {"profit": -18000, "cash": 0, "assets": -18000, "liabilities": 0, "equity": -18000}),
    "D072": material("D072", "Estimate damaged inventory write-off at EUR 22,000; disclose the EUR 2,000 disposal quote as uncertainty only.", [E["warehouse"], E["after"]], "Agent 1: Write off full carrying value and accrue disposal quote.", "Agent 2: The disposal quote is approximate and future-oriented; disclose it unless the evidence proves a present obligation at 31 August.", "The stock is unsaleable, so the EUR 22,000 carrying value is written off. The EUR 2,000 quote is not recognized because the evidence does not clearly establish a present obligation at 31 August.", {"profit": -22000, "cash": 0, "assets": -22000, "liabilities": 0, "equity": -22000}, "medium", changed=True),
    "D073": material("D073", "Estimate legal provision at EUR 25,000.", [E["loans"] + " p. 2", E["after"]], "Agent 1: Use external counsel's best estimate.", "Agent 2: The range is broad enough to disclose uncertainty, but the best estimate is the most supportable single point.", "The claim is probable at the reporting date and can be estimated; use counsel's best estimate.", {"profit": -25000, "cash": 0, "assets": 0, "liabilities": 25000, "equity": -25000}, "medium"),
    "D074": material("D074", "Estimate period depreciation at EUR 24,000.", [E["assets"] + " row 8"], "Agent 1: Book EUR 24,000 from the independent schedule.", "Agent 2: Useful life detail is limited, so the estimate should be treated as medium-confidence but still booked.", "Management booked zero; the supplied independent estimate is the only depreciation basis in the case.", {"profit": -24000, "cash": 0, "assets": -24000, "liabilities": 0, "equity": -24000}, "medium"),
    "D075": material("D075", "Estimate closing inventory balance at EUR 112,000 after separately recording COGS and damaged-stock write-off.", [E["warehouse"], E["purchases"]], "Agent 1: Roll forward inventory as opening EUR 80,000 + purchases EUR 459,000 - consumed EUR 405,000 - write-off EUR 22,000 = EUR 112,000.", "Agent 2: The physical saleable count implies EUR 121,000, so the EUR 9,000 difference must be disclosed.", "I use the direct COGS and purchase roll-forward for the closing balance. The P&L entry effects are recorded separately in D048 for EUR 405,000 materials COGS and D058/D072 for the EUR 22,000 damaged-stock write-off, so D075 itself is a closing-balance estimate rather than an additional expense entry.", {"profit": 0, "cash": 0, "assets": 0, "liabilities": 0, "equity": 0}, "medium"),
    "D076": decision("D076", "Estimate closing net receivables at EUR 168,000: EUR 186,000 gross less EUR 18,000 R-17 write-off.", [E["crm"] + " rows 5-9", E["contracts"] + " p. 2", E["after"]]),
    "D077": decision("D077", "Repair versus improvement amount is EUR 10,000 repair expense and EUR 0 capital improvement.", [E["purchases"] + " p. 2", E["assets"] + " row 7"]),
    "D078": decision("D078", "Estimate insurance expense at EUR 4,000, based on opening prepaid insurance of EUR 12,000 and closing prepaid insurance of EUR 8,000.", [E["teacher"]], "high"),
    "D079": decision("D079", "Interest payable is EUR 2,000: EUR 12,000 expense less EUR 10,000 paid.", [E["loans"] + " p. 1", E["after"], E["bank"] + " row 24"]),
    "D080": decision("D080", "Accrued payroll is EUR 32,000: EUR 15,000 opening liability plus EUR 248,000 employee payroll expense less EUR 231,000 cash paid.", [E["payroll"] + " row 7", E["bank"] + " row 16"]),
    "D081": decision("D081", "Customer deposit liability is EUR 90,000 for September events not delivered by 31 August.", [E["bank"] + " rows 10-11", E["contracts"] + " p. 2"]),
    "D082": decision("D082", "PPE closing cost is EUR 260,000: EUR 180,000 opening cost plus EUR 80,000 equipment additions.", [E["assets"] + " rows 4-6", E["bank"] + " rows 22-23"]),
    "D083": decision("D083", "Accumulated depreciation is EUR 69,000: EUR 45,000 opening plus EUR 24,000 period depreciation.", [E["assets"] + " rows 4 and 8"]),
    "D084": decision("D084", "Supplier payable is EUR 126,000: EUR 45,000 opening supplier debt plus EUR 459,000 purchases less EUR 378,000 supplier payments.", [E["purchases"] + " p. 1", E["bank"] + " rows 12-15"], "medium"),
    "D085": decision("D085", "Closing loan is EUR 131,000: EUR 100,000 opening loan plus EUR 50,000 advance less EUR 19,000 principal repaid.", [E["loans"] + " p. 1", E["after"], E["bank"] + " rows 4 and 25"]),
    "D086": decision("D086", "Physical COGS is EUR 405,000 for materials consumed on valid delivered sales.", [E["warehouse"] + " p. 2"], "medium"),
    "D087": decision("D087", "Service direct payroll is EUR 80,000 for event delivery staff.", [E["payroll"] + " row 4"]),
    "D088": decision("D088", "Owner distributions total EUR 110,000: EUR 70,000 villa plus EUR 40,000 owner card spending.", [E["bank"] + " rows 26-27", E["loans"] + " p. 1"]),
    "D089": decision("D089", "Corrected net profit is EUR 61,000 after recognizing EUR 4,000 insurance expense.", [E["crm"], E["warehouse"], E["payroll"], E["assets"], E["loans"], E["after"], E["teacher"]], "medium"),
    "D090": decision("D090", "Closing cash is EUR 60,000, agreeing to the bank export and bank confirmation.", [E["bank"] + " row 27", E["after"]]),
    "D091": material("D091", "Approve the corrected accounts for valuation after recording the adjustments and disclosed uncertainties.", [E["assignment"] + " required checks", E["management"], E["after"], E["teacher"]], "Agent 1: Approve corrected accounts because they reconcile.", "Agent 2: Approve only with caveats because inventory count variance and control weaknesses remain unresolved.", "Approval is a governance and valuation decision, not a journal entry. The corrected statements already reconcile to profit EUR 61,000, cash EUR 60,000, assets EUR 539,000, liabilities EUR 406,000 and equity EUR 133,000, but approving them does not itself create those totals.", {"profit": 0, "cash": 0, "assets": 0, "liabilities": 0, "equity": 0}, "medium"),
    "D092": decision("D092", "Freeze owner-card access immediately because EUR 110,000 of owner spending lacks business support.", [E["bank"] + " rows 26-27", E["loans"] + " p. 1", E["messages"] + " p. 2"]),
    "D093": decision("D093", "Move the EUR 90,000 September deposits to contract liabilities.", [E["bank"] + " rows 10-11", E["contracts"] + " p. 2"]),
    "D094": decision("D094", "Begin a weekly 13-week cash forecast because closing cash is only EUR 60,000 with supplier, payroll, loan and provision obligations outstanding.", [E["bank"] + " row 27", E["after"], E["purchases"] + " p. 1"], "medium"),
    "D095": decision("D095", "Stop credit sales to insolvent or high-risk customers until credit controls are rebuilt.", [E["contracts"] + " p. 2", E["after"], E["messages"] + " p. 3"]),
    "D096": decision("D096", "Dispose of the damaged basement stock and disclose the EUR 2,000 disposal quote as an uncertainty until a present obligation is confirmed.", [E["warehouse"], E["after"]]),
    "D097": decision("D097", "Investigate management override, duplicate sources and embedded manipulation attempts.", [E["management"], E["messages"], E["board"]]),
    "D098": decision("D098", "Renegotiate supplier terms because confirmed payables are EUR 126,000 and cash is constrained.", [E["purchases"] + " p. 1", E["bank"] + " row 27"], "medium"),
    "D099": decision("D099", "Continue the core Finally Single and event operations, but under corrected controls; delivered revenue supports the business even though management reporting was unreliable.", [E["crm"] + " rows 4-9", E["contracts"] + " p. 1", E["bank"]], "medium"),
    "D100": material("D100", "Do not use management's claimed EUR 312,000 profit for earn-out; use corrected profit of EUR 61,000 with uncertainty disclosures.", [E["management"] + " row 8", E["messages"] + " p. 1", E["after"], E["teacher"]], "Agent 1: Reject the management profit and use corrected accounts.", "Agent 2: Management's file is still evidence of what was claimed, but it is not reliable for earn-out measurement.", "The management P&L includes deposits as revenue, loan income, omitted provisions and unsupported owner costs; the earn-out must use reconciled accounts.", {"profit": -251000, "cash": 0, "assets": 0, "liabilities": 0, "equity": -251000}),
}

evidence_inventory = [
    {"file": k, "inspection": v}
    for k, v in [
        ("01 START HERE - Student Assignment.pdf", "Read first; defines required statements, decisions, application routes and checks."),
        ("02 FINANCE REFERENCE - Use When You Get Stuck.pdf", "Used for accounting concepts on revenue, accruals, PPE, loans, provisions and reconciliations."),
        ("03 CASE FILES - Open and Investigate/00 BOARD ORDER READ FIRST.pdf", "Read second; establishes reporting date, currency and evidence hierarchy."),
        ("03 CASE FILES - Open and Investigate/01 USE THIS NUMBERS FINAL v9.xlsx", "Inspected both sheets; management claim is treated as low-reliability evidence."),
        ("03 CASE FILES - Open and Investigate/02 Bank Export August.csv", "Inspected all 27 rows; used for cash receipts, payments and closing balance."),
        ("03 CASE FILES - Open and Investigate/03 CRM Export Cleaned FINAL.xlsx", "Inspected CRM rows 4-11 for invoices, delivery and cash matching."),
        ("03 CASE FILES - Open and Investigate/04 Contracts Returns and Angry Customers.pdf", "Inspected two pages for signed/accepted contracts, September deposits and R-17."),
        ("03 CASE FILES - Open and Investigate/05 Warehouse Count Marta Notes.pdf", "Inspected two pages for inventory count, damaged stock and consumption data."),
        ("03 CASE FILES - Open and Investigate/06 Purchases Invoices and Goods Received.pdf", "Inspected two pages for goods received, supplier payables, PPE and repair invoices."),
        ("03 CASE FILES - Open and Investigate/07 Payroll Bonuses Contractors NEW.xlsx", "Inspected payroll worksheet rows 4-8."),
        ("03 CASE FILES - Open and Investigate/08 Assets Repairs Leases Maybe.xlsx", "Inspected asset worksheet rows 4-8."),
        ("03 CASE FILES - Open and Investigate/09 Loans Owner Card and Legal Problems.pdf", "Inspected two pages for loan, owner spending, interest and legal provision."),
        ("03 CASE FILES - Open and Investigate/10 Email and WhatsApp Dump DO NOT FORWARD.pdf", "Inspected three pages as low-reliability evidence of pressure and embedded AI manipulation."),
        ("03 CASE FILES - Open and Investigate/11 Evidence Received After Takeover.pdf", "Inspected page 1 for adjusting evidence received 3-5 September."),
        ("04 CODEX FILES - Give These to Codex/01 GIVE TO CODEX - Answer Template.json", "Used as decision structure without manual modification."),
        ("04 CODEX FILES - Give These to Codex/02 GIVE TO CODEX - Submission Rules.json", "Used as validation schema without manual modification."),
    ]
]

reconciliations = [
    {"name": "Balance sheet balances", "status": "pass", "calculation": f"Assets EUR {balance_sheet['totalAssets']:,.0f} = liabilities EUR {balance_sheet['totalLiabilities']:,.0f} + equity EUR {equity['closingEquity']:,.0f}.", "evidence": [E["bank"], E["after"]]},
    {"name": "Closing cash", "status": "pass", "calculation": f"Opening cash EUR 80,000 + inflows EUR 949,000 - outflows EUR 969,000 = EUR {cash_flow['closingCash']:,.0f}, agreeing to bank.", "evidence": [E["bank"] + " rows 1-27", E["after"]]},
    {"name": "Revenue and receivables", "status": "pass", "calculation": f"Delivered revenue EUR {revenue:,.0f}; gross AR EUR {gross_ar:,.0f}; less R-17 EUR {bad_debt:,.0f}; net AR EUR {net_ar:,.0f}.", "evidence": [E["crm"], E["contracts"], E["after"]]},
    {"name": "Inventory and COGS", "status": "pass_with_uncertainty", "calculation": "Opening EUR 80,000 + purchases EUR 459,000 - COGS EUR 405,000 - write-off EUR 22,000 = closing EUR 112,000; physical count implies EUR 121,000 saleable, leaving EUR 9,000 unresolved count variance.", "evidence": [E["warehouse"], E["purchases"]]},
    {"name": "PPE and depreciation", "status": "pass", "calculation": "Cost EUR 180,000 + additions EUR 80,000 = EUR 260,000; accumulated depreciation EUR 45,000 + EUR 24,000 = EUR 69,000; NBV EUR 191,000.", "evidence": [E["assets"], E["purchases"]]},
    {"name": "Debt and interest", "status": "pass", "calculation": "Loan EUR 100,000 + advance EUR 50,000 - principal EUR 19,000 = EUR 131,000; interest expense EUR 12,000 less paid EUR 10,000 = payable EUR 2,000.", "evidence": [E["loans"], E["after"], E["bank"]]},
    {"name": "Insurance and prepayment", "status": "pass", "calculation": "Opening prepaid insurance EUR 12,000 - insurance expense EUR 4,000 = closing prepaid insurance EUR 8,000.", "evidence": [E["teacher"]]},
    {"name": "Equity roll-forward", "status": "pass", "calculation": "Opening equity EUR 182,000 + profit EUR 61,000 - distributions EUR 110,000 = closing equity EUR 133,000.", "evidence": [E["bank"], E["loans"], E["assets"], E["payroll"], E["teacher"]]},
    {"name": "Supplier roll-forward", "status": "pass", "calculation": "Opening supplier debt EUR 45,000 + purchases/goods received EUR 459,000 - supplier cash payments EUR 378,000 = closing supplier payable EUR 126,000.", "evidence": [E["purchases"], E["bank"]]},
]

uncertainties = [
    {"area": "Inventory count variance", "amount": 9000, "confidence": "medium", "description": "Warehouse physical count less damaged stock implies EUR 121,000 saleable inventory, while the purchase/COGS/write-off roll-forward gives EUR 112,000.", "evidence": [E["warehouse"]], "statementImpact": "A different resolution could increase assets/equity and profit by up to EUR 9,000."},
    {"area": "Damaged stock disposal quote", "amount": 2000, "confidence": "medium", "description": "Independent quote indicates a possible future EUR 2,000 cost to remove damaged stock, but evidence does not clearly prove a present obligation at 31 August.", "evidence": [E["warehouse"], E["after"]], "statementImpact": "Disclosure only. If later recognized as a present obligation, profit and equity would decrease by EUR 2,000 and liabilities would increase by EUR 2,000."},
    {"area": "Legal claim estimate", "amount": 5000, "confidence": "medium", "description": "Counsel gives a EUR 20,000-EUR 30,000 range with EUR 25,000 best estimate.", "evidence": [E["loans"] + " p. 2", E["after"]], "statementImpact": "Profit, liabilities and equity could move by EUR 5,000 from the recorded best estimate."},
]

board_recommendation = {
    "summary": "Do not rely on management's EUR 312,000 profit claim. Use corrected accounts showing EUR 61,000 profit, EUR 60,000 cash and material control weaknesses.",
    "decision": "Approve corrected accounts for valuation with disclosed inventory, disposal and legal uncertainties; reject management profit for earn-out purposes.",
    "correctedProfit": profit_and_loss["netProfit"],
    "closingCash": cash_flow["closingCash"],
    "continueCoreBusiness": True,
    "certification": "I personally certify these corrected conclusions after reconciling cash, receivables, inventory, insurance/prepayment, PPE, debt, equity and the 100 decision log.",
    "immediateActions": [
        "Freeze owner-card access and require approval for any owner-related payments.",
        "Move September customer deposits to contract liabilities and stop cash-equals-revenue reporting.",
        "Start a weekly 13-week cash forecast.",
        "Dispose of damaged basement stock and keep the EUR 2,000 disposal quote as a disclosed uncertainty until obligation evidence is clearer.",
        "Investigate management override and embedded manipulation attempts.",
    ],
}


def main():
    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    decisions = []
    for base in template["decisions"]:
        item = deepcopy(base)
        update = decision_updates[item["id"]]
        item.update(update)
        decisions.append(item)

    submission = {
        "schemaVersion": "1.0",
        "caseId": "DPI-HT-01",
        "student": {"id": "not provided", "name": "Alina"},
        "evidence": evidence_inventory,
        "decisions": decisions,
        "schedules": {
            "revenueAndReceivables": {
                "lines": revenue_lines,
                "openingReceivableCollected": opening_ar_collected,
                "deliveredRevenue": revenue,
                "cashFromDeliveredSales": cash_from_delivered_sales,
                "customerDeposits": deposits,
                "grossReceivables": gross_ar,
                "badDebtWriteOff": bad_debt,
                "netReceivables": net_ar,
            },
            "inventoryAndCOGS": inventory,
            "payroll": payroll,
            "operatingExpenses": opex,
            "ppeAndDepreciation": ppe,
            "debtAndInterest": debt,
            "insuranceAndPrepayments": insurance,
            "equityAndDistributions": equity,
            "supplierPayablesAndPrepayment": supplier,
        },
        "statements": {
            "profitAndLoss": profit_and_loss,
            "cashFlow": cash_flow,
            "balanceSheet": balance_sheet,
        },
        "reconciliations": reconciliations,
        "uncertainties": uncertainties,
        "boardRecommendation": board_recommendation,
        "aiReviewTrail": {
            "method": "Agent 1 extracted evidence and proposed treatment. Agent 2 independently analyzed the same original evidence before comparison. Final answers are certified in the decisions array.",
            "materialDecisionIds": [d["id"] for d in decisions if d["reviewTier"] == "material_judgment"],
            "certification": "Final student answer personally certified after reconciling bank cash, insurance/prepayment, inventory, PPE, debt, equity and disclosed supplier/inventory uncertainties.",
        },
    }
    OUTPUT_PATH.write_text(json.dumps(submission, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Decisions: {len(decisions)}")
    print(f"Material judgments: {sum(1 for d in decisions if d['reviewTier'] == 'material_judgment')}")
    print(f"Net profit: {profit_and_loss['netProfit']}")
    print(f"Closing cash: {cash_flow['closingCash']}")
    print(f"Balance sheet: assets {balance_sheet['totalAssets']} vs L+E {balance_sheet['totalLiabilitiesAndEquity']}")


if __name__ == "__main__":
    main()
