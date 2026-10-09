import json
import math
from functools import lru_cache
from app.config import DATA_PATH

@lru_cache(maxsize=1)
def load_market_data() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_city_profile(city: str) -> str:
    """Return research-backed area options, audiences, tradeoffs and recommended sequence for Dubai or Abu Dhabi."""
    data = load_market_data()
    city_key = next((c for c in data["cities"] if c.lower() == city.strip().lower()), None)
    if not city_key:
        return "Unsupported city. Use Dubai or Abu Dhabi."
    return json.dumps(data["cities"][city_key], ensure_ascii=False, indent=2)

def get_competitor_landscape(city: str = "both") -> str:
    """Return competitor categories, examples, positioning and differentiation opportunities."""
    data = load_market_data()
    rows = data["competitors"]
    if city.lower() != "both":
        rows = [r for r in rows if city in r["cities"] or city.lower() in [x.lower() for x in r["cities"]]]
    return json.dumps(rows, ensure_ascii=False, indent=2)

def get_menu_and_pricing() -> str:
    """Return recommended menu architecture and strategic AED price bands plus market anchors."""
    data = load_market_data()
    return json.dumps({"menu": data["menu_strategy"], "pricing": data["price_bands"]}, ensure_ascii=False, indent=2)

def get_marketing_playbook() -> str:
    """Return pre-launch, launch, retention and partnership recommendations."""
    return json.dumps(load_market_data()["marketing"], ensure_ascii=False, indent=2)

def get_expansion_risk_playbook() -> str:
    """Return operations, staffing, supply, regulatory, tax and seasonality guidance."""
    data = load_market_data()
    return json.dumps({
        "operations": data["operations"],
        "regulatory": data["regulatory"],
        "seasonality": data["seasonality"]
    }, ensure_ascii=False, indent=2)

def calculate_unit_economics(orders_per_day: int, average_ticket_aed: float, food_cost_pct: float = 0.30,
                             labor_rent_other_pct: float = 0.45, delivery_share: float = 0.35,
                             delivery_commission_pct: float = 0.25,
                             trading_days_per_month: int = 30) -> str:
    """Illustrative monthly contribution calculation from explicit planning assumptions.

    `labor_rent_other_pct` is modeled as a percent of *sales*, not fixed AED cost.
    This is an assumption-based contribution illustration, not a store P&L.
    """
    if isinstance(orders_per_day, bool) or not isinstance(orders_per_day, int) or orders_per_day <= 0:
        raise ValueError("orders_per_day must be a positive whole number")
    if (isinstance(average_ticket_aed, bool)
            or not isinstance(average_ticket_aed, (float, int))
            or not math.isfinite(average_ticket_aed) or average_ticket_aed <= 0):
        raise ValueError("average_ticket_aed must be a positive finite number")
    for name, value in (
        ("food_cost_pct", food_cost_pct),
        ("labor_rent_other_pct", labor_rent_other_pct),
        ("delivery_share", delivery_share),
        ("delivery_commission_pct", delivery_commission_pct),
    ):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a finite fraction between 0 and 1")

    if (isinstance(trading_days_per_month, bool) or not isinstance(trading_days_per_month, int)
            or not 1 <= trading_days_per_month <= 31):
        raise ValueError("trading_days_per_month must be between 1 and 31")
    daily_sales = orders_per_day * average_ticket_aed
    monthly_sales = daily_sales * trading_days_per_month
    food_cost = monthly_sales * food_cost_pct
    sales_based_ops = monthly_sales * labor_rent_other_pct
    delivery_fees = monthly_sales * delivery_share * delivery_commission_pct
    contribution = monthly_sales - food_cost - sales_based_ops - delivery_fees
    return json.dumps({
        "basis": f"Illustrative {trading_days_per_month}-day trading month; constant average ticket and order volume",
        "monthly_orders": orders_per_day * trading_days_per_month,
        "assumptions": {
            "orders_per_day": orders_per_day,
            "trading_days_per_month": trading_days_per_month,
            "average_ticket_aed": average_ticket_aed,
            "food_cost_pct": food_cost_pct,
            "labor_rent_other_pct": labor_rent_other_pct,
            "delivery_share": delivery_share,
            "delivery_commission_pct": delivery_commission_pct,
        },
        "monthly_sales_aed": round(monthly_sales, 2),
        "food_cost_aed": round(food_cost, 2),
        "labor_rent_other_aed": round(sales_based_ops, 2),
        "delivery_commission_aed": round(delivery_fees, 2),
        "illustrative_contribution_before_tax_and_capex_aed": round(contribution, 2),
        "contribution_margin_pct": round(contribution / monthly_sales * 100, 1),
        "warning": (
            "Planning scenario, not a real P&L or break-even forecast. Labour/rent/other "
            "are simplified as a percentage of sales; real rent and labour include fixed "
            "costs. Revenue VAT treatment, utilities, promotions, packaging, platform fees, "
            "setup capex, financing and tax require separate modeling. Validate actual "
            "supplier, lease, payroll and aggregator contract quotes."
        ),
    }, ensure_ascii=False, indent=2)
