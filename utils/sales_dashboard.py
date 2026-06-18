from database import supabase
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

# ==========================
# TOTAL PRODUCTS
# ==========================

def get_total_products(user_id):

    response = (
        supabase
        .table("shop")
        .select("*", count="exact")
        .eq("shop_id",user_id )
        .execute()
    )

    return response.count


# ==========================
# TOTAL STOCK
# ==========================

def get_total_stock(user_id):

    response = (
        supabase
        .table("shop")
        .select("stock")
        .eq("shop_id",user_id )
        .execute()
    )

    return sum(
        item["stock"]
        for item in response.data
    )


# ==========================
# LOW STOCK ITEMS
# ==========================

def get_low_stock_items(user_id,limit=10):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("shop_id",user_id )
        .lte("stock", limit) #Less Than or Equal To (<=)
        .execute()
    )

    return response.data


# ==========================
# TODAY SALES
# ==========================

def get_today_sales(user_id):

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    response = (
        supabase
        .table("invoice")
        .select("*")
        .eq("shop_id",user_id )
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

def get_today_revenue(user_id):

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    response = (
        supabase
        .table("invoice")
        .select("*")
        .eq("shop_id",user_id )
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
            revenue += row["sub_total"]

    return revenue

# ==========================
# GET INVENTORY
# ==========================

def get_inventory(user_id):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data
# ==========================
# view sales
# ==========================

def view_sales(user_id):
    try:

        test = supabase.table("invoice").select("*").eq("shop_id",user_id ).execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)
# ==========================
# get empty stock items
# ==========================

def get_empty_stock_items(user_id,limit=1):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("shop_id",user_id )
        .lt("stock", limit) #Less Than (<)
        .execute()
    )

    return response.data
    
def get_revenue_trend(days,user_id):

    sales = view_sales(user_id)

    sales["created_at"] = pd.to_datetime(
        sales["created_at"]
    )

    sales["date"] = sales[
        "created_at"
    ].dt.date

    sales["revenue"] = (
        sales["quantity"] *
        sales["selling_price"]
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
