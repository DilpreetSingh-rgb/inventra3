from datetime import datetime
from zoneinfo import ZoneInfo

from database import supabase

# ==========================
# GET ALL TAX
# ==========================

def get_tax():

    response = (
        supabase
        .table("tax")
        .select("*")
        .execute()
    )

    return response.data

# ==========================
# GET ALL PRODUCTS
# ==========================

def get_products(user_id):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data


# ==========================
# GET NEXT BILL NUMBER
# ==========================

def get_bill_no():

    response = (
        supabase
        .table("invoice")
        .select("invoice_no")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return "BILL-0001"

    last_bill = response.data[0]["invoice_no"]

    number = int(
        last_bill.split("-")[1]
    )

    return f"BILL-{number+1:04d}"


# ==========================
# SAVE COMPLETE BILL
# ==========================

def save_bill(
    bill_no,
    customer_name,
    customer_address,
    mobile_no,
    bill_items,
    cgst_rate,
    sgst_rate,
    user_id
):

    for item in bill_items:

        sale_data = {
            "invoice_no": bill_no,
            "customer_name":customer_name,
            "customer_phone":mobile_no,
            "customer_address":customer_address,
            "product_id": item["product_id"],
            "product_name": item["product_name"],
            "quantity": item["quantity"],
            "selling_price": int(item["unit_price"]),
            "sub_total": int(item["total"]),
            "sgst":sgst_rate,
            "cgst":cgst_rate,
            "igst":0,
            "grand_total":int(item["total"] + (item["total"] * sgst_rate / 100) + (item["total"] * cgst_rate / 100)),
            "created_at": datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).isoformat(),
            "shop_id": user_id
        }

        (
            supabase
            .table("invoice")
            .insert(sale_data)
            .execute()
        )

        new_stock = (
            item["stock"]
            - item["quantity"]
        )

        (
            supabase
            .table("shop")
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
        

        