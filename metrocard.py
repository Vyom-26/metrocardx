# simple metro recharge calculation
def calculate_recharge(current_balance, top_up_amount, bonus_pct=0.0):
    """
    Returns new balance after topping up.
    bonus_pct is decimal (e.g. 0.10 for 10% bonus applied to top_up_amount)
    """
    if top_up_amount < 0:
        raise ValueError("top_up_amount must be >= 0")

    bonus = top_up_amount * bonus_pct
    return round(current_balance + top_up_amount + bonus, 2)
