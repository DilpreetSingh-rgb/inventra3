from datetime import datetime
from zoneinfo import ZoneInfo

from database import supabase

# ==========================
# GET ALL PRODUCTS
# ==========================

def get_products():

    response = (
        supabase
        .table("products")
        .select("*")
        .execute()
    )

    return response.data


# ==========================
# GET NEXT BILL NUMBER
# ==========================

def get_bill_no():

    response = (
        supabase
        .table("sales")
        .select("bill_no")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return "BILL-0001"

    last_bill = response.data[0]["bill_no"]

    number = int(
        last_bill.split("-")[1]
    )

    return f"BILL-{number+1:04d}"


# ==========================
# SAVE COMPLETE BILL
# ==========================

def save_bill(
    bill_no,
    bill_items
):

    for item in bill_items:

        sale_data = {
            "bill_no": bill_no,
            "product_id": item["product_id"],
            "product_name": item["product_name"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "total": item["total"],
            "created_at": datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).isoformat()
        }

        (
            supabase
            .table("sales")
            .insert(sale_data)
            .execute()
        )

        new_stock = (
            item["stock"]
            - item["quantity"]
        )

        (
            supabase
            .table("products")
            .update(
                {
                    "stock": new_stock
                }
            )
            .eq(
                "id",
                item["product_id"]
            )
            .execute()
        )
        

        