import pandas as pd

def churn_rate(customer_df:pd.DataFrame,churn_df:pd.DataFrame) -> float:
    n_cust = customer_df['customer_id'].nunique()
    n_churn = churn_df["customer_id"].nunique()

    if n_cust==0.0:
        return 0.0
    
    return n_churn/n_cust


def revenue_by_segment(subscriptions_df:pd.DataFrame,customer_df:pd.DataFrame):
    merged= subscriptions_df.merge(customer_df,on="customer_id")
    return merged.groupby("segment")["monthly_revenue"].sum().reset_index()


