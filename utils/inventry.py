from database import supabase 
import pandas as pd



# # ADD PRODUCT

def add_product(name, price, stock,user_id):

    data = {
        "name": name,
        "price": price,
        "stock": stock,
        "shop_id": user_id
    }

    response = (
        supabase.table("shop").insert(data).execute()
    )

    return response.data

# # VIEW PRODUCTS

def view_products(user_id):
    try:

        test = supabase.table("shop").select("*").eq("shop_id",user_id ).execute()

        df = pd.DataFrame(test.data)
        return df
    except Exception as e:

        print("Connection failed:", e)

# # get product by id

def get_product_by_id(product_id, user_id):

    response = (
        supabase
        .table("shop")
        .select("*")
        .eq("id", product_id)
        .eq("shop_id", user_id)
        .execute()
    )

    return response.data
        

# UPDATE PRODUCT

def update_product(product_id, data,user_id):

    response = (
        supabase
        .table("shop")
        .update(data)
        .eq("id", product_id)
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data

# DELETE PRODUCT

def delete_product(product_id,user_id):

    response = (
        supabase
        .table("shop")
        .delete()
        .eq("id", product_id)
        .eq("shop_id",user_id )
        .execute()
    )

    return response.data