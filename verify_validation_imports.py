
import sys
import os

# Add project root to sys.path explicitly just in case, though PYTHONPATH should handle it
sys.path.append(os.getcwd())

try:
    from ui.validation_ui import validate_receipt
    print("✅ Successfully imported ui.validation_ui.validate_receipt")
except ImportError as e:
    print(f"❌ Failed to import ui.validation_ui: {e}")
    sys.exit(1)

# Test case 1: Missing field
data_missing = {"bill_id": "123"}
result = validate_receipt(data_missing)
if not result["passed"] and "Missing fields" in result["results"][0]["message"]:
    print("✅ Test 1 (Missing Field): Passed")
else:
    print(f"❌ Test 1 (Missing Field): Failed. Result: {result}")

# Test case 2: Valid data
data_valid = {
    "bill_id": "124",
    "vendor": "Test Vendor",
    "date": "2023-10-27",
    "amount": 100.0,
    "tax": 8.0  # 8% tax
}
# Mock receipt_exists to return False
import database.queries
database.queries.receipt_exists = lambda x: False

result_valid = validate_receipt(data_valid)
if result_valid["passed"]:
    print("✅ Test 2 (Valid Data): Passed")
else:
    print(f"❌ Test 2 (Valid Data): Failed. Result: {result_valid}")

# Test case 3: Invalid Tax
data_invalid_tax = {
    "bill_id": "125",
    "vendor": "Test Vendor",
    "date": "2023-10-27",
    "amount": 100.0,
    "tax": 20.0 
}
result_invalid = validate_receipt(data_invalid_tax)
if not result_invalid["passed"] and "Tax mismatch" in result_invalid["results"][-1]["message"]:
    print("✅ Test 3 (Invalid Tax): Passed")
else:
    print(f"❌ Test 3 (Invalid Tax): Failed. Result: {result_invalid}")
