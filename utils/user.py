from database import supabase
from datetime import datetime
from zoneinfo import ZoneInfo

def add_user(name):

    data = {
        "name": name,
        "used_at": datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).isoformat()
    }

    response = (
        supabase.table("users").insert(data).execute()
    )

    return response.data
