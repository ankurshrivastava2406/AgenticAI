METADATA = {
    "customers": {
        "description": "Customer master data",
        "columns": {
            "customer_id": "Unique customer identifier",
            "region": "Geographic region",
            "segment": "Customer segment",
            "signup_date": "Customer signup date"
        }
    },
    "subscriptions": {
        "description": "Subscription and revenue data",
        "columns": {
            "customer_id": "Customer identifier",
            "plan": "Subscription plan",
            "monthly_revenue": "Monthly recurring revenue",
            "start_date": "Subscription start date",
            "end_date": "Subscription end date (blank if active)"
        }
    },
    "churn_events": {
        "description": "Customer churn records",
        "columns": {
            "customer_id": "Customer identifier",
            "churn_date": "Date customer churned",
            "churn_reason": "Reason for churn"
        }
    }
}

def get_metadata(table_name: str):
    if table_name not in METADATA:
        raise ValueError(f"No metadata for table {table_name}")
    return METADATA[table_name]
