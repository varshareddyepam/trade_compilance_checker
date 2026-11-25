
import csv
portfolios = {
    "POR001": {
        "cash_balance": 20000,
        "restricted_securities": ["XYZCORP"], #oadded this only to include the step 2 of restricted it
        "max_position_pct": 40,
        "current_holdings": [
            ("AAPL", 100, 140),
            ("TCS", 50, 300),
            ("INFY", 20, 1400)
        ]
    },

    "POR002": {
        "cash_balance": 30000,
        "restricted_securities": [],
        "max_position_pct": 35,
        "current_holdings": [
            ("GOOGL", 10, 1900),
            ("MSFT", 10, 300)
        ]
    },

    "POR003": {
        "cash_balance": 100000,
        "restricted_securities": ["BADCO"],
        "max_position_pct": 40,
        "current_holdings": [
            ("TCS", 100, 290),
            ("INFY", 100, 1450),
            ("RELIANCE", 30, 2300)
        ]
    },

    "POR004": {
        "cash_balance": 50000,
        "restricted_securities": [],
        "max_position_pct": 35,
        "current_holdings": [
            ("GOOGL", 5, 1900),
            ("AAPL", 100, 145)
        ]
    },

    "POR005": {
        "cash_balance": 10000,
        "restricted_securities": [],
        "max_position_pct": 30,
        "current_holdings": [
            ("AAPL", 10, 145),
            ("TCS", 10, 240)
        ]
    }
}


def check_trade(trade):

    portfolio_id = trade["portfolio_id"]
    security_id = trade["security_id"]
    action = trade["action"]

    try:
        quantity = float(trade["quantity"])
        price = float(trade["price"])
    except (ValueError, TypeError):
        return "Rejected,Invalid trade data."


    if quantity <= 0 or price <= 0 or action not in ["Buy", "Sell"]:
        return "Rejected,Invalid trade data."

    portfolio = portfolios[portfolio_id]


    if security_id in portfolio["restricted_securities"]:
        return "Rejected"


    existing_quantity = 0

    for holding in portfolio["current_holdings"]:
        if holding[0] == security_id:
            existing_quantity += holding[1]

    if action == "Sell":

        if existing_quantity < quantity:
            return "Rejected,Insufficient holdings to sell."

    if action == "Buy":

        trade_value = quantity * price

        if trade_value > portfolio["cash_balance"]:
            return "Rejected,Insufficient cash"

        post_trade_cash = portfolio["cash_balance"] - trade_value

        post_trade_quantity = existing_quantity + quantity

        post_trade_value = post_trade_quantity * price

        value_of_other_holdings = 0

        for holding in portfolio["current_holdings"]:
            if holding[0] != security_id:
                value_of_other_holdings += holding[1] * holding[2]

        total_portfolio_value_after = (
            post_trade_cash
            + post_trade_value
            + value_of_other_holdings
        )

        position_pct = (
            post_trade_value / total_portfolio_value_after
        ) * 100

        if position_pct > portfolio["max_position_pct"]:
            return (
                "Needs Manual Sign-off"
            )
    return "Approved"

with open("trades_test.csv", "r", newline="") as file:

    reader = csv.DictReader(file)

    results = []

    for trade in reader:

        decision = check_trade(trade)

        results.append({
            **trade,
            "decision": decision,
        })

print("Final Report")

print(f"{'PORTFOLIO':<12} {'SECURITY':<12} {'ACTION':<8} {'DECISION':<25}")
for trade in results:
    print(
        f"{trade['portfolio_id']:<12} "
        f"{trade['security_id']:<12} "
        f"{trade['action']:<8} "
        f"{trade['decision']:<25} "
    
    )

print("Done.")
#type "python project.py" in the terminal to run 
