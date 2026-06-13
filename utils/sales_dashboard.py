from database import supabase
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

# ==========================
# TOTAL PRODUCTS
# ==========================

def get_total_products():

    response = (
        supabase
        .table("products")
        .select("*", count="exact")
        .execute()
    )

    return response.count


# ==========================
# TOTAL STOCK
# ==========================

def get_total_stock():

    response = (
        supabase
        .table("products")
        .select("stock")
        .execute()
    )

    return sum(
        item["stock"]
        for item in response.data
    )


# ==========================
# LOW STOCK ITEMS
# ==========================

def get_low_stock_items(limit=10):

    response = (
        supabase
        .table("products")
        .select("*")
        .lte("stock", limit) #Less Than or Equal To (<=)
        .execute()
    )

    return response.data


# ==========================
# TODAY SALES
# ==========================

def get_today_sales():

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    response = (
        supabase
        .table("sales")
        .select("*")
        .execute()
    )

    count = 0

    for row in response.data:

        created = (
            datetime
            .fromisoformat(row["created_at"])
            .date()
        )

        if created == today:
            count += row["quantity"]

    return count

# ==========================
# TODAY REVENUE
# ==========================

def get_today_revenue():

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    response = (
        supabase
        .table("sales")
        .select("*")
        .execute()
    )

    revenue = 0

    for row in response.data:

        created = (
            datetime
            .fromisoformat(row["created_at"])
            .date()
        )

        if created == today:
            revenue += row["total"]

    return revenue

# ==========================
# GET INVENTORY
# ==========================

def get_inventory():

    response = (
        supabase
        .table("products")
        .select("*")
        .execute()
    )

    return response.data
# ==========================
# view sales
# ==========================

def view_sales():
    try:

        test = supabase.table("sales").select("*").execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)
# ==========================
# get empty stock items
# ==========================

def get_empty_stock_items(limit=1):

    response = (
        supabase
        .table("products")
        .select("*")
        .lt("stock", limit) #Less Than (<)
        .execute()
    )

    return response.data
    
def get_revenue_trend(days):

    sales = view_sales()

    sales["created_at"] = pd.to_datetime(
        sales["created_at"]
    )

    sales["date"] = sales[
        "created_at"
    ].dt.date

    sales["revenue"] = (
        sales["quantity"] *
        sales["unit_price"]
    )

    start_date = (
        pd.Timestamp.today()
        - pd.Timedelta(days=days)
    ).date()

    sales = sales[
        sales["date"] >= start_date
    ]

    revenue_df = (
        sales.groupby("date")
        ["revenue"]
        .sum()
        .reset_index()
    )

    return revenue_df
