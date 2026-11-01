#!/usr/bin/env python3
"""Amazon Price Monitoring & ScraperAPI Credit Cost Calculator 2026."""
import argparse

PLANS = {
    "hobby": {"api_credits": 100000, "monthly": 49.0, "annual_monthly": 44.10, "concurrency": 20},
    "startup": {"api_credits": 1000000, "monthly": 149.0, "annual_monthly": 134.10, "concurrency": 50},
    "business": {"api_credits": 3000000, "monthly": 299.0, "annual_monthly": 269.10, "concurrency": 100},
    "enterprise": {"api_credits": 10000000, "monthly": 999.0, "annual_monthly": 899.10, "concurrency": 200}
}

def calculate(plan="startup", tracked_asins=5000, checks_per_day=4, render_js=False):
    data = PLANS.get(plan.lower(), PLANS["startup"])
    # Standard HTML scraping = 1 credit. JS rendering = 5 credits.
    credit_multiplier = 5 if render_js else 1
    daily_requests = tracked_asins * checks_per_day
    monthly_requests = daily_requests * 30
    monthly_credits_consumed = monthly_requests * credit_multiplier
    
    plan_credits = data["api_credits"]
    overage_credits = max(0, monthly_credits_consumed - plan_credits)
    overage_cost = (overage_credits / 10000.0) * 1.50 # ~$1.50 per 10k overage
    effective_monthly = data["annual_monthly"] + overage_cost
    cost_per_check = effective_monthly / monthly_requests if monthly_requests else 0.0

    print("=" * 65)
    print(f"ScraperAPI E-Commerce Price Monitoring TCO: Plan {plan.upper()}")
    print("=" * 65)
    print(f"Tracked Amazon ASINs:      {tracked_asins:,} products")
    print(f"Daily Check Frequency:     {checks_per_day}x per day ({daily_requests:,} reqs/day)")
    print(f"Monthly Extraction Volume: {monthly_requests:,} requests/month")
    print(f"Credits Required:          {monthly_credits_consumed:,} ({'JS Render 5x' if render_js else 'Standard 1x'})")
    print(f"Plan Allowance:            {plan_credits:,} credits (@${data['annual_monthly']:.2f}/mo)")
    print(f"Effective Monthly Total:   ${effective_monthly:.2f}/mo")
    print(f"Unit Cost per Price Check: ${cost_per_check:.5f} / check")
    print("=" * 65)
    return effective_monthly, cost_per_check

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ScraperAPI Amazon Monitoring Calculator")
    parser.add_argument("--plan", default="startup", choices=["hobby", "startup", "business", "enterprise"])
    parser.add_argument("--asins", type=int, default=5000)
    parser.add_argument("--checks", type=int, default=4)
    parser.add_argument("--render-js", action="store_true")
    args = parser.parse_args()
    calculate(plan=args.plan, tracked_asins=args.asins, checks_per_day=args.checks, render_js=args.render_js)
