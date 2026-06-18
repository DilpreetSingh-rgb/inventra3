from database import supabase 
import pandas as pd


# # ADD sup

def add_supplier(name, phone_no, address,user_id):

    data = {
        "name": name,
        "phone_no": phone_no,
        "address": address,
        "shop_id": user_id
    }

    response = (
        supabase.table("supplier").insert(data).execute()
    )

    return response.data

# # VIEW sup

def view_suppliers(user_id):
    try:

        test = supabase.table("supplier").select("*").eq("shop_id",user_id ).execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)

# # get product by id

def get_supplier_by_id(supplier_id, user_id):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("id", supplier_id)
        .eq("shop_id", user_id)
        .execute()
    )

    return response.data


# UPDATE sup

def update_supplier(supplier_id, data,user_id):

    response = (
        supabase
        .table("supplier")
        .update(data)
        .eq("id", supplier_id)
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data

# DELETE PRODUCT

def delete_supplier(supplier_id,user_id):

    response = (
        supabase
        .table("supplier")
        .delete()
        .eq("id", supplier_id)
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data