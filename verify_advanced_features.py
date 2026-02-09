import pandas as pd
from datetime import datetime, timedelta
from analytics.advanced_analytics import detect_subscriptions, calculate_burn_rate
from analytics.forecasting import predict_spending_polynomial
from typing import cast

def test_subscriptions():
    print("Testing Subscription Detection...")
    # Create dummy data: Netflix (subscription) and Random (one-time)
    data = []
    base_date = datetime.now() - timedelta(days=100)
    
    # 3 Monthly Netflix payments
    for i in range(3):
        data.append({
            "vendor": "Netflix",
            "date": base_date + timedelta(days=30*i),
            "amount": 15.99
        })
        
    # Random coffee
    data.append({"vendor": "Starbucks", "date": base_date, "amount": 5.50})
    data.append({"vendor": "Starbucks", "date": base_date + timedelta(days=2), "amount": 6.50}) # Different amount, close date
    
    df = pd.DataFrame(data)
    subs = detect_subscriptions(df)
    
    if not subs.empty and "Netflix" in subs["Vendor"].values and "Starbucks" not in subs["Vendor"].values:
        print("✅ Subscription detection passed")
    else:
        print("❌ Subscription detection failed")
        print(subs)

def test_burn_rate():
    print("\nTesting Burn Rate...")
    # Budget 1000, Spent 500, Half month passed
    res = calculate_burn_rate(500, 1000, 15)
    if res is not None and res["status"] == "On Track" and res["percent_used"] == 50.0:
        print("✅ Burn rate passed")
    else:
        print("❌ Burn rate failed")
        print(res)

def test_forecast():
    print("\nTesting Polynomial Forecast...")
    # Linear growth
    dates = [datetime.now() - timedelta(days=i) for i in range(10, 0, -1)]
    amounts = [100 + i*10 for i in range(10)] # 100, 110, 120...
    
    df = pd.DataFrame({"date": dates, "amount": amounts})
    forecast = predict_spending_polynomial(df, degree=1)
    
    if forecast is not None and len(forecast) == 30 and cast(pd.Series, forecast["predicted_amount"]).iloc[0] > 190:
        print("✅ Forecast passed")
    else:
        print("❌ Forecast failed")
        print(forecast)

if __name__ == "__main__":
    test_subscriptions()
    test_burn_rate()
    test_forecast()
