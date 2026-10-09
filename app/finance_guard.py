"""Deterministic routing for *fully specified* financial scenarios.

Never delegate arithmetic for these scenarios to a language model. If a prompt
cannot be safely parsed, leave it to advisory dialogue, which must avoid
unsupported arithmetic and instead request use of the calculator tab.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from app.tools.market_tools import calculate_unit_economics


@dataclass(frozen=True)
class FinancialInputs:
    orders: int
    ticket: float
    days: int
    food: float
    other: float
    delivery: float
    commission: float
    scenarios: tuple[int, ...]


def _get(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1) if match else None


def extract_financial_inputs(text: str) -> FinancialInputs | None:
    """Parse explicitly labelled values only; never infer missing percentages."""
    if not re.search(r"\b(financial|economic|contribution|margin|revenue|profitability|costs?)\b", text, re.I):
        return None
    patterns = {
        "orders": r"\b(?:daily\s+orders|orders\s+per\s+day|orders/day)\s*[:=]\s*(\d+)",
        "ticket": r"\b(?:average\s+order\s+value|average\s+ticket|aov)\s*[:=]\s*(?:AED\s*)?(\d+(?:\.\d+)?)",
        "days": r"\b(?:trading\s+days\s+per\s+month|trading\s+days/month)\s*[:=]\s*(\d+)",
        "food": r"\bfood\s+cost(?:s)?\s*[:=]\s*(\d+(?:\.\d+)?)\s*%",
        "other": r"\b(?:combined\s+)?(?:labou?r(?:,\s*rent)?(?:,\s*and\s*other\s+operating)?\s+costs?|labou?r/rent/other(?:\s+costs?)?|operating\s+costs?)\s*[:=]\s*(\d+(?:\.\d+)?)\s*%",
        "delivery": r"\bdelivery\s+(?:share|sales\s+share)\s*[:=]\s*(\d+(?:\.\d+)?)\s*%",
        "commission": r"\bdelivery\s+commission\s*[:=]\s*(\d+(?:\.\d+)?)\s*%",
    }
    vals = {key: _get(pat, text) for key, pat in patterns.items()}
    # An explicit, complete assumption set is required: otherwise a model can
    # discuss strategy but should not fabricate precise financial outputs.
    if any(value is None for key, value in vals.items() if key != "days"):
        return None
    days = int(vals["days"]) if vals["days"] is not None else 30
    match = re.search(r"(?:scenarios?\s+(?:with|of)\s+)(\d+)\s*,\s*(\d+)\s*,\s*and\s*(\d+)\s+(?:daily\s+orders|orders\s+per\s+day)", text, re.I)
    orders = int(vals["orders"])
    scenarios = tuple(int(x) for x in match.groups()) if match else (orders,)
    # All numeric constraints are checked by the deterministic calculator.
    parsed = FinancialInputs(
        orders=orders, ticket=float(vals["ticket"]), days=days,
        food=float(vals["food"])/100, other=float(vals["other"])/100,
        delivery=float(vals["delivery"])/100, commission=float(vals["commission"])/100,
        scenarios=scenarios,
    )
    if not 1 <= parsed.days <= 31:
        raise ValueError("trading days per month must be 1–31")
    for volume in {*parsed.scenarios, parsed.orders}:
        calculate_unit_economics(volume, parsed.ticket, parsed.food, parsed.other,
                                 parsed.delivery, parsed.commission,
                                 trading_days_per_month=parsed.days)
    return parsed


def format_financial_scenarios(inputs: FinancialInputs) -> str:
    """Generate an auditable table without making an LLM call."""
    outputs = []
    for orders in inputs.scenarios:
        outputs.append(json.loads(calculate_unit_economics(
            orders, inputs.ticket, inputs.food, inputs.other,
            inputs.delivery, inputs.commission,
            trading_days_per_month=inputs.days,
        )))
    header = "| Metric (AED unless noted) | " + " | ".join(f"{int(r['assumptions']['orders_per_day'])} orders/day" for r in outputs) + " |"
    separator = "|---|" + "---:|" * len(outputs)
    fields = [
        ("Monthly orders", "monthly_orders"),
        ("Monthly revenue", "monthly_sales_aed"),
        ("Food cost", "food_cost_aed"),
        ("Labour/rent/other", "labor_rent_other_aed"),
        ("Delivery commission", "delivery_commission_aed"),
        ("Illustrative residual contribution", "illustrative_contribution_before_tax_and_capex_aed"),
        ("Contribution margin (%)", "contribution_margin_pct"),
    ]
    rows = [header, separator]
    for label, key in fields:
        rows.append("| " + label + " | " + " | ".join(f"{r[key]:,.2f}" for r in outputs) + " |")
    return "\n".join([
        "### Financial scenario — calculated in Python (no AI arithmetic)",
        "These figures use **only the explicit assumptions supplied**. They are not actual forecasts or net profit.",
        f"Trading days per month: **{inputs.days}**; average order value: **AED {inputs.ticket:,.2f}**.",
        "",
        *rows,
        "",
        "**Method:** monthly revenue = daily orders × average ticket × trading days; "
        "food and operating costs are percentages of sales; delivery commission = revenue × delivery share × commission rate.",
        "",
        "**Interpretation:** With fixed cost and delivery percentages, the contribution *margin* "
        "is identical across order-volume scenarios. Contribution in AED changes linearly.",
        "",
        "**Limitations:** Labour and rent are modeled as percentages, although important parts "
        "are fixed in reality. The model does not resolve VAT-inclusive vs VAT-exclusive sales, "
        "packaging, card fees, marketing discounts, depreciation, capex, financing, or actual "
        "Corporate Tax liability. It is **not** a cash-flow, break-even, or net-profit estimate.",
        "",
        "**Validate before investment:** signed rent and service charges, supplier quotes, "
        "recipe yield/food costs, actual staffing schedules, delivery contract terms, "
        "tax treatment, and realistic demand scenarios.",
    ])


def deterministic_financial_answer(question: str) -> str | None:
    parsed = extract_financial_inputs(question)
    return format_financial_scenarios(parsed) if parsed else None
