from database import supabase 
import pandas as pd


# # ADD PRODUCT

def add_supplier(name, phone_no, address):

    data = {
        "name": name,
        "phone_no": phone_no,
        "address": address,
    }

    response = (
        supabase.table("supplier").insert(data).execute()
    )

    return response.data

# # VIEW PRODUCTS

def view_suppliers():
    try:

        test = supabase.table("supplier").select("*").execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)


# UPDATE PRODUCT

def update_supplier(supplier_id, data):

    response = (
        supabase
        .table("supplier")
        .update(data)
        .eq("id", supplier_id)
        .execute()
    )

    return response.data

# DELETE PRODUCT

def delete_supplier(supplier_id):

    response = (
        supabase
        .table("supplier")
        .delete()
        .eq("id", supplier_id)
        .execute()
    )

    return response.data