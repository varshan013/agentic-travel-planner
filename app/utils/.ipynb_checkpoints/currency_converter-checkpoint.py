def convert_currency(amount: float, from_currency="INR", to_currency="INR"):
    """
    Dummy static conversion (we'll add real API later)
    """
    rates = {
        "INR": 1,
        "USD": 0.012,
        "EUR": 0.011
    }

    if from_currency not in rates or to_currency not in rates:
        return amount

    amount_in_inr = amount / rates[from_currency]
    return round(amount_in_inr * rates[to_currency], 2)
