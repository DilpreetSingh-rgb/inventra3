from database import supabase 
import pandas as pd



# # ADD PRODUCT

def add_product(name, price, stock):

    data = {
        "name": name,
        "price": price,
        "stock": stock,
    }

    response = (
        supabase.table("products").insert(data).execute()
    )

    return response.data

# # VIEW PRODUCTS

def view_products():
    try:

        test = supabase.table("products").select("*").execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)


# UPDATE PRODUCT

def update_product(product_id, data):

    response = (
        supabase
        .table("products")
        .update(data)
        .eq("id", product_id)
        .execute()
    )

    return response.data

# DELETE PRODUCT

def delete_product(product_id):

    response = (
        supabase
        .table("products")
        .delete()
        .eq("id", product_id)
        .execute()
    )

    return response.data