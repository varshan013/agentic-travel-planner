# app/utils/expense_calculator.py

def estimate_daily_expense(budget_type: str) -> dict:
    """
    Per-person per-day expense breakdown in INR
    """
    if budget_type == "budget":
        return {
            "stay": 1500,
            "food": 800,
            "local_travel": 500,
            "activities": 700
        }

    elif budget_type == "mid":
        return {
            "stay": 3000,
            "food": 1500,
            "local_travel": 800,
            "activities": 1200
        }

    else:  # luxury
        return {
            "stay": 6000,
            "food": 3000,
            "local_travel": 1500,
            "activities": 2500
        }
