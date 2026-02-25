# ERPNext Integration Documentation

## Overview
The Receipt Vault Analyzer is equipped with a native integration engine designed specifically for **ERPNext** (built on the Frappe framework). This integration allows for the seamless transfer of extracted receipt data into your ERPNext instance as specialized accounting documents.

---

## 🛠️ Technical Implementation

### 1. DocType Mapping
The system maps individual receipts to the **"Purchase Invoice"** DocType in ERPNext. This ensures that every scanned receipt is treated as a valid financial record for accounts payable.

### 2. Field Mapping Schema
Our API (`api/main.py`) performs the following data transformations to ensure compatibility with ERPNext:

| Receipt Vault Field | ERPNext Field | Description |
| :--- | :--- | :--- |
| `vendor` | `supplier` | The identified vendor name mapping to a Supplier record. |
| `date` | `posting_date` | The receipt date used for the ledger entry. |
| `bill_id` | `description` | The unique receipt identifier stored in the item description. |
| `amount` | `rate` & `amount` | The total cost allocated to a "Generic Expense" item. |
| `tax` | (Calculated) | Tax values are included in the itemized table for reconciliation. |

### 3. ERPNext API Payload Format (JSON)
When a sync is triggered, the system generates a payload adhering to the **Frappe REST API** structure:

```json
{
    "doctype": "Purchase Invoice",
    "supplier": "Walmart",
    "posting_date": "2024-02-15",
    "apply_tds": 0,
    "items": [
        {
            "item_code": "Generic Expense",
            "qty": 1,
            "rate": 150.50,
            "amount": 150.50,
            "description": "Receipt TC#12345 from Walmart"
        }
    ]
}
```

---

## 👩‍💻 User Guide: How to Sync

### 1. Select ERPNext
Navigate to the **ERP & API** tab in the sidebar and select **ERPNext** from the "Select Target ERP System" dropdown.

### 2. Configure Endpoints
- **ERP Endpoint URL**: Enter your ERPNext instance API endpoint (e.g., `https://your-company.erpnext.com/api/resource/Purchase%20Invoice`).
- **Authorization**: Enter your Frappe API Secret or Token.

### 3. Trigger Sync
Click the **🚀 Trigger Manual ERP Sync** button. The system will:
1. Fetch the latest extracted receipts.
2. Transform them into the ERPNext-specific JSON format.
3. Provide a **Payload Preview** for you to verify before final transmission.

---

## ⚙️ Configuration File
The logic for this integration is located in:
`c:\Users\p.pranitha\OneDrive\Documents\Receipt-Vault-Analyzer\api\main.py`

*Note: Ensure the API server is running (`python api/main.py`) for the sync features to be active in the UI.*
