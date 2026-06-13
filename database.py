from supabase import create_client, Client

# SUPABASE CONNECTION

SUPABASE_URL = "https://mjyysbguqocuybtgnnei.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1qeXlzYmd1cW9jdXlidGdubmVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEyMjE1MzcsImV4cCI6MjA5Njc5NzUzN30.9aj8mQli6iVQWaBs_JCuykKRQSP2X7y0Q6sMeOLCUp0"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
