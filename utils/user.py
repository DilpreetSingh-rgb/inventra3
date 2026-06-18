from database import supabase

def login_user(username, password):

    response = (
        supabase
        .table("userss")
        .select("*")
        .eq("username", username)
        .eq("password", password)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None